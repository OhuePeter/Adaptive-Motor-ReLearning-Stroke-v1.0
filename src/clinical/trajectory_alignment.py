"""
==========================================================
RL reference vs. human reach trajectory alignment

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Aligns a human joint trajectory (from TRSP) with an RL reference
trajectory (from src.environment / evaluation rollouts) so the two
can be compared on a common 2-D reach-plane and common time base.

Pipeline:
1. Project the human wrist trajectory onto its own best-fit reach
   plane (PCA of the 3-D joint path) -> 2-D coordinates.
2. Resample both trajectories to a common number of time points
   (default 200) via linear interpolation, so trial duration and
   RL episode length no longer need to match.
3. Rigid-align (translate + uniformly scale) the human trajectory
   onto the RL reference using start/end point correspondence, so
   comparisons reflect path *shape*, not absolute position/scale.
4. Report path-length ratio and mean lateral deviation, reusing the
   path_length metric already defined in src.evaluation.metrics.
==========================================================
"""

from typing import Tuple

import numpy as np

from src.evaluation.metrics import BehaviourMetrics


def _resample(path: np.ndarray, n_points: int) -> np.ndarray:
    """Resample an (n, d) path to (n_points, d) via linear interpolation."""

    t_src = np.linspace(0.0, 1.0, path.shape[0])
    t_dst = np.linspace(0.0, 1.0, n_points)

    return np.stack([
        np.interp(t_dst, t_src, path[:, dim]) for dim in range(path.shape[1])
    ], axis=1)


def project_to_reach_plane(joint_xyz: np.ndarray) -> np.ndarray:
    """
    Project a (n_frames, 3) joint trajectory onto its dominant 2-D
    plane of motion via PCA, returning (n_frames, 2) coordinates.
    """

    centered = joint_xyz - joint_xyz.mean(axis=0, keepdims=True)

    # SVD-based PCA: first two principal axes define the reach plane
    _, _, vt = np.linalg.svd(centered, full_matrices=False)

    plane_axes = vt[:2]  # (2, 3)

    return centered @ plane_axes.T


def align_to_reference(
    human_path_2d: np.ndarray,
    rl_reference_2d: np.ndarray,
    n_points: int = 200,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Resample both trajectories to n_points, then translate+scale the
    human trajectory so its start/end points match the RL reference's
    start/end points. Returns (aligned_human, resampled_reference).
    """

    human_rs = _resample(human_path_2d, n_points)
    ref_rs = _resample(rl_reference_2d, n_points)

    human_disp = human_rs[-1] - human_rs[0]
    ref_disp = ref_rs[-1] - ref_rs[0]

    human_scale = np.linalg.norm(human_disp)
    ref_scale = np.linalg.norm(ref_disp)
    scale = ref_scale / human_scale if human_scale > 1e-8 else 1.0

    aligned = (human_rs - human_rs[0]) * scale + ref_rs[0]

    return aligned, ref_rs


def compare_trajectories(human_path_2d: np.ndarray, rl_reference_2d: np.ndarray) -> dict:
    """
    Compute path-length ratio and mean lateral (perpendicular)
    deviation between an aligned human trajectory and its matching
    RL reference trajectory.
    """

    aligned_human, ref = align_to_reference(human_path_2d, rl_reference_2d)

    human_len = BehaviourMetrics.path_length(aligned_human)
    ref_len = BehaviourMetrics.path_length(ref)

    # perpendicular deviation at each resampled time point
    diffs = aligned_human - ref
    ref_dir = np.gradient(ref, axis=0)
    ref_dir_norm = np.linalg.norm(ref_dir, axis=1, keepdims=True)
    ref_dir_norm[ref_dir_norm == 0] = 1e-8
    ref_unit = ref_dir / ref_dir_norm

    # perpendicular component = diff - (diff . ref_unit) ref_unit
    proj = np.sum(diffs * ref_unit, axis=1, keepdims=True) * ref_unit
    lateral = diffs - proj
    lateral_dev = np.linalg.norm(lateral, axis=1)

    return {
        "path_length_ratio": float(human_len / ref_len) if ref_len > 1e-8 else float("nan"),
        "mean_lateral_deviation": float(np.mean(lateral_dev)),
        "max_lateral_deviation": float(np.max(lateral_dev)),
    }
