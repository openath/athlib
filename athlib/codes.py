"""
Standard event codes, and things to parse and check them
Ensure all interesting lists and regexps are in the __all__
variable and no other objects are present.

All the exports should have capital letters.

>>> set(__all__) == set((_ for _ in globals().keys() if _.upper()==_))
True
"""
__all__ = (
        'FIELD_EVENTS', 'FIELD_SORT_ORDER', 'JUMPS', 'MULTI_EVENTS', 'STANDARD_FEMALE_TRACK_EVENTS',
        'STANDARD_MALE_TRACK_EVENTS', 'THROWS', 'CUSTOM_EVENTS', 'CUSTOM_HIGHSCORING_EVENTS', 'CUSTOM_LOWSCORING_EVENTS',
        'PAT_EVENT_CODE', 'PAT_FIELD', 'PAT_FINISH_RECORD', 'PAT_HORIZONTAL_JUMPS', 'PAT_HURDLES',
        'PAT_JUMPS', 'PAT_LEADING_DIGITS', 'PAT_LEADING_FLOAT', 'PAT_LENGTH_EVENT', 'PAT_LONG_SECONDS',
        'PAT_MULTI', 'PAT_NOT_FINISHED', 'PAT_PERF', 'PAT_RACES_FOR_DISTANCE', 'PAT_RELAYS', 'PAT_ROAD',
        'PAT_RUN', 'PAT_THROWS', 'PAT_TIMED_EVENT', 'PAT_TRACK', 'PAT_VERTICAL_JUMPS',
        'PAT_HIGHSCORING_EVENT', 'PAT_LOWSCORING_EVENT'
        )
import re
JUMPS = ("HJ", "PV", "LJ", "TJ",
        # Standing High Jump, Standing Long Jump, Standing Triple Jump
        "SHJ", "SLJ", "STJ"
        )
THROWS = (
    "DT", "JT", "HT", "SP", "WT", 

    # Superweight Throw, Ball Throw, Other Throw, Stone Throw
    "SWT", "BT", "ST", "GDT", "OT", 

    #Target Throw, Overhead Throw, Chest Throw from UK SportsHall (kids) format
    "TART", "OHT", "CHT"
)
MULTI_EVENTS = (
    # Greek prefixes for 2..12 events, and for 20.
    "BI", "TRI", "QUAD", "PEN", "HEX", "HEP", "OCT", "ENN", "DEC",
    "HEN", "DOD", "ICO",

    "PENI",  # Indoor Pentathlon, not sure if we should keep this
    "PENWT",  # Weights Pentathlon - defines what events go in it.
)
FIELD_EVENTS = JUMPS + THROWS

