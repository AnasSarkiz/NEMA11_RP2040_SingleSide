# Qualified-harness option and rejected full-controller placement

Status: **unqualified study, incomplete placement, no routing or manufacturing release**. Based on public study commit `993c71867f673983218bce3d5ff9d2d2797ecf4d`. Main, the published tscircuit project and the separate double-sided project are unchanged.

The user now permits a qualified compact crimp connector or transition harness. This resolves the requirement to retain a spring-clamp connection in this study; it does not qualify a particular connector, crimp, splice or wire.

## JST SH candidate

Exact supported CLI import: **JST BM04B-SRSS-TB(LF)(SN), C160390**, using `tsci import --jlcpcb --download --use-exact-footprint C160390`. The imported TSX/OBJ/STEP are retained unchanged. No custom footprint or native JSON edits are used.

The supplier courtyard is **34.3098214 mm²**, about **20.2841 mm² smaller than GH** and **165.6894 mm² smaller than the original WAGO**. An isolated native build has **zero errors, five warnings, six top paste apertures, zero bottom paste apertures, and no plated holes**. Warnings include generic reference designation, no ground metadata, missing sheet, connector accessibility and availability; a successful build is not connector qualification.

The four signal lands are 0.6 × 1.55 mm on 1.0 mm pitch; two reinforcement lands are 1.2 × 1.8 mm. Their centers and relative dimensions agree, to import rounding, with the JST top-entry reference layout. Both reinforcement lands share physical pin5 and are explicitly NC. Native pins1–4 retain A+, A−, B+, B− respectively. The independent audit verifies source-to-native geometry and all six top paste records.

Proposed mating parts are **SHR-04V-S** and **SSH-003T-P0.2-H**, with **AWG28 stranded wire and 0.4–0.8 mm insulation OD**. The manufacturer's current English catalog rates SH at 1 A with AWG28 and 50 V. Nominal motor phase current is 0.67 A. These values are a screening check, not thermal/current-limit qualification. The factory motor has AWG26 leads, which cannot be directly crimped in this SH contact. A transition harness therefore needs a specified, qualified connection to the factory wires. The motor-side housing has not been established as a JST housing and is not assumed to mate directly.

Still required before adoption: exact wire/length and splice or adapter specification; genuine contact/tool/process selection, crimp section and pull tests; insulation and continuity/phase mapping; actual temperature rise at maximum configured current; connector retention and strain relief under motor vibration; CAD body/mated height and cable bend clearance; procurement/assembly availability. The housing lance retains the contact and must not be mistaken for proof of a positive cable-plug latch.

Sources: [JST current SH catalog](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf), [manufacturer product page](https://www.jst-mfg.com/product/detail_e.php?series=231), [JLCPCB identity](https://jlcpcb.com/partdetail/C160390). The manufacturer download returned403 locally; the current manufacturer-authored drawing was also visually checked through an LCSC mirror. That mirror contains a different AWG annotation on its first page, so current official specifications govern; it is not evidence that AWG26 crimping is allowed. No manufacturer PDF is added here.

## Complete placement study

A conditional set using SH, two INA241A2 amplifiers and the previously reviewed radial 47 µF/35 V capacitor has about **679.3531 mm²** of fitted supplier courtyards. It retains every required function. This scalar area does not include seven bare test-pad access envelopes, routing, cable/tool access or process qualification.

Two bounded CP-SAT searches returned **UNKNOWN** (45 s seed11; 55 s seed23 with identical-part symmetry reduction). UNKNOWN is not infeasibility. A separate deterministic MaxRects search of500 randomized orders placed **87 of101 fitted components**, leaving **14 fitted components / 27.40544 mm² of rounded courtyard rectangles** unplaced. It uses enclosing0.47 mm horizontal steps around the actual ±11.5 mm screw axes, R2.35 mm provisional head exclusions, and opposite-edge upright USBs. The audit independently verifies every placed rectangle, exact circular screw exclusion and native transformed courtyard.

`controller.circuit.tsx` is the **complete rejected diagnostic**, not a proposed usable placement. All109 source components,73 nets and7 sheets remain. The14 unplaced fitted parts are deliberately parked beyond the right board edge; the7 bare test pads retain their previous, unpacked seed positions. The board remains28 ×28 ×1.6 mm,2 copper layers, fitted parts top, optional encoder bottom/DNP, both encoder capacitors top. Source net contracts are unchanged except the intentional, manufacturer-specified INA241 physical pin remapping.

Native build exits1 as expected: **74 placement errors,14 component-outside-board errors,5 footprint overlaps and2 pad-clearance errors**, plus270 warnings. Some edge messages round the measured value to0.250 mm although it remains just below the required value; none are waived. There are **zero routes and zero vias**. TypeScript and the independent diagnostic audit pass. No claim of full fit, routed current paths, thermal performance or manufacturability is made.

USB4145 remains unqualified because its imported locator slot is1.5099792 ×0.7099808 mm against the A2 drawing's1.01 ×0.71±0.05 mm recommendation. The existing supported import also produces bottom paste at its shell plated holes; assembly process approval remains open. Exact imports of all-SMT JAE **DX07S024WJ4R450/C20867323**, SameSky **UJ20-C-V-G-SMT-P16-TR-65/C45082773**, and GCT **USB4160-03-0070-C/C7407285** returned “Component not found in EasyEDA library search.” This is a supplier import blocker, not proof the physical parts are unavailable. No substitute definition was invented. The eight-contact SameSky UJ20-C-V-G-SMT-P8-TR drawing does not expose CC1/CC2 and specifies1.0 mm PCB, so it is not accepted for this data/PD design. Earlier qualified-import investigations remain in the [published USB followup](../usb-followup-20261112/README.md).

Other unchanged gates: INA241 pin4 remains erroneously imported as do-not-connect despite TI requiring ground; [upstream PR656](https://github.com/tscircuit/easyeda-converter/pull/656) remains a proposed fix, not a released import. The radial capacitor's solder/lead clearance, wave or selective solder process, actual body and motor gap remain unqualified. No component was adopted into the active controller.

## Native review images

[Complete rejected controller PCB](../../dist/studies/usb-layout-20261112/controller/pcb.png): the right-hand parts are deliberately outside the board. [Isolated SH header PCB](../../dist/studies/usb-layout-20261112/harness/pcb.png). Both images are direct rasterizations of retained native SVG output.

## Reproduction

Use the pinned project toolchain (CLI0.1.2454, tscircuit0.0.3165, core0.0.2347, Bun1.4.4). OR-Tools9.15.6755 is a local study dependency, not a production dependency. Solver searches may differ with platform and scheduling; the retained packing witness and independent audit do not depend on rerunning the solver.

```sh
python studies/usb-layout-20261112/pack.py --seconds 55 --seed 23
python studies/usb-layout-20261112/greedy.py
python studies/usb-layout-20261112/make-controller.py
bunx tsci build studies/usb-layout-20261112/harness.circuit.tsx --ignore-config --routing-disabled --pcb-svgs
bunx tsci build studies/usb-layout-20261112/controller.circuit.tsx --ignore-config --routing-disabled --pcb-svgs --schematic-svgs
bunx tsc --noEmit -p studies/usb-layout-20261112/tsconfig.json
python studies/usb-layout-20261112/audit.py
```

The controller build must remain rejected until its documented problems are resolved. No `tsci push`, main update or registry publication was performed for this study.
