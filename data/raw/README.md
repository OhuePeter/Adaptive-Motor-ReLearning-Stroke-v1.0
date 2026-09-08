# Toronto Rehab Stroke Pose (TRSP) Dataset

Local copy extracted from `archive.zip` into `data_new/` (10 healthy subjects `H01`–`H10`, 9 post-stroke subjects `P01`–`P09`).

Cite: Dolatabadi et al. (2017); Zhi et al. (2018) — see `paper/references.bib`.

## Folder layout

```
data_new/<SUBJECT>/<TASK_CONDITION>/
    Joint_Positions.csv   # no header, 3 columns (x, y, z), rows stacked as 25 joints x N frames
    Labels.csv            # no header, 1 column, 1 row per frame (compensation label)
```

Row count check: `Joint_Positions.csv` rows = 25 x `Labels.csv` rows (25-joint Kinect-style skeleton per frame).

## Task condition codes

| Code | Meaning |
|---|---|
| `Rch_Fwr_Bck` | Reach forward-backward |
| `Rch_Sd2Sd_Bck` | Reach side-to-side, backward return |
| `_L` / `_R` | Left / right arm |
| `LnFwr` | Lean-forward compensation |
| `ShElev` | Shoulder-elevation compensation |
| `TrRot` | Trunk-rotation compensation |
| (no suffix) | Non-compensated / natural reach |

Subjects `H01`–`H10` are healthy controls asked to simulate each compensation; subjects `P01`–`P09` are post-stroke participants performing natural reaches.

## Usage in this project

Used as the empirical comparison set against RL-generated reference trajectories (see `paper/manuscript.md`, Methodology). Joint coordinates should be mapped to the same 2-D reach-plane convention as the RL environment before geometric comparison — see `docs/project_lineage.md`.

Data files are not tracked in git (large, subject to dataset license); confirm `.gitignore` excludes `data/raw/toronto_rehab_stroke_pose/` before committing.
