# sim2real: Project Plan (for Claude Code)

Status: v4.2, written 2026-10-09 12:21:07 EDT. Replaces plan v4.1 (kept in `archive/plan/PLAN_v4.1.MD`; v4 is in `archive/plan/PLAN_v4.MD`). Timestamps in this file use the real local date and time (`date "+%Y-%m-%d %H:%M:%S %Z"`). Older plans and logs are in `archive/plan/` and `sim2real_reference_archive.md` (read them only when a past decision must be revisited).

Labels used in this file:
- FOUNDATIONAL = a number or choice we make or measure. Not derivable.
- DERIVED = follows from other quantities or equations.
- VERIFIED = produced by running code and checked.
- MEMORY = recalled by the assistant, not checked. Verify before citing.

---

## 0. How Claude Code should work in this repo

Read this section first. These are the owner's standing rules.

1. **One piece at a time.** Do not generate scaffolds, packages, bulk files, or "full pipelines" unless asked. The owner wants to read and run one code piece, understand it, then move on.
2. **Follow the owner's code style.** The reference is `study/tutorial/src/tutorial_pendulum.py`: `# type: ignore` imports, `STEP n:` comment banners made of `─` lines, plain Python lists for logs, a `TIMESTAMP` in every output file name, separate figures with `fig.tight_layout()` and `fig.savefig(...)`, a GIF with a progress bar, `np.savez` with named arrays. No clever abstractions beyond what is needed.
3. **Explain purpose in comments.** For each step say what we have, what we want, what the step does, and why it is needed.
4. **Separate DERIVED from FOUNDATIONAL** in comments and explanations. Always include units (write liter as L, the number one as 1).
5. **Implement first, derive after** (owner's preference for this project). The loop per stage is:
   - A. implement with packages (MuJoCo etc.)
   - B. derive all the math and physics used, by hand, on paper or in a notes file
   - C. re-implement by hand with no predefined physics packages
   - D. compare A and C, then write the result up
6. **Never claim something is verified unless it was run.** State the numbers. If code was not run, say so.
7. **Ask before changing direction.** Any change to scope, system, or chapter order must be proposed first and logged in Section 12.
8. **No em dashes** in any output, file, or comment. Use a hyphen or a comma.
9. **Do not touch** `study/tutorial/` (Chapter 0, finished).
10. Results from notebooks are saved under the notebook's own folder in `result/`.

---

## 1. Goal and scope

**Goal:** balance an upright rod with motors, in simulation, using a learned controller, and understand every equation underneath it well enough to implement it by hand.

**Long-term direction:** physical AI, digital twins, synthetic-data training (NVIDIA Isaac Sim, Isaac Lab, Omniverse), eventually autonomous robot control.

**System (FOUNDATIONAL):** a rod standing on a 2-axis gimbal pivot with 2 torque motors. The rod can fall in any horizontal direction (360 degrees). Two perpendicular motor axes cover every direction: each axis pushes in two senses (+ and -), and any push direction is a sum of an x part and a y part.

**Out of scope for now:** real hardware. It comes only after the whole simulation pipeline, including Isaac training, works.

**Learning aim:** educational and professional-level. The owner must be able to derive and implement every piece by hand.

**Three chapters, tackled one at a time, same loop (A to D) in each:**
1. Mathematical modeling (class: MATH441)
2. Inverse problem (class: MATH440, name as the owner wrote it)
3. Machine learning (class: CSDS 440)

**Research question (from the owner's earlier plan):** does using the inverse-problem covariance (which parameters are well or poorly determined) to choose which parameters to randomize, and how widely, make RL training more sample-efficient and robust than random or uniform randomization?

**Scenario for Chapter 3:** real data is scarce, not absent. A hidden "true system" simulator plays the real world and gives only a small budget of N trajectories.

---

## 2. Current status

| Item | State |
|---|---|
| Chapter 0 (intro to MuJoCo and basic physics) | DONE, in `study/tutorial/` |
| Plan v4 and reference archive | this file, plus `sim2real_reference_archive.md` |
| Chapter 1, Stage 1.1 (MuJoCo gimbal rod, checks, plots, GIF) | DONE, notebook `sim2real/ch1_modeling/ch1_modeling.ipynb`. Audited 2026-10-09 12:20:02 EDT (v4.1): geometry, inertia, straightness, growth, energy checks all in the notebook. Owner should re-run it once in Jupyter to refresh saved outputs. |
| Chapter 1, Stage 1.2 onward | NOT STARTED |
| Chapters 2 and 3 | NOT STARTED |

**Next action:** Stage 1.2 (hand-derived kinematics). See Section 6.

---

## 3. Repo layout and conventions

Current tree:

```
sim2real-pendulum
├── README.md
├── sim2real
│   └── ch1_modeling
│       ├── ch1_modeling.ipynb      <- MuJoCo notebook (Stage 1.1)
│       └── result/                 <- created on first run
└── study
    └── tutorial                    <- Chapter 0, do not touch
        ├── notes/basic_physics.pdf
        ├── result/
        └── src/tutorial_pendulum.py, tutorial_pendulum_fetch.py
```

Conventions:
- Notebooks use `os.getcwd()` for the notebook folder (there is no `__file__` in a notebook). Print the save path on the first run and check it.
- Output names: `gimbal_<what>_<TIMESTAMP>.png|gif|npz`. Ground-truth data: `gimbal_ground_truth_data_<TIMESTAMP>.npz` with `time_log, q1_log, q2_log, q1_log_noisy, q2_log_noisy, w1_log, w2_log, x_log, y_log, z_log` and the true parameters.
- The directory design the owner liked earlier (configs, src package with a single `dynamics.py` source of truth, chapters, tests, data, results, docs) is NOT to be built yet. Add folders only when a chapter needs them.
- The CSDS 440 diary is a separate repo. Do not put it here.

---

## 4. System definition

### 4.1 Model structure (FOUNDATIONAL)

```
 world -> ring --(hinge jx, axis x)--> rod --(hinge jy, axis y)--> tip
```

- Rod points straight up (+z) when q1 = q2 = 0. This is the unstable equilibrium.
- `q1` = angle of hinge `jx` (about x). `q2` = angle of hinge `jy` (about y). Rotation is Rx(q1) then Ry(q2).
- The rod's inertia is given explicitly (`<inertial>`), not inferred from a capsule.
- The ring is a placeholder body of 1e-4 kg and 1e-8 kg*m^2, only because MuJoCo needs mass on every moving body.
- Two torque motors, gear 1 (input is the torque in N*m), clipped to +-3 N*m each.
- Integrator RK4, MuJoCo `flag energy="enable"` for energy readouts.

### 4.2 Parameters

| Symbol | Meaning | Value | Unit | Type |
|---|---|---|---|---|
| g | gravity | 9.81 | m/s^2 | foundational |
| L | rod length (pivot to tip) | 1.0 | m | foundational |
| m | rod mass | 1.0 | kg | foundational |
| dt | time step | 0.001 | s | foundational |
| T_max | torque limit per motor | 3.0 | N*m | foundational |
| c | joint viscous damping (main run) | 0.04 | N*m*s/rad | foundational |
| f | joint Coulomb friction (main run) | 0.02 | N*m | foundational |
| sigma_angle | angle sensor noise std | 0.01 | rad | foundational |
| I_com | rod inertia about its centre, across the rod, m*L^2/12 | 0.08333 | kg*m^2 | derived |
| I_pivot | same axis moved to the pivot, m*L^2/3 | 0.33333 | kg*m^2 | derived |
| omega_u | tilt growth rate at upright, sqrt(1.5 g / L) | 3.836 | 1/s | derived |
| alpha_hold | steepest tilt the motor can resist, arcsin(T_max / (m g L / 2)) | 37.7 | deg | derived (necessary, not sufficient) |
| I_zz | rod inertia about its own axis, m r^2 / 2 with r = 0.02 m | 2e-4 | kg*m^2 | foundational (was 1e-6, see flag F1) |

The two physics checks (growth, energy) run with c = 0 and f = 0 because the theory has neither.

### 4.3 Conventions (VERIFIED against MuJoCo)

Tip position for joint angles (q1, q2), DERIVED by composing Rx(q1) then Ry(q2) on the vector (0, 0, L):

```
 x =  L sin(q2)
 y = -L sin(q1) cos(q2)
 z =  L cos(q1) cos(q2)
```

- Positive q2 leans toward +x. Positive q1 leans toward -y.
- Lean by `tilt` toward compass direction `dir` (0 = +x, 90 = +y): `ux = sin(tilt) cos(dir)`, `uy = sin(tilt) sin(dir)`, `q2 = arcsin(ux)`, `q1 = arcsin(-uy / cos(q2))`. This cannot represent tilts above 90 degrees (arcsin), so a "120 degree" tilt is really 60.
- Angle from vertical: `arctan2(hypot(x, y), z)` (accurate for small and large angles).

---

## 5. Verified facts so far

| Fact | Result | How |
|---|---|---|
| Tip formula vs MuJoCo, 1000 random poses | worst error 4.4e-16 m | ran (in notebook, 2026-10-09) |
| MuJoCo mass matrix at upright | diagonal 0.3333 kg*m^2 = I_pivot | ran (in notebook, 2026-10-09) |
| Small-tilt growth vs alpha0 * cosh(omega_u t) | max relative error 0.37% | ran (in notebook, 2026-10-09) |
| Energy drift, no damping/friction/motor, 5 s | 6.5e-7 J with I_zz = 2e-4 (4.3e-7 J with 1e-6), scale m g L = 9.81 J | ran (in notebook, 2026-10-09) |
| PD balance hold limit (frictionless, Kp 15, Kd 3) | 37 deg held, 38 deg fell; predicted 37.7 deg | ran (earlier notebook) |
| Passive fall direction | falls the way it leans, in every direction | ran |
| Outbound 45 degree path straightness | azimuth spans 44.85 to 45.00 degrees with damping and friction on (0.001 degrees was a frictionless run) | ran (in notebook, 2026-10-09) |
| Gimbal lock pose, I_zz = 2e-4 | lean toward 0 deg for 5 s without early stop, and lean 10 deg for 20 s: finite, no `MUJOCO_LOG.TXT` | ran (scratch, 2026-10-09) |
| Hand RK4 vs MuJoCo on the 2D single-hinge case (earlier work) | max error ~1e-14 rad | ran (archive) |

---

## 6. Chapter 1: Mathematical modeling (MATH441)

Each stage runs A (implement with MuJoCo), B (derive), C (hand code), D (compare and write up).

| Stage | Topic | Content | MATH441 hook | State |
|---|---|---|---|---|
| 1.1 | MuJoCo model and checks | gimbal model, geometry, growth and energy checks, passive falls in all directions, plots, GIF | Ch1 | DONE |
| 1.2 | Kinematics by hand | rotation matrices Rx, Ry, the tip formula derived, check against saved MuJoCo data | Ch1 calculus | NEXT |
| 1.3 | Rigid-body inertia | inertia tensor of a thin rod, parallel-axis theorem, how I_pivot = m L^2 / 3 arises, inertia seen by each hinge as a function of q2 | linear algebra | |
| 1.4 | Energy | kinetic energy T(q, q_dot) and potential energy V(q) in the gimbal coordinates | Ch1 | |
| 1.5 | Euler-Lagrange | equations of motion M(q) q_ddot + C(q, q_dot) q_dot + g(q) = tau for two angles, hand RK4 simulator, compare with MuJoCo (frictionless first) | Ch1 ODEs, numerics | |
| 1.6 | Non-conservative terms | viscous damping, Coulomb friction (smooth tanh model vs MuJoCo constraint friction), motor torque and saturation | Ch1 | |
| 1.7 | Numerics | explicit Euler vs RK4 vs semi-implicit, energy drift, step-size study (1-DOF Euler energy factor 1 + omega^2 dt^2 is derived) | Ch1 | |
| 1.8 | Linearization at upright | Jacobian, eigenvalues (expect +-3.836 1/s per axis), controllability | Ch1 | |
| 1.9 | Hand-built LQR | Riccati equation by hand, balance in hand sim and MuJoCo, compare with the PD baseline | | |
| 1.10 | Nondimensionalization | timescale, dimensionless groups, which effects matter | **Ch4 (important)** | |
| 1.11 | Noise and sensors | process noise, encoder noise, quantization, delay | Ch5, Ch6 | |
| 1.12 | Chapter report | modeling decisions, validation, limits | | |

Unused MATH441 chapters (2, 3, 7, 9) have no natural fit yet. Do not force them.

**Exit criterion for Chapter 1:** a hand-coded 3D simulator matches MuJoCo within a stated tolerance on several trajectories, and hand-built LQR balances the rod in both.

---

## 7. Chapter 2: Inverse problem (MATH440)

| Stage | Topic |
|---|---|
| 2.1 | Forward map and data design: what is measured (angles, maybe torque), excitation (weak vs rich) |
| 2.2 | Heavy realistic noise models: Gaussian, colored, bias or drift, quantization, delay, dropouts (details to be discussed with the owner) |
| 2.3 | Least squares by hand: MLE view, Jacobian, Gauss-Newton and Levenberg-Marquardt, compare with scipy `least_squares` |
| 2.4 | Ill-posedness: SVD of the Jacobian, condition number, what "unidentifiable" means |
| 2.5 | Tikhonov regularization: MAP view, choosing lambda (L-curve, discrepancy principle, cross-validation) |
| 2.6 | Identifiability and covariance: Cov ~ sigma^2 (J^T J)^-1, Fisher information, parameter ranking |
| 2.7 | Research question: covariance-guided domain randomization vs random or heuristic randomization (the RL test itself runs in Chapter 3) |
| 2.8 | Chapter report |

Notes:
- **Mass is not identifiable from angle-only data** (DERIVED in the 2D case): scaling (m, c, f, T) by the same factor gives the same trajectory. Only ratios such as c/m, f/m, T/m are identifiable. Redo this analysis for the gimbal before fixing the parameter vector in Stage 2.1.
- Chapter 0's script listed mass as an unknown to fit. Use the ratio parameterization instead.

---

## 8. Chapter 3: Machine learning (CSDS 440)

Philosophy (owner): learn to train this system by every reasonable method, including with no Isaac and no synthetic data (physics only). Then add Isaac and synthetic data, under the assumption that real data is scarce.

| Tier | Method | Real data needed |
|---|---|---|
| 0 | Hand LQR (from Chapter 1) | none |
| 1 | MPC, hand-written, short horizon (optional) | none |
| 2 | Physics-only RL: PPO then SAC, package first then hand-coded | none |
| 3 | Physics-only RL with domain randomization (random vs covariance-guided ranges) | none |
| 4 | Imitation: behavior cloning and DAgger from the LQR or MPC teacher | none |
| 5 | System identification (Chapter 2), then RL | small N |
| 6 | Learned dynamics (model-based RL): NN world model on scarce data, optionally physics plus a learned residual | small N |
| 7 | Isaac Sim / Isaac Lab: massively parallel PPO, USD model, randomization | none or small N |
| 8 | Synthetic-data training: large randomized noisy datasets from Isaac, train a model or policy, fine-tune on scarce real data | small N |

Suggested order: 0, 2, 3, 4, 5, 6 first (no GPU), then 7 and 8. Tier 1 can be inserted anywhere.

**Comparison metrics (same for all tiers):** sample efficiency (simulation steps and real-data trajectories), success rate and settling time on the "true" system, robustness to parameter shift, noise, delay and pushes, failure modes, compute cost.

**CSDS 440 focus:** physics-based (tiers 2 to 5) vs data-based (tiers 6 and 8) vs hybrid (residual, fine-tuning). Caveat: Isaac Sim runs a physics engine (PhysX), so "synthetic data" means simulator-generated data that a model learns from, not physics-free data. Confirm this definition at Stage 3.6.

**Hardware:** the owner has a GPU PC that can run Isaac Sim and Isaac Lab. Claude Code cannot assume it can run them in its own environment. Write scripts, the owner runs them locally and sends back logs. Tiers 0 to 6 need no GPU.

---

## 9. Class reports

| Class | Report built from |
|---|---|
| MATH441 mathematical modeling | Chapter 1 (plus noise parts of Chapter 2) |
| MATH440 inverse problems | Chapter 2 |
| CSDS 440 machine learning | Chapter 3 and the research question |

Bridge paper from the owner's professor: RankNet (Burges 2005, MEMORY). It only needs to be related, not used directly. A possible chain (all MEMORY, verify before citing): RankNet -> Bradley-Terry -> preference-based RL (Christiano 2017) -> DROPO or Fickinger -> GOODE (Attia 2018). Decide how to connect it when Chapter 3 is close.

---

## 10. Open flags

| ID | Flag |
|---|---|
| F1 | **Gimbal lock at +-x leans (mitigated).** At q2 = +-90 degrees, hinge jx spins the rod about its own axis, so the mass matrix there depends on I_zz. With I_zz = 1e-6 kg*m^2 damping and friction became stiff (dt c / I = 40) and RK4 could go unstable (`Nan, Inf or huge value in QACC at DOF 0`, seen only in older notebook versions). I_zz is now 2e-4 kg*m^2 and the 0 degree lean runs through the pose without warnings. Passive-fall runs still stop just after horizontal for a clean top view. Re-check if damping, friction, or dt grow. |
| F2 | **Friction model mismatch.** MuJoCo `frictionloss` is a hard constraint. Our hand model will use smooth tanh friction. Expect small differences near zero velocity. Not a bug. |
| F3 | Mass unidentifiable from angle-only data (see Chapter 2 notes). |
| F4 | Capsule geometry infers inertia 2.9% above a thin rod (0.08574 vs 0.08333 kg*m^2 in the Chapter 0 model). Always set inertia explicitly. |
| F5 | The gimbal ring has a placeholder mass (1e-4 kg). The hand model ignores it. |
| F6 | The lean-to-angle formula cannot start the rod below horizontal. |
| F7 | All literature citations are MEMORY. Verify. |
| F8 | Class name for inverse problems is written MATH440 by the owner. Confirm if a formal name is needed for a report. |
| F9 | The PD controller from the earlier notebook is hand-tuned and is only a placeholder for LQR. |

---

## 11. Definition of done for any stage

- Code runs top to bottom from a restarted kernel.
- Printed checks are stated with numbers.
- Outputs saved with a TIMESTAMP.
- Derivation (stage B) written in a notes file the owner can read.
- Hand implementation (stage C) compared against MuJoCo (stage D) with a tolerance stated up front.
- Open flags updated.

---

## 12. Change log

| Date and time | Change |
|---|---|
| 2026-10 (earlier, time not recorded) | Fresh plan v3 from the owner's answers. Chapter 0 added. 3D confirmed as a 2-axis gimbal with 2 motors. Chapter 3 rewritten as a method ladder with scarce real data. |
| 2026-10-09 12:21:07 EDT | v4.2: timestamps now carry the real time. Previous plan: `archive/plan/PLAN_v4.1.MD`. |
| 2026-10-09 12:20:02 EDT | v4.1: audit of Stage 1.1. Tip-formula, mass-matrix, and straightness checks added to the notebook with printed numbers and asserts. I_zz raised 1e-6 to 2e-4 kg*m^2 (F1 mitigated, notebook re-run clean from scratch). Straightness fact reworded (friction on). Previous plan: `archive/plan/PLAN_v4.MD`. |
| 2026-10-09 (time not recorded) | v4: Stage 1.1 recorded as done with verified results. Added Claude Code working rules, repo conventions, parameter table, conventions, flags F1 to F9. Previous plans archived in `sim2real_reference_archive.md`. |

---

## 13. Immediate next step

**Stage 1.2: kinematics by hand.**
- A (already done): MuJoCo geometry check at 4e-16 m.
- B: derive Rx(q1), Ry(q2), the composition, and the tip formula, with the sign conventions in Section 4.3. Write it in a notes file in `sim2real/ch1_modeling/notes/`.
- C: hand-coded tip position function with no MuJoCo call, using only numpy.
- D: compare with the saved MuJoCo tip positions from `result/gimbal_ground_truth_data_<TIMESTAMP>.npz` and state the maximum error.

Propose the first code piece and wait for the owner before building anything further.