"""Build the draft from physical pin contracts and byte-preserved supplier imports."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
plan=read('config/component-plan.json')['components']
c=read('config/connections.json')['components']
layout=read('config/schematic-layout.json')
poses=read('config/placement.json')['placements']
pop=read('config/population.json')
old=read('references/prior-studies/import-manifest.json')['imports']
parts={x['part']:x for x in old}
if (ROOT/'checks/import-manifest.json').exists():
 parts.update({x['part']:x for x in read('checks/import-manifest.json')['imports']})
# Fresh native outputs take precedence; no source transformations are allowed.
for p in (ROOT/'import-staging').rglob('*.tsx'):
 text=p.read_text();m=re.search(r'export const (\w+)',text);ids=re.findall(r'"(C\d+)"',text)
 if m and ids:
  part=ids[0];folder=ROOT/'imports'/p.parent.name
  if folder.exists():
   files=[{'path':str(x.relative_to(ROOT)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'bytes':x.stat().st_size} for x in sorted(folder.iterdir()) if x.is_file()]
   parts[part]={'part':part,'exported_symbol':m[1],'files':files,'origin':'supported native CLI 0.1.2454 exact-footprint download; untouched'}
missing=set(plan.values())-parts.keys()
if missing:raise SystemExit('Missing native imports: '+', '.join(sorted(missing)))
selected={k:parts[k] for k in sorted(set(plan.values()))}
for part in selected.values():
 for f in part['files']:
  if hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()!=f['sha256']:raise SystemExit('Changed import: '+f['path'])
lines=['// NEMA11 single-side DRAFT. Placement is a projection seed and FAILS acceptance.', '// Routing remains disabled. All fitted parts top; optional AS5600 bottom/DNP.', '// USB and telemetry use explicit physical pin numbers; no supplier overrides.', 'import poses from "./config/placement.json"']
for part in selected.values():
 path=next(f['path'] for f in part['files'] if f['path'].endswith('.tsx'))[:-4]
 lines.append(f'import {{ {part["exported_symbol"]} }} from "./{path}"')
lines+=['const position=(name: keyof typeof poses.placements)=>({...poses.placements[name],layer:poses.placements[name].layer as "top"|"bottom"})','export default function Nema11SingleSideDraft(){return (','<board width={28} height={28} thickness={1.6} layers={2} routingDisabled={true} schAutoLayoutEnabled={false} schLayout={{layoutMode:"relative"}} schTraceAutoLabelEnabled={true} schMaxTraceDistance={4} minTraceWidth={0.16} minTraceToPadEdgeClearance={0.15} minPadEdgeToPadEdgeClearance={0.15} minBoardEdgeClearance={0.25} minViaHoleDiameter={0.30} minViaPadDiameter={0.45} minViaHoleEdgeToViaHoleEdgeClearance={0.20} minPlatedHoleDrillEdgeToDrillEdgeClearance={0.45}>']
for n in sorted({n for v in c.values() for n in v['connections'].values()}):
 attr=' isGroundNet={true}' if n=='GND' else ' isPowerNet={true}' if n in ['V3V3','V1V1','PD_VBUS','DATA_VBUS','LOGIC_IN','PD_VHV'] else ''
 width=.30 if n in ['PD_VBUS','A_DRV_PLUS','A_PLUS','A_MINUS','B_DRV_PLUS','B_PLUS','B_MINUS','SENSE1','SENSE2'] else .16
 lines.append(f'<net name="{n}"{attr} nominalTraceWidth={{{width}}} />')
for i,(x,y) in enumerate([(-11.5,-11.5),(-11.5,11.5),(11.5,-11.5),(11.5,11.5)]):
 lines.append(f'<hole name="M{i+1}" pcbX={{{x}}} pcbY={{{y}}} diameter={{2.7}} />')
 lines.append(f'<keepout pcbX={{{x}}} pcbY={{{y}}} shape="circle" radius={{2.35}} layers={{["top","bottom"]}} allowPlacements={{false}} />')
for i,(title,names) in enumerate(layout['sheets'].items()):
 lines.append(f'<schematicsheet name="{title.replace("&","&amp;")}" sheetIndex={{{i}}} sheetSize="A4">')
 for name in names:
  v=c[name];s=layout['placements'][name]
  attrs=[f'name="{name}"',f'{{...position("{name}")}}',f'schX={{{s["schX"]}}}',f'schY={{{s["schY"]}}}']
  if 'schRotation'in s:attrs.append(f'schRotation={{{s["schRotation"]}}}')
  if name in pop['DNP']+pop['bare_pads']:attrs.append('doNotPlace={true}')
  if v['no_connect']:attrs.append('noConnect={'+json.dumps(['pin'+n for n in v['no_connect']])+'}')
  attrs.append('connections={'+json.dumps({'pin'+p:'net.'+n for p,n in v['connections'].items()})+'}')
  if name.startswith('TP_'):tag='testpoint';attrs+=['footprintVariant="pad"','padDiameter="1.1mm"']
  else:tag=selected[plan[name]]['exported_symbol']
  lines.append('<'+tag+' '+' '.join(attrs)+' />')
 lines.append('</schematicsheet>')
lines+=['</board>',')}','']
output='\n'.join(lines)
if '--check'in sys.argv:
 if (ROOT/'index.circuit.tsx').read_text()!=output:raise SystemExit('Generated source stale')
 print('Generated source reproduces exactly')
else:
 (ROOT/'index.circuit.tsx').write_text(output)
 (ROOT/'checks/import-manifest.json').write_text(json.dumps({'imports':list(selected.values())},indent=2)+'\n')
 print('Generated',len(c),'components; no fit acceptance')
