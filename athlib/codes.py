"Standard event codes, and things to parse and check them"

import re


#patterns allow both for generic (JT = Javelin Throw) and specific (JT800) patterns.
_ = r"\d\.?\d*K"
PAT_THROWS = re.compile(r"^(?:WT(P<wtnum>\d?%s|)|JT(P<jtnum>[45678]00|)|DT(?P<dtnum>%s|)|HT(?P<htnum>%s|))|SP(?P<spnum>%s|)$" % (_,_,_,_), re.IGNORECASE)
PAT_JUMPS = re.compile(r"^(?:LJ|PV|TJ|HJ)$", re.IGNORECASE)
PAT_TRACK = re.compile(r"^(?:(?P<meters>\d+)(?:[LS]?H(?:3[36])?|SC|W)?)|SC|[2345]MT|LH|SH$", re.IGNORECASE)
PAT_ROAD = re.compile(r"^(?:MILE|MAR|HM|\d+[MK]?)W?$", re.IGNORECASE)
del _

PAT_RUN = re.compile("%s|%s" % (PAT_TRACK.pattern, PAT_ROAD.pattern))
PAT_FIELD = re.compile("%s|%s" % (PAT_THROWS.pattern, PAT_JUMPS.pattern))