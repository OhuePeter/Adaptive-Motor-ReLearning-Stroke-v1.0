# Adaptive Motor Re-Learning: A Wearable Sensor Framework for Upper-Limb Stroke Rehabilitation

**Peter Ohue¹, Gunnar Blohm¹,²**

¹Centre for Neuroscience Studies, Queen's University, Kingston, ON, Canada
²Department of Biomedical and Molecular Sciences, Queen's University, Kingston, ON, Canada

*Draft: Phase 1 (Abstract / Introduction / Methodology). Results and Discussion to follow in later phases per author's iterative writeup process.*

---

## Abstract

*[To be completed once Results are finalized. Target ~200 words summarizing motivation, approach (RL reference trajectories + TRSP comparison + wearable sleeve concept), and key contribution.]*

---

## Introduction

Stroke, which is caused by the disruption of blood flow to the brain, affects more than 13 million people worldwide, kills more than 5 million annually, and is a major cause of disability [@Lu2012; @Kuriakose2020]. Motor deficits are one major neurological consequence of stroke, leading to a loss of independence and lower quality of life [@Lucchetti2025]. The physical impairments associated with stroke survivors need to be properly diagnosed, including changes in physical function of the affected limb, and the recommendation of appropriate remediation [@Gowland1993; @Mehrholz2015].

Shoulder-arm kinematics and muscular synergies involve at least 30 daily-life tasks, and hand postural synergies play a significant role in grasp force [@Hu2018; @Averta2018; @Saudabayev2018]. Linking forearm muscle activity and hand kinematics is essential for developing prosthetics and 3D modelling [@JarqueBou2019].

In general, compensation strategies for stroke survivors involve using new pathways, strong joints, and muscles, which can be at least ineffective [@Dolatabadi2017]. Existing rehabilitation devices are usually abandoned by users after delivery: abandonment is driven by poor fit between the device and the user's actual needs, insufficient user involvement in device selection, and lack of ongoing support once the device is in the home [@Sugawara2018]. Robotic and electromechanical devices carry the same risk, and their cost and clinic-based delivery model make sustained home use harder [@Mehrholz2015]. To address this challenge, we argue that an upper-limb rehabilitation device should be low-cost and open-hardware, so it can reach the home and the community clinic rather than only the specialized centre, and it should be adaptive, so it can flag emerging compensation in real time rather than depend only on intermittent clinical supervision.

The use of these devices needs to be supervised so that survivors do not recruit unaffected muscles and joints, which often leads to undesirable outcomes [@Zhi2018]. To understand these compensations, previous studies have simulated three types of compensation with healthy participants. These compensations include lean forward, trunk rotation, and shoulder elevation compensations [@Zhi2018; @Dolatabadi2017]. However, when post-stroke survivors are given homework-based rehabilitation programs, new and undesirable compensation paths risk being developed, making unlearning and relearning necessary [@Lin2019]. Rehabilitation programs should include task-specific training to induce plasticity and motor recovery. Individualized strategies have been useful in identifying relevant therapeutic goals and maximizing the future gain [@Takeuchi2013].

In this study, our overarching goal is to develop a user-friendly rehabilitation program for upper limb post-stroke management. We intend to provide a detailed diagnosis of undesirable compensation strategies used by post-stroke patients, comparing the standard trajectories set by artificial neural networks with the trajectories of both healthy and suffering patients. Using our framework, we want to show parallels that describe the internal representation in biological neurons during recovery [@Ohue2026]. This builds on our earlier work on accessible computational-neuroscience tools and training [@Chinagorom2025; @OhuePythonUnpub]. In addition, we seek to develop an adaptive motor relearning program using a neuroinspired wearable assistive device for upper-limb stroke rehabilitation. By pairing our open-source control algorithms with low-cost, open-hardware designs, our goal is to build accessible, adaptive wearable devices that help stroke survivors relearn natural movement.

---

## Methodology

We developed an open-source Proximal Policy Optimization (PPO) model, a reinforcement-learning control algorithm, to simulate how human arms adapt and navigate obstacles under unexpected physical disruptions [@Schulman2017]. This work is currently undergoing internal review for publication [@Ohue2026].

### Project vision

