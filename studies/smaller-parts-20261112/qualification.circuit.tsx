// Isolated component diagnostic; not the complete controller or a placement candidate.
// Supplier definitions are untouched. Pin 4 on INA241 is grounded per TI Rev D;
// its imported doNotConnect metadata is intentionally retained to expose the conflict.
import { BM04B_GHS_TBT_LF__SN_ } from './import-staging/imports/BM04B_GHS_TBT_LF__SN_/BM04B_GHS_TBT_LF__SN_'
import { INA241A2IDDFR } from './import-staging/imports/INA241A2IDDFR/INA241A2IDDFR'
export default function QualificationFixture(){return <board width={28} height={28} thickness={1.6} layers={2} routingDisabled={true} minPadEdgeToPadEdgeClearance={0.15} minBoardEdgeClearance={0.25}>
<net name="GND" isGroundNet />
<net name="V3V3" isPowerNet />
<BM04B_GHS_TBT_LF__SN_ name="J_MOTOR" pcbX={0} pcbY={-8} layer="top" noConnect={['pin5','pin6']} connections={{pin1:'net.A_PLUS',pin2:'net.A_MINUS',pin3:'net.B_PLUS',pin4:'net.B_MINUS'}} />
<INA241A2IDDFR name="U_IA" pcbX={-5} pcbY={2} layer="top" connections={{pin1:'net.A_PLUS',pin2:'net.GND',pin3:'net.GND',pin4:'net.GND',pin5:'net.I_A_RAW',pin6:'net.V3V3',pin7:'net.V3V3',pin8:'net.A_DRV_PLUS'}} />
<INA241A2IDDFR name="U_IB" pcbX={5} pcbY={2} layer="top" connections={{pin1:'net.B_PLUS',pin2:'net.GND',pin3:'net.GND',pin4:'net.GND',pin5:'net.I_B_RAW',pin6:'net.V3V3',pin7:'net.V3V3',pin8:'net.B_DRV_PLUS'}} />
</board>}
