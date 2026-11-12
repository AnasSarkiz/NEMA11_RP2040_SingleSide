// Isolated, unqualified harness-header diagnostic; not a motor controller.
// Exact supplier source and models are retained without overrides.
import { BM04B_SRSS_TB_LF__SN_ } from './import-staging/imports/BM04B_SRSS_TB_LF__SN_/BM04B_SRSS_TB_LF__SN_'
export default function HarnessHeaderStudy(){return <board width={28} height={28} thickness={1.6} layers={2} routingDisabled={true}>
<BM04B_SRSS_TB_LF__SN_ name="J_MOTOR" pcbX={0} pcbY={0} layer="top" noConnect={['pin5']} connections={{pin1:'net.A_PLUS',pin2:'net.A_MINUS',pin3:'net.B_PLUS',pin4:'net.B_MINUS'}} />
</board>}
