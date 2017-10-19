"""General athlib utility functions"""
import sys, os, json
from collections import OrderedDict
import jsonschema.validators
from jsonschema.validators import RefResolver as OriginalResolver
from jsonschema.exceptions import SchemaError, ValidationError
isPy3 = sys.version_info[0] == 3
_rootdir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.normpath(os.path.join(_rootdir, '..'))

from .codes import PAT_THROWS, PAT_JUMPS, PAT_RELAYS, PAT_HURDLES, PAT_TRACK, \
    PAT_LEADING_DIGITS, PAT_PERF, PAT_EVENT_CODE, \
    FIELD_EVENTS, MULTI_EVENTS, FIELD_SORT_ORDER

__all__ = """normalize_gender
            str2num
            parse_hms
            get_distance
            format_seconds_as_time
            check_performance_for_discipline
            discipline_sort_key
            text_discipline_sort_key
            sort_by_discipline
            schema_valid
            validate_against_schema
            lexec
            localpath
            isStr
            check_event_code""".split()

def normalize_gender(gender):
    """
    Return M, F or raise a ValueError

    :param gender: M or F (case variations and suffixes accepted)
    :returns: M or F
    :raises ValueError: raises an exception

    """
    g = gender.upper()

    if g:
        g = g[0]
    if g not in 'MF':
        raise ValueError('cannot normalize gender = %s' % repr(gender))
    return g

def str2num(s):
    """convert string to int if possible else float

    :param s: string number
    :returns: int(s) or float(s)
    :raises ValueError: if conversion impossible
    """
    try:
        return int(s)
    except ValueError:
        return float(s)

def parse_hms(t):
    """
    Parse a time duration with 0, 1 or 2 colons and return seconds.

    >>> from athlib.utils import parse_hms
    >>> parse_hms('10')
    10
    >>> parse_hms('1:10')
    70
    >>> parse_hms('1:1:10')
    3670
    >>> parse_hms('1:1:10.1')
    3670.1
    >>> parse_hms(3670.1)
    3670.1
    """
    if isinstance(t, (float, int)):
        return t

    # Try : and ; separators
    for sep in ':;':
        if sep not in t:
            continue

        sec = 0

        for s in t.split(sep):
            sec *= 60

            try:
                sec += str2num(s)
            except ValueError:
                raise ValueError('cannot parse seconds from %s' % repr(t))

        return sec
    try:
        return str2num(t)
    except ValueError:
        raise ValueError('cannot parse seconds from %s' % repr(t))

def get_distance(discipline):
    """
    Return approx distance in metres, for sanity checking
    :param discipline:
    :return:
    """

    # Ignore final words like ' road'

    discipline = discipline.split()[0]
    if discipline == "XC":
        return None
    elif discipline == 'MAR':
        return 42195
    elif discipline == "HM":
        return 21098
    elif discipline == "MILE":
        return 1609

    m = PAT_RELAYS.match(discipline)
    if m:
        g1 = int(m.group(1))
        g2 = m.group(2).upper()
        if g2=='RELAY': return None #cowardly refusing to guess
        return g1*int(g2)

    m = PAT_LEADING_DIGITS.match(discipline)
    if not m:
        return None

    qty_text = m.group()
    remains = discipline[len(qty_text):]
    qty = float(qty_text)

    if not remains:
        return int(qty)
    elif remains in ('m', 'mH', 'SC', 'h', 'H'):
        return int(qty)
    elif remains in ('k', 'K', 'km'):
        return int(1000 * qty)
    elif remains in ('M', 'Mi', 'MI'):
        return int(1609 * qty)

