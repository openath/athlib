from athlib import codes
import re
md = []
mp = {}
for pat in dir(codes):
    obj = getattr(codes,pat)
    if isinstance(obj,re.Pattern):
        mp[pat] = obj.pattern
        I = obj.groupindex
        if I:
            md.append('  %s: {%s}' % (pat,', '.join(('%s: %s' % i for i in I.items()))))
if md:
    print('var __codesmap = {')
    print(',\n'.join(md))
    print('};')
    print('''\nfunction codesmap(pattern, groupname, match) {
  var gx = __codesmap[pattern];
  if (!gx) return null;
  gx = gx[groupname];
  if (gx == null) return null;
  return match.group(gx);
}
''')

ng_pat = re.compile(r'\(\?P<[^>]*>',re.M)
def jsversion(r):
    return ng_pat.sub('(',r)

for pat in '''PAT_EVENT_CODE
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
PAT_VERTICAL_JUMPS'''.split():
    print('var %s = /%s/;' %(pat,jsversion(mp[pat])))
