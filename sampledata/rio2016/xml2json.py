import os
import glob
from json import dumps
from types import StringTypes
from lxml import etree
import re
from pprint import pprint

import sys
sys.path.insert(0, "../..")
import athlib


pat_DDMMYYYY = re.compile("\d\d\.\d\d\.\d\d\d\d")


"""

"""

def tag_to_dict(node):
    """Assume tag has one layer of children, each of which is text, e.g.

      <medalline>
        <rank>1</rank>
        <organization>USA</organization>
        <gold>13</gold>
        <silver>10</silver>
        <bronze>9</bronze>
        <total>32</total>
      </medalline>

    """

    d = {}
    for child in node:
        d[child.tag] = child.text
    return d



def all_children_different(node):
    seen = set()
    for child in node:
        if child.tag in seen:
            return False
        seen.add(child.tag)
    return True

def all_children_same(node):
    first = node[0]
    for rest in node[1:]:
        if rest.tag != first.tag:
            return False
    return True


def node_to_json(node):
    "transform into a Python value, top down"

    childCount = len(node)
    # print node.tag, childCount
    if childCount == 0:  #no children
        return node.text#{node.tag: node.text}
    elif childCount == 1:
        if isinstance(node[0], StringTypes):
            return node[0].strip()
        return {node.tag: node_to_json(node[0])}
    else:
        if all_children_different(node):
            d = {}
            for child in node:
                d[child.tag] =  node_to_json(child)  
            return d

        elif all_children_same(node):
            return [node_to_json(x) for x in node]
        else:
            #make lists for any multi-valued ones
            d = {}
            for child in node:
                transformed = node_to_json(child)
                tag = child.tag
                # print tag
                if not d.has_key(tag):
                    d[tag] = transformed
                elif isinstance(d[tag], list):
                    d[tag].append(transformed)
                else: #not a list yet
                    d[tag] = [d[tag],transformed]
            return d


def normalize_dates(text):
    if pat_DDMMYYYY.match(text):
        dd,mm,yyyy = text.split(".")
        return yyyy + '-' + mm + '-' + dd
    else:
        return text

def rename_key(d, oldkey, newkey):
    if oldkey in d:
        d[newkey] = d[oldkey]
        del d[oldkey]


def rename_recursive(d, nameMap):
    "Recursively renames keys in place"
    if isinstance(d, list):
        for elem in d:
            rename_recursive(elem, nameMap)
    elif isinstance(d, dict):
        for k, v in d.items():
            rename_recursive(v, nameMap)
            if k in nameMap:
                k2 = nameMap[k]
                d[k2] = v
                del d[k]



EVENT_NAMES_TO_CODES = {
    "3000 m steeple": "3000SC",
    "High jump": "HJ",
    "Pole vault": "PV",
    "Long jump": "LJ",
    "Triple jump": "TJ",
    "Shot": "SP",
    "Discus": "DT",
    "Hammer": "HT",
    "Javelin": "JT",
    "Decathlon": "DEC",
    "Heptathlon": "HEP",
    "20 km walk": "20KW",
    "50 km walk": "50KW",
    "4 x 100 m": "4x100",
    "4 x 400 m": "4x400",
    "Marathon": "MAR",
}


def cleanAgeGroups(text):
    if text is None:
        return []
    else:
        return text.split(",")

def cleanRecordFlags(d):
    if 'recordFlags' in d:
        rf = d['recordFlags']
        if rf: 
            rf = d['recordFlags'].strip().split()
            d['recordFlags'] = rf
        else:
            del d['recordFlags']

def event_name_to_code(event_name):
    words = event_name.split()
    if words[-1] in ["Men", 'Women']:
        words = words[0:-1]
        if len(words) == 2 and words[1] == 'm':
            return "%s" % words[0]
        elif len(words) == 3 and words[2] == 'hurdles':
            return "%sH" % words[0]
        else:
            name = " ".join(words)
            if name in EVENT_NAMES_TO_CODES:
                return EVENT_NAMES_TO_CODES[name]

    print "not done yet", event_name
    return event_name