def format_seconds_as_time(seconds, prec=0):
    """convert seconds to a string formatted as hours:min:secs

    :param seconds: floating point seconds
    :param prec=0: precision for seconds
    :returns formatted string:
    """
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)

    frac = secs - int(secs)

    if prec == 0:
        frac = ''
    elif prec == 1:
        frac = ('%0.1f' % frac)[1:]  # e.g.".3"
    elif prec == 2:
        frac = ('%0.2f' % frac)[1:]  # e.g.".34"
    elif prec == 3:
        frac = ('%0.3f' % frac)[1:]  # e.g.".342"
    else:
        raise ValueError("Precision must be 0, 1, 2 or 3 digits")
    if hours:
        t = "%d:%02d:%02d" % (hours, mins, secs)
    elif mins:
        t = "%d:%02d" % (mins, secs)
    else:
        t = "%d" % secs
    return t + frac

FIELD_EVENT_RECORDS_BY_GENDER = dict(
                        m = dict(
                                HJ = 2.45,
                                LJ = 8.95,
                                TJ = 18.29,
                                PV = 6.16,
                                HT = 86.74,
                                DT = 74.08,
                                WT = 24.57,
                                SP = 23.12,
                                JT = 104.80,
                                ),
                        f = dict(
                                HJ = 2.09,
                                LJ = 7.52,
                                TJ = 15.50,
                                PV = 5.06,
                                HT = 82.98,
                                DT = 76.80,
                                WT = 22.50,
                                SP = 22.63,
                                JT = 72.28,
                                ),
                        )
FIELD_EVENT_RECORDS_BY_GENDER['all'] = {k: max([FIELD_EVENT_RECORDS_BY_GENDER[r][k] for r in 'mf'])
                                            for k in FIELD_EVENT_RECORDS_BY_GENDER['m'].keys()}

def field_event_record(evc,gender='all'):
    gender = gender.lower()
    if gender not in FIELD_EVENT_RECORDS_BY_GENDER:
        gender = 'all'
    return FIELD_EVENT_RECORDS_BY_GENDER[gender].get(evc.upper(),None)