1. An open-access RL motor-control framework (PPO agent) modeling sensorimotor adaptation, obstacle avoidance, and unlearning/relearning dynamics during stroke recovery.
2. A low-cost, open-spec motorized arm sleeve designed for home recovery and community clinics, as an open-source alternative to expensive proprietary devices.
3. Extending our open-source AI models to lower-limb assistive devices to reduce device abandonment and support natural gait dynamics.

### RL reference trajectories

The RL controller is a PPO actor-critic agent trained in a 2-D point-mass reaching environment under Newtonian dynamics. Its state $\mathbf{s}_t = (x_t, y_t, \dot{x}_t, \dot{y}_t)$ evolves under

$$
\dot{\mathbf{s}}_t = f(\mathbf{s}_t, \mathbf{a}_t) = \begin{bmatrix} \dot{x}_t \\ \dot{y}_t \\ \tfrac{1}{m}\left(F_x(\mathbf{a}_t) + F_x^{\text{pert}}(t)\right) \\ \tfrac{1}{m}\left(F_y(\mathbf{a}_t) + F_y^{\text{pert}}(t)\right) \end{bmatrix},
$$

where $\mathbf{a}_t$ is the policy's continuous control action, $m$ is the point-mass, and $F^{\text{pert}}(t)$ is a graded lateral force impulse applied during a fixed perturbation window. Policy and value networks are two-hidden-layer (256-unit) feedforward networks, trained with the clipped PPO surrogate objective

$$
L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right], \qquad r_t(\theta) = \frac{\pi_\theta(\mathbf{a}_t\mid \mathbf{s}_t)}{\pi_{\theta_{\text{old}}}(\mathbf{a}_t\mid \mathbf{s}_t)}.
$$

We treat the trained policy's rollouts under each perturbation condition (P0 control; L1–L3, R1–R3 graded lateral perturbations) as reference trajectories: task-optimal movement paths, unconstrained by anatomy, against which human reach geometry can be compared for compensation.

### Human reach-kinematics data

We use the Toronto Rehab Stroke Pose (TRSP) dataset [@Dolatabadi2017; @Zhi2018]. It contains Kinect-derived 3-D joint-position time series (25-joint skeleton) for:

- 10 healthy participants (H01–H10), each performing standardized forward/backward and side-to-side reaches under a natural condition and under three simulated compensations: forward trunk lean (`LnFwr`), shoulder elevation (`ShElev`), and trunk rotation (`TrRot`), left and right (`_L`/`_R`).
- 9 post-stroke participants (P01–P09) performing the same reach tasks without an instructed compensation strategy.

Each trial directory contains `Joint_Positions.csv` (25 joints x 3 coordinates, stacked frame by frame) and `Labels.csv` (one label per frame). The file schema is documented in `data/raw/README.md`.

### Trajectory alignment and compensation quantification

Human wrist trajectories are projected onto their own 2-D reach plane by PCA, resampled to a common time base, and rigidly aligned (translation + uniform scale) to the matching RL reference trajectory. We report a path-length ratio and the mean/max lateral deviation between the two. Three compensation features are computed per frame directly from the joint data: forward lean angle, trunk rotation angle, and shoulder elevation, following the compensation categories used to build the TRSP dataset [@Zhi2018]. This pipeline is implemented in `src/clinical/` (`trsp_loader.py`, `compensation_metrics.py`, `trajectory_alignment.py`) and runs end-to-end via `scripts/compare_rl_vs_trsp.py`. The RL reference is currently a placeholder straight-line path; it will be replaced with real rollouts exported from `src/evaluation/`.

### Wearable sensor framework

We propose a motorized arm sleeve with three inertial measurement units (trunk, upper arm, forearm) to estimate the same three compensation features outside the lab, in real time. Sensor angles are compared continuously against the RL reference trajectory for the matching reach task; a deviation beyond a clinician-set tolerance triggers feedback. This extends the real-time visual-feedback approach shown to reduce compensatory motion in home-based exercise [@Lin2019] to a model-based, condition-specific reference rather than a single fixed target. The proposed sensor set, microcontroller choice, and validation plan are detailed in `docs/wearable_sleeve_hardware.md`.

---

## Results

*[Phase 2: to be added.]*

## Discussion

*[Phase 2: to be added.]*

## Acknowledgements

This work was supported in part by the Connected Minds Program, Canada First Research Excellence Fund, Grant No. CFREF-2022-00010.

## References

See `paper/references.bib`.
