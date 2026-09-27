# sim2real-pendulum

Learning physical AI by building a sim-to-real pipeline, starting from a simple pendulum. Study notes and small MuJoCo projects live here as I go.

## Setup

```
python=3.11

mamba install -c conda-forge ipykernel numpy matplotlib pillow mujoco scipy pytorch -y
```

## basic_pendulum

First MuJoCo tutorial: simulate a damped pendulum, generate noisy ground-truth data, then recover the unknown physical parameters from that data (an inverse problem).

- `notes/` — study notes on pendulum physics (PDF)
- `src/pendulum.py` — defines the pendulum as a MuJoCo XML model (hinge joint, capsule arm, gravity, viscous + Coulomb friction), simulates a 5s swing released from 90°, adds sensor noise to the angle, and saves ground-truth data + plots + an animated GIF to `result/`
- `src/pendulum_data_fetch.py` — loads the most recent `ground_truth_data_*.npz` from `result/` for downstream use (e.g. the inverse problem)
- `result/` — generated outputs (timestamped `.npz` data, angle/velocity plots, trajectory plot, swing animation)

Run:
```
python src/pendulum.py
```
