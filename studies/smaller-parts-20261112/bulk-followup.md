# Further bulk-capacitor screen — 12 November 2026

**Unqualified study only. No active controller substitution, placement, routing or publication.**

A supported supplier search for `47uF 35V` found Honor Elec **RYHG35V47UF5*8 / C48970434**. The exact untouched import is under `bulk-import-staging/`. The isolated `bulk-qualification.circuit.tsx` builds successfully with routing disabled; native output is under `dist/studies/smaller-parts-20261112/bulk-qualification/`. Reproduce the geometric audit with `python studies/smaller-parts-20261112/bulk-review.py`.

| Area screen | mm² |
| --- | ---: |
| Existing RVT1V470M0605 bulk courtyard | 66.314746 |
| New candidate, matching source and native courtyard | 30.291814 |
| Additional possible saving | 36.022931 |
| Conditional full set: GH + two INA241 + this bulk part | 699.637163 |
| Provisional available area | 714.602218 |
| Conditional arithmetic margin | 14.965055 |

This closes the previous 21.057877 mm² **arithmetic deficit** if all three kinds of replacement are accepted and qualified. It does not establish packing, electrical routing, assembly fit or manufacturability. No required feature is removed. The existing three-part assessment still correctly describes its own smaller candidate set.

The supplier lists 47 µF, 35 V, 5 mm diameter, 8 mm height, polymer construction, 55 mΩ ESR and 1.8 A ripple at 100 kHz, and 2,000 hours at 105 °C. It lists Extended, wave soldering, Economic and Standard. These are supplier specifications and process listings, not a quote or independently completed manufacturer qualification. The linked full manufacturer catalog exceeded the web extractor's 18 MB limit and the direct LCSC download returned HTTP 403; its complete mechanical/tolerance, derating, surge and life tables remain to be reviewed. Stock/prices in the saved search are dated observations, not reservations.

The import has **two through holes on both top and bottom copper**, nominal 2 mm lead pitch, 0.700024 mm drill and 1.099998 mm outer pad diameter. It has no downloaded body model. Native component bounds describe only the 3.099994 × 1.099998 mm land span, so those bounds cannot stand in for a verified 5 × 8 mm physical envelope. The build has zero native error records, one missing-schematic-sheet warning, and zero routed traces or vias. Study TypeScript passes.

Before selection, verify the exact manufacturer drawing, lead diameter/pitch and polarity, input ripple/regenerative energy, ESR/ringing and hot-plug behavior, lifetime/temperature, body clearance and bottom lead/solder protrusion against the motor, insulation and screw heads. Obtain supplier assembly/process acceptance for the actual order. Top-side component insertion does not eliminate bottom-side leads/solder or the wave-solder operation.

GH harness acceptance and factory-wire crimp qualification, the supported INA241 import correction, the upright USB footprint/process discrepancy, and complete motor/plug/tool envelopes remain open. A full placement and route must follow qualification; a scalar area margin is insufficient to accept either. No smaller SMT bulk capacitor was qualified by this search.

[Exact JLCPCB part and process listing](https://jlcpcb.com/partdetail/HonorElec-RYHG35V47UF58/C48970434) · [Manufacturer HG-series catalog, hosted by LCSC](https://datasheet.lcsc.com/datasheet/pdf/e43c4cd6aca07bed47cd761db6d42a22.pdf?productCode=C48970458)
