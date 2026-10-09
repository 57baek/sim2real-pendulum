# sim2real-pendulum

Learning physical AI by building a sim-to-real pipeline, starting from a simple pendulum. Study notes and small MuJoCo projects live here as I go.

## Setup

```
python=3.11

mamba install -c conda-forge ipykernel numpy matplotlib pillow mujoco scipy pytorch -y
```

## sim2real

Active work. See `sim2real/PLAN.MD` for the full plan.

- `ch1_modeling/ch1_modeling.ipynb` - MuJoCo model of a rod on a 2-axis gimbal with two torque motors. Simulates passive falls in several directions, checks growth rate and energy conservation, and saves plots, a GIF, and ground-truth data to `ch1_modeling/result/`. Run it from `ch1_modeling/`.

## study/tutorial

Chapter 0: first MuJoCo tutorial. Simulate a damped pendulum, generate noisy ground-truth data, then recover the unknown physical parameters from that data (an inverse problem).

- `notes/` - study notes on basic pendulum physics (PDF)
- `src/tutorial_pendulum.py` - defines the pendulum as a MuJoCo XML model (hinge joint, capsule arm, gravity, viscous + Coulomb friction), simulates a 5s swing released from 90°, adds sensor noise to the angle, and saves ground-truth data + plots + an animated GIF to `result/`
- `src/tutorial_pendulum_fetch.py` - loads the most recent `ground_truth_data_*.npz` from `result/` for downstream use (e.g. the inverse problem)
- `result/` - generated outputs (timestamped `.npz` data, angle/velocity plots, trajectory plot, swing animation)

Run (from `study/tutorial/`):
```
python src/tutorial_pendulum.py
```
