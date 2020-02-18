import sys, os, json, re
try:
    from athlib import codes
except ImportError:
    medir = os.path.dirname(sys.argv[0])
    if not medir: medir = os.getcwd()
    sys.path.insert(0,os.path.dirname(medir))
    from athlib import codes

def textWrapper(itext, texts, endText='}', endRemoveChars='\x20,', lim=80, wtext=4*'\x20'):
    L = [itext]
    w = len(itext)
    wtext = '\n' + wtext
    nwtext = len(wtext)
    for s in texts:
        ws = len(s)
        w += ws
        if w >= lim:
            while L[-1].endswith(' '): L[-1] = L[-1][:-1]
            s = wtext + s
            w = nwtext+ws
        L.append(s)
    while L[-1] and L[-1][-1] in endRemoveChars: L[-1] = L[-1][:-1]
    L[-1] += endText
    return ''.join(L)

md = []
mp = {}
pat_set = set()
for pat in dir(codes):
    obj = getattr(codes,pat)
    if isinstance(obj,re.Pattern):
        mp[pat] = obj.pattern
        I = obj.groupindex
        if pat.startswith('PAT_'): pat_set.add(pat)
        if I:
            md.append(textWrapper('  %s: {' % pat, (('%s: %s, ' % i) for i in I.items())))
if md:
    print('var __codesmap = {')
    print(',\n'.join(md))
    print('};')
    print(textWrapper('var __patObjs = [',('%s, ' % k for k in pat_set),endText='];',wtext='  '))
    print(textWrapper('var __patNames = [',('%r, ' % k for k in pat_set),endText='];',wtext='  '))
    print('''\nfunction codesmap(pattern, groupname, match) {
  var gx;

  if (typeof pattern === 'object') pattern = __patNames[__patObjs.indexOf(pattern)];
  gx = __codesmap[pattern];
  if (!gx) return null;
  gx = gx[groupname];
  if (gx == null) return null;
  gx = match[gx];
  return gx == null ? null : gx;
}
''')

ng_pat = re.compile(r'\(\?P<[^>]*>',re.M)
def jsversion(r):
    return ng_pat.sub('(',r)

PAT_LIST='''PAT_EVENT_CODE
PAT_FIELD
PAT_FINISH_RECORD
PAT_HORIZONTAL_JUMPS
PAT_HURDLES
PAT_JUMPS
PAT_LEADING_DIGITS
PAT_LEADING_FLOAT
PAT_LENGTH_EVENT
PAT_LONG_SECONDS
PAT_MULTI
PAT_NOT_FINISHED
PAT_PERF
PAT_RACES_FOR_DISTANCE
PAT_RELAYS
PAT_ROAD
PAT_RUN
PAT_THROWS
PAT_TIMED_EVENT
PAT_TRACK
PAT_VERTICAL_JUMPS'''.split();
PAT_SET = set(PAT_LIST)
for pat in PAT_LIST:
    print('var %s = /%s/;' %(pat,jsversion(mp[pat])))

if PAT_SET!=pat_set:
    print(40*'!')
    print('! PAT_SET does not match observed PATS_.....')
    print('! pat_set=%r' % pat_set)
    print('! PAT_SET=%r' % PAT_SET)
    print(40*'!')
