"""
==========================================================
Compare RL reference trajectories against TRSP human reach data

Authors:
Peter Ohue
Gunnar Blohm

Usage
-----
python scripts/compare_rl_vs_trsp.py --subject H01 --task Rch_Fwr_Bck_L --condition P0

Loads one TRSP trial, extracts the reaching-side wrist trajectory,
projects it onto its 2-D reach plane, and compares it against the RL
reference trajectory for the given perturbation condition (exported
by scripts/export_rl_reference.py; falls back to a straight-line
placeholder if that has not been run yet).
==========================================================
"""

import argparse
from pathlib import Path

from src.clinical.trsp_loader import load_trial, joint_series
from src.clinical.compensation_metrics import compensation_feature_matrix
from src.clinical.trajectory_alignment import project_to_reach_plane, compare_trajectories
from src.clinical.rl_reference import load_rl_reference

DATASET_ROOT = Path(__file__).resolve().parent.parent / "data" / "raw" / "toronto_rehab_stroke_pose" / "data_new"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True, help="e.g. H01 or P01")
    parser.add_argument("--task", required=True, help="e.g. Rch_Fwr_Bck_L")
    parser.add_argument("--side", default="Right", choices=["Left", "Right"])
    parser.add_argument("--condition", default="P0", help="RL perturbation condition to compare against")
    args = parser.parse_args()

    trial = load_trial(DATASET_ROOT, args.subject, args.task)

    wrist_xyz = joint_series(trial, f"Wrist{args.side}")
    wrist_2d = project_to_reach_plane(wrist_xyz)

    rl_reference = load_rl_reference(args.condition)

    result = compare_trajectories(wrist_2d, rl_reference)

    features = compensation_feature_matrix(trial, side=args.side)

    print(f"Subject {trial.subject}, task {trial.task}, {len(trial.labels)} frames")
    print(f"Comparison vs. RL reference condition {args.condition}:")
    for key, value in result.items():
        print(f"  {key}: {value:.4f}")
    print("Compensation feature means (lean_deg, trunk_rot_deg, shoulder_elev):")
    print(f"  {features.mean(axis=0)}")


if __name__ == "__main__":
    main()

