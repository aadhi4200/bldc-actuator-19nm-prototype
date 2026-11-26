# Phase 1: BLDC Motor

24N28P outrunner with an 80 mm laminated mild steel stator (1 mm plates), for the 9:1, 19 Nm actuator. Two variants, one folder each. Both use the **same stator plate DXF**, winding and air gap. They differ in stack height and magnets.

| Variant | Folder | Stack | Magnets | Output peak (est.) | Envelope |
|---|---|---|---|---|---|
| **N52** (high-grade magnets) | [`n52/`](n52/README.md) | 18 mm | Final: 28 arcs, 3 × 18 mm, N48SH / N52-class (custom order). Test: 28 × 20×5×2 N35 | ≈20 Nm (final rotor) | Ø106 × ~82 mm (phase2 v2) |
| **N35** (cheap blocks) | [`n35/`](n35/README.md) | **20 mm** | **28 × 20×5×2 N35** (one per pole) | ≈13 Nm | Ø106 × 88.5 mm |

- **N52** holds the original v1 motor files (stator DXFs, 18 mm stack, arc and block magnets, v1 test stand, previews, animation). Its rotor, stator hub and back plate are the actuator v2 parts in [`phase2-gearbox/`](../phase2-gearbox/README.md).
- **N35** (added 2026-11-26) is a full motor package in the v2 layout: 20 mm stack, rotor, stator hub, can, back plate and cover, with motor and full-actuator assemblies.
- Torque, Kv and current are hand estimates (±30 %). Confirm them on the test stand (Kv generator test, then the torque test with FOC).

Status: **Phase 1 not started.** Design files only; nothing has been cut, built or measured.

> **Check before machining the v2 / N52 parts:** with winding end turns assumed 4 mm above and below the 18 mm stack, the current v2 layout leaves no room for them (they would reach 1 mm into the rotor floor and 1.5 mm into the back plate). The N35 layout fixes this with 1 mm clearance at both ends. See [`n35/README.md`](n35/README.md#what-changed-from-variant-n52--actuator-v2).
