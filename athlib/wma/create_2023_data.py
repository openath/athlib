"""Create a 2023 json file with the factors in reasonably readable form.

The WMA factors for official athletics events are in a file sourced from
Howard Grubb's site, with event code hadn-adjusted to match OpenTrack.

We overwrite 2015 factors with the newer ones for official track events.

Other overwrites are anticipated for 
- factors for younger kids (5 up to adult)
- road and non-standard distances
- world records, in third column. 


This script and the input files are not part of the athlib runtime code,
but can be run to make it repeatable.  
"""
from pprint import pprint
import json


def run():
    stuff = json.loads(open("wma-howard-2023.json").read())



    new_factor_dict = {}
    new_events = []

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

    print("old M events list (%d): %s" % (len(old_mens_events), old_mens_events))
    print("old F events list (%d): %s" % (len(old_womens_events), old_womens_events))


    for gender in "mf":
        print("Doing gender", gender)
        oldtable = old[gender]
        newtable = []
        for row in oldtable: # mutate in place
            newrow = row[:]
            event = row[0]
            distance = row[1]
            wr = row[2]
            if event not in new_events:
                print("Event %s for %s not in new tables, unchanged" % (event, gender))
            else:
                print("Amending", ev, "cells", len(newrow))
                for age in range(30, 111):
                    colidx = age - 2 
                    # is there a new factor?
                    key = (gender, event, age)
                    new_factor = new_factor_dict.get(key, None)
                    # if new_factor: # overwrite
                    f = float(new_factor)
                    if f == 1.0:
                        f = 1
                    print(colidx, key, f)
                    newrow[colidx] = f
            newtable.append(newrow)
        old[gender] = newtable


    old["ages"].extend(list(range(101,111)))

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