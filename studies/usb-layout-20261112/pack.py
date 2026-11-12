"""Conservative whole-courtyard packing study; no routing or qualification claim.
Run with OR-Tools 9.15.6755. Coordinates are integer micrometres. Supplier
courtyards, exact 90-degree rotations, and circumscribed screw octagons are used.
"""
import argparse, hashlib, json, math, re
from pathlib import Path
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=45);p.add_argument('--seed',type=int,default=11);args=p.parse_args()
plan=json.loads((ROOT/'config/component-plan.json').read_text())['components']; pop=json.loads((ROOT/'config/population.json').read_text())
manifest=json.loads((ROOT/'checks/import-manifest.json').read_text())['imports']
paths={x['part']:next(f['path'] for f in x['files'] if f['path'].endswith('.tsx'))for x in manifest}
paths.update({'C160390':'studies/usb-layout-20261112/import-staging/imports/BM04B_SRSS_TB_LF__SN_/BM04B_SRSS_TB_LF__SN_.tsx','C5240853':'studies/smaller-parts-20261112/import-staging/imports/INA241A2IDDFR/INA241A2IDDFR.tsx','C48970434':'studies/smaller-parts-20261112/bulk-import-staging/imports/RYHG35V47UF5_8/RYHG35V47UF5_8.tsx'})
plan.update(J_MOTOR='C160390',U_IA='C5240853',U_IB='C5240853',C_BULK='C48970434')
rects={};inputs={}
for name,part in plan.items():
 if name in pop['DNP']: continue
 f=ROOT/paths[part]; t=f.read_text();points=json.loads(re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',t)[1]); xs=[v['x']for v in points];ys=[v['y']for v in points];bounds=[min(xs),min(ys),max(xs),max(ys)]
 if abs((max(xs)-min(xs))*(max(ys)-min(ys))-abs(sum(a['x']*b['y']-b['x']*a['y']for a,b in zip(points,points[1:]+points[:1])))/2)>1e-7: raise ValueError('Nonrectangular courtyard '+name)
 rects[name]={'part':part,'bounds':bounds,'path':paths[part]};inputs[paths[part]]=hashlib.sha256(f.read_bytes()).hexdigest()
model=cp_model.CpModel();vars={};xi=[];yi=[]
for name,r in rects.items():
 a,b,c,d=r['bounds'];w0=math.ceil((c-a)*1000);h0=math.ceil((d-b)*1000)
 x=model.new_int_var(-14000,14000,name+'_x');y=model.new_int_var(-14000,14000,name+'_y'); rot=model.new_int_var(0,1,name+'_rot');w=model.new_int_var(min(w0,h0),max(w0,h0),name+'_w');h=model.new_int_var(min(w0,h0),max(w0,h0),name+'_h')
 model.add(w==w0+(h0-w0)*rot);model.add(h==h0+(w0-h0)*rot);model.add(x+w<=14000);model.add(y+h<=14000)
 xi.append(model.new_fixed_size_interval_var(x,w0,name+'_ix0')) if False else None
 xe=model.new_int_var(-14000,14000,name+'_xe');ye=model.new_int_var(-14000,14000,name+'_ye'); model.add(xe==x+w);model.add(ye==y+h)
 xi.append(model.new_interval_var(x,w,xe,name+'_ix'));yi.append(model.new_interval_var(y,h,ye,name+'_iy'))
 # Any separating supporting line of the circumscribed octagon is sufficient
 # for avoiding its interior. This conservative test cannot overlap a disk.
 for cx,cy in [(-11500,-11500),(-11500,11500),(11500,-11500),(11500,11500)]:
  ds=[]
  for nx,ny in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   bv=model.new_bool_var(name+f'_sep{cx}_{cy}_{nx}_{ny}');ds.append(bv)
   nearest=nx*x+ny*y+(nx*w if nx<0 else 0)+(ny*h if ny<0 else 0)
   model.add(nearest>=nx*cx+ny*cy+math.ceil(2350*math.hypot(nx,ny))).only_enforce_if(bv)
  model.add_bool_or(ds)
 vars[name]=(x,y,w,h,rot)
 # Opposite board-edge USBs, all supplier courtyard inside board.
 if name in ['J_DATA','J_PD']:
  model.add(rot==0);model.add(x==-(w0//2));model.add(y==(-14000 if name=='J_DATA' else 14000-h0))
# Identical supplier courtyards are interchangeable for this geometry-only
# search. Break their permutation symmetry without claiming electrical order.
groups={}
for name,r in rects.items(): groups.setdefault(r['part'],[]).append(name)
for names in groups.values():
 for a,b in zip(names,names[1:]):
  ax,ay,*_=vars[a];bx,by,*_=vars[b]
  if a not in ['J_DATA','J_PD'] and b not in ['J_DATA','J_PD']:model.add(ax+28001*ay<=bx+28001*by)
model.add_no_overlap_2d(xi,yi)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=8;solver.parameters.random_seed=args.seed
status=solver.solve(model); result={'status':solver.status_name(status),'ortools_version':'9.15.6755','seconds_limit':args.seconds,'seed':args.seed,'workers':8,'wall_time_seconds':solver.wall_time,'fitted_count':len(rects),'rectangles':rects,'inputs_sha256':inputs,'qualified':False,'routed':False,'manufacturing_ready':False,'limits':'Whole supplier courtyards only, 0/90 rotation, screw circumscribed octagons. No body/height/mating cable/tool accessibility, proximity, thermal or electrical routing constraints. UNKNOWN is not proof of infeasibility.'}
if status in [cp_model.OPTIMAL,cp_model.FEASIBLE]:
 positions={};packing={}
 for name,(x,y,w,h,rot)in vars.items():
  xx,yy,ww,hh,rr=[solver.value(v)for v in [x,y,w,h,rot]];a,b,c,d=rects[name]['bounds'];angle=90*rr;ca=round(math.cos(math.radians(angle)));sa=round(math.sin(math.radians(angle))); pts=[(ca*u-sa*v,sa*u+ca*v)for u,v in [(a,b),(a,d),(c,b),(c,d)]]
  positions[name]={'pcbX':round(xx/1000-min(q[0]for q in pts),6),'pcbY':round(yy/1000-min(q[1]for q in pts),6),'pcbRotation':angle,'layer':'top'};packing[name]=[xx,yy,xx+ww,yy+hh]
 positions['U_ENCODER']={'pcbX':0,'pcbY':0,'pcbRotation':0,'layer':'bottom'}
 old=json.loads((ROOT/'config/placement.json').read_text())['placements'];positions.update({n:old[n]for n in pop['bare_pads']})
 result['packing_um']=packing; (OUT/'placement.json').write_text(json.dumps({'placements':positions},indent=2)+'\n')
(OUT/'packing.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['rectangles','inputs_sha256','packing_um']},indent=2))
