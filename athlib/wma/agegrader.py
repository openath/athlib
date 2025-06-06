import json
import re
import os

from collections import namedtuple

from ..utils import str2num, normalize_gender, parse_hms, get_distance
from ..codes import PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD

__all__ = ('AgeGrader',)

road_info = namedtuple('road_info', 'code distance standard factors')


class AgeGrader(object):
    """
    We implement an object to cache the data used for lookups.

    end users will appear to be calling a function.
    """
    min_age = 35
    max_age = 100
    data_file_name = "wma-data-2023.json"
    text_columns = 0,
    event_column = 0
    _data = None

    def __init__(self, year="2023"):
        # if year not in ["2015", "2023"]:
        #     raise ValueError("No age grade data for %s" % year) 
        self.data_file_name = "wma-data-%s.json" % year

    def get_data(self):
        """Defer this until the first call, so we can bubble a function up to
        the top of the package
        """
        if not self._data:
            codedir = os.path.dirname(__file__)
            self.data_path = os.path.join(codedir, self.data_file_name)

            with open(self.data_path, 'r') as f:
                self._data = json.load(f)

        return self._data

    @property
    def _all_event_codes(self):
        data = self.get_data()

        return list(set([t[self.event_column] for T in (
            data['m'], data['f']) for t in T]))

    @staticmethod
    def _check_table_column(table, x, func):
        for row in table:
            func(row[x])

    def _check_patterns(self):
        """
        >>> from athlib.wma.agegrader import AgeGrader
        >>> AgeGrader()._check_patterns()
        """
        for ec in self._all_event_codes:
            for p in (PAT_THROWS, PAT_JUMPS, PAT_TRACK, PAT_ROAD):
                if p.match(ec):
                    break
            else:
                print('could not match %s' % ec)

        nuc = []

        def ccase(x):
            if x.upper() != x:
                nuc.append(x)

        data = self.get_data()

        for j in self.text_columns:
            self._check_table_column(data['m'], j, ccase)
            self._check_table_column(data['f'], j, ccase)

        if nuc:
            print('these strings need uppercasing in the json %s' %
                   ' '.join(repr(t) for t in list(set(nuc))))

    @staticmethod
    def event_code_to_kind(code):
        for n, p in (('throw', PAT_THROWS),
                     ('jump', PAT_JUMPS),
                     ('track', PAT_TRACK),
                     ('road', PAT_ROAD)):
            if p.match(code):
                return n

        raise ValueError('could not find event kind for code %r' % code)

    @staticmethod
    def normalize_gender(gender):
        g = gender.lower()

        if g:
            g = g[0]

        if g not in 'mf':
            raise ValueError('cannot normalize gender = %s' % repr(gender))

        return g

    def calculate_factor(self, gender, age, event):
        """Work out 'slowdown factor' for a person of this
        age taking part in this event
        """
        kind = self.event_code_to_kind(event)
        event = event.upper()

        gender = self.normalize_gender(gender)

        # Which table we're using
        data = self.get_data()
        table = data[gender]
        ages = data['ages']
        nt = len(table)


        self.find_age(age, ages)

        try:
            self.find_row_by_event(event,
                                   table,
                                   label='wma.%s' % (gender))
        except ValueError:
            # parse event code and get distance
            distance = get_distance(event)
            # print("finding row by distance %s" % distance)
            self.find_row_by_distance(distance,
                                      table,
                                      label='wma.%s' % (gender))
            # we have rows above and below.
            event_shorter = table[self._fx][0]
            event_longer = table[self._fx1][0]
            # print(f"Longer = {event_longer}")
            # print(f"Shorter = {event_shorter}")
            factor_shorter = self.calculate_factor(gender, age, event_shorter)
            distance_shorter = get_distance(event_shorter)
            
            factor_longer = self.calculate_factor(gender, age, event_longer)
            distance_longer = get_distance(event_longer)
            # fraction between longer and shorter
            # print(f"d={distance}, ds={distance_shorter}, dl={distance_longer}")


            if distance_shorter is None:  # really short sprint, 
                return factor_longer

            if distance_longer is None: # more than 200 miles
                return factor_shorter
                
            frac = distance - distance_shorter
            frac = frac / (distance_longer - distance_shorter)
            factor_interpolated = ((1 - frac) * factor_shorter) + (frac * factor_longer)
            return factor_interpolated

        # for a known event, is all this interpolation of ages and distances needed?
        # AR 2024

        fx = self._fx
        fx1 = self._fx1
        pfac = self._pfac
        ax = self._ax
        ax1 = self._ax1
        page = self._page
        FX = table[fx][3:]
        FX1 = table[fx1][3:]
        fac = FX[ax]
        faca = FX[ax1]
        fac1 = FX1[ax]
        fac1a = FX1[ax1]
        fac = (
                (1 - pfac) * ((page * faca) + ((1 - page) * fac)) +
                (pfac * ((page * fac1a) + ((1 - page) * fac1)))
               )

        return fac

    def find_row_by_event(self, event, table, label=''):
        for i, row in enumerate(table):
            if row[0] == event:
                self._fx = self._fx1 = i
                self._pfac = 0
                return i

        raise ValueError('cannot locate event %s in %s' % (repr(event), label))

    def find_row_by_distance(self, dist, table, label=''):
        # second item in each row is the distance in metres


        d = 0.001 * dist
        i = 0
        x = 1
        nt = len(table)

        # skip past field and walks, we know runs are at the end
        while table[i][0] != "50":
            i += 1

        try:
            while i < nt and table[i][x] < d:
                i += 1
        except TypeError:
            raise

        if i == 0:
            pfac = fx = fx1 = 0
        elif i and i < nt:
            # Within the data
            fx = i - 1
            fx1 = i
            pfac = float(d - table[fx][x]) / (table[fx1][x] - table[fx][x])
        else:
            fx = fx1 = nt - 1
            pfac = 0
        self._fx = fx
        self._fx1 = fx1
        self._pfac = pfac

    def find_age(self, age, ages, interpolate=True):
        if not age:
            age = 29
        na = len(ages)
        i = 0

        while i < na and ages[i] < age:
            i += 1

        if i == 0:
            page = ax = ax1 = 0
        elif i and i < na:
            ax1 = i
            ax = ax1 - 1
            page = (float(age - ages[ax]) /
                    (ages[ax1] - ages[ax])) if interpolate else 0
        else:
            ax = ax1 = nt - 1
            page = 0

        self._ax = ax
        self._ax1 = ax1
        self._page = page

    def world_best(self, gender, event):
        "The relevant world-record performance on the date stats were compiled"
        kind = self.event_code_to_kind(event)
        data = self.get_data()
        table = data[gender]
        try:
            row = self.find_row_by_event(event, table)
            world_best = table[row][2]
            return world_best
        except ValueError:
            distance = get_distance(event)
            self.find_row_by_distance(distance,
                                      table,
                                      label='wma.%s' % (gender))
            # find the speeds of the previous and later bests in m/sec
            shorter_row = table[self._fx]
            longer_row = table[self._fx1]
            v_shorter_best = shorter_row[1] * 1000 / shorter_row[2]
            v_longer_best = longer_row[1] * 1000 / longer_row[2]

            # average in proportions
            v_averaged = v_longer_best + ((1 - self._pfac) * (v_shorter_best - v_longer_best))

            # print("speed between ", v_longer_best, "and", v_shorter_best)
            world_best = distance / v_averaged
            # print("choosing speed", v_averaged, "giving best of", world_best, "for", distance)

            return world_best


    def calculate_age_grade(self,
                            gender,
                            age,
                            event,
                            performance,
                            verbose=False):
        """Return the age grade score (0 to 100ish) for this result.

        >>> from .agegrader import AgeGrader
        >>> ag=AgeGrader()
        >>> "%0.4f" % ag.calculate_age_grade('m',50,'5K', '16:23')
        '0.8917'
        >>> "%0.4f" %  ag.calculate_age_grade('f',50,'5K', '18:00')
        '0.9159'
        >>>
        """

        # This works for jumps/throws too, as they are floats
        float_performance = parse_hms(performance)

        event = event.upper()
        if event[-1] == 'H' and event not in ('LH', 'SH', '60H'):
            if int(event[:-1]) <= 110:
                event = 'SH'
            elif int(event[:-1]) >= 200:
                event = 'LH'
            else:
                raise ValueError(f'Event {event} looks like hurdles, but is not a standard distance so not supported')
        elif event in ['2000SC', '3000SC']:
            # Generalise to steeplechase for championship steeple distances
            event = 'SC
        elif len(event) > 2 and event[:2] in ['DT', 'HT', 'JT', 'SP', 'WT']:
            # Chop off weights from throw event codes
            event = event[:2]
        world_best = self.world_best(gender, event)
        age_factor = self.calculate_factor(gender, age, event)
        age_group_best = world_best * 1.0 / age_factor

        if verbose:
            print("performance = %0.2f" % float_performance)
            print("world best for %s %s = %0.2f" % (gender, event, world_best))
            print("factor %s %s = %0.4f" % (gender, event, age_factor))
            print("age group best would be", age_group_best)

        kind = self.event_code_to_kind(event)

        if kind in ['road', 'track']:
            # Performance is a float.
            # Older people get lower values (shorter/lower)
            age_grade = age_group_best / float_performance
        else:
            age_grade = float_performance / age_group_best

        return age_grade


