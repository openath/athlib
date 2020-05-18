"""
UK SportsHall Athletics format for younger children

http://www.sportshall.org

Focusing on... http://www.sportshall.org/homepentathlon


Codes of interest:  
    SLJ
    STJ
    SHJ

"""

from decimal import Decimal
from math import floor, ceil

def load_data():
    "Transform data on first load into something more usable"

    data_by_event_code = {}
    event_codes = []
    by_col = zip(*RAWDATA)
    keys = by_col[0]
    for col in by_col[1:]:
        d = dict(zip(keys, col))
        code = d['code']
        data_by_event_code[code] = d


    # this is just strings, a bit clunky.  We want some facts about each event, 
    # and a mapping of performances to points

    db = {}
    for (code, info) in data_by_event_code.items():
        e = {}
        e['name'] = info['name']
        e['units'] = info['units']
        e['incpoints'] = info['increment_points']
        inctext = info['increment']
        if inctext.endswith('cm'):
            inc = float(inctext[0:-2]) * 0.01
            e['increment'] = inc
        perf2points = []
        for points in range(1, 81):
            perf = info[str(points)]
            perf2points.append((points, perf))
        e['perf2points'] = perf2points
        db[code] = e

    return db


def score_high_event(dperf, info):
    "Look in given event's info dict - binary search, high numbers good"

    p2p = info['perf2points']
    max_points, dmax_perf = p2p[-1]
    max_perf = float(dmax_perf)

    points = 0
    if dperf > max_perf:
        # above 80 points, use increment
        excess = dperf - max_perf
        excess_steps = int(floor(excess /  info['increment']))
        excess_points = excess_steps * int(info['incpoints'])
        points = max_points + excess_points
    elif dperf == max_perf:
        # special case, avoid binary search
        return max_points

    else:
        # binary search in 80 point array
        lo = 0
        hi = len(p2p)
        mid = int(floor(0.5 * (lo + hi)))

        tries = 0
        while 1:
            tries += 1
            (p0, v0) = p2p[mid]
            (p1, v1) = p2p[mid+1]

            if tries > 10: 
                return 0
            
            if dperf > float(v1):  # look higher
                mid = int(floor(0.5 * (mid + hi)))
            elif dperf < float(v0): # look higher
                mid = int(floor(0.5 * (lo + mid)))
            else:
                points = p0
                break

    return points

_DB = None

def score(event_code, perf):
    "Return Sportshall At Home score for the event"
    global _DB # initialize on first call
    if not _DB:
        _DB = load_data()
    perf = float(perf)
    ec = event_code.upper()

    event_info = _DB.get(ec, None)
    if not event_info:
        raise KeyError("Event Code '%s' not defined in sportshall scoring" % ec)
    
    if ec in ['SLJ', 'SHJ', 'STJ', 'SP']:  
        return score_high_event(perf, event_info)

    return 42





# Data provided in a Google Sheet we cleaned up.  Explicit points values
# given from 1 to 80 

