"""
==========================================================
RL reference trajectory loading/export helpers

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Turns the per-episode rollouts written by
src.evaluation.evaluator.PolicyEvaluator into a single canonical
(n_points, 2) reference path per perturbation condition, and loads
that reference for use in src.clinical.trajectory_alignment.

Before scripts/export_rl_reference.py has been run for a condition,
load_rl_reference() falls back to a straight-line placeholder so the
rest of the TRSP-comparison pipeline stays runnable.
==========================================================
"""

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from src.clinical.trajectory_alignment import resample_path

DEFAULT_N_POINTS = 200

PROCESSED_ROOT = Path(__file__).resolve().parent.parent.parent / "data" / "processed"


def placeholder_rl_reference(n_points: int = DEFAULT_N_POINTS) -> np.ndarray:
    """Straight-line reach placeholder, used only until a real reference is exported."""

    t = np.linspace(0.0, 1.0, n_points)

    return np.stack([t, np.zeros_like(t)], axis=1)


def build_reference_from_episodes(
    episode_paths: List[np.ndarray],
    n_points: int = DEFAULT_N_POINTS,
) -> np.ndarray:
    """
    Resample each (n, 2) episode trajectory to n_points and average them
    into a single canonical (n_points, 2) reference path.
    """

    if not episode_paths:
        raise ValueError("episode_paths is empty; nothing to average")

    resampled = np.stack(
        [resample_path(path, n_points) for path in episode_paths], axis=0
    )

    return resampled.mean(axis=0)


def reference_path_for_condition(condition: str, processed_root: Path = PROCESSED_ROOT) -> Path:

    return Path(processed_root) / f"rl_reference_{condition}.csv"


def save_reference(reference: np.ndarray, condition: str, processed_root: Path = PROCESSED_ROOT) -> Path:

    output_path = reference_path_for_condition(condition, processed_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(reference, columns=["x", "y"]).to_csv(output_path, index=False)

    return output_path


def load_rl_reference(condition: str, processed_root: Path = PROCESSED_ROOT) -> np.ndarray:
    """
    Load the real RL reference exported by scripts/export_rl_reference.py for
    the given perturbation condition (e.g. 'P0', 'L1', 'R3'). Falls back to a
    straight-line placeholder, with a printed warning, if it has not been
    exported yet.
    """

    reference_path = reference_path_for_condition(condition, processed_root)

    if reference_path.exists():
        return pd.read_csv(reference_path)[["x", "y"]].to_numpy(dtype=np.float64)

    print(
        f"[warning] {reference_path} not found; using straight-line placeholder. "
        f"Run scripts/train.py, scripts/evaluate.py (condition={condition}), then "
        f"scripts/export_rl_reference.py --condition {condition} for a real reference."
    )

    return placeholder_rl_reference()
