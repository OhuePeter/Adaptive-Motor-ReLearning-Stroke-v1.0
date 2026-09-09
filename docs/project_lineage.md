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

- `src/clinical/trsp_loader.py`, `compensation_metrics.py`, `trajectory_alignment.py`, `rl_reference.py` — implemented: TRSP loading, compensation-angle extraction, RL-vs-human trajectory alignment/comparison, and RL reference export/loading. `scripts/compare_rl_vs_trsp.py` (single trial) and `scripts/batch_compare_rl_vs_trsp.py` (all subjects/tasks) run end-to-end.
- `docs/wearable_sleeve_hardware.md` — v0.1 sensor/hardware design draft (3-IMU sleeve + microcontroller + BLE), not yet built or validated.
- Still open: train a policy with `scripts/train.py`, evaluate it per perturbation condition with `scripts/evaluate.py`, then run `scripts/export_rl_reference.py --condition <P0|L1|L2|L3|R1|R2|R3>` to replace the straight-line placeholder with the real trained-policy rollout for that condition.
