# Smaller-component qualification study — 12 November 2026

Based on published GitHub source `ebebbf2ef418557dfec44e8c2327d81e569e1b3e`.
This is a study checkpoint. **The active controller, its fitted features, its existing rejected placement and its dist/index outputs are unchanged. No fit, copper routing, manufacturing or physical motor-wire acceptance is claimed.**

## Exact candidates and measured area

Both parts were freshly imported using supported CLI 0.1.2454, tscircuit 0.0.3165, core 0.0.2347 and Bun 1.4.4, with `--jlcpcb --download --use-exact-footprint`. Imported TSX, OBJ and STEP bytes were not edited. The isolated three-component fixture contains one JST header and two amplifiers; it is not the complete controller.

| Function | Current candidate courtyard | Smaller candidate | Fresh supplier/native courtyard |
| --- | ---: | --- | ---: |
| Four-wire motor connection | WAGO 250-204 / C2765063: 199.999229 mm² | JST BM04B-GHS-TBT(LF)(SN) / C161692 | 54.593903 mm² |
| Coil A current amplifier | INA240A1PWR / C93965: 27.328825 mm² | INA241A2IDDFR / C5240853 | 13.327747 mm² |
| Coil B current amplifier | INA240A1PWR / C93965: 27.328825 mm² | INA241A2IDDFR / C5240853 | 13.327747 mm² |

Recomputed from exact supplier polygons and independently compared with native emitted courtyard polygons:
- Existing complete fitted set: **909.067160 mm²**.
- Hypothetical set with only these three replacements: **735.660095 mm²**.
- Saving: **173.407065 mm²**.
- Board area after four provisional R2.35 mm screw-head exclusions: **714.602218 mm²**.
- **Residual deficit: 21.057877 mm². The conditional courtyard screen still fails.**

All required electronics remain in this arithmetic: buzzer and driver/clamp, RGB circuitry, both independent winding-current channels and their filters/bypasses, A4988 regulation shunts, temperature circuit, two upright USBs, MCU/flash/crystal, power/protection/decoupling and the two fitted encoder capacitors. Optional AS5600 remains DNP. Debug pads are not fitted-component savings.

The existing 47 µF/35 V bulk capacitor occupies 66.314746 mm² of courtyard. If it were the only additional replacement, a suitable part would need a courtyard **at most 45.256869 mm² merely to reach this area threshold**. Routing, tolerances, insertion/tool access and actual polygon packing need additional evaluation. A smaller body dimension is not an imported courtyard measurement. No smaller bulk capacitor has been qualified or selected.

This is a screen for wholly contained nonoverlapping courtyards under the stated provisional exclusions. It is not an impossibility theorem about bodies, alternate qualified parts, permitted courtyard overlaps or a different approved mechanical design.

## JST GH motor connection — conditional candidate

Proposed mating set: BM04B-GHS-TBT PCB header, GHR-04V-S cable housing and SSHL-002T-P0.2 terminals. The connector would be on the controller PCB; the specified motor has fixed leads, not a motor-mounted JST socket.

Manufacturer ratings support 1 A with AWG26 and 50 V. The nominal 0.67 A/phase motor rating is within that stated current rating, but does not establish the complete temperature, mating, vibration or harness qualification.

**AWG compatibility alone is insufficient.** The specified contact accepts insulation diameter 0.76–1.0 mm. The saved NEMA11 drawing identifies AWG26/UL1569 but does not establish the actual lead insulation diameter. Do not infer it from AWG or UL style. Direct crimping therefore remains unapproved. Measure the factory lead and qualify terminal/crimp height, pull force, insulation support, harness length, pin order, latch access and insertion/extraction envelopes. If the leads do not fit, a fully specified transition harness or another qualified connector is needed; do not remove strands or shave insulation.

The source import emits six numbered terminals: four signal pads and two reinforcement pads numbered 5/6. The diagnostic leaves the two reinforcement pads NC. Signal numbering and the supplier land pattern still require complete manufacturer drawing and pin-one review; import success alone is not acceptance. In particular, the source signal lands measure 0.60 × 1.70 mm and should be reconciled with the manufacturer's recommended layout.