class AthlonsAgeGrader(AgeGrader):
    text_columns = 0, 2
    event_column = 2
    
    def __init__(self, data_file_name="wma-athlons-data.json"):
        self.data_file_name = data_file_name

    def calculate_factor(self, gender, age, event):
        """Work out 'slowdown factor' for a geezer of this
        age taking part in this event e.g.

        >>> from .agegrader import AthlonsAgeGrader
        >>> ag=AthlonsAgeGrader()
        >>> ag.calculate_factor('M',35,'100')
        0.9999
        >>> ag.calculate_factor('M',66,'60H')
        0.8351
        >>> ag.calculate_factor('M',69,'SH')
        0.8958
        >>> ag.calculate_factor('M',69,'100H')
        0.8958
        >>> ag.calculate_factor('f',69,'LJ')
        1.4736
        """
        event = event.upper()
        if event[-1] == 'H' and event not in ('LH', 'SH', '60H'):
            if int(event[:-1]) <= 110:
                event = 'SH'
            elif int(event[:-1]) >= 200:
                event = 'LH'
            else:
                raise ValueError('event %s looks like hurdles'
                ', but is not a standard distance so not supported' % event)
        gender = self.normalize_gender(gender)

        # Which table we're using
        data = self.get_data()
        table = data[gender]
        ages = data['ages']

        # We must match an event exactly
        self.find_row_by_event(event,
                               table,
                               label='wma-athlons.%s' % (gender))
        self.find_age(int(age // 5) * 5, ages, interpolate=False)
        fac = table[self._fx][self._ax1]
        return fac
