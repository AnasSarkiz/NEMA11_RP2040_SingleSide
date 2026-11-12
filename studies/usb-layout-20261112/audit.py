"""Read-only checks of supplier/native geometry, retained nets and rejected fit."""
import collections,hashlib,json,math,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
load=lambda p:json.loads((ROOT/p).read_text())
h=load('dist/studies/usb-layout-20261112/harness/circuit.json');c=load('dist/studies/usb-layout-20261112/controller/circuit.json');base=load('dist/index/circuit.json')
def counts(a):return dict(collections.Counter(x['type']for x in a))
def bindings(a):
 comps={x['source_component_id']:x['name']for x in a if x['type']=='source_component'}; nets={x['source_net_id']:x['name']for x in a if x['type']=='source_net'};ports={x['source_port_id']:(comps[x['source_component_id']],x.get('pin_number'))for x in a if x['type']=='source_port'};b=collections.defaultdict(set)
 for x in a:
  if x['type']=='source_trace':
   for p in x.get('connected_source_port_ids',[]):b[ports[p]].update(nets[n]for n in x.get('connected_source_net_ids',[]))
 return dict(b)
cb,bb=bindings(c),bindings(base);changed={n for n,p in set(bb)|set(cb)if cb.get((n,p),set())!=bb.get((n,p),set())};assert changed=={'U_IA','U_IB'}
for n,phase in [('U_IA','A'),('U_IB','B')]:
 expected={1:f'{phase}_PLUS',2:'GND',3:'GND',4:'GND',5:f'I_{phase}_RAW',6:'V3V3',7:'V3V3',8:f'{phase}_DRV_PLUS'}
 assert all(cb[n,p]=={net}for p,net in expected.items())
assert {x['name']for x in c if x['type']=='source_component'}=={x['name']for x in base if x['type']=='source_component'}
assert {x['name']for x in c if x['type']=='source_net'}=={x['name']for x in base if x['type']=='source_net'}
assert counts(c)['source_component']==109 and counts(c)['source_net']==73 and counts(c)['schematic_sheet']==7
assert not any(x['type']in ['pcb_trace','pcb_via']for x in c)
pc={x['pcb_component_id']:x for x in c if x['type']=='pcb_component'};sc={x['source_component_id']:x for x in c if x['type']=='source_component'}
assert all(x['layer']=='top'for x in pc.values()if not x.get('do_not_place'))
packing=load('studies/usb-layout-20261112/greedy.json');rects=load('studies/usb-layout-20261112/packing.json')['rectangles'];boxes=packing['packing_um'];assert len(boxes)+len(packing['unplaced'])==101
for n,(l,b,r,t,rot)in boxes.items():
 assert -14000<=l<r<=14000 and -14000<=b<t<=14000
 for cx,cy in [(-11500,-11500),(-11500,11500),(11500,-11500),(11500,11500)]:
  dx=max(l-cx,0,cx-r);dy=max(b-cy,0,cy-t);assert dx*dx+dy*dy>=2350**2
 for nn,(ll,bb_,rr,tt,_)in boxes.items():
  if n!=nn:assert not(l<rr and ll<r and b<tt and bb_<t)
# Independent native courtyard comparison uses the transformed supplier polygon,
# not pcb_component.center (which is not always the footprint origin).
for q in [x for x in c if x['type']=='pcb_courtyard_outline']:
 name=sc[pc[q['pcb_component_id']]['source_component_id']]['name']
 if name not in boxes:continue
 l,b,r,t,_=boxes[name];xs=[p['x']for p in q['outline']];ys=[p['y']for p in q['outline']]
 assert abs(min(xs)-l/1000)<.000002 and abs(min(ys)-b/1000)<.000002
 assert max(xs)<=r/1000+.000002 and max(ys)<=t/1000+.000002
hp={x['pcb_port_id']:x['source_port_id']for x in h if x['type']=='pcb_port'};sp={x['source_port_id']:int(next(v for v in x['port_hints']if v.isdigit()))for x in h if x['type']=='source_port'}
land=[]
for pad in [x for x in h if x['type']=='pcb_smtpad']:
 pin=sp[hp[pad['pcb_port_id']]];w,hh=pad['width'],pad['height']
 assert abs(w-(.6 if pin<=4 else 1.2))<.0001 and abs(hh-(1.55 if pin<=4 else 1.8))<.0001
 land.append({'pin':pin,'center_mm':[pad['x'],pad['y']],'size_mm':[w,hh]})
assert counts(h)['pcb_smtpad']==6 and counts(h)['pcb_solder_paste']==6
assert not any('error'in x['type']or x['type']=='pcb_plated_hole'for x in h)
assert all(x['layer']=='top'for x in h if x['type']=='pcb_solder_paste')
source=(OUT/'import-staging/imports/BM04B_SRSS_TB_LF__SN_/BM04B_SRSS_TB_LF__SN_.tsx').read_text();q=json.loads(re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',source)[1]);area=abs(sum(a['x']*b['y']-b['x']*a['y']for a,b in zip(q,q[1:]+q[:1])))/2
assert math.isclose(area,34.309821418905145,abs_tol=1e-8)
unchanged=subprocess.check_output(['git','diff','--name-only','ebebbf2','--','index.circuit.tsx','config','imports','scripts','dist/index'],cwd=ROOT,text=True).strip()=='';assert unchanged
inp=load('studies/usb-layout-20261112/packing.json')['inputs_sha256']
for p,digest in inp.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest
result={'active_controller_unchanged':unchanged,'user_allows_qualified_compact_harness':True,'header_part':'BM04B-SRSS-TB(LF)(SN)','header_jlcpcb':'C160390','header_courtyard_mm2':area,'header_native_lands':land,'header_paste_layers':dict(collections.Counter(x['layer']for x in h if x['type']=='pcb_solder_paste')),'header_native_errors':0,'header_native_warnings':sum(v for k,v in counts(h).items()if 'warning'in k),'header_current_A_at_AWG28':1,'motor_nominal_phase_current_A':.67,'direct_factory_AWG26_crimp_qualified':False,'harness_wire_AWG28_insulation_OD_mm':[.4,.8],'mating_housing':'SHR-04V-S','mating_contact':'SSH-003T-P0.2-H','harness_qualified':False,'conditional_full_fitted_courtyard_mm2':699.6371634994422-54.593903+area,'packing_fitted_placed':len(boxes),'packing_unplaced':packing['unplaced'],'testpoints_packed':False,'complete_source_components':109,'nets':73,'sheets':7,'only_changed_electrical_component_pin_maps':sorted(changed),'retained_features_verified_by_source_net_contract':True,'native_errors_by_type':{k:v for k,v in counts(c).items()if 'error'in k},'native_warnings':sum(v for k,v in counts(c).items()if 'warning'in k),'routes':0,'vias':0,'qualified':False,'manufacturing_ready':False,'limits':'Header land dimensions match JST reference layout; this is not process, CAD-body, cable, crimp, retention, motor or thermal qualification. Complete controller diagnostic is deliberately rejected with14 fitted parts parked off-board;7 bare test pads have not been packed. CP-SAT UNKNOWN and bounded constructive failure are not impossibility proofs. INA241 imported pin4 NC metadata remains incorrect; USB locator/paste and radial bulk process remain unresolved.'}
print(json.dumps(result,indent=2))
