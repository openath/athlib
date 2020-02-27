#!/usr/bin/env python
#process the qkids.tsv file to create qkis_score data
#*NB* these athletic idiots are unable to process times properly
#so their spreadsheet had 3.50 for 3:50 and 0.01 instead of 0:01
#bah :(
import sys, os, re, time
medir = os.path.dirname(sys.argv[0])
if not medir: medir = os.getcwd()
try:
    from athlib.utils import parse_hms
except ImportError:
    sys.path.insert(0,os.path.dirname(medir))
    from athlib import parse_hms, normalize_event_code, normalize_gender

def num(s):
    try:
        v = float(s)
        iv = int(v)
        return iv if v==iv else v
    except:
        pass

endCommaPat = re.compile(r',(?P<space>\s*)(?P<bracket>\]|\)|\})',re.M)

def shorten(line, indent=4, inc=2):
    if len(line)<80: return line
    indent = min(indent+inc,8)
    space = indent*'\x20'
    for pat in ('),', '],', '},', ','):
        x = line.rfind(pat,0,80-len(pat))
        if x>=0:
            x += len(pat)
            return line[:x]+'\n'+shorten(space+line[x:].strip(), indent, inc)
    return line

compTypeMap = {
            'Wessex League': 'QKWL',
            'Wessex League (U13)': 'QKWLU13',
            'QuadKids Secondary': 'QKSEC',
            'QuadKids Primary': 'QKPRI',
            'QuadKids Start': 'QKSTA',
            'QuadKids Club': 'QKCLUB',
            'QuadKids Club U13': 'QKCLU13',
            'QuadKids Club U9': 'QKCLU9',
            'QuadKids Pre-Start': 'QKPRE',
            }
ecodeMap = {
        '50m': '50',
        '75m': '75',
        '70/75mh': '70H',
        '100m': '100',
        '300m': '300',
        '400m': '400',
        '600m': '600',
        '800m': '800',
        'relay': '4x100',
        'long_jump': 'LJ',
        'howler': 'OT',
        'slj': 'SLJ',
        'shot': 'SP',
        }

def possible_hms(v):
    return parse_hms(v) if ':' in v else float(v)

def translate(txt, _70H):
    try:
        txt = decode('utf-8')
    except:
        pass

    out = [].append
    L = txt.split('\n')
    i = 0
    n = len(L)
    while i<n:
        line = L[i]
        i += 1
        if not line.strip(): continue
        line = line.split('\t')
        line = [_.strip() for _ in line if _.strip()]
        ll = len(line)
        if ll!=1: raise ValueError('bad comptype line %d:%r in tsv file' % (i, L[i]))
        try:
            if ll==1:
                #start of a new label
                l0 = line[0]
                compType = compTypeMap[l0]
                out('\x20\x20%r: {' % compType)
                data = [].append
                for kind in 'ecode inc min max'.split():
                    line = L[i]
                    i += 1
                    line = line.split('\t')
                    line = [_.strip() for _ in line if _.strip()]
                    if kind=='ecode':
                        data([ecodeMap[_.lower()] for _ in line[1:6]])
                    else:
                        data([possible_hms(_) for _ in line[1:6]])
                data = data.__self__
                t = [].append
                for j in range(5):
                    t('\x20\x20\x20\x20%r: ['%data[0][j])
                    if data[0][j]=='70H':
                        _70H.append(compType);
                    t('%s, ' % data[1][j])
                    t('%s, ' % data[2][j])
                    t('%s]%s' % (data[3][j],',\n' if j<4 else ','))
                out(''.join(t.__self__))
                out('\x20\x20\x20\x20},')
        except:
            raise ValueError('unexpected error in line %s: %s' % (i,L[i]))

    out('\x20\x20},')
    return out.__self__

def installText(s, fn, c='#', t=''):
    if not os.path.isfile(fn):
        raise ValueError('cannot locate file %r' % fn)
    with open(fn,'r') as f:
        txt = f.read()
    start = '%sstart qkids tables' % c
    i = txt.find('\n'+start)
    if i>=0:
        iold = txt.find('\n',i+1)
        if iold>=0:
            iold += 1
        else:
            raise ValueError('cannot find end of start line in %r' % fn)
        end = '%send qkids tables\n' % c
        nend = '\n' + end
        j = txt.find(nend)
        if j>=i:
            jold = j
            j += len(nend)
        else:
            raise ValueError('found start of qkids tables did not find end in %r' % fn)
        sold = txt[iold:jold]
        if sold==s:
            print('code unchanged in %r' % fn)
            return
        txt = ''.join((txt[:i] + '\n', start, t, '\n', s, '\n', end, txt[j:]))
    else:
        raise ValueError('could not find start of qkids tables in %r' % fn)
    bfn = os.path.splitext(os.path.basename(fn))
    bfn = os.path.normpath(os.path.join(medir,'..','tmp','%s-%s%s' % (bfn[0],int(time.time()),bfn[1])))
    import shutil
    shutil.move(fn, bfn)
    with open(fn,'w') as f:
        f.write(txt)

def main():
    tableName = '_qkidsTables'
    s = ['%s = {' % tableName]
    install = '--install' in sys.argv
    if install:
        while '--install' in sys.argv:
            sys.argv.remove('--install')
    FN = sys.argv[1:]
    if not FN:
        from glob import glob
        FN = glob(os.path.join(medir,'data','qkids.tsv'))
    _70H = []
    for fn in FN:
        with open(fn,'r') as f:
            s.extend(translate(f.read(), _70H))
    s.append('}')
    _70H = '\n'.join(("%s['%s']['75H'] = %s['%s']['70H']" % (tableName,_,tableName,_) for _ in _70H))
    s1 = '' if not _70H else '\n'+_70H
    s2 = shorten('\n_compTypeMap = {%s}' % ', '.join(("'%s': '%s'" % (k.replace(' ','').upper(),v) for k,v in compTypeMap.items())),
            indent=2, inc=0)
    s = endCommaPat.sub(r'\g<space>\g<bracket>','\n'.join(s))[:-2]
    if install:
        t = ' created by %s %s' % (os.path.basename(sys.argv[0]),time.asctime())
        installText(s+s1+s2, os.path.normpath(os.path.join(medir,'..','athlib','qkids_score.py')), c='#', t=t)
        js = '/* eslint-disable */\nvar '+s + ';'
        s1 = '\n '+s1[1:].replace('\n',';\n') + ';'
        installText(js+s1+'\nvar '+s2[1:]+';\n/* eslint-enable */', os.path.normpath(os.path.join(medir,'..','js','src', 'qkids_score.js')), c='// ', t=t)
    else:
        print(s+s1+s2)

if __name__=='__main__':
    main()