def check_performance_for_discipline(discipline, textvalue, gender='all', ulpc=120/100.0, errorKlass=ValueError):
    """
    Fix up and return what they typed in,  or raise errorKlass(default ValueError)
    """
    # print("checkperf %s %s" % (discipline, repr(textvalue)))
    textvalue = textvalue.strip()

    if discipline.lower() == "xc" and textvalue == "":
        return textvalue

    # fix up "," for the Frenchies
    if "," in textvalue and "." not in textvalue:
        textvalue = textvalue.replace(",", ".")

    if ";" in textvalue:
        textvalue = textvalue.replace(";", ':')

    if not PAT_PERF.match(textvalue):
        raise errorKlass(
            "Illegal numeric pattern.  Use digits, ':' and '.' only")

    if discipline in FIELD_EVENTS:
        try:
            distance = float(textvalue)
        except ValueError:
            raise errorKlass(
                "'%s' is not valid for length/height. Use "
                "metres/centimetres e.g. '2.34'" % textvalue
            )
        else:
            record = field_event_record(discipline,gender)
            if record and distance>record*ulpc:
                raise errorKlass('%s(%s) performance %s seems too large as record is %.2f' % (
                    discipline, gender, textvalue, record))
            return "%0.2f" % distance

    elif discipline.upper() in MULTI_EVENTS:
        try:
            points = int(textvalue)
        except ValueError:
            raise errorKlass(
                "'%s' is not a valid points value for multi-events"
                % textvalue)
        if points > 9999:
            raise errorKlass("Multi-events scores should be below 10000")
        return str(points)

    else:
        # It's a running distance.  format check.  Try to extract metres

        distance = get_distance(discipline)

        if textvalue.startswith("0:"):
            textvalue = textvalue[2:]
        if textvalue.startswith("00:"):
            textvalue = textvalue[3:]

        if distance and (distance <= 200) and (":" in textvalue) \
                and ("." not in textvalue):
            # print("fixing colon to stop ")
            textvalue = textvalue.replace(":", ".")

        if distance and (distance >= 800) and ("." in textvalue) and (":" not in textvalue):
            # print "fixing stop to colon "
            textvalue = textvalue.replace(".", ":")

        if discipline in ["800", "1500", "3000"]:
            if "." not in textvalue:
                chunks = textvalue.split(":")
                if len(chunks) == 3:
                    textvalue = chunks[0] + ':' + chunks[1] + "." + chunks[2]
                    # we got hours/mins/secs, should have been min/sec +
                    # fraction

        # Brain surgery for the idiots who think 2.33 is a valid 800m time
        # if expect_minutes and (':' not in textvalue) and ('.' in textvalue):
        #     textvalue = textvalue.replace('.', ':')
        # caught false positives
        chunks = textvalue.split(":")

        # The regex ensures we have 1, 2 or 3 chunks
        if len(chunks) == 1:
            hours = 0
            minutes = 0
            seconds = float(chunks[0])
        elif len(chunks) == 2:
            hours = 0
            minutes = int(chunks[0])
            seconds = float(chunks[1])
        elif len(chunks) == 3:
            hh, mm, ss = chunks
            hours = int(hh)
            minutes = int(mm)
            seconds = float(ss)

        if (minutes == 0) and (seconds >= 100):
            raise errorKlass(
                "Please use mm:ss or h:mm:ss for times above 99 seconds")

        if distance == 400 and minutes > 45:
            "63:40 instead of 63.40"
            seconds = minutes + 0.01 * seconds
            hours = 0
            minutes = 0

        duration = 3600 * hours + 60 * minutes + seconds
        # print("duration: %0.2f seconds" % duration)

        # do sanity checks.  Over 11 metres per second is pretty fishy for a
        # sprint
        if distance and duration:

            velocity = distance * 1.0 / duration
            # print('distance = %0.2d, duration = %d sec,
            #        velocity = %0.2f m/s' % (distance, duration, velocity))
            if distance <= 400:
                if velocity > 11.0:
                    raise errorKlass(
                        "%s too fast for %s, check the format" %
                        (textvalue, discipline))
            elif distance > 400:
                if velocity > 10.0:
                    raise errorKlass(
                        "%s too fast for %s, check the format" %
                        (textvalue, discipline))

            if velocity < 0.5:
                raise errorKlass(
                    "%s too slow for %s, check the format" %
                    (textvalue, discipline))

        else:
            if discipline.upper() == 'XC':
                if not minutes:
                    raise errorKlass(
                        "Please use mm:ss for minutes and seconds, not mm.ss")

        # Format consistently for output
        if hours and minutes:
            t = '%d:%02d:%05.2f' % (hours, minutes, seconds)
        elif minutes:
            t = '%d:%05.2f' % (minutes, seconds)
        else:
            t = '%0.2f' % seconds

        # Strip trailing zeroes except for short ones
        if len(t) > 4:
            while t.endswith('0') and len(t) > 4:
                t = t[0:-1]
            if t.endswith('.'):
                t = t[0:-1]

        return t

def discipline_sort_key(discipline):
    """
    Return a tuple which will sort into programme order

    Track should be ordered by distance.

    """
    if not discipline:
        # Goes at the end
        return 6, 0, "?"

    m = PAT_THROWS.search(discipline)
    if m:
        order = FIELD_SORT_ORDER.index(discipline[0:2])
        return 4, order, discipline

    m = PAT_HURDLES.search(discipline)
    if m:
        distance = int(m.group(1))
        return 2, distance, discipline

    m = PAT_JUMPS.search(discipline)
    if m:
        order = FIELD_SORT_ORDER.index(discipline[0:2])
        return 3, order, discipline

    m = PAT_RELAYS.search(discipline)
    if m:
        distance = int(m.group(2))
        return 5, distance, discipline

    # track last, so '100' doesn't match before '100H'
    m = PAT_TRACK.search(discipline)
    if m:
        distance = int(m.group(1))
        return 1, distance, discipline

    # anything else sorts to end
    return 6, 0, discipline

