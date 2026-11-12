import objPath from "./BM04B_GHS_TBT_LF__SN_.obj"
import stepPath from "./BM04B_GHS_TBT_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"],
  pin6: ["pin6"]
} as const

export const BM04B_GHS_TBT_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C161692"
  ]
}}
      manufacturerPartNumber="BM04B-GHS-TBT(LF)(SN)"
      footprint={<footprint>
        <smtpad portHints={["pin5"]} pcbX="3.72491mm" pcbY="-1.40000355mm" width="0.999998mm" height="2.7999944mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-3.72491mm" pcbY="-1.40000355mm" width="0.999998mm" height="2.7999944mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-1.87452mm" pcbY="1.95000245mm" width="0.5999988mm" height="1.6999966mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.62484mm" pcbY="1.95000245mm" width="0.5999988mm" height="1.6999966mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.62484mm" pcbY="1.95000245mm" width="0.5999988mm" height="1.6999966mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="1.87452mm" pcbY="1.95000245mm" width="0.5999988mm" height="1.6999966mm" shape="rect" />
<silkscreenpath route={[{"x":-4.572000000000003,"y":2.0529994500000157},{"x":-2.4053800000000365,"y":2.0529994500000157}]} />
<silkscreenpath route={[{"x":-1.3436599999999999,"y":2.0529994500000157},{"x":-1.155700000000138,"y":2.0529994500000157}]} />
<silkscreenpath route={[{"x":-0.09397999999998774,"y":2.0529994500000157},{"x":0.09397999999998774,"y":2.0529994500000157}]} />
<silkscreenpath route={[{"x":1.1557000000000244,"y":2.0529994500000157},{"x":1.3436599999999999,"y":2.0529994500000157}]} />
<silkscreenpath route={[{"x":-4.572000000000003,"y":2.0529994500000157},{"x":-4.572000000000003,"y":-3.1540005499998642},{"x":4.572000000000003,"y":-3.1540005499998642},{"x":4.572000000000003,"y":2.0529994500000157}]} />
<silkscreenpath route={[{"x":4.572000000000003,"y":2.0529994500000157},{"x":2.4053800000000365,"y":2.0529994500000157}]} />
<silkscreencircle pcbX="2.9464mm" pcbY="2.49737245mm" radius="0.127mm" />
<silkscreentext text="{NAME}" pcbX="-0.00889mm" pcbY="3.79099645mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-4.474909000000025,"y":3.0500007500000947},{"x":4.474909000000025,"y":3.0500007500000947},{"x":4.474909000000025,"y":-3.050000749999981},{"x":-4.474909000000025,"y":-3.050000749999981},{"x":-4.474909000000025,"y":3.0500007500000947}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 1.8749999999998863, y: -0.5384998500001347, z: -0.01 },
      }}
      {...props}
    />
  )
}