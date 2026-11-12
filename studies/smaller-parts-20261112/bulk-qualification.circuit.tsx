// Isolated through-hole capacitor diagnostic; not a controller placement.
// Exact supplier import retained. No motor clearance or process qualification.
import { RYHG35V47UF5_8 } from './bulk-import-staging/imports/RYHG35V47UF5_8/RYHG35V47UF5_8'
export default function BulkQualificationFixture(){return <board width={28} height={28} thickness={1.6} layers={2} routingDisabled={true}>
<RYHG35V47UF5_8 name="C_BULK_CANDIDATE" pcbX={0} pcbY={0} layer="top" connections={{pin1:'net.PD_VBUS',pin2:'net.GND'}} />
</board>}
