import pymupdf,re,sys,json
def spans(page):
  r=[]
  for b in page.get_text('dict')['blocks']:
    for l in b.get('lines',[]):
      for s in l['spans']:
        t=s['text'].strip()
        if t: r.append(dict(x=s['bbox'][0],y=(s['bbox'][1]+s['bbox'][3])/2,x1=s['bbox'][2],size=s['size'],font=s['font'],t=t))
  return r
def parse(path):
  d=pymupdf.open(path); res=[]
  for pi,p in enumerate(d):
    S=spans(p)
    nums=[s for s in S if re.fullmatch(r'\d{1,3}',s['t'])]
    others=[s for s in S if s not in nums]
    used=set(); pairs=[]
    for n in nums:
      c=[o for o in others if abs(o['y']-n['y'])<3.5 and 0<=o['x']-n['x1']<40 and id(o) not in used]
      if not c: pairs.append((n,None)); continue
      o=min(c,key=lambda o:o['x']-n['x1']); used.add(id(o)); pairs.append((n,o))
    rest=[o for o in others if id(o) not in used]
    res.append((pi,pairs,rest))
  return res
if __name__=='__main__':
  for pi,pairs,rest in parse(sys.argv[1]):
    print('#### page',pi,'pairs',len(pairs),'unpaired nums',[n['t'] for n,o in pairs if o is None])
    for o in sorted(rest,key=lambda o:(o['y'],o['x'])): print(f"  REST {o['x']:6.1f} {o['y']:6.1f} {o['size']:4.1f} {o['t']}")
