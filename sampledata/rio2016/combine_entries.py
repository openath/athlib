import os
import json
import glob


def run():
    all = []
    for filename in glob.glob('rio_entries_day_*.json'):
        root, ext = os.path.splitext(filename)
        words = root.split('_')
        daycode = words[-1]

        raw = open(filename).read()
        j = json.loads(raw)
        for dikt in j['athletes']:
            dikt['day'] = int(daycode)
            all.append(dikt)

    outfn = 'rio_entries.json'
    f = open(outfn, 'wb')
    f.write(json.dumps(all, indent=4))
    f.close()
    print "wrote", outfn


if __name__ == '__main__':
    run()
