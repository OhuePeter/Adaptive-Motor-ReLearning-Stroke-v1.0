"""
==========================================================
Batch comparison: all TRSP trials vs. an RL reference trajectory

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Iterates over every (subject, task) trial found under the TRSP
dataset root, compares each against the RL reference trajectory for
one perturbation condition, and writes one summary row per trial to
data/processed/rl_vs_trsp_summary.csv. A trial that fails to load or
lacks the expected wrist joint is skipped with a printed warning, so
one malformed trial does not stop the batch.

Usage
-----
python scripts/batch_compare_rl_vs_trsp.py --condition P0
==========================================================
"""

import argparse
from pathlib import Path

import pandas as pd

from src.clinical.trsp_loader import load_trial, joint_series, list_subjects, list_tasks, wrist_side_for_task
from src.clinical.compensation_metrics import compensation_feature_matrix
from src.clinical.trajectory_alignment import project_to_reach_plane, compare_trajectories
from src.clinical.rl_reference import load_rl_reference

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = REPO_ROOT / "data" / "raw" / "toronto_rehab_stroke_pose" / "data_new"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "rl_vs_trsp_summary.csv"


def compare_one_trial(subject: str, task: str, rl_reference, condition: str) -> dict:

    side = wrist_side_for_task(task)
    trial = load_trial(DATASET_ROOT, subject, task)

    wrist_xyz = joint_series(trial, f"Wrist{side}")
    wrist_2d = project_to_reach_plane(wrist_xyz)

    comparison = compare_trajectories(wrist_2d, rl_reference)
    feature_means = compensation_feature_matrix(trial, side=side).mean(axis=0)

    return {
        "subject": subject,
        "task": task,
        "side": side,
        "condition": condition,
        "n_frames": len(trial.labels),
        **comparison,
        "mean_lean_deg": feature_means[0],
        "mean_trunk_rot_deg": feature_means[1],
        "mean_shoulder_elev": feature_means[2],
    }


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", default="P0", help="RL perturbation condition to compare against")
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    args = parser.parse_args()

    rl_reference = load_rl_reference(args.condition)

    rows = []

    for subject in list_subjects(DATASET_ROOT):
        for task in list_tasks(DATASET_ROOT, subject):
            try:
                rows.append(compare_one_trial(subject, task, rl_reference, args.condition))
            except Exception as exc:
                print(f"[skip] {subject}/{task}: {exc}")

    summary = pd.DataFrame(rows)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)

    print(f"Wrote {len(summary)} trial rows to {output_path}")

    if not summary.empty:
        group_labels = {"H": "healthy (H)", "P": "post-stroke (P)"}
        grouped = summary.groupby(summary["subject"].str[0])[
            ["path_length_ratio", "mean_lateral_deviation"]
        ].mean()
        print(grouped.rename(index=group_labels))


if __name__ == "__main__":
    main()
