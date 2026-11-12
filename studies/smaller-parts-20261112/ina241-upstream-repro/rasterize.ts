import { Resvg } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/node_modules/@resvg/resvg-js'
const root='/workspace/scratch/07b71d1575ce/tmp/ina241-upstream-evidence'
for(const name of ['before','after']){
 const svg=await Bun.file(`${root}/${name}.schematic.svg`).text()
 const png=new Resvg(svg).render().asPng()
 await Bun.write(`${root}/${name}.schematic.png`,png)
}
