from json import dumps
from types import StringTypes
from lxml import etree
import re

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
    d[newkey] = d[oldkey]
    del d[oldkey]


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
    "4 x 100 m": "4x400",
    "4 x 400 m": "4x100",
    "Marathon": "MAR",
}

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

def athleticize(node):
    "Recursively modify the raw content in line with our proposed standards"


    node['startdate'] = normalize_dates(node['startdate'])
    node['enddate'] = normalize_dates(node['enddate'])
    for event in node['results']:
        event['infos']['date'] = normalize_dates(event['infos']['date'])


    del node["category"]
    del node["subcategory"]
    rename_key(node, "startdate", "start_date")
    rename_key(node, "enddate", "end_date")
    node["competition_ids"] = {"ITA:D3": node["calendareventid"]}
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

        for r in event["result"]:
            for key in r.keys():
                if r[key] is None:
                    del r[key]

            til_id = r["competitorid"]
            del r["competitorid"]
            r["ids"] = {"FIN:TILPA": til_id}

            rename_key(r, "athlete", "name")





def xml_to_json(xml):
    root = etree.fromstring(xml)

    out = node_to_json(root)

    #lose the top tag, it's pointless
    top = out["competition"]


    athleticize(top)

    return dumps(top, indent=2)

if __name__=="__main__":
    fn_in = "rio_athletics_results.xml"
    fn_out = "rio_athletics_results.json"
    xml = open(fn_in).read()
    json = xml_to_json(xml)
    open(fn_out, "w").write(json)
    print "wrote", fn_out