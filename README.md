# NEMA11 RP2040 — single-side assembly study

Fresh single-side project, separate from `AnasSarkiz/NEMA11_RP2040` double-sided 0.6.9 WIP. Separate project: [GitHub](https://github.com/AnasSarkiz/NEMA11_RP2040_SingleSide) · [tscircuit](https://tscircuit.com/AnasSarkiz/NEMA11_RP2040_SingleSide).

**Unqualified source draft. No single-side fit, routed PCB, manufacturing approval or hardware claim.**

28 × 28 × 1.6 mm, two copper layers; all fitted components targeted to top. Genuine 11HS12-0674S motor, required buzzer, original rear case-bolt axes at ±11.5 mm, no custom carrier. The optional AS5600 remains bottom/DNP, with its 100 nF and 1 µF capacitors fitted top. Bare debug pads do not require component assembly.

The 109-component physical-pin draft includes RP2040/flash/crystal, separate USB data and 15 V PD, buck/diode OR, A4988 regulation shunts, **separate** 50 mΩ inline winding shunts, two INA240A1 amplifiers and 100 Ω/10 nF ADC filters, LEDs, buzzer, TMP102 and encoder provision. I²C0 uses GPIO4/5; current channels use GPIO26/27. Nominal telemetry is 1.65 V zero, 1 V/A, before calibration. The USB4145 pin numbering differs from the previous flat connector and is explicitly rewired.

## Reference and scope

The authoritative NEMA14 V2 reference is pinned at `d9fcd4208bf7a93743447e1a0ab2c780aa08e304`. Four original documents and Git/SHA-256 provenance live in `references/nema14/`. `config/parity.json` enumerates all 38 previously registered requirement/acceptance rows; **every acceptance stays open** for fresh NEMA11 evidence. Reference checkmarks and NEMA14's current, four-layer stackup, 26 mm mounts and 34.5 mm outline do not transfer.

Current deliberate candidate differences needing qualification include compact CH224Q versus CH224A, NEMA11 current setting, motor termination and two-layer thermal/USB behavior. RGB still runs from DATA_VBUS and is unavailable with PD-only power.

## Blockers

- Upright C5815189 was freshly reimported using CLI 0.1.2454 and still fails the archived manufacturer locator criterion. It needs manufacturer/dimension/pin/model/CAM qualification. The archived study found a 1.51 × 0.71 mm locator versus 1.01 × 0.71 mm manufacturer layout, and four bottom shell-paste apertures. Do not shrink or patch supplier geometry.
- The WAGO 250-204/C2765063 parity candidate is not qualified for the NEMA11 motor's AWG26 leads; the documented bare-stranded range is AWG24–16. A compatible termination or clamp must be qualified, including access and motor clearance.
- `config/placement.json` is only a projection seed, with provisional added-part locations. Setting all fitted parts to top is **not packing success**. No placement result is accepted.
- The fresh full-feature screen totals **909.067160 mm²** fitted supplier courtyards against **714.602218 mm²** provisional available area: excess **194.464942 mm²**. It exceeds even the raw 784 mm² board by 125.067160 mm². The old 48.55 mm² deficit used JST rather than the WAGO candidate. That conditional screen is not a proof about all possible parts, bodies or allowed clearances. Fresh native geometry is required for a new conclusion.
- Rear bolts, gap, insulation, motor wire exit and whole-frame envelope remain open. Retained OEM geometry must not be hidden or cropped.
- Routing, electrical clearances/current paths/Kelvin pickups/USB impedance, source/schematic/3D, fabrication CAM, stencil/shell-joint process, live sourcing and physical bench checks remain open.

## Development

Pinned native toolchain: CLI 0.1.2454, tscircuit 0.0.3165, Bun 1.4.4. Install with `npm ci --ignore-scripts --legacy-peer-deps`; explicitly install the official Bun binary if lifecycle scripts were disabled. Use project-local `XDG_CONFIG_HOME=$PWD/.config`, and add `node_modules/.bin` to PATH. No credentials belong in the repository.

`npm run generate` preserves imported bytes and generates source from physical pins. `npm run check` checks source intent and import hashes; it does not certify native output. `python3 scripts/check.py --require-qualified` deliberately fails until acceptance closes. The first native build emitted matching `dist/index/circuit.json`, seven schematic sheets and zero routed traces/vias, but **exited 1 with 172 placement/clearance errors and 278 warnings**. The seed is rejected. Its 386 physical source-port bindings (350 connected, 36 NC) and all 101 fitted-on-top components match the draft contract; that is not physical fit. Both USBs still emit four bottom shell-paste apertures. Native build is a separate step and may contact tscircuit services. Keep meaningful native diagnostics as failures. Never edit emitted Circuit JSON to clear checks.

Publish fresh matching `dist/index/circuit.json` only with its status and validation evidence. Do not copy old double-sided JSON into this project's dist. No order, payment or PR merge is authorized here.
