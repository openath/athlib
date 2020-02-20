#!/usr/bin/env python
import sys, os, re, time
medir = os.path.dirname(sys.argv[0])
if not medir: medir = os.getcwd()
try:
    from athlib.utils import parse_hms
except ImportError:
    sys.path.insert(0,os.path.dirname(medir))
    from athlib import parse_hms, normalize_event_code, normalize_gender
jumpCodeMap = {u'H\xf8yde':u'HJ', u'H\xf8yde u.t.':u'SHJ', u'Lengde':u'LJ',
        u'Lengde u.t.':u'SLJ', u'Tresteg':u'TJ', u'Stav':u'PV',
        u'Kule': u'SP', u'Diskos': u'DT', u'Slegge': u'HT',
        u'Spyd': u'JT', u'Liten ball': u'OT', u'Slengball': u'BT',
        }

def num(s):
    try:
        v = float(s)
        iv = int(v)
        return iv if v==iv else v
    except:
        pass

endCommaPat = re.compile(r',(?P<space>\s*)(?P<bracket>\]|\)|\})',re.M)
def cyv(v):
    '''convert a year value'''
    while v.count('.')>1: v = v.replace('.',':',1)
    if ':' in v:
        v = parse_hms(v)
    return num(v)

def shorten(line, indent=4):
    if len(line)<80: return line
    indent = max(indent+2,8)
    space = indent*'\x20'
    for pat in ('),', '],', '},', ','):
        x = line.rfind(pat,0,80-len(pat))
        if x>=0:
            x += len(pat)
            return line[:x]+'\n'+shorten(space+line[x:].strip(), indent)
    return line

def translate(txt):
    gender = 'M' if 'Gutter' in txt else 'F'
    out = ['\x20\x20%r: {' % gender].append
    txt = txt.replace(',','.')
    try:
        txt = decode('utf-8')
    except:
        pass

    L = txt.split('\n')
    arPat = re.compile(r'^\d\d\s+år\s*$')
    hdrs = L.pop(0).split('\t')
    if hdrs[1]!='Multiplikator':
        raise ValueError('badly formatted Tyrving table text' % hdrs[0])
    years = [int(_.split()[0]) for _ in hdrs if arPat.match(_)]
    racePat = re.compile(r'^(?P<meters>\d+)\s*m\s*(?P<H>H)?\s*$')
    i = 0
    n = len(L)

    def xyv(line, start):
        values = [v.strip() for v in line[start:]]
        if len(values)!=len(years):
            raise ValueError('badly formatted age values in %r' % line)
        for y, v in enumerate(values):
            if v: break
        first = y
        for y,v in enumerate(reversed(values)):
            if v: break
        last = len(values) - y - 1
        if [v for v in values[first:last+1] if not v]:
            #we have a gap
            yv = {}
            for y,v in zip(years,values):
                v = v.strip()
                if not v: continue
                yv[y] = cyv(v)
            return yv
        else:
            return [years[first],[cyv(v) for v in values[first:last+1]]]
            
    while i<n:
        line = L[i]
        i += 1
        if not line.strip(): continue
        line = line.split('\t')
        l0 = line[0]
        m = racePat.match(l0)
        if m:
            kind = 'race'
            dist = int(m.group('meters'))
            xvx = 6
            if m.group('H'):
                #hurdle race
                if dist>400:
                    code = '%sSC' % dist
                    mx = 2
                else:
                    code = '%sH' % dist
                    hhh = line[1].strip()
                    hsd = line[2].strip()
                    if hhh and hsd:
                        code = ' '.join((code,hhh,hsd))
                    else:
                        raise ValueError('Badly formatted hurdle row %r' % line)
                    mx = 5
            elif line[1]==u'Kappgang':
                code = '%sW' % dist
                mx = 5
            else:
                code = m.group('meters')
                mx = 1
            multiplier = num(line[mx])
            yv = xyv(line,xvx)
            args = [dist,multiplier,yv]
            #out('%s%r: TyrvingRace(%s,%s,%r),' % (4*'\x20',code,dist,multiplier,yv))
        elif l0 in (u'H\xf8yde', u'H\xf8yde u.t.', u'Lengde', u'Lengde u.t.', u'Tresteg'):
            multiplier = num(line[1])
            yv = xyv(line,xvx)
            code = jumpCodeMap[l0]
            kind = 'jump'
            args = [multiplier,yv]
            #out('%s%r: TyrvingJump(%r,%s,%r),' % (4*'\x20',code,code,multiplier,yv))
        else:
            code = jumpCodeMap[l0]
            line1 = L[i].split('\t')
            line2 = L[i+1].split('\t')
            i += 2
            mx = 4
            xvx= 6
            multipliers = [num(_[mx]) for _ in (line,line1,line2)]
            yvs = [xyv(_,xvx) for _ in (line,line1,line2)]
            args = [multipliers,yvs]
            if l0=='Stav':
                kind = 'pv'
            elif l0 in (u'Kule',u'Diskos',u'Slegge',u'Spyd',u'Liten ball',u'Slengball'):
                code += line1[0].strip()
                kind = 'throw'
            else:
                raise ValueError('Unknown code in line %r' % line)
        out(shorten('%s%r: [%r, %r],' % (4*'\x20', normalize_event_code(code), kind, args)))
    out('\x20\x20},')
    return out.__self__

def installText(s, fn, c='#', t=''):
    if not os.path.isfile(fn):
        raise ValueError('cannot locate file %r' % fn)
    with open(fn,'r') as f:
        txt = f.read()
    start = '%sstart tyrving tables' % c
    i = txt.find('\n'+start)
    if i>=0:
        iold = txt.find('\n',i+1)
        if iold>=0:
            iold += 1
        else:                       
            raise ValueError('cannot find end of start line in %r' % fn)
        end = '%send tyrving tables\n' % c
        nend = '\n' + end
        j = txt.find(nend)
        if j>=i:
            jold = j
            j += len(nend)
        else:
            raise ValueError('found start of tyrving tables did not find end in %r' % fn)
        sold = txt[iold:jold]
        if sold==s:
            print('code unchanged in %r' % fn)
            return
        txt = ''.join((txt[:i] + '\n', start, t, '\n', s, '\n', end, txt[j:]))
    else:
        raise ValueError('could not find start of tyrving tables in %r' % fn)
    bfn = os.path.splitext(os.path.basename(fn))
    bfn = os.path.normpath(os.path.join(medir,'..','tmp','%s-%s%s' % (bfn[0],int(time.time()),bfn[1])))
    import shutil
    shutil.move(fn, bfn)
    with open(fn,'w') as f:
        f.write(txt)

def main():
    s = ['_tyrvingTables = {']
    install = '--install' in sys.argv
    if install:
        while '--install' in sys.argv:
            sys.argv.remove('--install')
    FN = sys.argv[1:]
    if not FN:
        from glob import glob
        FN = glob(os.path.join(medir,'data','tyrving_?.tsv'))
    for fn in FN:
        with open(fn,'r') as f:
            s.extend(translate(f.read()))
    s.append('}')
    s = endCommaPat.sub(r'\g<space>\g<bracket>','\n'.join(s))
    if install:
        t = ' created by %s %s' % (os.path.basename(sys.argv[0]),time.asctime())
        installText(s, os.path.normpath(os.path.join(medir,'..','athlib','tyrving_score.py')), c='#', t=t)
        js = ('/* eslint-disable */\nvar '+s+';\n/* eslint-enable */')
        installText(js, os.path.normpath(os.path.join(medir,'..','js','src', 'tyrving_score.js')), c='// ', t=t)
    else:
        print(s)

if __name__=='__main__':
    main()
