"""
==========================================================
Figure 1

Upper-Limb Reaching Schematic

Author:
Peter Ohue

Description
-----------
Publication-quality schematic of the upper-limb reaching chain
(trunk, shoulder, elbow, wrist) with the two compensation angles
(forward trunk lean, elbow/reach angle) used throughout
src/clinical/compensation_metrics.py and the manuscript Methodology.

Generated programmatically (matplotlib) rather than hand-traced in
Inkscape, so the figure stays reproducible and diffable; see
docs/schematic_workflow.md for the manual Inkscape alternative if a
hand-drawn anatomical style is preferred instead.
==========================================================
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle


class UpperLimbSchematic:
    """
    Publication-quality upper-limb reaching schematic for Figure 1.
    """

    def __init__(self):

        self.output_dir = Path("paper/figures")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Poster colour palette (docs/schematic_workflow.md Step 5)
        self.DEEP_BLUE = "#00355f"
        self.TEAL = "#2a9d8f"
        self.CORAL = "#e76f51"
        self.GOLD = "#f0c040"
        self.BLACK = "#222222"

    def draw(self):

        plt.rcParams["font.family"] = "DejaVu Sans"

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.set_xlim(-1.5, 4.0)
        ax.set_ylim(-0.5, 6.0)
        ax.set_aspect("equal")
        ax.axis("off")

        # --------------------------------------------------
        # Joint positions (spine base -> shoulder -> elbow -> wrist)
        # --------------------------------------------------

        spine_base = np.array([0.0, 0.0])
        shoulder = np.array([0.0, 3.5])
        elbow = np.array([1.6, 2.6])
        wrist = np.array([2.9, 4.2])

        # --------------------------------------------------
        # Vertical reference (for the trunk lean angle)
        # --------------------------------------------------

        ax.plot(
            [spine_base[0], spine_base[0]],
            [spine_base[1], shoulder[1] + 0.6],
            linestyle="--",
            linewidth=1.2,
            color="#999999",
            zorder=1,
        )

        # --------------------------------------------------
        # Limb segments
        # --------------------------------------------------

        ax.plot(*zip(spine_base, shoulder), linewidth=4, color=self.DEEP_BLUE, solid_capstyle="round", zorder=2, label="Trunk")
        ax.plot(*zip(shoulder, elbow), linewidth=4, color=self.TEAL, solid_capstyle="round", zorder=2, label="Upper arm")
        ax.plot(*zip(elbow, wrist), linewidth=4, color=self.CORAL, solid_capstyle="round", zorder=2, label="Forearm")

        # --------------------------------------------------
        # Joint markers
        # --------------------------------------------------

        for point in (spine_base, shoulder, elbow, wrist):
            ax.add_patch(Circle(point, radius=0.08, facecolor=self.GOLD, edgecolor=self.BLACK, linewidth=1.2, zorder=3))

        # --------------------------------------------------
        # Trunk lean angle (vertical reference vs. trunk segment)
        # --------------------------------------------------

        trunk_vec = shoulder - spine_base
        lean_deg = np.degrees(np.arctan2(trunk_vec[0], trunk_vec[1]))

        ax.add_patch(Arc(
            spine_base, 1.4, 1.4,
            angle=0, theta1=90 - max(lean_deg, 0.1), theta2=90,
            color=self.BLACK, linewidth=1.4, zorder=2,
        ))
        ax.annotate(r"$\theta_{lean}$", spine_base + np.array([0.55, 0.75]), fontsize=11)

        # --------------------------------------------------
        # Elbow (reach) angle between upper arm and forearm
        # --------------------------------------------------

        upper_arm_vec = shoulder - elbow
        forearm_vec = wrist - elbow

        angle_upper = np.degrees(np.arctan2(upper_arm_vec[1], upper_arm_vec[0]))
        angle_forearm = np.degrees(np.arctan2(forearm_vec[1], forearm_vec[0]))

        ax.add_patch(Arc(
            elbow, 1.0, 1.0,
            angle=0, theta1=min(angle_upper, angle_forearm), theta2=max(angle_upper, angle_forearm),
            color=self.BLACK, linewidth=1.4, zorder=2,
        ))
        ax.annotate(r"$\theta_{elbow}$", elbow + np.array([0.35, 0.15]), fontsize=11)

        # --------------------------------------------------
        # Joint labels
        # --------------------------------------------------

        ax.annotate("Spine base", spine_base + np.array([-1.15, -0.05]), fontsize=10)
        ax.annotate("Shoulder", shoulder + np.array([-1.15, 0.05]), fontsize=10)
        ax.annotate("Elbow", elbow + np.array([0.15, -0.35]), fontsize=10)
        ax.annotate("Wrist", wrist + np.array([0.15, 0.15]), fontsize=10)

        ax.legend(loc="lower right", frameon=False, fontsize=9)

        fig.tight_layout()

        svg_path = self.output_dir / "fig1_schematic.svg"
        png_path = self.output_dir / "fig1_schematic.png"

        fig.savefig(svg_path)
        fig.savefig(png_path, dpi=600)

        plt.close(fig)

        return svg_path, png_path
