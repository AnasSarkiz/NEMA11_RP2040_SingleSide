import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["IN_NEG"],
  pin2: ["GND"],
  pin3: ["REF2"],
  pin4: ["NC"],
  pin5: ["OUT"],
  pin6: ["VS"],
  pin7: ["REF1"],
  pin8: ["IN_POS"]
} as const

const pinAttributes = {
  pin2: {requiresGround: true}
} as const

export const INA241A2IDDFR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C5240853"
  ]
}}
      manufacturerPartNumber="INA241A2IDDFR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.974979mm" pcbY="-1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.324993mm" pcbY="-1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="0.324993mm" pcbY="-1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="0.974979mm" pcbY="-1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.974979mm" pcbY="1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="0.324993mm" pcbY="1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-0.324993mm" pcbY="1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-0.974979mm" pcbY="1.259967mm" width="0.3999992mm" height="0.8999982mm" shape="rect" />
<silkscreenpath route={[{"x":1.450035200000002,"y":-0.7998968000000133},{"x":1.450035200000002,"y":0.8001000000000005}]} />
<silkscreenpath route={[{"x":-1.4499844000000195,"y":-0.7998968000000133},{"x":-1.3341350000000034,"y":-0.7998968000000133}]} />
<silkscreenpath route={[{"x":1.3341858000000002,"y":-0.7998968000000133},{"x":1.450035200000002,"y":-0.7998968000000133}]} />
<silkscreenpath route={[{"x":-1.4499844000000195,"y":0.8001000000000005},{"x":-1.3341350000000034,"y":0.8001000000000005}]} />
<silkscreenpath route={[{"x":1.3341858000000002,"y":0.8001000000000005},{"x":1.450035200000002,"y":0.8001000000000005}]} />
<silkscreenpath route={[{"x":-1.4499844000000195,"y":0.8001000000000005},{"x":-1.4499844000000195,"y":0.2541015999999843}]} />
<silkscreenpath route={[{"x":-1.4499844000000195,"y":-0.7998968000000133},{"x":-1.4499844000000195,"y":-0.2538983999999971}]} />
<silkscreenpath route={[{"x":-1.4499844000000195,"y":0.2541015999999843},{"x":-1.2716684622421042,"y":0.17838329744550663},{"x":-1.198234294967392,"y":-0.0008853782256608156},{"x":-1.272186762442999,"y":-0.179940865587767},{"x":-1.4507210000000157,"y":-0.2551430000000039}]} />
<silkscreencircle pcbX="-1.523873mm" pcbY="-1.270127mm" radius="0.100076mm" />
<silkscreentext text="{NAME}" pcbX="-0.079121mm" pcbY="2.705737mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-1.6999844000000195,"y":1.9599661000000026},{"x":1.7000097999999753,"y":1.9599661000000026},{"x":1.7000097999999753,"y":-1.9599661000000026},{"x":-1.6999844000000195,"y":-1.9599661000000026},{"x":-1.6999844000000195,"y":1.9599661000000026}]} />
      </footprint>}
      
      {...props}
    />
  )
}