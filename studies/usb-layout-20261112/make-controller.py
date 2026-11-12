"""Make a complete, explicitly rejected placement diagnostic from source config.
Only component selections, physical pin connections, and study poses change.
Supplier definitions and native circuit JSON are never edited.
"""
import json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
packing=json.loads((OUT/'greedy.json').read_text());rects=json.loads((OUT/'packing.json').read_text())['rectangles'];old=json.loads((ROOT/'config/placement.json').read_text())['placements'];poses={n:dict(p)for n,p in old.items()}
for n,(x,y,xx,yy,rr)in packing['packing_um'].items():
 a,b,c,d=rects[n]['bounds'];points=[(u,v)if rr==0 else(-v,u)for u,v in [(a,b),(a,d),(c,b),(c,d)]]
 poses[n]={'pcbX':round(x/1000-min(p[0]for p in points),6),'pcbY':round(y/1000-min(p[1]for p in points),6),'pcbRotation':90*rr,'layer':'top'}
# Failed parts are visibly parked beyond the right edge, never silently dropped.
for i,n in enumerate(packing['unplaced']):poses[n]={'pcbX':18+(i%3)*3,'pcbY':-11+(i//3)*4,'pcbRotation':0,'layer':'top'}
(OUT/'rejected-placement.json').write_text(json.dumps({'status':'REJECTED_PARTIAL','unplaced':packing['unplaced'],'testpoints_not_packed':True,'placements':poses},indent=2)+'\n')
s=(ROOT/'index.circuit.tsx').read_text();s=s.replace('./config/placement.json','./rejected-placement.json');s=re.sub(r'from "\./imports/', 'from "../../imports/',s)
subs=[('A_250_204','BM04B_SRSS_TB_LF__SN_','./import-staging/imports/BM04B_SRSS_TB_LF__SN_/BM04B_SRSS_TB_LF__SN_'),('INA240A1PWR','INA241A2IDDFR','../smaller-parts-20261112/import-staging/imports/INA241A2IDDFR/INA241A2IDDFR'),('RVT1V470M0605','RYHG35V47UF5_8','../smaller-parts-20261112/bulk-import-staging/imports/RYHG35V47UF5_8/RYHG35V47UF5_8')]
for oldtag,newtag,path in subs:
 s,count=re.subn(r'import \{ '+oldtag+r' \} from "[^"]+"',f'import {{ {newtag} }} from "{path}"',s);assert count==1
 s=s.replace('<'+oldtag+' ','<'+newtag+' ')
for name,phase in [('U_IA','A'),('U_IB','B')]:
 line=next(l for l in s.splitlines()if f'name="{name}"'in l)
 mapped={'pin1':f'net.{phase}_PLUS','pin2':'net.GND','pin3':'net.GND','pin4':'net.GND','pin5':f'net.I_{phase}_RAW','pin6':'net.V3V3','pin7':'net.V3V3','pin8':f'net.{phase}_DRV_PLUS'}
 replacement=re.sub(r' noConnect=\{\[[^\]]*\]\}', '',line);replacement=re.sub(r'connections=\{\{.*?\}\}', 'connections={'+json.dumps(mapped)+'}',replacement);s=s.replace(line,replacement)
line=next(l for l in s.splitlines()if 'name="J_MOTOR"'in l);s=s.replace(line,line.replace(' connections=', ' noConnect={["pin5"]} connections='))
s=s.replace('Nema11SingleSideDraft','Nema11RejectedCompactStudy');s='// REJECTED study: 14 fitted parts parked outside board; test pads not packed.\n// Unqualified SH/INA241/radial bulk/USB. All functions retained; NO routing.\n'+s
(OUT/'controller.circuit.tsx').write_text(s)
print('Retained',len(poses),'source component poses, including',len(packing['unplaced']),'explicitly unplaced fitted parts')
