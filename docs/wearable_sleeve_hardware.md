# Wearable sleeve hardware: proposed architecture (v0.1 design draft)

Status: design phase, not yet built. This is a starting specification meant to be iterated on with a hardware collaborator/engineer — treat all part numbers and costs as placeholders to validate, not final BOM.

## 1. Sensing requirements (derived from Section 2.3/2.4 of the manuscript)

To reconstruct the same three compensation features already computed in `src/clinical/compensation_metrics.py` (forward lean, trunk rotation, shoulder elevation) without a Kinect camera, the minimum sensor set is:

| Feature | Requires angle/position of | Minimum sensors |
|---|---|---|
| Forward lean | Trunk pitch relative to vertical | 1 IMU on sternum/upper trunk |
| Trunk rotation | Trunk yaw relative to facing direction | Same trunk IMU (yaw axis) |
| Shoulder elevation | Shoulder height relative to trunk | 1 IMU on the affected upper arm, near the acromion |
| Reach trajectory (wrist path) | Forearm orientation + elbow angle | 1 IMU on the forearm, near the wrist |

**Minimum viable sensor set: 3 IMUs** (trunk, upper arm, forearm). A 4th IMU on the hand/glove is optional, useful only if grasp orientation becomes a target metric later.

## 2. Sensor selection

- **IMU**: 9-DOF (accelerometer + gyroscope + magnetometer) modules, e.g. BNO055 or ICM-20948 class parts — chosen for on-chip sensor fusion (quaternion output), which avoids needing a separate Kalman/Madgwick filter implementation on the microcontroller.
- **Sampling rate**: 100 Hz per IMU is sufficient for reach-speed movements (TRSP recordings run well under this bandwidth); 100 Hz also keeps the 3-sensor data rate low enough for a single low-power microcontroller and Bluetooth Low Energy (BLE) link.
- **Communication between sensors and hub**: wired I²C/SPI daisy chain along the sleeve (simpler, more robust than 3 independent wireless links) feeding a single microcontroller.
- **Microcontroller**: an ESP32-class board (built-in BLE + WiFi, enough compute for on-device quaternion-to-Euler conversion and the compensation-angle formulas already implemented in Python) or a Nordic nRF52-class board if BLE power budget is the priority over WiFi.
- **Actuation (motorized assist)**: a small geared DC or servo motor at the elbow/shoulder joint of the sleeve, driven only when a compensation threshold is crossed, providing corrective torque or haptic cueing rather than continuous assistance — matching the "flag deviations, don't replace the movement" design goal in the manuscript.
- **Power**: single rechargeable Li-Po cell (sized for ≥2 hours continuous use at 100 Hz), with a low-battery cutoff to avoid actuator misbehavior.

## 3. Data flow

```
[Trunk IMU] --I2C--\
[Upper-arm IMU] --I2C--+--> [MCU: quaternion fusion, angle extraction] --BLE--> [phone/laptop app]
[Forearm IMU] --I2C--/                                                              |
                                                                                     v
                                                                     [compare vs. RL reference
                                                                      trajectory, same formulas as
                                                                      src/clinical/compensation_metrics.py]
                                                                                     |
                                                                                     v
                                                                     [feedback: haptic buzz / sleeve
                                                                      motor / on-screen cue if a
                                                                      threshold is crossed]
```

On-device, the MCU only needs to convert each IMU's quaternion to the same trunk-pitch / trunk-yaw / shoulder-elevation angles already defined for the Kinect data, so the exact same threshold logic and RL-reference comparison can run on either data source with minimal code change (swap `src/clinical/trsp_loader.py` for a live BLE stream reader with the same output shape).

## 4. Open-hardware sourcing (low-cost goal)

- IMU breakout boards, ESP32 dev boards, and small geared motors are all available from open-hardware-friendly suppliers (Adafruit, SparkFun, generic ESP32 dev kits) at low per-unit cost, consistent with the "low-cost, open-spec" goal in the Introduction/Methodology.
- Enclosure/sleeve textile: 3D-printed sensor mounts + elastic compression sleeve fabric, so the whole BOM (sensors + MCU + motor + fabric) can realistically target a small fraction of the cost of proprietary robotic rehabilitation devices cited in the Introduction [@Mehrholz2015].
- Firmware and the on-device angle-extraction logic should be released open-source alongside this repository, mirroring the "pairing open-source control algorithms with low-cost, open-hardware designs" goal stated in the manuscript.

## 5. Validation plan (before any patient use)

1. Bench-test each IMU's angle output against the corresponding TRSP-derived angle definitions, using a rigid mannequin arm or a healthy volunteer performing the same `Rch_Fwr_Bck` / `Rch_Sd2Sd_Bck` tasks, to confirm the wearable's angle estimates agree with the Kinect-derived ground truth within an acceptable tolerance.
2. Only after (1) passes should any motorized/haptic feedback be enabled, and only under supervision — this is a research prototype, not a certified medical device.
