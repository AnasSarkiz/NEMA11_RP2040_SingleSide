import { readFile, writeFile } from 'node:fs/promises'
import { convertRawEasyToTsx } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/lib/websafe/convert-to-typescript-component'
import { runTscircuitCode } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/node_modules/tscircuit'
import { convertCircuitJsonToPcbSvg, convertCircuitJsonToSchematicSvg } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/node_modules/circuit-to-svg'
import { wrapTsxWithBoardFor3dSnapshot } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/tests/fixtures/wrap-tsx-with-board-for-3d-snapshot'
const mode=process.argv[2]
if(!['before','after'].includes(mode))throw Error('Expected before or after')
const root='/workspace/scratch/07b71d1575ce/tmp/ina241-upstream-evidence'
const raw=JSON.parse(await readFile('/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/tests/assets/C5240853.raweasy.json','utf8'))
// Deterministic public component repro: no source, model, or datasheet requests leave this process.
globalThis.fetch=Object.assign(async()=>new Response(null,{status:404}),{preconnect:fetch.preconnect})
const source=await convertRawEasyToTsx({rawEasy:raw})
await writeFile(`${root}/${mode}.tsx`,source)
const wrapped=wrapTsxWithBoardFor3dSnapshot(source).replace('<board >','<board routingDisabled={true} schAutoLayoutEnabled={false}>')
const json=await runTscircuitCode(wrapped)
await writeFile(`${root}/${mode}.circuit.json`,JSON.stringify(json,null,2)+'\n')
await writeFile(`${root}/${mode}.schematic.svg`,convertCircuitJsonToSchematicSvg(json))
await writeFile(`${root}/${mode}.pcb.svg`,convertCircuitJsonToPcbSvg(json))
console.log(JSON.stringify({mode,port4:json.find(x=>x.type==='source_port'&&x.pin_number===4),records:json.length}))
