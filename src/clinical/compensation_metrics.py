"""
==========================================================
Compensation feature extraction

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Quantifies the three canonical stroke-rehabilitation compensation
strategies used in the TRSP dataset (Zhi et al., 2018):
  - forward trunk lean
  - trunk rotation
  - shoulder elevation

Each function takes a TRSPTrial (see trsp_loader.py) and returns a
per-frame (n_frames,) array of the corresponding angle/displacement,
so features can be compared frame-by-frame against RL reference
trajectories or thresholded for real-time feedback.
==========================================================
"""

import numpy as np

from src.clinical.trsp_loader import TRSPTrial, joint_series


def forward_lean_angle(trial: TRSPTrial) -> np.ndarray:
    """
    Angle (degrees) of the SpineBase->Neck vector from vertical,
    projected onto the sagittal (forward-backward, i.e. y-z) plane.
    Larger values indicate more forward trunk lean.
    """

    base = joint_series(trial, "SpineBase")
    neck = joint_series(trial, "Neck")

    spine_vec = neck - base

    vertical = np.array([0.0, 1.0, 0.0])

    # angle between spine vector and vertical, using only y (up) and z (forward) components
    yz = spine_vec[:, [1, 2]]
    yz_norm = np.linalg.norm(yz, axis=1)
    yz_norm[yz_norm == 0] = 1e-8

    cos_angle = yz[:, 0] / yz_norm

    angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

    return angle


def trunk_rotation_angle(trial: TRSPTrial) -> np.ndarray:
    """
    Angle (degrees) of the ShoulderLeft->ShoulderRight vector relative
    to the fronto-parallel (x) axis, projected onto the transverse
    (x-z) plane. Larger absolute values indicate more trunk rotation.
    """

    sl = joint_series(trial, "ShoulderLeft")
    sr = joint_series(trial, "ShoulderRight")

    shoulder_vec = sr - sl

    xz = shoulder_vec[:, [0, 2]]
    xz_norm = np.linalg.norm(xz, axis=1)
    xz_norm[xz_norm == 0] = 1e-8

    angle = np.degrees(np.arctan2(xz[:, 1], xz[:, 0]))

    return angle


def shoulder_elevation(trial: TRSPTrial, side: str = "Right") -> np.ndarray:
    """
    Vertical (y) displacement of the shoulder joint relative to the
    SpineShoulder reference point. Larger values indicate more
    shoulder-elevation compensation.
    """

    shoulder = joint_series(trial, f"Shoulder{side}")
    spine_shoulder = joint_series(trial, "SpineShoulder")

    return shoulder[:, 1] - spine_shoulder[:, 1]


def compensation_feature_matrix(trial: TRSPTrial, side: str = "Right") -> np.ndarray:
    """
    Stack all three compensation features into a (n_frames, 3) matrix,
    suitable as input to the PCA/decoding pipeline in
    src/neural_analysis (analogous to hidden-layer activity in the
    companion RL study).
    """

    return np.stack([
        forward_lean_angle(trial),
        trunk_rotation_angle(trial),
        shoulder_elevation(trial, side=side),
    ], axis=1)
