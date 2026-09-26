import mujoco # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

# ─────────────────────────────────────────────
# STEP 1: Define the pendulum as a MuJoCo XML model
#
# This XML describes the STRUCTURE of the system (a hinge joint, an arm, gravity). 
# The structure is FOUNDATIONAL, you are choosing it, MuJoCo does not derive it for you.
#
# mass = 1.0 kg
# arm length = 0.5 m
# position = "x y z" initial anchor point position
# axis = "0 1 0" points along the Y-AXIS
# damping = 0.1 (N*m*s/rad, resistance propotional to velocity not position)
# damping_torque (N*m) = damping_coefficient (N*m*s/rad) × angular_velocity (rad/s) -> τ = c × ω

# ─────────────────────────────────────────────

xml = """
<mujoco>    
  <option gravity="0 0 -9.81" timestep="0.001"/>
  <worldbody>
    <body name="pendulum" pos="0 0 1">
      <joint name="hinge" type="hinge" axis="0 1 0" damping="0.1" frictionloss="0.03"/>
      <geom name="arm" type="capsule" fromto="0 0 0 0 0 -0.5" size="0.02" mass="1.0"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)

# ─────────────────────────────────────────────
# STEP 2: Set initial condition and run the simulation
#
# Release the pendulum from 30 degrees (converted to radians, MuJoCo works in radians).
# This initial angle is FOUNDATIONAL, a choice you made for this experiment, not something derived.
# ─────────────────────────────────────────────

initial_angle_deg = 30.0
initial_angle_rad = np.deg2rad(initial_angle_deg)

data.qpos[0] = initial_angle_rad   # set starting angle
data.qvel[0] = 0.0                 # start at rest

n_steps = 3000  # 3000 * 0.001s timestep = 3 seconds of simulation
time_log = []
angle_log = []
velocity_log = []

for step in range(n_steps):
    mujoco.mj_step(model, data)     # DERIVED: MuJoCo solves the equations of motion internally.
    time_log.append(step * model.opt.timestep)
    angle_log.append(data.qpos[0])
    velocity_log.append(data.qvel[0])

# ─────────────────────────────────────────────
# STEP 3: Plot the result, sanity check
# ─────────────────────────────────────────────

fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

axes[0].plot(time_log, np.rad2deg(angle_log))
axes[0].set_ylabel("Angle (degrees)")
axes[0].set_title("Pendulum swing, released from 30 degrees")
axes[0].grid(True)

axes[1].plot(time_log, velocity_log)
axes[1].set_ylabel("Angular velocity (rad/s)")
axes[1].set_xlabel("Time (s)")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("pendulum_test.png")
plt.show()

print(f"Simulation complete. Final angle: {np.rad2deg(angle_log[-1]):.2f} degrees")