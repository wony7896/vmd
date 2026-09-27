import csv,sys
from parse import parse
def dedup(pairs):
  seen=set();out=[]
  for n,o in pairs:
    k=(n['t'],round(n['x']),round(n['y']))
    if k in seen or o is None: continue
    seen.add(k); out.append((n,o))
  return out
def colsort(pairs):
  # column-major: group by x of number
  xs=sorted({round(n['x']) for n,o in pairs})
  cols=[];
  for x in xs:
    if cols and x-cols[-1][-1]<15: cols[-1].append(x)
    else: cols.append([x])
  def ci(n): return next(i for i,c in enumerate(cols) if round(n['x']) in c)
  return sorted(pairs,key=lambda p:(ci(p[0]),p[0]['y']))
def run(path,tiers):
  (p0,f,frest),(p1,b,brest)=parse(path)
  heads=sorted([n for n,o in f if o is None],key=lambda n:n['y'])
  f=dedup(f); b=dedup(b)
  front={}
  for i,h in enumerate(heads):
    y2=heads[i+1]['y'] if i+1<len(heads) else 1e9
    sec=[p for p in f if h['y']<p[0]['y']<y2]
    for k,(n,o) in enumerate(colsort(sec)):
      front.setdefault(int(n['t']),[]).append((tiers[i],o['t'],k))
  # genre headers
  gs={}
  for o in brest:
    if o['x']<120 and o['size']>9.5 and o['t']!='|' and o['y']<800: gs.setdefault(round(o['y']),[]).append(o)
  gh=sorted((y,' | '.join(s['t'] for s in sorted(v,key=lambda s:s['x']))) for y,v in gs.items())
  back={}
  for i,(y,g) in enumerate(gh):
    y2=gh[i+1][0] if i+1<len(gh) else 1e9
    sec=[p for p in b if y<p[0]['y']<y2]
    for k,(n,o) in enumerate(colsort(sec)):
      back.setdefault(int(n['t']),[]).append((g,o['t'],k))
  return front,back,[h['t'] for h in heads],gh
