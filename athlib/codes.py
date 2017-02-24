"""
Standard event codes, and things to parse and check them
"""

import re


JUMPS = ("HJ", "PV", "LJ", "TJ")
THROWS = ("DT", "JT", "HT", "SP", "WT")
MULTI_EVENTS = ("PEN", "HEP", "DEC", "PENI", "PENWT")
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
_ = r"\d\.?\d*K"
PAT_THROWS = re.compile((r"^(?:WT(P<wtnum>\d?%s|)|JT(P<jtnum>[45678]00|)|"
                         r"DT(?P<dtnum>%s|)|HT(?P<htnum>%s|))|"
                         r"SP(?P<spnum>%s|)$") % (_, _, _, _),
                        re.IGNORECASE)
PAT_JUMPS = re.compile(r"^(?:LJ|PV|TJ|HJ)$", re.IGNORECASE)
PAT_TRACK = re.compile((r"^(?:(?P<meters>\d+)(?:[LS]?H(?:3[36])?|SC|W)?)|SC|"
                        r"[2345]MT|LH|SH$"),
                       re.IGNORECASE)
PAT_ROAD = re.compile(r"^(?:MILE|MAR|HM|\d+[MK]?)W?$", re.IGNORECASE)
del _

PAT_RUN = re.compile("%s|%s" % (PAT_TRACK.pattern, PAT_ROAD.pattern))
PAT_FIELD = re.compile("%s|%s" % (PAT_THROWS.pattern, PAT_JUMPS.pattern))

# Although part of PAT_RUN, these
PAT_RELAYS = re.compile("(\d{1,2})x(\d{2,5})")   # 4x100, 4x400
PAT_HURDLES = re.compile("(\d{2,4})(H|SC)")  # 80H, 110H, 400H

PAT_LEADING_DIGITS = re.compile("^\d+")
PAT_PERF = re.compile("^(\d{1,2}:)?(\d{1,2}:)?(\d{1,2})(\.?\d+)?$")
