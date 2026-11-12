"""Audit untouched USB imports against native geometry and isolated CAM; never edits inputs."""
from pathlib import Path
import collections,hashlib,json,math,re,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[2]
STUDY=Path(__file__).resolve().parent
def area(q):return abs(sum(a['x']*b['y']-b['x']*a['y']for a,b in zip(q,q[1:]+q[:1])))/2
def source_area(p):return area(json.loads(re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',p.read_text())[1]))
def load_native(n):return json.loads((ROOT/f'dist/studies/usb-followup-20261112/{n}/circuit.json').read_text())
def counts(a):return dict(collections.Counter(x['type']for x in a))
a=load_native('rotation'); sc={x['source_component_id']:x for x in a if x['type']=='source_component'}
rows=[]
for c in [x for x in a if x['type']=='pcb_component']:
 i=c['pcb_component_id'];angle=c['rotation'];h=[x for x in a if x['type']=='pcb_hole'and x.get('pcb_component_id')==i];slots=[x for x in h if x['hole_shape']in ['pill','rotated_pill']];shell=[x for x in a if x['type']=='pcb_plated_hole'and x.get('pcb_component_id')==i];pads=[x for x in a if x['type']=='pcb_smtpad'and x.get('pcb_component_id')==i];paste=collections.Counter(x['layer']for x in a if x['type']=='pcb_solder_paste'and x.get('pcb_component_id')==i)
 assert len(h)==2 and len(slots)==1 and len(shell)==4 and len(pads)==16
 slot=slots[0];theta=math.radians(angle);x,y=3.7999924,.0000254;expected=(c['footprint_origin']['x']+x*math.cos(theta)-y*math.sin(theta),c['footprint_origin']['y']+x*math.sin(theta)+y*math.cos(theta))
 assert math.dist((slot['x'],slot['y']),expected)<1e-7
 assert math.isclose(slot['hole_width'],1.5099792,abs_tol=1e-8)and math.isclose(slot['hole_height'],.7099808,abs_tol=1e-8)
 assert math.isclose(slot.get('ccw_rotation',0)%360,angle%360,abs_tol=1e-8)
 assert all(math.isclose((p['ccw_rotation']-angle)%360,90,abs_tol=1e-8)for p in shell)
 assert paste=={'top':20,'bottom':4}
 rows.append({'name':sc[c['source_component_id']]['name'],'rotation_deg':angle,'slot':slot,'shell_slots':len(shell),'signal_pads':len(pads),'paste_by_layer':dict(paste)})
assert not any('error'in x['type']or x['type']in ['pcb_trace','pcb_via']for x in a)
cam=STUDY/'cam'
def drill_slots(name):
 tools={};tool=None;last=None;out=[]
 for line in (cam/name).read_text().splitlines():
  m=re.fullmatch(r'T(\d+)C([\d.]+)',line)
  if m:tools[m[1]]=float(m[2]);continue
  m=re.fullmatch(r'T(\d+)',line)
  if m:tool=m[1];continue
  m=re.fullmatch(r'(G85)?X(-?[\d.]+)Y(-?[\d.]+)',line)
  if m:
   point=(float(m[2]),float(m[3]))
   if m[1]:
    out.append({'center':[(last[0]+point[0])/2,(last[1]+point[1])/2],'diameter':tools[tool],'total_length':math.dist(last,point)+tools[tool],'axis_deg':math.degrees(math.atan2(point[1]-last[1],point[0]-last[0]))%180})
   last=point
 return out
slots=drill_slots('drill_npth.drl');assert len(slots)==4
for r in rows:
 s=r['slot'];c=min(slots,key=lambda x:math.dist(x['center'],(s['x'],s['y'])))
 assert math.dist(c['center'],(s['x'],s['y']))<.0005
 assert math.isclose(c['total_length'],s['hole_width'],abs_tol=.0005)and math.isclose(c['diameter'],s['hole_height'],abs_tol=.0005)
 assert abs(c['axis_deg']-r['rotation_deg']%180)<.1
assert len(drill_slots('drill-L1-L2.drl'))==16
flashes={n:len(re.findall(r'D03\*',(cam/n).read_text()))for n in ['F_Paste.gbr','B_Paste.gbr']};assert flashes=={'F_Paste.gbr':80,'B_Paste.gbr':16}
b=load_native('alternatives');bs={x['source_component_id']:x for x in b if x['type']=='source_component'}
alternatives=[]
for c in [x for x in b if x['type']=='pcb_component']:
 comp=bs[c['source_component_id']];id=comp['supplier_part_numbers']['jlcpcb'][0];files=list((STUDY/'import-staging/imports').glob('*/*.tsx'));f=next(p for p in files if id in p.read_text());q=next(x['outline']for x in b if x['type']=='pcb_courtyard_outline'and x['pcb_component_id']==c['pcb_component_id']);ar=area(q);assert math.isclose(ar,source_area(f),abs_tol=1e-8)
 alternatives.append({'part':id,'manufacturer_part_number':comp['manufacturer_part_number'],'native_and_source_courtyard_mm2':ar,'increase_vs_USB4145_mm2':ar-46.55962273044746,'native_holes':[x for x in b if x['type']=='pcb_hole'and x.get('pcb_component_id')==c['pcb_component_id']],'paste_by_layer':dict(collections.Counter(x['layer']for x in b if x['type']=='pcb_solder_paste'and x.get('pcb_component_id')==c['pcb_component_id'])),'qualified':False})
assert not any('error'in x['type']or x['type']in ['pcb_trace','pcb_via']for x in b)
raw=json.loads((STUDY/'sources/C7374561.raweasy.json').read_text());raw_holes=[]
for s in raw['packageDetail']['dataStr']['shape']:
 if s.startswith('HOLE~'):raw_holes.append({'raw':s,'diameter_mm':float(s.split('~')[3])*.254*2})
assert sorted(round(x['diameter_mm'],7)for x in raw_holes)==[.649986,.8499856]
unchanged=subprocess.check_output(['git','diff','--name-only','ebebbf2','--','index.circuit.tsx','config','imports','scripts','dist/index'],cwd=ROOT,text=True).strip()==''
assert unchanged
result={'base_commit':'90f86f315744263af66219bfe5e9094a67678fe7','cli':'0.1.2454','tscircuit':'0.0.3165','core':'0.0.2347','active_controller_unchanged':unchanged,'rotations':rows,'npth_CAM_slots':slots,'paste_CAM_flashes':flashes,'rotation_native_counts':counts(a),'alternative_native_counts':counts(b),'alternatives':alternatives,'USB4140_supplier_raw_holes':raw_holes,'USB4145_A2_recommended_slot_mm':[1.01,.71],'drawing_slot_tolerance_mm':.05,'USB4145_slot_excess_above_max_mm':1.5099792-1.06,'USB4140_A3_recommended_round_and_slot_mm':{'round':.70,'slot':[1.00,.70]},'qualified':False,'routing_attempted':False,'manufacturing_ready':False,'limits':'Independent connector diagnostics, not full controller placement or a top-only assembly acceptance. CAM is measurement evidence, not manufacturing release. Alternatives are larger and unqualified. No native/import override or source edit.'}
print(json.dumps(result,indent=2))