RAWDATA = [
  ["code","SLJ","SHJ","STJ","SP"  ],
  ["name","Standing long jump","vertical jump","standing triple jump","shot"  ],
  ["increment","2cm","1cm","6cm","0.25cm"  ],
  ["increment_points","1","1","1","1"  ],
  ["units","mtrs","cms","mtrs","mtrs"  ],
  ["80","2.80","68","8.00","12.00"  ],
  ["79","2.75","67","7.87","11.75"  ],
  ["78","2.70","66","7.75","11.50"  ],
  ["77","2.65","65","7.67","11.25"  ],
  ["76","2.60","64","7.50","11.00"  ],
  ["75","2.55","63","7.37","10.75"  ],
  ["74","2.52","62","7.25","10.50"  ],
  ["73","2.49","61","7.12","10.25"  ],
  ["72","2.46","-","7.05","10.00"  ],
  ["71","2.43","60","6.95","9.75"  ],
  ["70","2.40","59","6.85","9.50"  ],
  ["69","2.37","-","6.75","9.25"  ],
  ["68","2.34","58","6.65","9.00"  ],
  ["67","2.31","57","6.55","8.75"  ],
  ["66","2.28","-","6.45","8.50"  ],
  ["65","2.25","56","6.36","8.25"  ],
  ["64","2.22","55","6.28","8.00"  ],
  ["63","2.19","-","6.20","7.75"  ],
  ["62","2.16","54","6.12","7.50"  ],
  ["61","2.13","53","6.04","7.25"  ],
  ["60","2.10","-","5.96","7.00"  ],
  ["59","2.07","52","5.88","6.75"  ],
  ["58","2.04","51","5.80","6.50"  ],
  ["57","2.01","-","5.72","6.25"  ],
  ["56","1.98","50","5.64","6.00"  ],
  ["55","1.95","49","5.56","-"  ],
  ["54","1.92","48","5.48","5.75"  ],
  ["53","1.89","47","5.40","-"  ],
  ["52","1.86","46","5.34","5.50"  ],
  ["51","1.83","45","5.28","-"  ],
  ["50","1.80","44","5.22","5.25"  ],
  ["49","1.78","43","5.16","-"  ],
  ["48","1.76","42","5.10","5.00"  ],
  ["47","1.74","41","5.04","-"  ],
  ["46","1.72","40","4.98","4.75"  ],
  ["45","1.70","-","4.92","-"  ],
  ["44","1.68","39","4.86","4.50"  ],
  ["43","1.66","38","4.80","-"  ],
  ["42","1.64","-","4.75","4.25"  ],
  ["41","1.62","37","4.70","-"  ],
  ["40","1.60","36","4.65","4.00"  ],
  ["39","1.59","-","4.60","-"  ],
  ["38","1.58","35","4.55","-"  ],
  ["37","1.57","34","4.50","3.75"  ],
  ["36","1.56","-","4.45","-"  ],
  ["35","1.55","33","4.40","-"  ],
  ["34","1.54","32","4.35","-"  ],
  ["33","1.53","-","4.30","-"  ],
  ["32","1.52","31","4.25","3.50"  ],
  ["31","1.51","30","4.20","-"  ],
  ["30","1.50","29","4.15","-"  ],
  ["29","1.48","-","4.10","-"  ],
  ["28","1.46","28","4.05","-"  ],
  ["27","1.44","27","4.00","3.25"  ],
  ["26","1.42","26","3.95","-"  ],
  ["25","1.40","-","3.90","-"  ],
  ["24","1.38","25","3.80","-"  ],
  ["23","1.36","24","3.70","-"  ],
  ["22","1.34","23","3.60","3.00"  ],
  ["21","1.32","-","3.50","-"  ],
  ["20","1.30","22","3.40","-"  ],
  ["19","1.25","-","3.30","-"  ],
  ["18","1.20","21","3.20","-"  ],
  ["17","1.15","-","3.10","2.75"  ],
  ["16","1.10","20","3.00","-"  ],
  ["15","1.05","19","2.90","-"  ],
  ["14","1.00","18","2.80","-"  ],
  ["13","0.95","17","2.70","-"  ],
  ["12","0.90","16","2.60","2.50"  ],
  ["11","0.85","15","2.50","-"  ],
  ["10","0.80","14","2.40","2.25"  ],
  ["9","0.75","13","2.20","-"  ],
  ["8","0.70","12","2.00","2.00"  ],
  ["7","0.65","11","1.90","-"  ],
  ["6","0.60","10","1.80","1.50"  ],
  ["5","0.55","9","1.70","-"  ],
  ["4","0.50","8","1.50","1.00"  ],
  ["3","0.45","7","1.30","-"  ],
  ["2","0.40","6","1.10","0.50"  ],
  ["1","0.35","4","1.00","-"  ]
]



if __name__=='__main__':
    d = load_data()
    
    print score("SLJ", "2.0")

