__all__ =   (
            'AgeGrader',
            )
import json, re, os
from collections import namedtuple
_ = r"\d\.?\d*K"
_throw_codes = re.compile(r"^(?:WT(P<wtnum>\d?%s|)|JT(P<jtnum>[45678]00|)|DT(?P<dtnum>%s|)|HT(?P<htnum>%s|))|SP(?P<spnum>%s|)$" % (_,_,_,_), re.IGNORECASE)
_jump_codes = re.compile(r"^(?:LJ|PV|TJ|HJ)$", re.IGNORECASE)
_track_codes = re.compile(r"^(?:(?P<meters>\d+)(?:[LS]?H(?:3[36])?|SC|W)?)|SC|[2345]MT|LH|SH$", re.IGNORECASE)
_road_codes = re.compile(r"^(?:MILE|MAR|HM|\d+[MK]?)W?$", re.IGNORECASE)
del _

road_info = namedtuple('road_info','code distance standard factors')
class AgeGrader(object):
    min_age = 35
    max_age = 100
    data_year = "2015"
    data_file_name = 'wma-data.json'
    text_columns = 0,
    event_column = 0

    def __init__(self,):
        self._get_data(self.data_file_name)

    def _get_data(self,data_file_name):
        from athlib import wma
        self.data_path = os.path.join(wma.__path__[0],data_file_name)
        with open(self.data_path,'rb') as f:
            self.data = json.load(f)

    @property
    def _all_event_codes(self):
        data = self.data
        return list(set([t[self.event_column] for T in (data[self.data_year]['m'],data[self.data_year]['f']) for t in T]))

    @staticmethod
    def _check_table_column(table,x,func):
        for row in table:
            func(row[x])

    def _check_patterns(self):
        '''
        >>> from athlib.wma.agegrader import AgeGrader
        >>> AgeGrader()._check_patterns()
        '''
        for ec in self._all_event_codes:
            for p in (_throw_codes, _jump_codes, _track_codes, _road_codes):
                if p.match(ec): break
            else:
                print 'could not match %s' % ec
        nuc = []
        def ccase(x):
            if x.upper()!=x:
                nuc.append(x)
        data = self.data[self.data_year]
        for j in self.text_columns:
            self._check_table_column(data['m'],j,ccase)
            self._check_table_column(data['f'],j,ccase)
        if nuc:
            print 'these strings need uppercasing in the json %s' % ' '.join(repr(t) for t in list(set(nuc)))

    @staticmethod
    def event_code_to_kind(code):
        for n,p in (('throw',_throw_codes), ('jump',_jump_codes), ('track',_track_codes), ('road',_road_codes)):
            if p.match(code): return n
        raise ValueError('could not find event kind for code %R' % code)

    @staticmethod
    def normalize_gender(gender):
        g = gender.lower()
        if g:
            g = g[0]
        if g not in 'mf':
            raise ValueError('cannot nomalize gender = %s' % repr(gender))
        return g

    def calculate_factor(self,gender,age,event,distance=None):
        '''Work out 'slowdown factor' for a geezer of this
        age taking part in this event e.g.

        >>> from athlib.wma.agegrader import AgeGrader
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
        '''
        kind = self.event_code_to_kind(event)
        event = event.upper()
        gender = self.normalize_gender(gender)
        #which table we're using
        data = self.data[self.data_year]
        table = data[gender]
        ages = data['ages']
        nt = len(table)
        if distance is None:
            #we must match an event exactly
            self.find_row_by_event(event,table,x=self.event_column,label='wma.%s.%s'%(self.data_year,gender))
        else:
            self.find_row_by_distance(distance,table,x=1,label='wma.%s.%s'%(self.data_year,gender))
        self.find_age(age,ages)
        fx = self._fx
        fx1 = self._fx1
        pfac = self._pfac
        ax = self._ax
        ax1 = self._ax1
        page = self._page
        FX = table[fx][3:]
        FX1 = table[fx1][3:]
        fac =  FX[ax]
        faca = FX[ax1]
        fac1 = FX1[ax]
        fac1a = FX1[ax1]
        fac = (1-pfac)*(page*faca+(1-page)*fac)+pfac*(page*fac1a+(1-page)*fac1)
        return fac

    @staticmethod
    def str2num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    @staticmethod
    def parse_hms(t):
        '''
        >>> from athlib.wma.agegrader import AgeGrader
        >>> ag=AgeGrader()
        >>> ag.parse_hms('10')
        10
        >>> ag.parse_hms('1:10')
        70
        >>> ag.parse_hms('1:1:10')
        3670
        >>> ag.parse_hms('1:1:10.1')
        3670.1
        >>> ag.parse_hms(3670.1)
        3670.1
        '''
        if isinstance(t,(float,int)):
            return t
        #try : and ; separators
        for sep in ':;':
            if sep not in t: continue
            sec = 0
            for s in t.split(sep):
                sec *= 60
                try:
                    sec += AgeGrader.str2num(s)
                except:
                    raise ValueError('cannot parse seconds from %s' % repr(t))
            return sec
        try:
            return AgeGrader.str2num(t)
        except:
            raise ValueError('cannot parse seconds from %s' % repr(t))


    def find_row_by_event(self,event,table,x=0,label=''):
        for i,row in enumerate(table):
            if row[x]==event:
                self._fx = self._fx1 = i
                self._pfac = 0
                return i
        raise ValueError('cannot locate event %s in %s' % (repr(event),label))

    def find_row_by_distance(self,d,table,x=0,label=''):
        i = 0
        nt = len(table)
        while i<nt and table[i][x]<d: i += 1
        if i==0:
            pfac = fx = fx1 = 0
        elif i and i<nt:
            #within the data
            fx = i-1
            fx1 = i
            pfac = float(dist-table[fx][x])/(table[fx1][x]-table[fx][x])
        else:
            fx = fx1 = nt-1
            pfac = 0
        self._fx = fx
        self._fx1 = fx1
        self._pfac = pfac

    def find_age(self,age,ages,interpolate=True):
        if not age: age=29
        na = len(ages)
        i = 0
        while i<na and ages[i]<age: i += 1
        if i==0:
            page = ax = ax1 = 0
        elif i and i<na:
            ax1 = i
            ax = ax1 - 1
            page = float(age-ages[ax])/(ages[ax1]-ages[ax]) if interpolate else 0
        else:
            ax = ax1 = nt-1
            page = 0
        self._ax = ax
        self._ax1 = ax1
        self._page = page


    def world_best(self, gender, event, performance):
        "The world best on the data stats were compiled for this event"
        kind = self.event_code_to_kind(event)


        row = self.find_row_by_event(self,event,table)
        if kind=='road':
            return self.calculate_road_factor(gender,age,event)
        else:
            return self.calculate_tf_factor(gender,age,event)


    def calculate_age_grade(self, gender, age, event, performance, 
        verbose=False):
        """Return the age grade score (0 to 100ish) for this result.

        >>> from athlib.wma.agegrader import AgeGrader
        >>> ag=AgeGrader()
        >>> "%0.4f" % ag.calculate_age_grade('m',50,'5K', '16:23')
        '0.9004'
        >>> "%0.4f" %  ag.calculate_age_grade('f',50,'5K', '18:00')
        '0.9179'
        >>>

        """

        #This works for jumps/throws too, as they are floats
        float_performance = self.parse_hms(performance)
        if verbose:  print "performance = %0.2f" % float_performance

        kind = self.event_code_to_kind(event)
        data = self.data[self.data_year]
        table = data[gender]
        row = self.find_row_by_event(event, table, x=0)
        world_best = table[row][2]
        
        if verbose: print "world best for %s %s = %0.2f" % (gender, event, world_best)

        age_factor = self.calculate_factor(gender, age, event)
        if verbose: print "factor %s %s = %0.4f" % (gender, event, age_factor)

        age_group_best = world_best * 1.0 / age_factor
        if verbose: print "age group best would be", age_group_best

        kind = self.event_code_to_kind(event)
        if kind in ['road', 'track']:
            #performance is a float.  Older people get lower values (shorter/lower)
            age_grade = age_group_best / float_performance
        else:
            age_grade = float_performance / age_group_best

        return age_grade

class AthlonsAgeGrader(AgeGrader):
    data_file_name="wma-athlons-data.json"
    text_columns = 0,2
    event_column = 2

    def calculate_factor(self,gender,age,event):
        '''
        >>> from athlib.wma.agegrader import AthlonsAgeGrader
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
        '''
        event = event.upper()
        gender = self.normalize_gender(gender)
        #which table we're using
        data = self.data[self.data_year]
        table = data[gender]
        ages = data['ages']
        #we must match an event exactly
        self.find_row_by_event(event,table,x=2,label='wma-athlons.%s.%s'%(self.data_year,gender))
        self.find_age(int(age/5)*5,ages,interpolate=False)
        fac =  table[self._fx][3:][self._ax1]
        return fac

if __name__=='__main__':
    import doctest
    doctest.testmod()
