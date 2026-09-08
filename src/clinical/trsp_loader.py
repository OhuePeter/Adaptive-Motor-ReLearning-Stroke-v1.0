"""
==========================================================
Toronto Rehab Stroke Pose (TRSP) data loader

Authors:
Peter Ohue
Gunnar Blohm

Description
-----------
Loads Joint_Positions.csv / Labels.csv trial pairs from the TRSP
dataset into (frames, joints, xyz) arrays, using the standard
Kinect v2 25-joint skeleton order used by Dolatabadi et al. (2017)
and Zhi et al. (2018).
==========================================================
"""

from pathlib import Path
from typing import NamedTuple

import numpy as np

# Standard Kinect v2 25-joint order (index -> name)
KINECT_V2_JOINTS = [
    "SpineBase", "SpineMid", "Neck", "Head",
    "ShoulderLeft", "ElbowLeft", "WristLeft", "HandLeft",
    "ShoulderRight", "ElbowRight", "WristRight", "HandRight",
    "HipLeft", "KneeLeft", "AnkleLeft", "FootLeft",
    "HipRight", "KneeRight", "AnkleRight", "FootRight",
    "SpineShoulder", "HandTipLeft", "ThumbLeft", "HandTipRight", "ThumbRight",
]

N_JOINTS = len(KINECT_V2_JOINTS)

JOINT_INDEX = {name: i for i, name in enumerate(KINECT_V2_JOINTS)}


class TRSPTrial(NamedTuple):
    subject: str
    task: str
    positions: np.ndarray   # (n_frames, 25, 3)
    labels: np.ndarray      # (n_frames,)


def load_trial(dataset_root: Path, subject: str, task: str) -> TRSPTrial:
    """
    Load one (subject, task) trial from the extracted TRSP dataset.

    dataset_root should point at .../toronto_rehab_stroke_pose/data_new
    """

    trial_dir = Path(dataset_root) / subject / task

    positions_path = trial_dir / "Joint_Positions.csv"
    labels_path = trial_dir / "Labels.csv"

    raw = np.loadtxt(positions_path, delimiter=",")

    if raw.shape[0] % N_JOINTS != 0:
        raise ValueError(
            f"{positions_path}: {raw.shape[0]} rows is not a multiple of "
            f"{N_JOINTS} joints"
        )

    n_frames = raw.shape[0] // N_JOINTS

    positions = raw.reshape(n_frames, N_JOINTS, 3)

    labels = np.loadtxt(labels_path, delimiter=",").reshape(-1)

    if labels.shape[0] != n_frames:
        raise ValueError(
            f"{labels_path}: {labels.shape[0]} labels != {n_frames} frames"
        )

    return TRSPTrial(subject=subject, task=task, positions=positions, labels=labels)


def joint_series(trial: TRSPTrial, joint_name: str) -> np.ndarray:
    """Return the (n_frames, 3) xyz series for a named joint."""

    return trial.positions[:, JOINT_INDEX[joint_name], :]


def list_subjects(dataset_root: Path) -> list:

    return sorted(p.name for p in Path(dataset_root).iterdir() if p.is_dir())


def list_tasks(dataset_root: Path, subject: str) -> list:

    return sorted(p.name for p in (Path(dataset_root) / subject).iterdir() if p.is_dir())
