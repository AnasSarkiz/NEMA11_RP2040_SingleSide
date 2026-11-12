// Supplier-identity/geometry diagnostic only. No full-board replacement.
import { USB4140_GF_0070_C } from './import-staging/imports/USB4140_GF_0070_C/USB4140_GF_0070_C'
import { USB4120_03_C } from './import-staging/imports/USB4120_03_C/USB4120_03_C'
export default function UsbAlternativesStudy(){return <board width={40} height={25} thickness={1.6} layers={2} routingDisabled={true}>
<schematicsheet name="USB_ALTERNATIVES">
<USB4140_GF_0070_C name="J1" pcbX={-9} pcbY={0} layer="top" schX={-5} noConnect={["pin1","pin2","pin3","pin4","pin5","pin6","pin7"]} />
<USB4120_03_C name="J2" pcbX={9} pcbY={0} layer="top" schX={5} noConnect={["pin1","pin2","pin3","pin4","pin5","pin6","pin7","pin8","pin9","pin10","pin11","pin12","pin13","pin14","pin15","pin16","pin17"]} />
</schematicsheet>
</board>}
