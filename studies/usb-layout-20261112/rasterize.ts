// Render retained native SVGs for review; no geometry or image edits.
// Use the installed @resvg/resvg-js dependency from the upstream repro checkout.
import { Resvg } from '/workspace/scratch/07b71d1575ce/easyeda-ina241-20261112/node_modules/@resvg/resvg-js'
for(const name of ['harness','controller']){
 const root=`dist/studies/usb-layout-20261112/${name}`
 const svg=await Bun.file(`${root}/pcb.svg`).text()
 await Bun.write(`${root}/pcb.png`,new Resvg(svg,{fitTo:{mode:'width',value:1600}}).render().asPng())
}
