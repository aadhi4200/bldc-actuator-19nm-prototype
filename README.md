# DIY High-Torque BLDC Actuator (9:1, 19 Nm): CAD

CAD and design files for a DIY robotic actuator: a custom BLDC motor, a 9:1 gearbox and an FOC controller, for precision robot arm joints. Developed in three phases, one folder each.

| Phase | Folder | Status |
|---|---|---|
| 1. BLDC motor (stator, rotor, magnets, winding) | [phase1-motor/](phase1-motor/README.md) | Not started (v1 design files ready) |
| 2. 9:1 gearbox | [phase2-gearbox/](phase2-gearbox/README.md) | Not started |
| 3. FOC controller (ODrive-class board first, custom PCB later) | [phase3-foc-controller/](phase3-foc-controller/README.md) | Not started |

Design notes, decisions and status live in the knowledge base: [engineering-assistant / BLDC_ACTUATOR.md](https://github.com/aadhi4200/engineering-assistant/blob/main/projects/electronics/BLDC_ACTUATOR.md).

## Conventions

- Units: mm. Z = actuator axis.
- File names: `bldc_v<N>_<part>_<key dims>_<material>.<ext>`.
- Each phase keeps the same layout where it applies: `dxf/`, `step/`, `fusion360_import/`, `previews/`, `scripts/`.
- Generated files are rebuilt from each phase's `scripts/`; edit the parameters, not the outputs.
