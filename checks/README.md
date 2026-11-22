# NEMA11 single-side validation evidence

These files document the latest checked-in engineering checkpoint for the single-side RP2040 board. The source and pin checks passed, but the placement was rejected. Routing remains disabled, and the board is not qualified for fabrication.

## Start here

| What you want to verify | Evidence |
| --- | --- |
| Build exit status, open gates and the matching Circuit JSON SHA-256 | [Checkpoint status](checkpoint-status.json) |
| Which physical pins, fitted sides and native errors were seen | [Native audit](native-audit.json) and [build log](native-build.log) |
| Which source files went into the checkpoint | [Build receipt](build-receipt.json) and [source contracts](source-contracts.json) |
| Upright USB-C locator mismatch | [Import review](upright-import-review.json) and [import manifest](import-manifest.json) |
| Whether the current part set fits by the area screen | [Courtyard area screen](courtyard-area-screen.json) |

## What a green source check means

From the repository root, with Node.js 22 and Python 3, run the same checks as the [source workflow](../.github/workflows/source.yml):

```sh
npm ci --ignore-scripts --legacy-peer-deps --no-audit --no-fund
npm run check
npm run check:generated
npm run typecheck
```

These checks cover source intent, generated files and types. For physical evidence, compare the checkpoint hash to the [saved Circuit JSON](../dist/index/circuit.json) and read the [validation summary](../VALIDATION.md). The recorded native build exited 1 with 172 errors and 278 warnings, and the JSON contains no routed traces or vias. Having all fitted parts on top is not proof that they fit or that assembly is qualified.

Before routing, resolve the USB-C locator and shell-joint process, qualify a termination for the motor's AWG26 leads, and demonstrate a fitting placement that preserves fastener and wire access.
