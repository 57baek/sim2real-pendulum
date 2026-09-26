import os
import mujoco                   # type: ignore
import numpy as np              # type: ignore
import matplotlib.pyplot as plt # type: ignore
from matplotlib.animation import FuncAnimation, PillowWriter #type:ignore
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(SCRIPT_DIR, "..", "result")
os.makedirs(RESULT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# SINGLE SOURCE OF TRUTH: every physical parameter, defined ONCE, with units labeled.
# Both the XML below AND any hand-derived formula (I = (1/3)mL², etc.) must reference these variables, never a separately typed number.
# ─────────────────────────────────────────────

GRAVITY = 9.81           # m/s^2, foundational (measured constant)
TIMESTEP = 0.001         # s, foundational (numerical choice)
ARM_LENGTH = 0.5         # m, foundational (your choice for this experiment)
ARM_RADIUS = 0.02        # m, foundational (capsule thickness, cosmetic only, see earlier discussion)
ARM_MASS = 1.0           # kg, foundational, ALSO one of your three unknowns for the inverse problem
DAMPING = 0.1            # N*m*s/rad, foundational, unknown #2
FRICTIONLOSS = 0.03      # N*m, foundational, unknown #3


# ─────────────────────────────────────────────
# STEP 1: Define the pendulum as a MuJoCo XML model
#
# This XML describes the STRUCTURE of the system (a hinge joint, an arm, gravity). 
# The structure is FOUNDATIONAL, you are choosing it, MuJoCo does not derive it for you.
#
# mass = 1.0 kg
# arm length = 0.5 m
# position = "x y z" - initial anchor point position
# axis = "0 1 0" - points along the Y-AXIS
# damping = viscous friction (N*`m*s/rad)
# damping_torque (N*m) = damping_coefficient [N*m*s/rad] × angular_velocity [rad/s] -> τ = c × ω
# frictionloss = coulomb friction (τ_frictionloss [N·m] = -frictionloss [N·m] × sign(ω) [dimensionless])
# fromto = "0 0 0 0 0 -0.5" 3 starting and 3 ending points - defines a line segment from one 3D point to another: starting right at the body's own anchor point (0,0,0) and ending 0.5 meters straight DOWN (negative z: 0,0,-0.5 (L:arm length))
# size = 0.02 m - radius of the tube itself (how thick the rod is)
# mass = 1.0 kg - the mass of the tube
# ─────────────────────────────────────────────

xml = f"""
<mujoco>
    <option gravity="0 0 -{GRAVITY}" timestep="{TIMESTEP}"/>
    <worldbody>
        <body name="pendulum" pos="0 0 1">
        <joint name="hinge" type="hinge" axis="0 1 0" damping="{DAMPING}" frictionloss="{FRICTIONLOSS}"/>
        <geom name="arm" type="capsule" fromto="0 0 0 0 0 -{ARM_LENGTH}" size="{ARM_RADIUS}" mass="{ARM_MASS}"/>
        </body>
    </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml) # blueprint
data = mujoco.MjData(model)                 # object

# ─────────────────────────────────────────────
# STEP 2: Set initial condition and run the simulation
#
# Release the pendulum from 90 degrees (converted to radians, MuJoCo works in radians).
# This initial angle is FOUNDATIONAL, a choice you made for this experiment, not something derived.
# ─────────────────────────────────────────────

INITIAL_ANGLE_DEG = 90.0                            # 90°
INITIAL_ANGLE_RAD = np.deg2rad(INITIAL_ANGLE_DEG)   # 1.57 rad

data.qpos[0] = INITIAL_ANGLE_RAD    # set starting angle - 1.57 rad starting angle
data.qvel[0] = 0.0                  # start at rest - zero angular velocity

N_STEPS = 5000     # 5000 * 0.001s TIMESTEP = 5 seconds of simulation

time_log = []
angle_log = []
velocity_log = []
x_log = []
z_log = []

for step in range(N_STEPS):
    mujoco.mj_step(model, data)     # advance the simulation by the TIMESTEP
    time_log.append(step * model.opt.timestep) # model.opt.timestep = TIMESTEP
    x_log.append(ARM_LENGTH * np.sin(data.qpos[0])) 
    z_log.append(-ARM_LENGTH * np.cos(data.qpos[0]))
    angle_log.append(data.qpos[0])
    velocity_log.append(data.qvel[0])

# ─────────────────────────────────────────────
# STEP 3: Plot the results, sanity check
#
# Two SEPARATE figures: one for angle/velocity over time, one for the tip's actual x-z trajectory.
# Both filenames include a timestamp so repeated runs don't silently overwrite each other.
# ─────────────────────────────────────────────

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ─────────────────────────────────────────────
# FIGURE 1: angle and angular velocity over time
# ─────────────────────────────────────────────

fig1, axes1 = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

axes1[0].plot(time_log, np.rad2deg(angle_log))
axes1[0].set_ylabel("Angle (degrees)")
axes1[0].set_title(f"Pendulum swing, released from {INITIAL_ANGLE_DEG} degrees")
axes1[0].grid(True)

axes1[1].plot(time_log, velocity_log)
axes1[1].set_ylabel("Angular velocity (rad/s)")
axes1[1].set_xlabel("Time (s)")
axes1[1].grid(True)

fig1.tight_layout()
fig1.savefig(os.path.join(RESULT_DIR, f"pendulum_angle_velocity_{timestamp}.png"))

# ─────────────────────────────────────────────
# FIGURE 2: tip trajectory in x-z space
# ─────────────────────────────────────────────

fig2, ax2 = plt.subplots(figsize=(6, 6))

ax2.plot(x_log, z_log)
ax2.set_xlabel("x (m)")
ax2.set_ylabel("z (m)")
ax2.set_title("Pendulum tip trajectory")
ax2.axis("equal")
ax2.grid(True)

fig2.tight_layout()
fig2.savefig(os.path.join(RESULT_DIR, f"pendulum_trajectory_{timestamp}.png"))

# ─────────────────────────────────────────────
# STEP 4: Build an animated GIF of the pendulum swinging
#
# Only keep every Nth frame, so the GIF isn't 3000 frames long and slow to render.
# ─────────────────────────────────────────────

# fps = number_of_frames / total_duration = (N_STEPS / FRAME_SKIP) / (N_STEPS × TIMESTEP) = 1 / (FRAME_SKIP × TIMESTEP)
# count how many indices survived the FRAME_SKIP filtering, then divide by the total real duration
# each frame that we selected should maintain at least 
FRAME_SKIP = 50                                         # Only keeping every 50th step
frame_indices = range(0, N_STEPS, FRAME_SKIP)           # 0, 50, 100, ..., 4950 (N_STEP=5000) -> 100 indices kept
total_duration = N_STEPS * model.opt.timestep           # N_STEPS * TIMESTEP = 5000 * 0.001 = 5 sec
real_time_per_frame = FRAME_SKIP * model.opt.timestep   # 50 * 0.001 = 0.05 sec
matched_fps = 1 / real_time_per_frame                   # 1 / 0.05 = 20 frames per sec -> need to display 20 frames every real second to match the real simulation duration.

fig3, (ax3, ax_bar) = plt.subplots(
    2, 1, figsize=(5, 6), gridspec_kw={"height_ratios": [13, 1]}
)

ax3.set_xlim(-ARM_LENGTH * 1.2, ARM_LENGTH * 1.2) # 1.2 adds a 20% margin on every side
ax3.set_ylim(-ARM_LENGTH * 1.2, ARM_LENGTH * 1.2)
ax3.set_aspect("equal")
ax3.grid(True)
ax3.set_title("Pendulum swing animation")

rod_line, = ax3.plot([], [], "o-", linewidth=2, markersize=8)

ax_bar.set_xlim(0, total_duration)
ax_bar.set_ylim(0, 1)
ax_bar.set_yticks([])
ax_bar.set_xlabel("Time (s)")

progress_fill = ax_bar.barh(0.5, 0, height=1.0, color="steelblue")[0]
time_text = ax_bar.text(
    total_duration / 2, 0.5, "",
    ha="center", va="center", color="white", fontsize=10
)

def update(frame_index):
    x_tip = x_log[frame_index]
    z_tip = z_log[frame_index]
    rod_line.set_data([0, x_tip], [0, z_tip])

    current_time = time_log[frame_index]
    progress_fill.set_width(current_time)
    time_text.set_text(f"{current_time:.2f}s / {total_duration:.2f}s")

    return rod_line, progress_fill, time_text

animation = FuncAnimation(fig3, update, frames=frame_indices, interval=30, blit=True)

animation.save(
    os.path.join(RESULT_DIR, f"pendulum_swing_{timestamp}.gif"),
    writer=PillowWriter(fps=matched_fps),
)

plt.show()