import os
import glob
import numpy as np  # type: ignore #

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(SCRIPT_DIR, "..", "result")

npz_files = sorted(glob.glob(os.path.join(RESULT_DIR, "ground_truth_data_*.npz")))

if not npz_files:
    raise FileNotFoundError(
        f"No ground_truth_data_*.npz files found in {RESULT_DIR}. "
        "Run pendulum_ground_truth.py first."
    )

latest_file = npz_files[-1]
print(f"Loading: {latest_file}")

data = np.load(latest_file)

angle_log_noisy = data["angle_log_noisy"]
time_log = data["time_log"]
angle_log = data["angle_log"]
velocity_log = data["velocity_log"]
x_log = data["x_log"]
z_log = data["z_log"]
true_mass = data["true_mass"]
true_damping = data["true_damping"]
true_frictionloss = data["true_frictionloss"]
true_arm_length = data["true_arm_length"]
