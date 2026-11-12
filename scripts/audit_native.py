"""Inspect untouched native output against the independent physical-pin contract."""
import collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'dist/index/circuit.json';data=p.read_bytes();d=json.loads(data);types=collections.Counter(x['type']for x in d)
source={x['source_component_id']:x['name']for x in d if x['type']=='source_component'}
nets={x['source_net_id']:x['name']for x in d if x['type']=='source_net'}
ports={x['source_port_id']:x for x in d if x['type']=='source_port'}
bindings=collections.defaultdict(set)
for x in d:
 if x['type']=='source_trace':
  for port in x.get('connected_source_port_ids',[]):
   for net in x.get('connected_source_net_ids',[]):bindings[port].add(nets[net])
# Native duplicate shell terminals inherit their explicit internal common node.
for component in d:
 if component['type']=='source_component':
  for group in component.get('internally_connected_source_port_ids',[]):
   shared=set().union(*(bindings[p]for p in group))
   for portid in group:bindings[portid].update(shared)
def pin_number(port):
 if 'pin_number'in port:return str(port['pin_number'])
 hints=[m[1]for h in port.get('port_hints',[])if (m:=re.fullmatch(r'pin(\d+)',h))]
 if len(set(hints))==1:return hints[0]
 raise ValueError('Unresolved physical pin: '+str(port))
contract=json.loads((ROOT/'config/connections.json').read_text())['components'];failures=[];checked=0
for portid,port in ports.items():
 name=source[port['source_component_id']];pin=pin_number(port);expected=contract[name]['connections'].get(pin)
 if expected:
  checked+=1
  if bindings[portid]!={expected}:failures.append({'component':name,'pin':pin,'expected':expected,'actual':sorted(bindings[portid])})
 elif pin not in contract[name]['no_connect']:failures.append({'component':name,'pin':pin,'error':'unaccounted physical pin'})
 elif bindings[portid]:failures.append({'component':name,'pin':pin,'error':'NC connected'})
found={(source[p['source_component_id']],pin_number(p))for p in ports.values()}
for name,v in contract.items():
 for pin in set(v['connections'])|set(v['no_connect']):
  if (name,pin)not in found:failures.append({'component':name,'pin':pin,'error':'missing emitted pin'})
pcbs={x['pcb_component_id']:x for x in d if x['type']=='pcb_component'}
fitted=[x for x in pcbs.values()if not x.get('do_not_place',False)]
if len(fitted)!=101 or any(x['layer']!='top'for x in fitted):failures.append({'error':'fitted population/side mismatch'})
errors={k:v for k,v in types.items()if k.endswith('_error')};warnings={k:v for k,v in types.items()if k.endswith('_warning')}
usb={}
for cid,x in pcbs.items():
 name=source[x['source_component_id']]
 if name in ['J_PD','J_DATA']:
  paste=[v for v in d if v['type']=='pcb_solder_paste'and v.get('pcb_component_id')==cid]
  usb[name]={'component_layer':x['layer'],'paste_by_layer':dict(collections.Counter(v['layer']for v in paste)),'source_physical_ports':sum(p['source_component_id']==x['source_component_id']for p in ports.values())}
result={'circuit_json_sha256':hashlib.sha256(data).hexdigest(),'pin_contract_pass':not failures,'connected_physical_ports_checked':checked,'physical_source_ports':len(ports),'source_components':len(source),'source_nets':len(nets),'fitted_components':len(fitted),'fitted_sides':dict(collections.Counter(x['layer']for x in fitted)),'schematic_sheets':types['schematic_sheet'],'pcb_trace_records':types['pcb_trace'],'pcb_via_records':types['pcb_via'],'native_errors':errors,'native_error_count':sum(errors.values()),'native_warnings':warnings,'native_warning_count':sum(warnings.values()),'usb':usb,'failures':failures,'native_build_exit':1,'placement_accepted':False,'manufacturing_ready':False,'scope':'Pin-binding/population check only. Native errors remain failures, source draft not physically qualified.'}
print(json.dumps(result,indent=2))
if failures:raise SystemExit(1)
