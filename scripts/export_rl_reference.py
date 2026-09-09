"""
==========================================================
Export a canonical 2-D RL reference trajectory

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Reads the per-episode trajectory_*.csv files written by
src.evaluation.evaluator.PolicyEvaluator for one perturbation
condition, averages them into a single canonical (n_points, 2)
reference path, and saves it to data/processed/. Run this after
scripts/train.py and scripts/evaluate.py, once per condition you
want to compare TRSP data against.

Usage
-----
python scripts/export_rl_reference.py --condition P0
python scripts/export_rl_reference.py --condition R3 --episodes-dir experiments/version_1_0/results/evaluation_R3
==========================================================
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.clinical.rl_reference import (
    DEFAULT_N_POINTS,
    build_reference_from_episodes,
    save_reference,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_episode_trajectories(episodes_dir: Path) -> list:
    """Load every trajectory_*.csv (x, y columns) found in episodes_dir."""

    paths = sorted(episodes_dir.glob("trajectory_*.csv"))

    if not paths:
        raise FileNotFoundError(
            f"No trajectory_*.csv files found in {episodes_dir}. "
            "Run scripts/evaluate.py first to generate episode rollouts."
        )

    return [pd.read_csv(p)[["x", "y"]].to_numpy(dtype=np.float64) for p in paths]


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", required=True, help="e.g. P0, L1, L2, L3, R1, R2, R3")
    parser.add_argument(
        "--episodes-dir",
        default=None,
        help="Defaults to experiments/version_1_0/results/evaluation_<condition>",
    )
    parser.add_argument("--n-points", type=int, default=DEFAULT_N_POINTS)
    args = parser.parse_args()

    episodes_dir = (
        Path(args.episodes_dir)
        if args.episodes_dir
        else REPO_ROOT / "experiments" / "version_1_0" / "results" / f"evaluation_{args.condition}"
    )

    episode_paths = load_episode_trajectories(episodes_dir)

    reference = build_reference_from_episodes(episode_paths, args.n_points)

    output_path = save_reference(reference, args.condition)

    print(f"Averaged {len(episode_paths)} episodes from {episodes_dir}")
    print(f"Saved {reference.shape[0]}-point reference to {output_path}")


if __name__ == "__main__":
    main()