def cleanAthleteName(result):
    raw = result["athlete"]
    raw = raw.strip()
    if raw:
        #someone with one name...
        parts = raw.split(None)
        if len(parts) == 1:
            raw = "? " + raw

        first, last = raw.split(None, 1)
        first = first.title()
        last = last.title()
        result["givenName"] = first
        result["familyName"] = last
    del result["athlete"]

def cleanRelays(result):
    rename_key(result, 'recordflag', 'recordFlags')
    cleanRecordFlags(result)
    rename_key(result, 'tpAthleteId', 'tpTeamId')
    result['teamCode'] = result['country']
    #del result["competitor"]
    runners = []
    rr = result['relayrunners']
    for i in range(1,5):
        name = rr['relayrunner%d' % i]
        id = rr['relayrunner%did' % i]
        first, last = name.split(None, 1)
        first = first.title()
        last = last.title()

        runner = dict(
            familyName=last,
            givenName=first,
            tpAthleteId=id,
            legNumber=i
            )
        runners.append(runner)
    result['runners'] = runners
    del result['relayrunners']

def cleanAthlon(result, eventCode):
    rename_key(result, 'recordflag', 'recordFlags')
    cleanRecordFlags(result)
    
    if eventCode == 'DEC':
        events = '100 LJ SP HJ 400 110H DT PV JT 1500'.split()
        gender = 'M'
    elif eventCode == 'HEP':
        events = '100H HJ SP 200 LJ JT 800'.split()
        gender = "F"


    cb = result['combinedresults']
    results = []
    total = 0
    for i in range(len(events)):
        eventNo = i + 1
        perf = cb['event%d' % eventNo]
        # if perf is None:
        #     perf = 'DNF'
        wind = None
        if perf and ('/' in perf):
            perf, wind = perf.split('/')
        res = dict(
            eventNo=eventNo,
            eventCode=events[i],
            performance=perf
            )
        if perf not in ('DNF', 'NH', None):

            numeric = athlib.parse_hms(perf)
            points = athlib.athlon_score(gender, events[i], numeric)
            res['points'] = points
            if points:
                total += points

        if wind:
            res['wind'] = wind
        results.append(res)

    officialScore = result['performance']
    if officialScore != 'DNF':
        if total != int(officialScore):
            result['performance2'] = total
            print total, officialScore

    result['results'] = results
    del result['combinedresults']



