__all__ =   (
            'AgeGrader',
            )
import json, re, os
_ = r"\d\.?\d*K"
_throw_codes = re.compile(r"^(?:WT\d?%s|JT[45678]00|DT%s|HT%s|SP%s)" % (_,_,_,_), re.IGNORECASE)
_jump_codes = re.compile(r"^(?:LJ|PV|TJ|HJ)$", re.IGNORECASE)
_track_codes = re.compile(r"^\d+(?:H(?:3[36])?|SC)?", re.IGNORECASE)
_road_codes = re.compile(r"^(?:MILE|MAR|HM|\d+[MK]?)", re.IGNORECASE)

class AgeGrader(object):
    min_age = 35
    max_age = 100
    _jump_codes = re.compile("^(?:LJ|PV|TJ|HJ)$", re.IGNORECASE)
    _throw_codes = re.compile("^(WT|JT|DT|HT|SP)", re.IGNORECASE)
    def __init__(self):
        self._get_data()

    def _get_data(self):
        from athlib import wma
        with open(os.path.join(wma.__path__[0],'wma-data.json'),'rb') as f:
            self.data = json.load(f)

    @property
    def _all_event_codes(self):
        data = self.data
        return list(set([t[0] for T in (data['road']['m'],data['road']['f']) for t in T]+
            [t[2] for T in (data['tf']['m'],data['tf']['f']) for t in T]))

    def _check_patterns(self):
        for ec in self._all_event_codes:
            for p in _throw_codes, _jump_codes, _track_codes, _road_codes:
                if p.match(ec): break
            else:
                print 'could not match %s' % ec
