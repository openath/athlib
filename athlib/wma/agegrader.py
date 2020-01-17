import json
import re
import os

from collections import namedtuple

from ..utils import str2num, normalize_gender, parse_hms
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
    data_year = "2015"
    data_file_name = "wma-data.json"
    text_columns = 0,
    event_column = 0
    _data = None

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
            data[self.data_year]['m'], data[self.data_year]['f']) for t in T]))

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

        data = self.get_data()[self.data_year]

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

    def calculate_factor(self, gender, age, event, distance=None):
        """Work out 'slowdown factor' for a geezer of this
        age taking part in this event e.g.

        >>> from .agegrader import AgeGrader
        >>> ag=AgeGrader()
        >>> ag.calculate_factor('M',68,'5k')
        0.7592
        >>> ag.calculate_factor('M',68,'200K')
        0.7561
        >>> ag.calculate_factor('M',68.5,'200K')
        0.7522
        >>> ag.calculate_factor('f',35,'5k')
        0.9935
        >>> ag.calculate_factor('f',35,'200K')
        0.9926
        >>> ag.calculate_factor('F',35.5,'200K')
        0.99095
        >>> ag.calculate_factor('M',65,'10000')
        0.7691
        >>> ag.calculate_factor('M',69,'10000')
        0.7402
        >>> ag.calculate_factor('F',35,'1500')
        0.9822
        >>> ag.calculate_factor('f',39,'1500')
        0.9547
        >>> ag.calculate_factor('f',35,'SH')
        0.9791
        >>> ag.calculate_factor('f',39,'SH')
        0.9576
        >>> ag.calculate_factor('m',35,'LH')
        0.9647
        >>> ag.calculate_factor('m',39,'LH')
        0.9254
        """
        kind = self.event_code_to_kind(event)
        event = event.upper()
        gender = self.normalize_gender(gender)

        # Which table we're using
        data = self.get_data()[self.data_year]
        table = data[gender]
        ages = data['ages']
        nt = len(table)

        if distance is None:
            # We must match an event exactly
            self.find_row_by_event(event,
                                   table,
                                   x=self.event_column,
                                   label='wma.%s.%s' % (self.data_year,
                                                        gender))
        else:
            self.find_row_by_distance(distance,
                                      table,
                                      x=1,
                                      label='wma.%s.%s' % (self.data_year,
                                                           gender))

        self.find_age(age, ages)
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
        fac = ((1 - pfac) * ((page * faca) + ((1 - page) * fac)) +
               (pfac * ((page * fac1a) + ((1 - page) * fac1))))

        return fac

    def find_row_by_event(self, event, table, x=0, label=''):
        for i, row in enumerate(table):
            if row[x] == event:
                self._fx = self._fx1 = i
                self._pfac = 0
                return i

        raise ValueError('cannot locate event %s in %s' % (repr(event), label))

    def find_row_by_distance(self, d, table, x=0, label=''):
        i = 0
        nt = len(table)

        while i < nt and table[i][x] < d:
            i += 1

        if i == 0:
            pfac = fx = fx1 = 0
        elif i and i < nt:
            # Within the data
            fx = i - 1
            fx1 = i
            pfac = float(dist - table[fx][x]) / (table[fx1][x] - table[fx][x])
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
        kind = self.event_code_to_kind(event)
        data = self.get_data()[self.data_year]
        table = data[gender]
        row = self.find_row_by_event(event, table, x=0)
        world_best = table[row][2]
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
        '0.9004'
        >>> "%0.4f" %  ag.calculate_age_grade('f',50,'5K', '18:00')
        '0.9179'
        >>>
        """

        # This works for jumps/throws too, as they are floats
        float_performance = parse_hms(performance)
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
    data_file_name = "wma-athlons-data.json"
    text_columns = 0, 2
    event_column = 2

    def calculate_factor(self, gender, age, event):
        """Work out 'slowdown factor' for a geezer of this
        age taking part in this event e.g.

        >>> from .agegrader import AthlonsAgeGrader
        >>> ag=AthlonsAgeGrader()
        >>> ag.calculate_factor('M',65,'100H')
        0.8637
        >>> ag.calculate_factor('M',69,'100H')
        0.8637
        >>> ag.calculate_factor('M',65,'10000')
        0.7858
        >>> ag.calculate_factor('M',69,'10000')
        0.7858
        >>> ag.calculate_factor('f',35,'100H')
        0.9852
        >>> ag.calculate_factor('F',39,'100H')
        0.9852
        >>> ag.calculate_factor('F',35,'1500')
        0.9872
        >>> ag.calculate_factor('f',39,'1500')
        0.9872
        """
        event = event.upper()
        gender = self.normalize_gender(gender)

        # Which table we're using
        data = self.get_data()[self.data_year]
        table = data[gender]
        ages = data['ages']

        # We must match an event exactly
        self.find_row_by_event(event,
                               table,
                               x=2,
                               label='wma-athlons.%s.%s' % (self.data_year,
                                                            gender))
        self.find_age(int(age // 5) * 5, ages, interpolate=False)
        fac = table[self._fx][3:][self._ax1]
        return fac
