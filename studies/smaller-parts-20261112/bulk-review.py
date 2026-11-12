"""Recompute the unqualified radial-bulk area screen from untouched supplier/native data."""
from pathlib import Path
import collections,hashlib,json,math,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
STUDY=Path(__file__).resolve().parent
old=json.loads(subprocess.check_output(['python',str(STUDY/'review.py')],cwd=ROOT,text=True))
p=STUDY/'bulk-import-staging/imports/RYHG35V47UF5_8/RYHG35V47UF5_8.tsx'
q=json.loads(re.search(r'<courtyardoutline outline=\{(\[[\s\S]*?\])\}',p.read_text())[1])
def area(q):return abs(sum(a['x']*b['y']-b['x']*a['y']for a,b in zip(q,q[1:]+q[:1])))/2
f=ROOT/'dist/studies/smaller-parts-20261112/bulk-qualification/circuit.json'
a=json.loads(f.read_text());types=collections.Counter(x['type']for x in a)
native=next(x for x in a if x['type']=='pcb_courtyard_outline')
caps=[x for x in a if x['type']=='source_component']
assert math.isclose(area(q),area(native['outline']),abs_tol=1e-8)
assert len(caps)==1 and caps[0]['manufacturer_part_number']=='RYHG35V47UF5*8' and math.isclose(caps[0]['capacitance'],47e-6)
holes=[x for x in a if x['type']=='pcb_plated_hole']
assert len(holes)==2 and all(set(x['layers'])=={'top','bottom'} for x in holes)
base=json.loads((ROOT/'checks/courtyard-area-screen.json').read_text())
new_total=old['hypothetical_replacement_courtyard_mm2']-base['per_component_mm2']['C_BULK']+area(q)
result={'part':'C48970434','manufacturer_part_number':'RYHG35V47UF5*8','source_courtyard_mm2':area(q),'native_courtyard_mm2':area(native['outline']),'previous_bulk_courtyard_mm2':base['per_component_mm2']['C_BULK'],'hypothetical_full_courtyard_mm2':new_total,'provisional_available_mm2':old['provisional_available_mm2'],'conditional_area_margin_mm2':old['provisional_available_mm2']-new_total,'conditional_area_screen_pass':new_total<=old['provisional_available_mm2'],'native_counts':dict(types),'through_holes':holes,'routing_attempted':False,'qualified':False,'full_board_placement_pass':False,'manufacturing_ready':False,'native_body_model_verified':False,'active_controller_unchanged':old['active_controller_unchanged'],'native_build_exit':0,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'limits':'Area arithmetic only. Requires GH harness acceptance and qualification, supported INA241 correction/fresh import, capacitor manufacturer/process/electrical validation, bottom lead/solder and motor clearance, USB footprint validation and actual placement/routing. Native capacitor bounds describe the lands, not a verified 5x8mm body.'}
print(json.dumps(result,indent=2))