CUSTOM_LOWSCORING_EVENTS = ('L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9')
CUSTOM_HIGHSCORING_EVENTS = ('H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'BAL')
CUSTOM_EVENTS = CUSTOM_HIGHSCORING_EVENTS + CUSTOM_LOWSCORING_EVENTS



STANDARD_MALE_TRACK_EVENTS = ("100", "200", "400", "800", "1500",
                              "5000", "10000",
                              "110H", "400H", "3000SC", "4x100", "4x400")
STANDARD_FEMALE_TRACK_EVENTS = tuple(("100H" if x == "110H" else
                                x for x in STANDARD_MALE_TRACK_EVENTS))
# When listing field events, the Blazer Brigade suggest this should be the
# order
FIELD_SORT_ORDER = [
        "HJ", "SHJ",
        "PV", 
        "LJ", "SLJ",
        "TJ", "STJ",
        "SP", "DT", "HT", "JT", 
        "ST", "GDT", "BT", "WT", "SWT", "OT", "TART", "OHT", "CHT",
        "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9",   #Custom Events
        "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9",   #Custom Events
        ]

def _orjoin(*res):
    pats = [_.pattern for _ in res]
    ap = [_ for _ in pats if _.startswith('^(?:') and _.endswith(')$')]
    bp = [_ for _ in pats if not (_.startswith('^(?:') and _.endswith(')$'))]
    if ap and bp:
        raise ValueError('bad _orjoin pattern mix\nanchored=%r\nunanchored=%s' % (ap,bp))
    r = '|'.join(pats)
    if ap:
        r = r.replace(')$|^(?:','|')
    return r

# Patterns allow both for generic (JT = Javelin Throw) and
# weight-specific (JT800) patterns.
_ = r"\s*\d\.?\d*\s*[Kk][Gg]?"
PAT_THROWS = re.compile(
                        (
                        r"^(?:"
                        r"[dD][tT](?P<dtnum>%s|)|"
                        r"[jJ][tT](?P<jtnum>[45678]00\s*g?|)|"
                        r"[hH][tT](?P<htnum>%s|)|"
                        r"[sS][pP](?P<spnum>%s|)|"
                        r"[wW][tT](?P<wtnum>\d?%s|)|"
                        r"[sS][sW][tT](?P<swtnum>%s|)|"
                        r"[bB][tT](?P<btnum>%s|)|"
                        r"[sS][tT](?P<stnum>%s|)|"
                        r"[gG][dD][tT](?P<gdtnum>%s|)|"
                        r"[oO][tT](?P<otnum>\d+\s*g?|)|"
                        r"[tT][aA][rR][tT]|"  # weight not relevant
                        r"[cC][hH][tT]|"
                        r"[oO][hH][tT]|"                         
                        r"[Hh][1-9]|"
                        r"[Ll][1-9]"
                        ")$"
                        ) % (_, _, _, _, _, _, _, _),
                        )
PAT_VERTICAL_JUMPS = re.compile(r"^(?:[sS]?[hH][jJ]|[pP][vV])$")
PAT_HORIZONTAL_JUMPS = re.compile(r"^(?:[sS]?[lL][jJ]|[sS]?[tT][jJ])$")
PAT_JUMPS = re.compile(_orjoin(PAT_VERTICAL_JUMPS,PAT_HORIZONTAL_JUMPS))

#msfx = metres suffix optional
#hsfx = hurdle suffix optional
#hhi = hurdle height in inches deprecated
#hhh = hurdle height cm
#hsd = hurdle separation m
#hid = hurdle initial distance m
_ = r"[lLsS]?[hH]\s*(?P<hsfx>(?P<hhi>3[36])|(?P<hhh>\d{2,3}\.?\d*cm)\s*(?:(?P<hsd>\d{1,3}\.?\d*m)(?:\s*(?P<hid>\d{1,3}\.?\d*m))?)?)?|[sS][cC]"
PAT_TRACK = re.compile(r"^(?:(?:(?P<meters>\d+)\s*(?P<msfx>%s|[yY]|[wW])?)|[sS][cC]|[2345][mM][tT]|[lL][hH]|[sS][hH])$" % _)
PAT_HURDLES = re.compile(r"^(?:(\d{2,4})(?:%s))$" % re.sub(r'\(\?P<[^>]*>','(',_)) # 80H, 110H, 400H

PAT_ROAD = re.compile(r"^(?:(?:[mM][iI][lL][eE]|[mM][aA][rR]|[hH][mM])[wW]?|[xX][cC]|(?:\d{1,3}(\.\d\d?)?(?:[MKk]|[MKk][wW]|[wW])))$")

PAT_RACES_FOR_DISTANCE = re.compile(r"^(?:(?P<dhours>\d\d?)([hH](?:[rR]|[wW]))|[tT](?P<dmins>\d+))$")

PAT_HIGHSCORING_EVENT = re.compile(r"^(?:[Hh][1-9]|SPB|BAL)$")
PAT_LOWSCORING_EVENT = re.compile(r"^(?:[Ll][1-9])$")

PAT_RELAYS = re.compile(r"^(?:(\d{1,2})[xX](\d{2,5}[hH]?|[rR][eE][lL][aA][yY]))$") # 4x100, 4x400, 4xReLAy, 12x200H
PAT_RUN = re.compile(_orjoin(PAT_TRACK, PAT_ROAD, PAT_RELAYS))
PAT_FIELD = re.compile(_orjoin(PAT_THROWS, PAT_JUMPS))

PAT_MULTI = '|'.join((''.join(('[%s%s]' % (v.lower(),v.upper()) for v in _)) for _ in MULTI_EVENTS))
PAT_MULTI = re.compile(r"^(?:%s)$" % PAT_MULTI)

PAT_EVENT_CODE=re.compile(_orjoin(PAT_MULTI,PAT_RUN,
                PAT_FIELD,PAT_RELAYS,PAT_HURDLES,PAT_RACES_FOR_DISTANCE, 
                PAT_HIGHSCORING_EVENT, PAT_LOWSCORING_EVENT))

PAT_LEADING_FLOAT = re.compile(r"^\d+\.\d*")
PAT_LEADING_DIGITS = re.compile(r"^\d+")

PAT_LENGTH_EVENT = re.compile(_orjoin(PAT_HORIZONTAL_JUMPS, PAT_THROWS))
PAT_TIMED_EVENT = re.compile(_orjoin(PAT_TRACK, PAT_HURDLES, PAT_ROAD, PAT_RELAYS))

# matches optional hours, optional minutes, optional seconds, optional two decimal places
PAT_PERF = re.compile(r"^(\d{1,2}:)?(\d{1,2}:)?(\d{1,2})(\.?\d+)?$")

# matches time pasted as seconds only, more than 100 sec.
PAT_LONG_SECONDS = re.compile(r"^\d{3,6}(\.?\d+)?$")

PAT_NOT_FINISHED =  re.compile(r"^(DNF|DQ|DNS)$")

# these are the values one might get in results - valid time, DNF, DQ etc.
PAT_FINISH_RECORD = re.compile(_orjoin(PAT_PERF, PAT_NOT_FINISHED))
del _, _orjoin
