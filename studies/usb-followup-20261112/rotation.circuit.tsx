// Isolated native rotation and paste diagnostic. Not a controller placement.
// Retains the existing exact supplier USB definition without edits.
import { USB4145_03_0070_C } from '../../imports/USB4145_03_0070_C/USB4145_03_0070_C'
export default function UsbRotationStudy(){return <board width={45} height={40} thickness={1.6} layers={2} routingDisabled={true}>
<schematicsheet name="USB_ROTATION_STUDY">
{[0,90,180,270].map((angle,i)=><USB4145_03_0070_C key={angle} name={`J${i+1}`} layer="top" pcbX={i%2?10:-10} pcbY={i<2?9:-9} pcbRotation={angle} schX={i%2?5:-5} schY={i<2?4:-4} noConnect={["pin1","pin2","pin3","pin4","pin5","pin6","pin7","pin8","pin9","pin10","pin11","pin12","pin13","pin14","pin15","pin16","pin17"]} />)}
</schematicsheet>
</board>}
