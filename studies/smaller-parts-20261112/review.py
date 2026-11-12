"""Reproduce the exact-import area comparison and semantic qualification blocker.
No board source, native JSON, supplier definition or registry file is modified.
"""
import collections,hashlib,json,math,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STUDY=Path(__file__).resolve().parent
BASE='ebebbf2ef418557dfec44e8c2327d81e569e1b3e'
def area(p):
 if len(p)<3 or any(not math.isfinite(q[k])for q in p for k in ['x','y']):raise ValueError('Invalid polygon')
 return abs(sum(x['x']*y['y']-y['x']*x['y']for x,y in zip(p,p[1:]+p[:1])))/2
manifest=json.loads((STUDY/'inputs.json').read_text())
for entry in manifest['files']:
 if hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Changed input '+entry['path'])
old=json.loads((ROOT/'checks/courtyard-area-screen.json').read_text())
source={}
for file in (STUDY/'import-staging/imports').glob('*/*.tsx'):
 text=file.read_text();part=re.search(r'"(C\d+)"',text)[1];match=re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',text)
 if not match:raise ValueError('Missing supplier courtyard')
 source[part]={'area_mm2':area(json.loads(match[1])),'file':str(file.relative_to(ROOT)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'text':text}
native_file=ROOT/'dist/studies/smaller-parts-20261112/qualification/circuit.json';native=json.loads(native_file.read_text());types=collections.Counter(x['type']for x in native)
sc={x['source_component_id']:x for x in native if x['type']=='source_component'}
pc={x['pcb_component_id']:x for x in native if x['type']=='pcb_component'}
netnames={x['source_net_id']:x['name']for x in native if x['type']=='source_net'}
bindings=collections.defaultdict(set)
for x in native:
 if x['type']=='source_trace':
  for port in x.get('connected_source_port_ids',[]):bindings[port].update(netnames[n]for n in x.get('connected_source_net_ids',[]))
geometry=[]
for x in native:
 if x['type']=='pcb_courtyard_outline':
  comp=sc[pc[x['pcb_component_id']]['source_component_id']];part=comp['supplier_part_numbers']['jlcpcb'][0];a=area(x['outline'])
  geometry.append({'name':comp['name'],'part':part,'native_area_mm2':a,'source_area_mm2':source[part]['area_mm2'],'matches':math.isclose(a,source[part]['area_mm2'],abs_tol=1e-8)})
conflicts=[]
for port in native:
 if port['type']=='source_port'and sc[port['source_component_id']]['name']in ['U_IA','U_IB']and port.get('pin_number')==4:
  conflicts.append({'name':sc[port['source_component_id']]['name'],'pin':4,'native_do_not_connect':port.get('do_not_connect',False),'actual_nets':sorted(bindings[port['source_port_id']]),'manufacturer_requirement':'Ground reserved pin 4, TI SBOSA30D Table 5-1','qualified':False})
a=old['per_component_mm2'];replacement=old['courtyard_sum_mm2']-a['J_MOTOR']-a['U_IA']-a['U_IB']+source['C161692']['area_mm2']+2*source['C5240853']['area_mm2'];deficit=replacement-old['provisional_available_mm2']
unchanged=subprocess.check_output(['git','diff','--name-only',BASE,'--','index.circuit.tsx','config','imports','scripts','dist/index'],cwd=ROOT,text=True).strip()==''
result={'base_commit':BASE,'active_controller_unchanged':unchanged,'source_and_native_courtyards_match':all(x['matches']for x in geometry),'geometry':geometry,'baseline_fitted_courtyard_mm2':old['courtyard_sum_mm2'],'hypothetical_replacement_courtyard_mm2':replacement,'provisional_available_mm2':old['provisional_available_mm2'],'saving_mm2':old['courtyard_sum_mm2']-replacement,'residual_deficit_mm2':deficit,'conditional_area_screen_pass':deficit<=0,'maximum_bulk_courtyard_mm2_if_only_further_replacement':a['C_BULK']-deficit,'parts_removed_from_active_controller':[],'manufacturer_metadata_conflicts':conflicts,'diagnostic_fixture_counts':dict(types),'diagnostic_json_sha256':hashlib.sha256(native_file.read_bytes()).hexdigest(),'expected_gain_v_per_a':20*.05,'nominal_zero_v':3.3/2,'nominal_output_at_motor_rating_v':[3.3/2-.67,3.3/2+.67],'two_channel_iq_max_mA_at_full_temperature':6.4,'jst_gh_wire_insulation_diameter_mm':[.76,1.0],'factory_wire_insulation_diameter_verified':False,'spring_clamp_requirement_change_accepted':False,'native_build_exit':0,'native_pin_check_exit':0,'native_pin_findings':{'errors':0,'warnings':4},'candidate_qualified':False,'full_board_placement_pass':False,'routing_attempted':False,'manufacturing_ready':False,'limits':'Isolated three-part fixture, not a controller. Source/net geometry is not copper connectivity or hardware validation. Body size is not courtyard area. Imported pin4 metadata contradicts manufacturer. GH mechanical pads5/6 are NC; direct motor wire crimp and mating/strain relief remain unqualified.'}
print(json.dumps(result,indent=2))
if not unchanged or not all(x['matches']for x in geometry)or len(conflicts)!=2 or not all(x['native_do_not_connect']and x['actual_nets']==['GND']for x in conflicts):raise SystemExit('Unexpected study input or diagnostic result')
