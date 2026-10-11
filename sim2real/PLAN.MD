# sim2real: Project Plan (for Claude Code)

Status: v4.4, written 2026-10-10 22:06:58 EDT. Replaces plan v4.3 (kept in `archive/plan/PLAN_v4.3.MD`; v4.2 is in `archive/plan/PLAN_v4.2.MD`; v4.1 is in `archive/plan/PLAN_v4.1.MD`; v4 is in `archive/plan/PLAN_v4.MD`). Timestamps in this file use the real local date and time (`date "+%Y-%m-%d %H:%M:%S %Z"`). Older plans and logs are in `archive/plan/` and `sim2real_reference_archive.md` (read them only when a past decision must be revisited).

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

**Future direction, NOT a chapter and NOT required (added in v4.3):** after everything above (including Isaac Sim and synthetic data), the owner may study realistic rods and edge cases, because a real object is rarely a uniform thin rod. See Section 8A. The project is complete without it.

**Research question (from the owner's earlier plan):** does using the inverse-problem covariance (which parameters are well or poorly determined) to choose which parameters to randomize, and how widely, make RL training more sample-efficient and robust than random or uniform randomization?

**Scenario for Chapter 3:** real data is scarce, not absent. A hidden "true system" simulator plays the real world and gives only a small budget of N trajectories.

---

## 2. Current status

| Item | State |
|---|---|
| Chapter 0 (intro to MuJoCo and basic physics) | DONE, in `study/tutorial/` |
| Plan v4 and reference archive | this file, plus `sim2real_reference_archive.md` |
| Chapter 1, Stage 1.1 (MuJoCo gimbal rod, checks, plots, GIF) | DONE, notebook `sim2real/ch1_modeling/ch1_modeling.ipynb`. Audited 2026-10-09 12:20:02 EDT (v4.1): geometry, inertia, straightness, growth, energy checks all in the notebook. Owner should re-run it once in Jupyter to refresh saved outputs. |
| Chapter 1, notebook walkthrough (owner reads the Stage 1.1 notebook part by part, before any hand math) | IN PROGRESS. Part 0 (imports, result folder) and Part 1A (constants) done. Part 1B (XML model) is next, then Part 2 (model checks), 3 (run_fall), 4 (main run and saving), 5 (extra runs and physics checks), 6 (plots), 7 (GIF). The derived constants are being taught one by one: moment of inertia about the center of mass and about the long axis (taught, with the diaginertia naming), the parallel-axis step and OMEGA_UNSTABLE (still to teach). |
| Chapter 1, Stage 1.2 onward | NOT STARTED |
| Chapters 2 and 3 | NOT STARTED |
| Future direction: realistic rods and edge cases (optional, not a chapter) | NOT STARTED, only after Chapter 3. See Section 8A. |
| Reading list (Section 9A) | NOT STARTED. Paper 1 is the Muratore et al. review. Reading needs no code. |
| Prerequisites for 3D rotation (torque, cross product, right-hand rule, inertia tensor) | IN PROGRESS, see "Promised explanations" in Section 6. The owner is relearning torque first. |

**Next action:** relearn torque in 3D (step 3 of the order in Section 6: 3D torque as three flat torques), then the parallel-axis theorem and `OMEGA_UNSTABLE`, then the notebook walkthrough from Part 1B. After that Stage 1.2 (hand-derived kinematics). See Section 6. In parallel, no code: read paper 1 of the reading list (Section 9A).

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
| r | rod radius (capsule size in the XML) | 0.02 | m | foundational |
| I_zz | rod inertia about its own long axis, m r^2 / 2 | 2e-4 | kg*m^2 | derived from m and r (the notebook still hard-codes 2e-4, see flag F10). Was 1e-6, see flag F1 |

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
| Thin slices of a uniform rod, 1.0 kg, 1.0 m: about the center across the rod 0.083333 kg*m^2, about the end 0.333333 kg*m^2, ratio 4.000 | matches m L^2 / 12 and m L^2 / 3 | ran (scratch script, 2026-10-10) |
| Solid cylinder about its long axis, m = 1 kg, r = 0.02 m, thin-ring sum | 2.000000e-04 kg*m^2; random-point sampling 2.0008e-04 | ran (scratch script, 2026-10-10) |
| Rod leaning along x: hinge jx effective inertia vs I_pivot cos^2 q2 + I_zz sin^2 q2 | entries matched the formula in the scratch check | ran (scratch, 2026-10-10). Re-run in the notebook when Stage 1.3 is done |
| Four mass layouts about the pivot (A uniform, B heavy tip, C heavy base, D lump off to one side), 1.0 kg, 1.0 m | A: d 0.500 m, I_pivot 0.3333, rate 3.836 1/s. B: 0.900, 0.8667, 3.192. C: 0.260, 0.0987, 5.084. D: d 0.500, I_pivot 0.3167, I_xz -0.0100, center of mass 0.020 m off to the side, balance lean 2.29 deg | computed from the formulas in a scratch script (hand arithmetic on the lumps), NOT compared with MuJoCo |
| Rectangular bar 0.04 m x 0.01 m x 1.0 m, 1.0 kg, 4 million random points vs table formulas | I_xx 8.3368e-02 vs 8.3342e-02, I_yy 8.3493e-02 vs 8.3467e-02, I_zz 1.4161e-04 vs 1.4167e-04; all within 0.05% | ran (scratch, 2026-10-10) |

---

## 6. Chapter 1: Mathematical modeling (MATH441)

Each stage runs A (implement with MuJoCo), B (derive), C (hand code), D (compare and write up).

| Stage | Topic | Content | MATH441 hook | State |
|---|---|---|---|---|
| 1.1 | MuJoCo model and checks | gimbal model, geometry, growth and energy checks, passive falls in all directions, plots, GIF | Ch1 | DONE |
| 1.2 | Kinematics by hand | rotation matrices Rx, Ry, the tip formula derived, check against saved MuJoCo data | Ch1 calculus | NEXT |
| 1.3 | Rigid-body inertia | inertia tensor of a thin rod (naming: I_ab = torque about axis a per unit angular acceleration about axis b), parallel-axis theorem, products of inertia (zero for our rod by mirror symmetry), how I_pivot = m L^2 / 3 arises, inertia seen by each hinge as a function of q2 (jx: I_pivot cos^2 q2 + I_zz sin^2 q2, jy: I_pivot) | linear algebra | |
| 1.4 | Energy | kinetic energy T(q, q_dot) and potential energy V(q) in the gimbal coordinates. T has a translational part (center of mass moving, mass times speed squared over 2) and a rotational part (angular velocity and the inertia table); the body angular velocity is (q1_dot cos q2, q2_dot, q1_dot sin q2) | Ch1 | |
| 1.5 | Euler-Lagrange | equations of motion M(q) q_ddot + C(q, q_dot) q_dot + g(q) = tau for two angles, hand RK4 simulator, compare with MuJoCo (frictionless first) | Ch1 ODEs, numerics | |
| 1.6 | Non-conservative terms | viscous damping, Coulomb friction (smooth tanh model vs MuJoCo constraint friction), motor torque and saturation | Ch1 | |
| 1.7 | Numerics | explicit Euler vs RK4 vs semi-implicit, energy drift, step-size study (1-DOF Euler energy factor 1 + omega^2 dt^2 is derived) | Ch1 | |
| 1.8 | Linearization at upright | Jacobian, eigenvalues (expect +-3.836 1/s per axis), controllability. Derive omega_u = sqrt(m g d / I_pivot) in general form (effective pendulum length I_pivot / (m d)), not only sqrt(1.5 g / L) | Ch1 | |
| 1.9 | Hand-built LQR | Riccati equation by hand, balance in hand sim and MuJoCo, compare with the PD baseline | | |
| 1.10 | Nondimensionalization | timescale, dimensionless groups, which effects matter | **Ch4 (important)** | |
| 1.11 | Noise and sensors | process noise, encoder noise, quantization, delay | Ch5, Ch6 | |
| 1.12 | Chapter report | modeling decisions, validation, limits | | |

Unused MATH441 chapters (2, 3, 7, 9) have no natural fit yet. Do not force them.

### Promised explanations (owner asked to cover all of these; tick them off here)

| Topic | Where it is taught | State |
|---|---|---|
| Moment of inertia from first principles (integral of r^2 dm), about the center of mass across the rod (m L^2/12) | notebook walkthrough, Part 1A | DONE (2026-10-10) |
| Moment of inertia about the long axis (m r^2 / 2) via thin rings, and its naming (I_zz = row z, column z of the 3 x 3 table; MuJoCo diaginertia = "Ixx Iyy Izz") | notebook walkthrough, Part 1A | DONE (2026-10-10) |
| Parallel-axis theorem, turning the center-of-mass value into the pivot value (0.0833 + 1.0 x 0.5^2 = 0.3333) | next teaching step, then Stage 1.3 by hand | TO DO |
| OMEGA_UNSTABLE = sqrt(1.5 g / L) and its general form sqrt(m g d / I_pivot) | next after the parallel-axis theorem (walkthrough), derived by hand in Stage 1.8 | TO DO |
| Products of inertia (off-diagonal entries), why they are 0 for our rod | concept taught in the inertia tensor lesson (2026-10-10); by hand in Stage 1.3 | CONCEPT DONE, BY HAND TO DO |
| Inertia each hinge feels as the rod leans (jx: I_pivot cos^2 q2 + I_zz sin^2 q2, jy: I_pivot); why this explains flag F1 | Stages 1.3 to 1.5 | TO DO |
| Kinetic energy including the translational mass part | Stage 1.4 | TO DO |
| Inertia tensor (the 3 x 3 table): definition from L = I omega, link to the covariance matrix (I = trace(S) 1 - S with S the mass-weighted second-moment table), principal axes, diaginertia | lesson 2026-10-10 | CONCEPT DONE, BY HAND TO DO in Stage 1.3 |
| Cross product: perpendicular, length |a||b| sin(theta) (area), component formula forced by the rules, anticommutative, not associative, triple products | lessons 2026-10-10 | TAUGHT (owner is relearning torque first, then returns to it) |
| Right-hand rule: handedness, determinant, why it is a convention, physics does not depend on the hand | lesson 2026-10-10 | TAUGHT (learning order puts it last) |
| Torque and the 3D torque arrow. Learning order: (1) 2D torque, (2) a spin as an arrow (axis, right hand picks the end), (3) 3D torque as three 2D torques (the cross product formula appears), (4) the cross product as a general tool, (5) v = omega x r, (6) right-hand rule in depth, (7) back to the inertia tensor | relearning, started 2026-10-10 | IN PROGRESS: what torque is (tau = F d = I alpha derived for a lever) and step 2 done, step 3 next |
| Remaining notebook walkthrough, Parts 1B to 7 | before Stage 1.2 | TO DO |
| Edge cases: a rod that is not conventional (future direction, optional) | Section 8A, after Chapter 3 | OPTIONAL, FUTURE |

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

After tier 8, an optional future direction exists (Section 8A): the same pipeline, but with objects that are not a uniform thin rod. It is not part of the three-chapter plan.

---

## 8A. Future direction (optional, not a chapter): realistic rods and edge cases

**Status:** optional study direction, not a required part of the plan. Do it only after Chapters 1 to 3 are finished, including Isaac Sim (tier 7) and synthetic data (tier 8), and only if the owner wants it. Nothing in Chapters 1 to 3 may wait for it.

**Why:** everything so far uses one idealised object: a uniform, thin, round rod, pivoting at its end, with the motors acting directly on the hinges. Real objects are not like that. The owner asked (2026-10-10) to keep these edge cases as the follow-up direction after everything else, because they are much closer to real life. Numbering is 8A (not 9) so that the references to Sections 9 to 13 elsewhere stay valid.

**What changes when the object is not a conventional rod** (the lists below are the lesson plan; each item is a stage):

| Topic (numbered 4.x for reference only) | Case | What changes | Honest status |
|---|---|---|---|
| 4.1 | Center of mass not in the middle (heavy tip, heavy base) | Center of mass height d and I_pivot change, so the tilt growth rate sqrt(m g d / I_pivot) changes. Computed: uniform 3.836 1/s, heavy tip 3.192, heavy base 5.084 (formula arithmetic only) | formulas computed, not checked in MuJoCo |
| 4.2 | Non-round cross section (flat bar) | The three diagonal inertias differ: I_xx = m (b^2 + L^2) / 12, I_yy = m (a^2 + L^2) / 12, I_zz = m (a^2 + b^2) / 12. Then the two hinges feel different inertias at the same lean | sampled check passed within 0.05% |
| 4.3 | Asymmetric mass (lump off to one side) | Products of inertia become non-zero (I_xz = -0.0100 kg*m^2 in the example), the mass matrix has off-diagonal terms, and the upright pose is no longer the balance point: the balance lean is arctan(x_com / d), 2.29 deg in the example | formula arithmetic only |
| 4.4 | Different pivot location | Parallel-axis theorem with a different distance: I_pivot = I_com + m d^2 with the new d | formula |
| 4.5 | Motor rotor inertia and gearbox | The motor rotor adds inertia seen by the joint. Through a gear ratio N it counts N^2 times (reflected inertia). In MuJoCo this is the `armature` joint attribute (MEMORY, verify in the MuJoCo docs before using). Also gearbox friction and backlash | MEMORY |
| 4.6 | Identifiability link | For small tilts the growth only measures m g d / I_pivot, so many (m, d, I_pivot) combinations look the same (same idea as flag F3). Connect this to the Chapter 2 covariance analysis | to be derived |
| 4.7 | Write-up and decision | Which of these effects matter enough to randomize in Isaac (domain randomization ranges), and which can be ignored | to decide |

**How MuJoCo would be asked to hold an asymmetric body (all MEMORY, verify before use):**
- The `<inertial>` element can take a full inertia (`fullinertia`) or a rotated frame instead of `diaginertia`. The center of mass position (`pos`) moves off the middle.
- Expectation, NOT yet checked: the straightness check of the outbound path (azimuth stays at the lean direction) will fail for an asymmetric body, because the body no longer falls straight along its lean. Do not treat that failure as a bug without checking.

**Loop for each stage:** A (MuJoCo with the changed XML), B (derive by hand), C (hand code), D (compare). Same rules as Section 0.

**Entry condition (if the owner chooses to do it):** Chapters 1 to 3 are done, including Isaac Sim (tier 7) and synthetic data (tier 8). Propose the first piece to the owner and wait before building.

---

## 9. Class reports

| Class | Report built from |
|---|---|
| MATH441 mathematical modeling | Chapter 1 (plus noise parts of Chapter 2) |
| MATH440 inverse problems | Chapter 2 |
| CSDS 440 machine learning | Chapter 3 and the research question |

Bridge paper from the owner's professor: RankNet (Burges 2005, MEMORY). It only needs to be related, not used directly. A possible chain (all MEMORY, verify before citing): RankNet -> Bradley-Terry -> preference-based RL (Christiano 2017) -> DROPO or Fickinger -> GOODE (Attia 2018). Decide how to connect it when Chapter 3 is close.

---

## 9A. Reading list (papers)

Added in v4.4 at the owner's request: which papers to read for this project and for professional practice, and in what order. Reading is not code, so the "one code piece at a time" rule does not apply, but read **one paper at a time**. The number 9A keeps the references to Sections 10 to 13 valid.

**Start with paper 1.** It is a review: it maps the whole field and gives a reading list. The owner's research question (choose randomization ranges from data instead of guessing them) is its "adaptive randomization" branch.

| # | Paper | Why read it | Plan link | Existence and venue |
|---|---|---|---|---|
| 1 | Muratore, Ramos, Turk, Yu, Gienger, Peters (2022), "Robot Learning From Randomized Simulations: A Review", Frontiers in Robotics and AI. https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2022.799893/full , arXiv 2111.00956 | the map of the field | everything | VERIFIED by search (2026-10-10). Contents: MEMORY |
| 2 | Tobin et al. (2017), "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World", IROS | the original idea: randomize the simulator so the real world looks like one more sample | Chapter 3, tier 3 | MEMORY, not searched |
| 3 | Peng et al. (2018), "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization", ICRA. arXiv 1710.06537 | randomizes dynamics (mass, friction, damping, latency), the same kind of parameters as Section 4.2 | Chapters 1 and 3 | Paper VERIFIED by search (arXiv listing). Venue ICRA: MEMORY |
| 4 | Chebotar et al. (2019), "Closing the Sim-to-Real Loop: Adapting Simulation Randomization with Real World Experience", ICRA (SimOpt). arXiv 1810.05687 | uses real data to update the randomization ranges | research question | Paper VERIFIED by search. Venue ICRA: MEMORY |
| 5 | Ramos, Possas, Fox (2019), "BayesSim: adaptive domain randomization via probabilistic inference for robotics simulators", RSS XV. https://roboticsproceedings.org/rss15/p29.html , arXiv 1906.01728 | infers a posterior over simulator parameters from real data: the closest published cousin of the covariance-guided idea | research question, Chapter 2 | VERIFIED by search. Contents: MEMORY |
| 6 | Tiboni et al. (2022), "DROPO: Sim-to-Real Transfer with Offline Domain Randomization", arXiv 2201.08434 (journal version in Robotics and Autonomous Systems, 2023, as the search listing suggested) | works from a small fixed real dataset: the same scarce-data scenario as Section 1 | Chapter 3 | VERIFIED by search. Journal venue: MEMORY |
| 7 | Gautier and Khalil (1990), on the minimum set of identifiable inertial parameters of serial robots (title as I remember it: "Direct calculation of minimum set of inertial parameters of serial robots", IEEE Transactions on Robotics and Automation) | the classical result behind "mass alone is not identifiable, only combinations are" | Chapter 2, flag F3 | NOT CONFIRMED: the search did not return it. MEMORY. Verify the title, venue and year before citing |

Later, for Chapter 3 (all MEMORY): PPO (Schulman 2017), the Isaac Gym paper (Makoviychuk 2021), Rudin 2021.

**The RankNet bridge paper** (Section 9) is separate. Read it after paper 6, once it is clear which question it is being connected to.

**How to read:**
- Three passes (Keshav, "How to Read a Paper", MEMORY): (1) title, abstract, introduction, headings, figures, conclusion; (2) the method, skipping proofs; (3) the details, only for papers the project builds on.
- For each paper write three lines: the problem, the trick, what it assumes. One short notes file per paper. Decide the folder when the first one is written (Section 3: do not create folders in advance).
- Keep one running question: "does this say how wide to randomize each parameter, and why?"
- Do not implement a paper unless the owner asks.

---

## 10. Open flags

| ID | Flag |
|---|---|
| F1 | **Gimbal lock at +-x leans (mitigated).** At q2 = +-90 degrees, hinge jx spins the rod about its own axis, so the mass matrix there depends on I_zz. With I_zz = 1e-6 kg*m^2 damping and friction became stiff (dt c / I = 40) and RK4 could go unstable (`Nan, Inf or huge value in QACC at DOF 0`, seen only in older notebook versions). I_zz is now 2e-4 kg*m^2 and the 0 degree lean runs through the pose without warnings. Passive-fall runs still stop just after horizontal for a clean top view. Re-check if damping, friction, or dt grow. At q2 = 90 degrees the effective inertia of hinge jx equals I_zz (from I_pivot cos^2 q2 + I_zz sin^2 q2), which is why a tiny I_zz made it stiff. |
| F2 | **Friction model mismatch.** MuJoCo `frictionloss` is a hard constraint. Our hand model will use smooth tanh friction. Expect small differences near zero velocity. Not a bug. |
| F3 | Mass unidentifiable from angle-only data (see Chapter 2 notes). |
| F4 | Capsule geometry infers inertia 2.9% above a thin rod (0.08574 vs 0.08333 kg*m^2 in the Chapter 0 model). Always set inertia explicitly. |
| F5 | The gimbal ring has a placeholder mass (1e-4 kg). The hand model ignores it. |
| F6 | The lean-to-angle formula cannot start the rod below horizontal. |
| F7 | **Literature citations.** Papers 1, 3, 4, 5 and 6 of Section 9A were confirmed to exist by web search on 2026-10-10 (title, link and, for papers 1 and 5, venue). The descriptions of what they contain, the venues the search did not show, paper 2, paper 7 (Gautier and Khalil) and the RankNet chain are MEMORY. Verify before citing. |
| F8 | Class name for inverse problems is written MATH440 by the owner. Confirm if a formal name is needed for a report. |
| F9 | The PD controller from the earlier notebook is hand-tuned and is only a placeholder for LQR. |
| F10 | **Pending notebook change (agreed with the owner, not yet applied).** Replace the hard-coded `I_ZZ = 2e-4` by `ROD_RADIUS = 0.02` and `I_ZZ = ROD_MASS * ROD_RADIUS**2 / 2`, use `{ROD_RADIUS}` for the capsule `size` in the XML, then re-run the gimbal lock check (F1) and the other checks. The value stays 2e-4 kg*m^2, so results should not change. Apply it when the owner's walkthrough reaches Part 1A again, or earlier if asked. |
| F11 | **Edge cases are not covered yet.** Until the future direction in Section 8A is studied, every result in this repo holds only for a uniform, thin, round rod pivoting at its end. Do not generalise claims (growth rate, identifiability, controller limits) to other objects. |

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
| 2026-10-10 22:06:58 EDT | v4.4: added Section 9A (reading list: the Muratore review first, then Tobin, Peng, Chebotar, BayesSim, DROPO, Gautier and Khalil), flag F7 reworded, "Promised explanations" updated (inertia tensor, cross product, right-hand rule, torque in 3D with the learning order), next action and Section 13 updated. Also fixes a mismatch: the repo copy of v4.3 still said "Four chapters" with Section 8A as Chapter 4, although the owner decided it is an optional future direction, not a chapter. v4.4 has the three-chapter wording. Previous plan: `archive/plan/PLAN_v4.3.MD`. |
| 2026-10-10 16:08:27 EDT | v4.3: added Section 8A, an OPTIONAL future direction (realistic rods and edge cases) after Chapter 3 including Isaac Sim; the project stays a three-chapter plan. Added the "Promised explanations" list (Section 6), the notebook walkthrough status (Section 2), parameter r and I_zz formula (4.2), new verified facts with honest labels (Section 5), stage 1.3, 1.4, 1.8 content, flags F10 and F11, flag F1 note. Flat-bar check stated as "within 0.05%" (an earlier message said 0.03%, which was slightly too tight for I_zz). Previous plan: `archive/plan/PLAN_v4.2.MD`. |
| 2026-10 (earlier, time not recorded) | Fresh plan v3 from the owner's answers. Chapter 0 added. 3D confirmed as a 2-axis gimbal with 2 motors. Chapter 3 rewritten as a method ladder with scarce real data. |
| 2026-10-09 12:21:07 EDT | v4.2: timestamps now carry the real time. Previous plan: `archive/plan/PLAN_v4.1.MD`. |
| 2026-10-09 12:20:02 EDT | v4.1: audit of Stage 1.1. Tip-formula, mass-matrix, and straightness checks added to the notebook with printed numbers and asserts. I_zz raised 1e-6 to 2e-4 kg*m^2 (F1 mitigated, notebook re-run clean from scratch). Straightness fact reworded (friction on). Previous plan: `archive/plan/PLAN_v4.MD`. |
| 2026-10-09 (time not recorded) | v4: Stage 1.1 recorded as done with verified results. Added Claude Code working rules, repo conventions, parameter table, conventions, flags F1 to F9. Previous plans archived in `sim2real_reference_archive.md`. |

---

## 13. Immediate next step

**First: finish relearning torque in 3D** (step 3 of the order in Section 6, then the parallel-axis theorem and `OMEGA_UNSTABLE`). In parallel, no code: read paper 1 of Section 9A.

**Then: finish the notebook walkthrough** (owner's request). Teach the parallel-axis theorem and then `OMEGA_UNSTABLE`, then Part 1B (XML model) onward, one part at a time, no hand math or hand code before the owner understands the notebook. Apply the pending notebook change F10 when appropriate. Cover the other items in "Promised explanations" (Section 6) when their stages arrive.

**Then Stage 1.2: kinematics by hand.**
- A (already done): MuJoCo geometry check at 4e-16 m.
- B: derive Rx(q1), Ry(q2), the composition, and the tip formula, with the sign conventions in Section 4.3. Write it in a notes file in `sim2real/ch1_modeling/notes/`.
- C: hand-coded tip position function with no MuJoCo call, using only numpy.
- D: compare with the saved MuJoCo tip positions from `result/gimbal_ground_truth_data_<TIMESTAMP>.npz` and state the maximum error.

Propose the first code piece and wait for the owner before building anything further.