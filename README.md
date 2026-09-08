# Adaptive-Motor-ReLearning-Stroke-v1.0

**Adaptive Motor Re-Learning: A Wearable Sensor Framework for Upper-Limb Stroke Rehabilitation**

*Peter Ohue¹, Gunnar Blohm¹,² — ¹Centre for Neuroscience Studies, Queen's University; ²Department of Biomedical and Molecular Sciences, Queen's University*

This project extends [`NeuroRL-ObstacleAvoidance-v1.0`](https://github.com/OhuePeter/NeuroRL-ObstacleAvoidance-v1.0) (Ohue, Oby & Blohm, 2026) from a pure computational model of adaptive obstacle avoidance into a clinically-motivated framework for upper-limb stroke rehabilitation. It compares reinforcement-learning-generated reference trajectories against healthy and post-stroke movement data (Toronto Rehab Stroke Pose dataset), diagnoses compensatory movement strategies, and proposes an open-hardware, sensor-driven wearable sleeve for adaptive motor re-learning.

---

## Why this repository exists

Stroke survivors frequently develop compensatory movement strategies (trunk lean, trunk rotation, shoulder elevation) that substitute for lost range of motion at the shoulder and elbow. Left uncorrected, home-based rehabilitation risks reinforcing these compensations rather than restoring natural kinematics. This project asks:

1. Can an RL-trained control policy — validated as a proxy for adaptive biological motor control in our companion paper (Ohue, Oby & Blohm, 2026) — provide a principled "reference trajectory" against which compensatory deviations in stroke survivors can be measured?
2. Can this comparison be delivered through a low-cost, open-hardware wearable sensor sleeve suitable for home and community clinic use?

## Relationship to prior work

This repository inherits the RL environment, PPO training pipeline, and neural-population analysis tools from `NeuroRL-ObstacleAvoidance-v1.0`. See [`docs/project_lineage.md`](docs/project_lineage.md) for a full breakdown of what was carried over and what is new.

## What is included

- Inherited PPO training/evaluation pipeline and perturbation framework (`src/`, `scripts/`, `configs/`).
- Inherited neural-population analysis tools: PCA, clustering, linear decoding (`analysis/`).
- New: methodology and manuscript draft comparing RL reference kinematics to the Toronto Rehab Stroke Pose dataset (`paper/`).
- New: wearable sleeve design notes and schematic workflow (`docs/schematic_workflow.md`).
- Poster template inherited from paper 1, adapted for this project (`presentation/poster/`).

## Repository structure

- `src/`: environment, training, evaluation, and perturbation utilities (inherited).
- `analysis/`: PCA, clustering, decoding, and behavioural analysis utilities (inherited).
- `scripts/`: entry points for training, evaluation, and figure generation (inherited).
- `configs/`: environment, training, evaluation, and perturbation configurations (inherited).
- `data/`: raw and processed data, including Toronto Rehab Stroke Pose dataset references.
- `paper/`: manuscript draft, references, figures, and tables for this project.
- `docs/`: project lineage, schematic workflow, and reproducibility documentation.
- `presentation/`: poster template adapted from paper 1.
- `tests/`: automated tests inherited from paper 1.

## Quick start

```bash
git clone <this-repo-url>
cd Adaptive-Motor-ReLearning-Stroke-v1.0

# Option A — conda
conda env create -f environment.yml
conda activate neurorl

# Option B — pip
pip install -r requirements.txt
```

Training/evaluation entry points are unchanged from paper 1 — see `scripts/` and `docs/reproducibility_guide.md` (to be adapted).

## Data

This project uses the **Toronto Rehab Stroke Pose (TRSP) Dataset** (Dolatabadi et al., 2017; Zhi et al., 2018) for compensatory-movement comparison. Data is not redistributed in this repository; see `data/raw/README.md` for access instructions and citation requirements.

## Citation

If you use this repository, please cite both this project and the companion computational paper:

- Ohue, P., Oby, E., & Blohm, G. (2026). *Neural Population Dynamics Reveal Internal Representations Underlying Adaptive Obstacle Avoidance in Reinforcement Learning.*
- Chinagorom, I. P., & Ohue, P. O. (2025). Integrating computational neuroscience into Africa's academic curriculum: Challenges, opportunities, and strategic implementation. *Journal of Computational Neuroscience, 53*(3), 393–395. https://doi.org/10.1007/s10827-025-00906-5

## Acknowledgements

Supported in part by the Connected Minds Program, Canada First Research Excellence Fund (Grant No. CFREF-2022-00010).

## License

MIT — see [`LICENSE`](LICENSE).
