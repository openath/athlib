"""
Standard event codes, and things to parse and check them
"""

import re


JUMPS = ("HJ", "PV", "LJ", "TJ")
THROWS = ("DT", "JT", "HT", "SP", "WT")
MULTI_EVENTS = (
    # Greek prefixes for 2..12 events, and for 20.
    "BI", "TRI", "QUAD", "PEN", "HEX", "HEP", "OCT", "ENN", "DEC",
    "HEN", "DOD", "ICO",

    "PENI",  # Indoor Pentathlon, not sure if we should keep this
    "PENWT",  # Weights Pentathlon - defines what events go in it.
)
FIELD_EVENTS = JUMPS + THROWS
STANDARD_MALE_TRACK_EVENTS = ("100", "200", "400", "800", "1500",
                              "5000", "10000",
                              "110H", "400H", "3000SC", "4x100", "4x400")
STANDARD_FEMALE_TRACK_EVENTS = ["100H" if x == "110H" else
                                x for x in STANDARD_MALE_TRACK_EVENTS]
# When listing field events, the Blazer Brigade suggest this should be the
# order
FIELD_SORT_ORDER = ["HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT"]


# Patterns allow both for generic (JT = Javelin Throw) and
# weight-specific (JT800) patterns.
_ = r"\d\.?\d*[Kk]"
PAT_THROWS = re.compile((r"^(?:(?:[wW][tT](?P<wtnum>\d?%s|)|[jJ][tT](?P<jtnum>[45678]00|)|"
                         r"[dD][tT](?P<dtnum>%s|)|[hH][tT](?P<htnum>%s|))|"
                         r"[sS][pP](?P<spnum>%s|))$") % (_, _, _, _),
                        )
PAT_JUMPS = re.compile(r"^(?:[lL][jJ]|[pP][vV]|[tT][jJ]|[hH][jJ])$")
PAT_TRACK = re.compile(r"^(?:(?:(?P<meters>\d+)(?:[lLsS]?[hH](?:3[36])?|[sS][cC]|[wW])?)|[sS][cC]|"
                        r"[2345][mM][tT]|[lL][hH]|[sS][hH])$",
                       )
PAT_ROAD = re.compile(r"^(?:(?:[mM][iI][lL][eE]|[mM][aA][rR]|[hH][mM]|\d{1,3}[MKk]?)[wW]?)$")

PAT_RUN = re.compile("%s|%s" % (PAT_TRACK.pattern, PAT_ROAD.pattern))
PAT_FIELD = re.compile("%s|%s" % (PAT_THROWS.pattern, PAT_JUMPS.pattern))

# Although part of PAT_RUN, these
PAT_RELAYS = re.compile("^(?:(\d{1,2})[xX](\d{2,5}|[rR][eE][lL][aA][yY]))") # 4x100, 4x400
PAT_HURDLES = re.compile("^(?:(\d{2,4})([hH]|[sS][cC]))") # 80H, 110H, 400H
PAT_MULTI = re.compile(r"^(?:[dD][eE][cC]|[hH][eE][pP]|[oO][cC][tT]|[pP][eE][nN]|[hH][eE][pP][iI]|[pP][eE][nN][eW][tT]|[mM][eU][;L][tT][iI])$")
PAT_EVENT_CODE=re.compile('|'.join(_.pattern for _ in (PAT_MULTI,PAT_RUN,
                PAT_FIELD,PAT_RELAYS,PAT_HURDLES)))

PAT_VERTICAL_JUMPS = re.compile(r"^(?:HJ|PV)$")
PAT_HORIZONTAL_JUMPS = re.compile(r"^(?:LJ|TJ)$")

PAT_LEADING_DIGITS = re.compile("^\d+")

PAT_LENGTH_EVENT = re.compile("|".join(_.pattern for _ in (PAT_HORIZONTAL_JUMPS, PAT_THROWS)))
PAT_TIMED_EVENT = re.compile("|".join(_.pattern for _ in (PAT_TRACK, PAT_HURDLES, PAT_ROAD, PAT_RELAYS)))

# matches optional hours, optional minutes, optional seconds, optional two decimal places
PAT_PERF = re.compile("^(\d{1,2}:)?(\d{1,2}:)?(\d{1,2})(\.?\d+)?$")

# matches time pasted as seconds only, more than 100 sec.
PAT_LONG_SECONDS = re.compile(u"^\d{3,6}(\.?\d+)?$")

PAT_NOT_FINISHED =  re.compile(r"^(DNF|DQ|DNS)$")

# these are the values one might get in results - valid time, DNF, DQ etc.
PAT_FINISH_RECORD = re.compile("|".join(_.pattern for _ in (PAT_PERF, PAT_NOT_FINISHED)))
del _
