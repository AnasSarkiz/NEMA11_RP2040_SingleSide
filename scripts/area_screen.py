"""Audit source courtyard polygons; this does not establish body packing or routing."""
import hashlib,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def calculate():
 plan=json.loads((ROOT/'config/component-plan.json').read_text())['components'];pop=json.loads((ROOT/'config/population.json').read_text());req=json.loads((ROOT/'config/requirements.json').read_text());manifest=json.loads((ROOT/'checks/import-manifest.json').read_text())['imports'];areas={}
 for part in manifest:
  entry=next(f for f in part['files']if f['path'].endswith('.tsx'));data=(ROOT/entry['path']).read_bytes()
  if hashlib.sha256(data).hexdigest()!=entry['sha256']:raise ValueError('Import hash changed')
  match=re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',data.decode())
  if not match:raise ValueError('Missing courtyard: '+part['part'])
  points=json.loads(match[1])
  if len(points)<3 or any(not math.isfinite(p[a]) for p in points for a in ['x','y']):raise ValueError('Invalid polygon')
  areas[part['part']]=abs(sum(p['x']*q['y']-q['x']*p['y']for p,q in zip(points,points[1:]+points[:1])))/2
 fitted={n:areas[p]for n,p in plan.items()if n not in pop['DNP']}
 raw=math.prod(req['PCB_outline_mm']);available=raw-4*math.pi*req['provisional_head_exclusion_radius_mm']**2;total=sum(fitted.values())
 return {'metric':'whole, nonoverlapping supplier courtyards outside provisional circular screw exclusions','source_files_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['config/component-plan.json','config/population.json','config/requirements.json','checks/import-manifest.json']},'fitted_count':len(fitted),'courtyard_sum_mm2':total,'raw_board_mm2':raw,'provisional_available_mm2':available,'excess_mm2':total-available,'excess_even_without_screw_exclusions_mm2':total-raw,'passes_conditional_area_screen':total<=available,'per_component_mm2':fitted,'limits':'Not body-packing impossibility, approved courtyard overlap/overhang, actual screw tolerances, routing, height, cable/tool envelope or assembly approval. USB locator/paste and WAGO AWG26 compatibility still fail qualification.'}
if __name__=='__main__':
 result=calculate();print(json.dumps(result,indent=2))
