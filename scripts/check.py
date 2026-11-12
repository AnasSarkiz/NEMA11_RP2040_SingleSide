"""Independent source contract checks, with separate acceptance failures."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
c=load('config/connections.json')['components'];plan=load('config/component-plan.json')['components'];poses=load('config/placement.json')['placements'];pop=load('config/population.json');layout=load('config/schematic-layout.json');req=load('config/requirements.json')
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
check(set(c)==set(poses),'placement coverage')
names=[n for ns in layout['sheets'].values() for n in ns]
check(len(names)==len(set(names)) and set(names)==set(c),'seven-sheet component coverage')
check(len(layout['sheets'])==7,'seven sheets')
check(len(c)==109 and len(plan)==102,'complete component set')
check(set(c)-set(plan)==set(pop['bare_pads']),'supplier/bare-pad coverage')
check(all(p['layer']=='top' for n,p in poses.items() if n!='U_ENCODER'),'top-only fitted source')
check(pop['DNP']==['U_ENCODER'],'only optional IC is DNP')
check(set(pop['capacitors_fitted_top'])=={'C_ENCODER','C_ENCODER_BULK'},'encoder caps fitted')
for n,v in c.items():check(not(set(v['connections'])&set(v['no_connect'])),'connected/NC overlap: '+n)
check(c['U_MCU']['connections']['6']=='TEMP_SDA' and c['U_MCU']['connections']['7']=='TEMP_SCL','I2C0 pins')
check(c['U_MCU']['connections']['38']=='I_A_ADC' and c['U_MCU']['connections']['39']=='I_B_ADC','ADC0/1 pins')
for phase,pin in [('A','24'),('B','26')]:
 check(c['U_DRV']['connections'][pin]==phase+'_DRV_PLUS','inline load topology')
 check(c['R_SHUNT_'+phase]['connections']=={'1':phase+'_DRV_PLUS','2':phase+'_PLUS'},'separate inline shunt')
 check(c['R_SHUNT_'+phase]['resistance']==.05,'50mOhm shunt')
 check(c['U_I'+phase]['connections']=={'2':phase+'_DRV_PLUS','3':phase+'_PLUS','4':'GND','5':'V3V3','6':'GND','7':'V3V3','8':'I_'+phase+'_RAW'},'TI PW pin map')
 check(c['R_I'+phase]['resistance']==100 and c['C_IADC_'+phase]['capacitance']==1e-8,'ADC filter')
check(c['R_SA']['connections']=={'1':'SENSE1','2':'GND'} and c['R_SB']['connections']=={'1':'SENSE2','2':'GND'},'A4988 regulation retained')
for name,prefix in [('J_PD','PD'),('J_DATA','DATA')]:
 v=c[name];check(set(v['connections'])|set(v['no_connect'])=={str(i)for i in range(1,18)},'USB all17 physical pins')
 check(all(v['connections'][str(i)]==prefix+'_VBUS'for i in [3,8,11,16]),'upright USB VBUS mapping')
 check(all(v['connections'][str(i)]=='GND'for i in [1,5,9,13,17]),'upright USB GND/shell mapping')
 check(v['connections']['4']==prefix+'_CC1' and v['connections']['15']==prefix+'_CC2','upright USB CC mapping')
check(all(c['J_DATA']['connections'][str(i)]=='USB_DP'for i in [2,14]),'USB DP mapping')
check(all(c['J_DATA']['connections'][str(i)]=='USB_DM'for i in [6,10]),'USB DM mapping')
check(poses['J_PD']['pcbY']>0>poses['J_DATA']['pcbY'],'opposite USB edges')
check(req['PCB_outline_mm']==[28,28] and req['PCB_layers']==['top','bottom'],'two-layer NEMA11 outline')
check(req['motor']=='11HS12-0674S' and req['motor_phase_current_A']==.67,'actual NEMA11 motor')
check(not req['routing_enabled'] and not req['manufacturing_release'],'acceptance stays closed')
if (ROOT/'checks/import-manifest.json').exists():
 for part in load('checks/import-manifest.json')['imports']:
  for f in part['files']:check(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'],'changed import: '+f['path'])
for f in load('references/nema14/provenance.json'):check(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'],'changed reference')
print(json.dumps({'source_contract_pass':not errors,'components':len(c),'fitted_supplier_components':len(plan)-1,'bare_pads':len(pop['bare_pads']),'nets':len({n for v in c.values() for n in v['connections'].values()}),'failures':errors,'placement_verified':False,'manufacturing_ready':False},indent=2))
if errors:raise SystemExit(1)
if '--require-qualified'in sys.argv:raise SystemExit('Acceptance BLOCKED: upright USB locator/paste/seating, WAGO/AWG26, packing/clearance, rear hardware, routing/CAM, stock/process and bench checks remain open')