def text_discipline_sort_key(discipline):
    "Return a text version of the event_sort_key"
    return "%d_%05d_%s" % discipline_sort_key(discipline)

def sort_by_discipline(stuff, attr="discipline"):
    "Sort dicts or objects into the normal athletics order"

    sorter = []
    for thing in stuff:
        if isinstance(thing, dict):
            disc = thing.get(attr, None)
        else:
            # assume object
            disc = getattr(thing, attr, None)
        priority = discipline_sort_key(disc)
        sorter.append((priority, thing))

    sorter.sort()
    return [thing for (priority, thing) in sorter]

def check_event_code(c):
    return PAT_EVENT_CODE.match(c)

if isPy3:
    import builtins
    lexec = getattr(builtins, 'exec')
    def isStr(o):
        return isinstance(o,(str,bytes))
else:
    def lexec(obj, G=None, L=None):
        if G is None:
            frame = sys._getframe(1)
            G = frame.f_globals
            if L is None:
                L = frame.f_locals
            del frame
        elif L is None:
            L = G
        exec("""exec obj in G, L""")
    def isStr(o):
        return isinstance(o,basestring)

def localpath(relpath,pstart=0):
    if os.path.isfile(relpath):
        if pstart==0:
            relpath = os.path.abspath(relpath)
    else:
        fn = os.path.join(_rootdir, relpath)
        if os.path.isfile(fn):
            if pstart==0:
                relpath = fn
        else:
            fn = relpath.replace('\\','/').split('/')
            if fn[0]=='json':
                fn = fn[1:]
            fn = tuple(fn)
            for pathdefs in (('athlib','json-schemas'),('json',)):
                pathdefs = (_rootdir,)+pathdefs+fn
                if os.path.isfile(os.path.join(*pathdefs)):
                    relpath = os.path.join(*pathdefs[pstart:])
                    break
    return relpath

class LocalFileResolver(OriginalResolver):

    def resolve_from_url(self, url):
        if url.startswith("file:///"):
            relpath = localpath(url[8:].rstrip('#'),1).replace(os.sep,'/')
            url = ("file:///%s/%s" if sys.platform ==
                   'win32' else 'file://%s/%s') % (_rootdir, relpath)
        return super(LocalFileResolver, self).resolve_from_url(url)

# Monkeypatch jsonschema to resolve local, relative urls.
jsonschema.validators.RefResolver = LocalFileResolver

def _add_to_cache(c,t,v,maxlen=20):
    while len(c)>=maxlen:
        c.popitem(False)
    c[t] = v
    return v

_schema_valid_cache = OrderedDict()
def schema_valid(schema_file,  # should be relative path
                 validator=jsonschema.Draft3Validator,
                 expect_failure=False):
    """Test that schema is itself valid, using a jsonschema validator"""

    t = (schema_file,validator)
    if t in _schema_valid_cache:
        return _schema_valid_cache[t]
    with open(localpath(schema_file)) as f:
        schema = json.load(f)

        try:
            validator.check_schema(schema)
            return _add_to_cache(_schema_valid_cache,t,True)
        except SchemaError as e:
            if not expect_failure:
                print(e)
                return _add_to_cache(_schema_valid_cache,t,False)
            else:
                raise

    return False

_valid_against_schema_cache = OrderedDict()
def valid_against_schema(json_file, schema_file, expect_failure=False):
    """Test that JSON file valid against a schema"""
    t = (json_file,schema_file)
    if t in _valid_against_schema_cache:
        return _valid_against_schema_cache[t]
    with open(localpath(json_file)) as f:
        json_data = json.load(f)

        with open(localpath(schema_file)) as f2:
            schema = json.load(f2)

            try:
                jsonschema.validate(json_data, schema)
                return _add_to_cache(_valid_against_schema_cache,t,True)
            except ValidationError as e:
                if not expect_failure:
                    print(e)
                    return _add_to_cache(_valid_against_schema_cache,t,False)
                else:
                    raise

    return False
