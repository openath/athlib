"""General athlib utility functions"""

from .codes import PAT_THROWS, PAT_JUMPS, PAT_RELAYS, PAT_HURDLES, PAT_TRACK, \
    PAT_LEADING_DIGITS, PAT_PERF, \
    FIELD_EVENTS, MULTI_EVENTS, FIELD_SORT_ORDER


def normalize_gender(gender):
    "Return M, F or raise a ValueError"
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


def check_performance_for_discipline(discipline, textvalue):
    """
    Fix up and return what they typed in,  or raise ValueError

    """
    # print "checkperf %s %s" % (discipline, repr(textvalue))
    textvalue = textvalue.strip()

    if discipline.lower() == "xc" and textvalue == "":
        return textvalue

    # fix up "," for the Frenchies
    if "," in textvalue and "." not in textvalue:
        textvalue = textvalue.replace(",", ".")

    if ";" in textvalue:
        textvalue = textvalue.replace(";", ':')

    if not PAT_PERF.match(textvalue):
        raise ValueError(
            "Illegal numeric pattern.  Use digits, ':' and '.' only")

    if discipline in FIELD_EVENTS:
        try:
            distance = float(textvalue)
            return "%0.2f" % distance
        except ValueError:
            raise ValueError(
                "'%s' is not valid for length/height. Use "
                "metres/centimetres e.g. '2.34'" % textvalue
            )

    elif discipline.upper() in MULTI_EVENTS:
        try:
            points = int(textvalue)
        except ValueError:
            raise ValueError(
                "'%s' is not a valid points value for multi-events"
                % textvalue)
        if points < 500:
            raise ValueError("Multi-events scores should be above 500")
        if points > 9999:
            raise ValueError("Multi-events scores should be below 10000")
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
            # print "fixing colon to stop "
            textvalue = textvalue.replace(":", ".")

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
        
        #The regex ensures we have 1, 2 or 3 chunks
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
            raise ValueError(
                "Please use mm:ss or h:mm:ss for times above 99 seconds")

        if distance == 400 and minutes > 45:
            "63:40 instead of 63.40"
            seconds = minutes + 0.01 * seconds
            hours = 0
            minutes = 0

        duration = 3600 * hours + 60 * minutes + seconds
        # print "duration: %0.2f seconds" % duration

        # do sanity checks.  Over 11 metres per second is pretty fishy for a
        # sprint
        if distance and duration:

            velocity = distance * 1.0 / duration
            # print 'distance = %0.2d, duration = %d sec, velocity = %0.2f m/s' % (
            #     distance, duration, velocity)
            if distance <= 400:
                if velocity > 11.0:
                    raise ValueError(
                        "%s too fast for %s, check the format" %
                        (textvalue, discipline))
            elif distance > 400:
                if velocity > 10.0:
                    raise ValueError(
                        "%s too fast for %s, check the format" %
                        (textvalue, discipline))

            if velocity < 0.5:
                raise ValueError(
                    "%s too slow for %s, check the format" %
                    (textvalue, discipline))

        else:
            if discipline.upper() == 'XC':
                if not minutes:
                    raise ValueError(
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


def event_sort_key(event_name):
    """
    Return a tuple which will sort into programme order

    Track should be ordered by distance.

    """
    if not event_name:
        #Goes at the end
        return 6, 0, "?"

    m = PAT_THROWS.search(event_name)
    if m:
        order = FIELD_SORT_ORDER.index(event_name[0:2])
        return 4, order, event_name

    m = PAT_HURDLES.search(event_name)
    if m:
        distance = int(m.group(1))
        return 2, distance, event_name

    m = PAT_JUMPS.search(event_name)
    if m:
        order = FIELD_SORT_ORDER.index(event_name[0:2])
        return 3, order, event_name

    m = PAT_RELAYS.search(event_name)
    if m:
        distance = int(m.group(2))
        return 5, distance, event_name

    # track last, so '100' doesn't match before '100H'
    m = PAT_TRACK.search(event_name)
    if m:
        distance = int(m.group(1))
        return 1, distance, event_name

    # anything else sorts to end
    return 6, 0, event_name


def text_event_sort_key(event_name):
    "Return a text version of the event_sort_key"
    return "%d_%05d_%s" % event_sort_key(event_name)


def sort_by_discipline(stuff, attr="discipline"):
    "Sort dicts or objects into the normal athletics order"

    sorter = []
    for thing in stuff:
        if isinstance(thing, dict):
            disc = thing.get(attr, None)
        else:  #assume object
            disc = getattr(thing, attr, None)
        priority = event_sort_key(disc)
        sorter.append((priority, thing))

    sorter.sort()
    return [thing for (priority, thing) in sorter]
