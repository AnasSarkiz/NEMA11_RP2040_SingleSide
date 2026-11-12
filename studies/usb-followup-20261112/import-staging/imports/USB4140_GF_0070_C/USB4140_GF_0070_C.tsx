import objPath from "./USB4140_GF_0070_C.obj"
import stepPath from "./USB4140_GF_0070_C.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["CC2","B5"],
  pin2: ["CC1","A5"],
  pin3: ["VBUS1","A9"],
  pin4: ["VBUS2","B9"],
  pin5: ["GND1","A12"],
  pin6: ["GND2","B12"],
  pin7: ["pin7"]
} as const

export const USB4140_GF_0070_C = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C7374561"
  ]
}}
      manufacturerPartNumber="USB4140-GF-0070-C"
      footprint={<footprint>
        <hole pcbX="3.875024mm" pcbY="-1.7874996mm" diameter="0.8499856mm" />
<hole pcbX="-3.875024mm" pcbY="-1.7874996mm" diameter="0.649986mm" />
<platedhole  portHints={["pin7"]} pcbX="-4.320032mm" pcbY="0.0125984mm" holeWidth="0.5999988mm" holeHeight="0.999998mm" outerWidth="1.0999978mm" outerHeight="1.499997mm" shape="pill" />
<platedhole  portHints={["pin7"]} pcbX="4.320032mm" pcbY="0.0125984mm" holeWidth="0.5999988mm" holeHeight="0.999998mm" outerWidth="1.0999978mm" outerHeight="1.499997mm" shape="pill" />
<platedhole  portHints={["pin7"]} pcbX="-2.29997mm" pcbY="-1.4174216mm" holeWidth="0.5999988mm" holeHeight="1.0999978mm" outerWidth="1.0999978mm" outerHeight="1.5999968mm" pcbRotation="90deg" shape="pill" />
<platedhole  portHints={["pin7"]} pcbX="2.29997mm" pcbY="-1.4174216mm" holeWidth="0.5999988mm" holeHeight="1.0999978mm" outerWidth="1.0999978mm" outerHeight="1.5999968mm" pcbRotation="90deg" shape="pill" />
<smtpad portHints={["pin1"]} pcbX="0.499872mm" pcbY="1.2124944mm" width="0.7599934mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.500126mm" pcbY="1.2124944mm" width="0.7599934mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="1.519936mm" pcbY="1.2124944mm" width="0.7599934mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-1.519936mm" pcbY="1.2124944mm" width="0.7599934mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="2.750058mm" pcbY="1.2124944mm" width="0.7999984mm" height="1.999996mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-2.750058mm" pcbY="1.2124944mm" width="0.7999984mm" height="1.999996mm" shape="rect" />
<silkscreenpath route={[{"x":4.449927600000024,"y":1.7976088000000345},{"x":3.3810448000000406,"y":1.7976088000000345}]} />
<silkscreenpath route={[{"x":4.449927600000024,"y":0.9827768000000106},{"x":4.449927600000024,"y":1.7976088000000345}]} />
<silkscreenpath route={[{"x":4.449927600000024,"y":-1.5653003999999555},{"x":4.449927600000024,"y":-0.9575799999998935}]} />
<silkscreenpath route={[{"x":-4.450054600000044,"y":-0.9575799999998935},{"x":-4.450054600000044,"y":-2.5024080000000595},{"x":4.449927600000024,"y":-2.5024080000000595},{"x":4.449927600000024,"y":-2.009470199999896}]} />
<silkscreenpath route={[{"x":-3.381222600000001,"y":1.7976088000000345},{"x":-4.450054600000044,"y":1.7976088000000345},{"x":-4.450054600000044,"y":0.9827768000000106}]} />
<silkscreentext text="{NAME}" pcbX="-0.010668mm" pcbY="3.2223984mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-5.120030900000074,"y":2.4624924000000874},{"x":5.120030900000074,"y":2.4624924000000874},{"x":5.120030900000074,"y":-2.6024463999999625},{"x":-5.120030900000074,"y":-2.6024463999999625},{"x":-5.120030900000074,"y":2.4624924000000874}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 3.087462199999872, z: -3.0650116 },
      }}
      {...props}
    />
  )
}