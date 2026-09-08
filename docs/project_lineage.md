# Project lineage: from NeuroRL-ObstacleAvoidance-v1.0 to this project

## Inherited unchanged

- `src/` — Gymnasium environment, PPO training loop, perturbation injection.
- `analysis/` — PCA, clustering, linear decoding, behavioural/kinematic analysis.
- `scripts/` — training, evaluation, and figure-generation entry points.
- `configs/` — environment, training, evaluation, perturbation YAML configs.
- `presentation/poster/create_poster.py` — poster template (Queen's colour palette, 3-column A0 layout).
- `tests/` — unit tests for environment/analysis utilities.

## New in this project

- `data/raw/toronto_rehab_stroke_pose/` — Toronto Rehab Stroke Pose dataset (healthy + post-stroke reach kinematics).
- `paper/manuscript.md` — new manuscript draft (this project's clinical framing).
- `paper/references.bib` — new bibliography (stroke rehabilitation + assistive technology literature).
- `docs/schematic_workflow.md` — Inkscape workflow for the upper-limb schematic figure.

## What needs adaptation (not yet done)

- `src/clinical/trsp_loader.py`, `compensation_metrics.py`, `trajectory_alignment.py` — implemented: TRSP loading, compensation-angle extraction, and RL-vs-human trajectory alignment/comparison. See `scripts/compare_rl_vs_trsp.py` for a runnable example (currently compares against a placeholder straight-line reference — swap in a real RL rollout array once evaluation rollouts are exported for this project).
- `docs/wearable_sleeve_hardware.md` — v0.1 sensor/hardware design draft (3-IMU sleeve + microcontroller + BLE), not yet built or validated.
- Still open: export a real RL reference trajectory (2-D array) per perturbation condition from `src/evaluation/` so `scripts/compare_rl_vs_trsp.py` can replace `placeholder_rl_reference()` with the actual companion-paper rollouts.
