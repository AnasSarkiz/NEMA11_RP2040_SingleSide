# Validation status

Source drafting and qualification are separate. No inherited CAD pass applies to this project.

The draft adds ten telemetry parts, fits both encoder capacitors, selects two upright USB candidates and a spring-clamp candidate, and retains seven schematic sheets. The 109 source components include 101 fitted supplier components, one DNP encoder and seven bare pads.

All required physical acceptance remains OPEN. `config/placement.json` is unqualified. Routing is disabled. The new native Circuit JSON is `dist/index/circuit.json`, SHA-256 `7ef84e3036abcababc1946553b5f7e12de4b92c62d63da77ccb8ee964227a7b1`. The native build exited 1: 73 courtyard conflicts, 65 footprint overlaps, 22 pad-clearance errors, 11 placement/access errors and one WAGO board-boundary error. There are 278 warnings, including 131 schematic-sheet overflows, 101 availability warnings and three datasheet timeouts. Seven sheets exist, but readability/coverage acceptance is still open. Zero PCB traces/vias were emitted; the 73 source nets are not routed. The native pin-contract audit passes after resolving the explicit internally common shell terminals; the six duplicated shell ports have no independent net trace and must inherit their explicit internal connection. No JSON was modified. Each USB emits 20 top and four bottom paste apertures. A source contract pass is not footprint, clearance, placement, routing, CAM, assembly or hardware acceptance.

The fresh courtyard screen is 909.067160 mm² fitted / 714.602218 mm² provisional area; excess 194.464942 mm². Fresh exact USB import still has a 1.5099792 × 0.7099808 mm locator, 0.4499792 mm above the archived drawing maximum width. Both are qualification failures, not permission to change imported geometry.
