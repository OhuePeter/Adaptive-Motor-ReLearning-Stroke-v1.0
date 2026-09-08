"""
==========================================================
Compare RL reference trajectories against TRSP human reach data

Authors:
Peter Ohue
Gunnar Blohm

Usage
-----
python scripts/compare_rl_vs_trsp.py --subject H01 --task Rch_Fwr_Bck_L

Loads one TRSP trial, extracts the reaching-side wrist trajectory,
projects it onto its 2-D reach plane, and compares it against an RL
reference trajectory (loaded from an evaluation rollout .npy/.csv if
available; falls back to a straight-line placeholder reference so the
pipeline is runnable before RL rollouts are wired in).
==========================================================
"""

import argparse
from pathlib import Path

import numpy as np

from src.clinical.trsp_loader import load_trial, joint_series
from src.clinical.compensation_metrics import compensation_feature_matrix
from src.clinical.trajectory_alignment import project_to_reach_plane, compare_trajectories

DATASET_ROOT = Path(__file__).resolve().parent.parent / "data" / "raw" / "toronto_rehab_stroke_pose" / "data_new"


def placeholder_rl_reference(n_points: int = 200) -> np.ndarray:
    """Straight-line reach placeholder, to be replaced with a real RL rollout."""

    t = np.linspace(0.0, 1.0, n_points)

    return np.stack([t, np.zeros_like(t)], axis=1)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True, help="e.g. H01 or P01")
    parser.add_argument("--task", required=True, help="e.g. Rch_Fwr_Bck_L")
    parser.add_argument("--side", default="Right", choices=["Left", "Right"])
    args = parser.parse_args()

    trial = load_trial(DATASET_ROOT, args.subject, args.task)

    wrist_xyz = joint_series(trial, f"Wrist{args.side}")
    wrist_2d = project_to_reach_plane(wrist_xyz)

    rl_reference = placeholder_rl_reference()

    result = compare_trajectories(wrist_2d, rl_reference)

    features = compensation_feature_matrix(trial, side=args.side)

    print(f"Subject {trial.subject}, task {trial.task}, {len(trial.labels)} frames")
    print("Trajectory comparison vs. RL reference:")
    for key, value in result.items():
        print(f"  {key}: {value:.4f}")
    print("Compensation feature means (lean_deg, trunk_rot_deg, shoulder_elev):")
    print(f"  {features.mean(axis=0)}")


if __name__ == "__main__":
    main()