Changing WAGO to GH also changes the spring-clamp requirement to a crimped detachable harness. **That requirement change has not been accepted.** The active board still selects WAGO. The former NEMA11 C131334 part is a JST **PH** B4B-PH-K-S, not this GH part; do not confuse their pitch, wire contacts or supplier identities.

[JST GH manufacturer catalog](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf) · [JLCPCB C161692 identity/process listing](https://jlcpcb.com/partdetail/JST-BM04B_GHS_TBT_LF_SN/C161692)

## INA241A2 — smaller package, blocked metadata qualification

The A2 gain is 20 V/V. Retaining each separate 50 mΩ inline shunt gives 1 V/A nominal, with split REF pins at 3.3 V/GND giving 1.65 V zero and 0.98–2.32 V at ±0.67 A. These are nominal calculations, not measured current accuracy. Both current channels, 100 Ω/10 nF output filters, local bypasses and the separate A4988 regulation shunts must remain.

TI specifies 2.7–20 V supply, −5 to 110 V operational common mode, enhanced PWM rejection and a 3.2 mA maximum quiescent current per channel over temperature. A 3.3 V supply and the nominal 15 V application fall within those ranges. Bridge ringing, settling, filter/ADC behavior, noise, calibration, two-layer Kelvin paths, motor-current widths and thermal behavior still need qualification.

The physical pin map differs from INA240 PW: 1 IN−, 2 GND, 3 REF2, 4 reserved, 5 OUT, 6 VS, 7 REF1, 8 IN+. **TI SBOSA30D Table 5-1 requires reserved pin 4 to be grounded.** The fresh untouched import instead contains `pin4: {doNotConnect: true}`. Both diagnostic instances retain this metadata while their board wiring grounds pin 4, exposing the conflict in untouched native JSON.

The native build exits 0 and pin check reports zero errors/four unrelated warnings. Neither result settles the manufacturer/import contradiction. Do not leave pin 4 floating to satisfy metadata, override the imported pin attributes, or edit emitted JSON. A supported upstream correction followed by fresh import/positive and negative checks, or a different qualified amplifier, is required before adoption.

[TI manufacturer datasheet](https://www.ti.com/lit/ds/symlink/ina241a.pdf) · [JLCPCB C5240853 identity/process listing](https://jlcpcb.com/partdetail/TexasInstruments-INA241A2IDDFR/C5240853)

## Verification and remaining gates

- Both supplier imports completed; the GH import reported a datasheet-service timeout.
- Isolated fixture native build: exit 0; zero native PCB errors, 12 warnings. All 22 SMT pads and paste apertures are top-side; zero routed traces or vias.
- Native pin check on the fixture JSON: exit 0; errors 0, warnings 4.
- Native readable netlist check using the supported TSX entrypoint: exit 0; errors 0, warnings 0. It shows both reserved pins grounded. An earlier JSON-input attempt was treated as a React component and failed; that invocation is not a netlist pass or an attributed upstream defect.
- Study TypeScript passes. Exact imported/source and native courtyard areas agree.
- The active full-board source/config/imports/scripts and dist/index match the base source. No feature was removed and no new full-board placement or route was accepted.
- JLCPCB lists both candidates as Extended, SMT, Economic and Standard. Catalog eligibility does not establish current stock, price, reservation, supplier pickup rotation or assembled-order acceptance.
- The original upright-USB locator mismatch and bottom shell-paste/process concerns remain open.
- Factory motor wires, rear fasteners, motor gap/insulation, wire exit, cable/plug/tool access and the complete assembly envelope remain unqualified.

The complete untouched import/model files, fixture source/native output, hashes and review script are retained in the local study checkpoint. This published report preserves the verified result and exact candidate identities; it does not replace the full artifact transfer.

Consequential decisions still open: accept a crimped motor harness instead of a spring clamp; resolve factory-wire fit/process; obtain a supported amplifier metadata correction; and select enough additional qualified size reductions to close the remaining area deficit before real packing and routing.
