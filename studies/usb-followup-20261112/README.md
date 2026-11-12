# Upright USB follow-up - 12 November 2026

**Independent connector diagnostics only. No controller replacement, full-board placement, routing or manufacturing acceptance. Do not manufacture from this study CAM.**

Based on study branch commit `90f86f315744263af66219bfe5e9094a67678fe7`; the active controller and `dist/index` remain byte-for-byte unchanged from main `ebebbf2`. All supplier TSX, OBJ and STEP definitions are untouched. CLI 0.1.2454, tscircuit 0.0.3165, core 0.0.2347, Bun 1.4.4.

## Current USB4145: source, native rotation and CAM

The previous archived study already attributed the oversized C5815189 locator to the raw supplier NPTH path. This follow-up does not repeat that attribution as a fresh supplier read. It uses the unchanged current import (TSX SHA-256 `f94a118e3e73f17a560d7456b982abddf23244e6a2f3897b05ec952e93af11e5`) and verifies its native/CAM behavior with the current toolchain.

The archived GCT USB4145 A2 drawing (31 January 2023, PDF SHA-256 `c38c5977f6123b0178fa25853140c16bb2d8c70808f2203f3ab604ce31d18516`) was rendered and visually reviewed again. The live GCT product page still links the A2 PCN, which explains that its PCB layout update improves pick-and-placement. Current manufacturer-page drawing download links returned HTTP 403; no newer drawing was obtained. The archived PDF is retained in the existing source history, not duplicated here.

The drawing specifies one round 0.71 mm locator and one **1.01 x 0.71 mm slot**, tolerance +/-0.05 mm, on an 8 mm pitch. The import instead defines **1.5099792 x 0.7099808 mm** for the slot, 0.4499792 mm above the drawing's maximum long dimension.

`rotation.circuit.tsx` tests top-side copies at 0, 90, 180 and 270 degrees on an intentionally oversized diagnostic board. Native slot centers, orientation, width/height, four shell slots and 16 signal lands are checked using the emitted **footprint origin**, which differs from the asymmetric pad-bounds center. Native rotations pass. Official CAM export preserves all four NPTH capsule axes and approximately 1.509981 x 0.709981 mm dimensions after output rounding. This is not a rotation or capsule-conversion explanation for the mismatch.

Every top-side connector emits **20 top and four bottom paste apertures**. The exported F_Paste/B_Paste contain 80/16 flashes for the four copies. In the installed core bundle, `PlatedHole.doInitialPcbPrimitiveRender` detects the hybrid package as SMT because it contains SMT pads, then creates both top and bottom paste for its plated shell pills. The installed typed `PlatedHoleProps` expose solder-mask controls but no per-side solder-paste control. This identifies the current native behavior; it does not establish assembler approval or claim that all-top fitted assembly is impossible. No imported metadata, geometry, native JSON or CAM was patched to suppress it.

A supported tooling/configuration change or explicitly approved assembler process, appropriate shell-anchor paste/slot fill, and the locator correction/fresh import remain necessary. Model seating/contact planes, plug and tool envelopes, motor gap, fasteners and real assembly still need validation. A scalar courtyard screen cannot clear these gates.

## Alternatives imported, measured and rejected as area savings

| Exact supplier identity | Height from manufacturer | Exact source/native courtyard | Change against current 46.559623 mm2 |
| --- | ---: | ---: | ---: |
| GCT USB4120-03-C / C3445864 | 6.50 mm | 55.695583 mm2 | +9.135960 mm2 |
| GCT USB4140-GF-0070-C / C7374561 | 6.50 mm | 51.865286 mm2 | +5.305664 mm2 |

Both supported exact imports completed, including local models, and were built in `alternatives.circuit.tsx`. Their native courtyards match the supplier polygons. Lower height and fewer terminals do not save XY area here. Replacing the PD port with USB4140 would increase the earlier GH/INA241 area deficit from 21.057877 to 26.363541 mm2. Two USB4120s add 18.271920 mm2. Neither is selected or qualified.

USB4140 is charging-only: it retains CC1/CC2, VBUS and GND, but cannot replace the required data/programming port. Its import uses seven numbered ports, with four shell anchors on pin 7; any future use requires a new reviewed physical pin contract, not reuse of USB4145 numbering.

The GCT-authored USB4140 A3 drawing (29 August 2024), downloaded from Mouser and visually reviewed, specifies a 0.70 mm round locator and 1.00 x 0.70 mm slotted locator. Its PDF SHA-256 is `290f529eff40fd2379a6ea1684f8d1c54ec743f18613a7efa2b070eb7956c02a`. The fresh import instead has two round holes of **0.649986 and 0.8499856 mm**. Fresh raw supplier `HOLE` records reproduce those diameters (EasyEDA radius x 2 x 0.254 mm), so this discrepancy also originates in supplier source data. It remains unqualified independently of the area increase. USB4140 emits 10 top/four bottom paste apertures; USB4120 emits 20 top/four bottom.

The live GCT USB4120 page and GCT-authored A6 drawing available through TME establish the alternative's identity and height. The A6 PDF could be read through the web extractor, but the direct download returned 403 and it was not visually inspected locally; complete footprint qualification is not claimed. The initial generic CLI searches for USB4120 and USB4140 returned HTTP 500. Exact identities were subsequently obtained from supplier listings and exact imports succeeded. A successful import is not stock, process or order acceptance. The USB4140 import also reported a datasheet-service timeout. Catalog/mirror counts are not reservations.

## Reproduce and limitations

Run:

```sh
bunx tsci build studies/usb-followup-20261112/rotation.circuit.tsx --ignore-config --routing-disabled --pcb-svgs
bunx tsci build studies/usb-followup-20261112/alternatives.circuit.tsx --ignore-config --routing-disabled --pcb-svgs
bunx tsci export dist/studies/usb-followup-20261112/rotation/circuit.json --format gerbers --output rotation-gerbers.zip
python studies/usb-followup-20261112/audit.py
bunx tsc --noEmit --project studies/usb-followup-20261112/tsconfig.json
```

The audited CAM files are retained under `cam/`; re-export to a separate folder before comparing to avoid treating generated evidence as a manufacturing release. `inputs.json` records source/native/CAM/model hashes. Native outputs have zero error records, zero routed traces and zero vias. Framework reference-designator, missing insertion-direction and availability warnings remain: 12 in the rotation fixture and six in the alternatives fixture. TypeScript passes. The warnings are not evidence of availability or physical accessibility.

No required function was removed. There is still no qualified upright USB replacement, accepted single-side packing or routed controller. The previous bulk/GH/amplifier candidates retain all their qualification gates. No registry push or main-branch change was made for this study.

## Primary sources

- [GCT USB4145](https://gct.co/connector/usb4145) and [A2 PCN](https://gct.co/files/pcns/gct%20usb4145%20a2%20pcn%2020230214.pdf).
- [GCT USB4120](https://gct.co/connector/usb4120) and [GCT-authored A6 drawing hosted by TME](https://www.tme.eu/Document/32a5997cfd5c9e51007a55afe4128ff4/usb4120.pdf).
- [GCT USB4140](https://gct.co/connector/usb4140), [GCT-authored A3 drawing hosted by Mouser](https://www.mouser.com/catalog/specsheets/GCT_USB4140_Product_Drawing.pdf), and [LCSC exact C7374561 identity](https://lcsc.com/product-detail/usb-connectors_global-connector-technology-usb4140-gf-0070-c_C7374561.html).
- Untouched public EasyEDA component records for C3445864 and C7374561 under `sources/`; existing archived C5815189 source evidence under `references/prior-studies/upright-usb-evidence.tar.gz`.
