import type { CapacitorProps } from "@tscircuit/props"

export const RYHG35V47UF5_8 = (props: Omit<CapacitorProps, "capacitance">) => {
  const { name = "C1", ...restProps } = props

  return (
    <capacitor
      name={name}
      capacitance="47uF"
      polarized
      supplierPartNumbers={{
  "jlcpcb": [
    "C48970434"
  ]
}}
      manufacturerPartNumber="RYHG35V47UF5*8"
      footprint={<footprint>
        <platedhole  portHints={["pin2"]} pcbX="0.999998mm" pcbY="0mm" outerDiameter="1.0999978mm" holeDiameter="0.700024mm" shape="circle" />
<platedhole  portHints={["pin1"]} pcbX="-0.999998mm" pcbY="0mm" outerDiameter="1.0999978mm" holeDiameter="0.700024mm" shape="circle" />
<silkscreencircle pcbX="0mm" pcbY="0mm" radius="2.500122mm" />
<silkscreentext text="+" pcbX="-0.889mm" pcbY="0.889mm" anchorAlignment="bottom_left" fontSize="1.500124mm" />
<silkscreentext text="{NAME}" pcbX="0.0127mm" pcbY="3.4892mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.7391999999999825,"y":2.7392000000000962},{"x":2.764599999999973,"y":2.7392000000000962},{"x":2.764599999999973,"y":-2.7645999999998594},{"x":-2.7391999999999825,"y":-2.7645999999998594},{"x":-2.7391999999999825,"y":2.7392000000000962}]} />
      </footprint>}
      
      {...restProps}
    />
  )
}