def athleticize(node):
    "Recursively modify the raw content in line with our proposed standards"


    node['startdate'] = normalize_dates(node['startdate'])
    node['enddate'] = normalize_dates(node['enddate'])
    for event in node['results']:
        event['infos']['date'] = normalize_dates(event['infos']['date'])


    del node["category"]
    del node["subcategory"]
    rename_key(node, "organiser_id", "organiserId")
    rename_key(node, "startdate", "startDate")
    rename_key(node, "enddate", "endDate")
    node["competitionId"] = node["calendareventid"]
    node["slug"] = "OG"
    node["year"] = "2016"
    node["organiser_id"] = "IOC"
    del node["calendareventid"]

    #rename results to events
    rename_key(node, "results", "events")
    #infos is redundant
    for event in node["events"]:
        event.update(event["infos"])
        del event["infos"]


    #some results only have one item (sole relay team) so ended up dict not list.
    for event in node["events"]:
        res = event["result"]
        if isinstance(res, dict):
            event["result"] = [res]


    for event in node["events"]:

        event_code = event_name_to_code(event["event_name"])
        event["discipline"] = event_code
        event_name = event["event_name"]
        rename_key(event, "age_group", "athlon")
        rename_key(event, "round_name", "round")
        rename_key(event, "round_detail", "roundName")



        text = event["round"].strip().lower()[0:4]
        event["round"] = {
            "prel": "PRELIM",
            "heat": "HEAT",
            "semi": "SEMI",
            "fina": "FINAL",
            "qual": "PRELIM"
        }[text]


        if event["athlon"] is None:
            del event["athlon"]
        # rename_key(event, 'age_group', 'ageGroups')

        # #include age groups only if needed
        # event["ageGroups"] = cleanAgeGroups(event['ageGroup'] or "SEN")


        for r in event["result"]:
            for key in r.keys():
                if r[key] is None:
                    del r[key]

            try:
                cleanAthleteName(r)                    
            except (KeyError, ValueError):
                print r
                raise

            rename_key(r, 'competitorid', 'tpAthleteId')                    


            group = r.get("group", "")
            if group.startswith("0."):
                r["reactionTime"] = group
                del r["group"]

            cleanRecordFlags(r)


            rename_key(r, "best_performance", "performance")

            #vertical?
            if event_code in ["HJ", "PV"]:
                rename_key(r, "roundresults", "heights")

                if 'heights' in r:
                    if isinstance(r['heights'], dict):
                        r['heights'] = [r['heights']]
                    for att in r['heights']:
                        rename_key(att, 'recordflag', 'recordFlags')
                        cleanRecordFlags(att)
                        rename_key(att, 'round', 'results')
                        rename_key(att, 'performance', 'height')

            elif event_code in ["LJ", "TJ", "JT", "HT", "DT", "SP"]:
                rename_key(r, "roundresults", "attempts")
                if 'attempts' in r:
                    atts = r['attempts']
                    if isinstance(atts, dict):
                        r['attempts'] = [atts['roundresults']]
                    attNo = 1
                    for att in r['attempts']:
                        att['round'] = attNo
                        rename_key(att, 'recordflag', 'recordFlags')
                        cleanRecordFlags(att)
                        attNo += 1
            elif event_code in ["4x100", "4x400"]:
                cleanRelays(r)

            elif event_code == 'DEC':
                cleanAthlon(r, event_code)
            elif event_code == 'HEP':
                cleanAthlon(r, event_code)
            else: #running events
                rename_key(r, 'recordflag', 'recordFlags')
                cleanRecordFlags(r)


    del node['medaltable']
    del node['placingtable']

    rename_recursive(node, {
        'start_date': 'startDate',
        'end_date': 'endDate',
        'discipline': 'eventCode',
        'event_name': 'name',
        'event_gender': 'gender',

        })


def xml_to_json(xml):
    root = etree.fromstring(xml)

    top = node_to_json(root)

    athleticize(top)

    return dumps(top, indent=2)


def daily_entries_to_json(xml):

    root = etree.fromstring(xml)

    top = node_to_json(root)



    # we get some redundant infolike this
    # "seasonalBest": {
      #   "seasonalBest": "1:19:32"
      # }, 
      # "personalBest": {
      #   "personalBest": "1:17:40"
      # }, 

    for ath in top["athletes"]:
        if ath.has_key("seasonalBest"):
            if ath["seasonalBest"].has_key("seasonalBest"):
                ath["seasonalBest"] = ath["seasonalBest"]["seasonalBest"]

        if ath.has_key("personalBest"):
            if ath["personalBest"].has_key("personalBest"):
                ath["personalBest"] = ath["personalBest"]["personalBest"]


    return dumps(top, indent=2)

if __name__=="__main__":
    # fn_in = "rio_athletics_results.xml"
    # fn_out = "rio_athletics_results.json"
    fn_in = "rio_athletics_results.xml"
    fn_out = "rio_athletics_results.json"
    xml = open(fn_in).read()
    json = xml_to_json(xml)
    open(fn_out, "w").write(json)
    print "wrote", fn_out

    # #pass two - convert entries
    # for xml_filename in glob.glob("rio_entries*.xml"):
    #     xml = open(xml_filename).read()
    #     json_filename = os.path.splitext(xml_filename)[0] + '.json'
    #     json = daily_entries_to_json(xml)
    #     open(json_filename, "w").write(json)
    #     print "wrote", json_filename
