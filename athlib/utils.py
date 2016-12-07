"""General athlib utility functions"""


def normalize_gender(gender):
    g = gender.upper()

    if g:
        g = g[0]
    if g not in 'MF':
        raise ValueError('cannot normalize gender = %s' % repr(gender))
    return g


def str2num(s):
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
            except:
                raise ValueError('cannot parse seconds from %s' % repr(t))

        return sec
    try:
        return str2num(t)
    except:
        raise ValueError('cannot parse seconds from %s' % repr(t))
