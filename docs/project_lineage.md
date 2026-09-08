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

- Map the 2-D point-mass RL environment's reach trajectory onto the same coordinate/plane convention as the TRSP Kinect joint data (shoulder-elbow-wrist chain) so RL vs. human trajectories are directly comparable.
- Extend `analysis/behavioural/` with a compensation-detection metric (trunk rotation angle, shoulder elevation, forward lean) mirroring Zhi et al. (2018)'s automatic detection features, applied to both TRSP joint data and any wearable-sensor stream.
- Define the wearable sleeve's sensor set (IMU/EMG channel count, sampling rate) and its mapping onto the RL policy's hidden-layer state space, once hardware specs are finalized.
