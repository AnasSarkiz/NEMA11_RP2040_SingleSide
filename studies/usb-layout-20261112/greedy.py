"""Independent constructive rectangle search. No manufacture/route claim."""
import json, math, random, time
from pathlib import Path
OUT=Path(__file__).resolve().parent; data=json.loads((OUT/'packing.json').read_text()); rects=data['rectangles']; W=28000
sizes={n:tuple(math.ceil((r['bounds'][j+2]-r['bounds'][j])*1000)for j in [0,1])for n,r in rects.items()}
def intersects(a,b):return a[0]<b[2]and b[0]<a[2]and a[1]<b[3]and b[1]<a[3]
def split(free,used):
 out=[]
 for f in free:
  if not intersects(f,used):out.append(f);continue
  l,b,r,t=f;x,y,xx,yy=used
  if l<x<r:out.append((l,b,x,t))
  if l<xx<r:out.append((xx,b,r,t))
  if b<y<t:out.append((l,b,r,y))
  if b<yy<t:out.append((l,yy,r,t))
 out=list(set(out));return [a for i,a in enumerate(out)if not any(i!=j and b[0]<=a[0]and b[1]<=a[1]and b[2]>=a[2]and b[3]>=a[3]for j,b in enumerate(out))]
obstacles=[]
# Enclosing step approximation of exact circular screw exclusions. Each row
# uses the maximum disk x extent over the row, rounded outward, never inward.
for cx,cy in [(2500,2500),(2500,25500),(25500,2500),(25500,25500)]:
 for y in range(cy-2350,cy+2350,470):
  top=min(y+470,cy+2350);dy=max(0,y-cy,cy-top);dx=math.ceil(math.sqrt(2350**2-dy**2));obstacles.append((cx-dx,y,cx+dx,top))
fixed={}
for n,y0 in [('J_DATA',0),('J_PD',W-sizes['J_PD'][1])]:
 w,h=sizes[n];x0=(W-w)//2;fixed[n]=(x0,y0,x0+w,y0+h,0);obstacles.append(fixed[n][:4])
base=[(0,0,W,W)]
for o in obstacles:base=split(base,o)
rng=random.Random(53);best=None;start=time.monotonic()
for iteration in range(500):
 mode=iteration%4;power=[1,1.3,.8,1][mode]
 order=sorted([n for n in sizes if n not in fixed],key=lambda n:-(sizes[n][0]*sizes[n][1])**power*rng.uniform(.75,1.25))
 free=base[:];poses=dict(fixed);unplaced=[]
 for n in order:
  w,h=sizes[n];choices=[]
  for l,b,r,t in free:
   for rr,(ww,hh)in enumerate([(w,h),(h,w)]):
    if ww<=r-l and hh<=t-b:
     small=min(r-l-ww,t-b-hh);large=max(r-l-ww,t-b-hh)
     score=(small,large,b,l)if mode in [0,1]else((r-l)*(t-b)-ww*hh,small,b,l)
     choices.append((score,(l,b,l+ww,b+hh,rr)))
  if not choices:unplaced.append(n);continue
  _,chosen=min(choices);poses[n]=chosen;free=split(free,chosen[:4])
 missing=sum(sizes[n][0]*sizes[n][1]for n in unplaced)
 if best is None or missing<best[0]:
  best=(missing,poses,unplaced,iteration);print('best',iteration,'missing_area',missing/1e6,'unplaced',unplaced,flush=True)
 if not unplaced:break
result={'iterations':iteration+1,'wall_seconds':time.monotonic()-start,'missing_area_mm2':best[0]/1e6,'unplaced':best[2],'packing_um':{n:[v[0]-14000,v[1]-14000,v[2]-14000,v[3]-14000,v[4]]for n,v in best[1].items()},'complete':not best[2],'qualified':False,'obstacles_um':obstacles,'method':'MaxRects with enclosing 0.47mm circle steps, fixed opposite USBs, seed53; 500-order limit'}
(OUT/'greedy.json').write_text(json.dumps(result,indent=2)+'\n')
if result['complete']:
 pos={}
 for n,(x,y,xx,yy,rr)in result['packing_um'].items():
  a,b,c,d=rects[n]['bounds'];points=[(u,v)if rr==0 else(-v,u)for u,v in [(a,b),(a,d),(c,b),(c,d)]]
  pos[n]={'pcbX':round(x/1000-min(q[0]for q in points),6),'pcbY':round(y/1000-min(q[1]for q in points),6),'pcbRotation':90*rr,'layer':'top'}
 old=json.loads((OUT.parents[1]/'config/placement.json').read_text())['placements'];pop=json.loads((OUT.parents[1]/'config/population.json').read_text());pos.update({n:old[n]for n in pop['bare_pads']+pop['DNP']});(OUT/'placement.json').write_text(json.dumps({'placements':pos},indent=2)+'\n')
