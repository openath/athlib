"""Create a 2023 json file with the factors in reasonably readable form.

The starting point was Howard Grubb's 2015 calculator data which combined
track and field, walks and road factors.  We have all the factors from this in
one json file, wma-data-2015.json.

To create a newer version of this for use in 2024, we need to find the factors
for track and field (from WMA 2023) and walks, and road (from Alan Lytton Jones' USATF MLDR
work in 2020), and overwrite with new standards when changed.

The WMA factors for official athletics events are published in PDF in
Appendix B of the WMA rules, and taken here from  a file sourced from
Howard Grubb's site, with event code hand-adjusted to match OpenTrack.

The standards come from John Seto in email, and represent the World Record
when statisticians are comfortable with that performance, or in other cases 
what they consider as the best legitimate performance

We overwrite 2015 factors and standards with the newer ones for official track events.





This script and the input files are not part of the athlib runtime code,
but can be run to make sure it is repeatable.  We have some unit tests in
test/test_age_grades.py to ensure agreement with John Seto and Howard Grubb's
calculators.

"""
from pprint import pprint
import json



def looksLikeMiles(kmdist):
    "Sport whether a figure in Alan's road tables is within a few feet of a distance in miles"
    epsilon = 0.001 # this works up to 100 miles
    miledist = (kmdist + epsilon) / 1.609344
    if abs(miledist - int(miledist)) < epsilon:
        return int(miledist + epsilon)
    else:
        return 0


def kmdist_to_eventcode(kmdist):
    "Turn Alan's heading to an OpenTrack event code"
    if kmdist == "21.0975":
        return "HM"
    elif kmdist == "42.195":
        return "MAR"
    
    miledist = looksLikeMiles(float(kmdist))
    if miledist:
        return "%dM" % miledist
    else:
        # trailing zeros
        kmdist = int(float(kmdist))
        return "%sK" % kmdist


def run():
    stuff = json.loads(open("wma-inputs-2023.json").read())



    new_factor_dict = {}
    new_events = []

    standards = {}
    for (event_code, female_wr, male_wr) in stuff["standards"]:
        standards[(event_code, "f")] = female_wr
        standards[(event_code, "m")] = male_wr
    print("Standards:", standards)

    gender_tables = (
        ("f", stuff["female"]),
        ("m", stuff["male"])
        )

    for (gender, tbl) in gender_tables:
        tnumbers = tbl[0]
        events = tbl[1][1:]
        factors = tbl[2:]

        for row in factors:
            age = int(row[0])

            for j in range(len(events)):
                ev = events[j]
                if ev not in new_events:
                    new_events.append(ev)
                factor = row[j+1]

                key = (gender, ev, age)
                new_factor_dict[key] = factor
    print("loaded 2023 factors with %d data points" % len(new_factor_dict))
    print("new events list (%d): %s" % (len(new_events), new_events))




    # now create comparable table to 2015 one, using old factors from 5 years to 30
    old = json.loads(open("wma-data-2015.json").read())


    # 
    old_factor_dict = {}
    old_mens_events = [] # build a unique list
    old_womens_events = [] # build a unique list
    old_ages = old["ages"]
    for gender in "mf":
        oldtable = old[gender]
        for row in oldtable:
            event = row[0]
            distance = row[1]
            wr = row[2]
            last = row[-1]

            while len(row) < 109: 
                row.append(None) # pad list out
            if gender == "m":
                if event not in old_mens_events:
                    old_mens_events.append(event)
            else:
                if event not in old_womens_events:
                    old_womens_events.append(event)

    # print("old M events list (%d): %s" % (len(old_mens_events), old_mens_events))
    # print("old F events list (%d): %s" % (len(old_womens_events), old_womens_events))


    for gender in "mf":
        # print("Doing gender", gender)
        oldtable = old[gender]
        newtable = []
        for row in oldtable: # mutate in place
            newrow = row[:]
            event = row[0]
            distance = row[1]
            wr = newrow[2]
            standards_key = (event, gender)
            if standards_key in standards:
                standard = standards[standards_key]
                newrow[2] = standard
            else:
                print("Could not find WMA standard for", standards_key)


            if event not in new_events:
                print("Event %s for %s not in new WMA tables, unchanged" % (event, gender))
            else:
                # print("Amending", ev, "cells", len(newrow))
                for age in range(30, 111):
                    colidx = age - 2 
                    # is there a new factor?
                    key = (gender, event, age)
                    new_factor = new_factor_dict.get(key, None)
                    # if new_factor: # overwrite
                    f = float(new_factor)
                    if f == 1.0:
                        f = 1
                    newrow[colidx] = f
            newtable.append(newrow)
        old[gender] = newtable


    old["ages"].extend(list(range(101,111)))



    # now to parse the road factors and overwrite
    roadstuff = json.loads(open("mldr-data-2020.json").read())
    for gender in "mf":
        print("Road gender", gender)
        standards_by_event = {}
        factors_by_event_and_age = {}

        tbl = roadstuff[gender]
        distances = tbl[0][1:]
        event_codes = []
        for colnum in range(1, len(distances) + 1):
            kmdist = tbl[0][colnum]
            standard = tbl[1][colnum]
            event_code = kmdist_to_eventcode(kmdist)
            event_codes.append(event_code)
            standards_by_event[event_code] = float(standard)


        # now for factors
        for row in tbl[3:]:
            age = row[0]
            factors = row[1:]
            for colnum, factor in enumerate(factors):
                event_code = event_codes[colnum]
                factors_by_event_and_age[(event_code, age)] = float(factor)


        # now look through our own older data and overwrite with new stuff.
        # aged above 100, we keep factors constant
        table = old[gender]
        newtable = []
        for row in table:
            ec = row[0]
            if ec in event_codes:  # we are only interested in road events
                standard = standards_by_event[ec]

                row[2] = int(float(standard))
                for j, factor in enumerate(row[3:]): # start with age 5 factor and move across
                    age = str(j + 5)
                    key = (ec, age)
                    factor = factors_by_event_and_age.get(key, None)
                    row[j+3] = factor
            else:
                "Warning, %s %s not in new MLDR data" % (gender, ec)
            newtable.append(row)
        old[gender] = newtable



        # Be nice to anyone over 100 running on the roads.  Track factors go to 110,
        # road to 100.  Assume they score like a 100 year old, rather then getting "None"
        newtable = []

        for row in table:

            hundred_factor = row[-12]
            for tail in range(1, 12):
                if row[-tail] is None:
                    row[-tail] = hundred_factor
            newtable.append(row)
        old[gender] = newtable


        # row is already reference to our output structure, in-place mutation, so will be written when we save the table


    jout = json.dumps(old)

    # quick and dirty indent to make readable file
    tidied = jout.replace("[[", "[\n    [")
    tidied = tidied.replace("]]", "]\n ]")
    tidied = tidied.replace("],", "],\n   ")
    tidied = tidied.replace('"ages', '\n    "ages')


    open("wma-data-2023.json", "w").write(tidied)
    print("Wrote wma-data-2023.json")


if __name__=='__main__':
    run()