# sim2real: Study Plan (Chapter 1 only)

Written 2026-10-11, revised the same day (v2). A separate, short plan for learning. It does not replace `plan.md` (the project plan); `plan.md` Section 6 points here.

Labels: FOUNDATIONAL = a given or chosen input (not derivable). DERIVED = follows from other equations.

---

## The goal in one sentence

Read and fully understand the Stage 1.1 MuJoCo notebook line by line, filling gaps live. Then study the extra concepts (cross product, right-hand rule, T5, T6, the full tensor). Then build the same gimbal rod system by hand and match MuJoCo.

## How lessons run

- One short lesson per message. Each opens with an AIM box, then the definition, then what we have, what we want, step by step from first principles.
- Math is typeset (real symbols), units always written (liter as L, the number one as 1).
- Every lesson separates DERIVED from FOUNDATIONAL.
- Full names of quantities (moment of inertia about the center of mass, not I_COM).
- No skim pass: reading starts at Part 0, because a skim would not mean anything yet.

---

## Guardrails (so prerequisites do not eat the project)

### Deliverables (what "done" means)

| ID | Deliverable | Proof |
|---|---|---|
| D1 | Notebook understood line by line | the Phase 1 close test (diagram, tip formula derivation, flow) |
| D2 | Hand-coded tip function matches the saved MuJoCo data | max error printed, below a tolerance stated up front |
| D3 | Hand-coded 3D simulator matches MuJoCo trajectories | overlaid plots, tolerance stated up front |

Small extra win: the hand-coded growth curve alpha0 cosh(Omega t) compared with MuJoCo, right after lesson L3.

### Labels

Every lesson is labeled **ON-PATH** (D1 to D3 cannot be done without it) or **OFF-PATH** (understanding only). ON-PATH: L1 to L11, H1 to H10. OFF-PATH: E1 to E8 (T5, cross product proofs, right-hand rule proofs, T6, the general tensor with BAC-CAB). Off-path does not mean worthless, it means the project does not stop without it.

### Rules

1. No new prerequisite is added without a label. Claude says "OFF-PATH" before teaching an off-path lesson.
2. A mini-deliverable follows each live lesson where possible: after L3 the hand growth check, after L8 the hand tip function against the saved data (this is D2, inside Phase 1).
3. Tripwire: 5 lessons in a row without a printed number or a plot. Claude flags it and suggests running code instead of learning more.
4. Off-path budget: one OFF-PATH lesson is allowed after each finished deliverable, not before it.
5. Re-planning is capped: the plan changes only when a fact changed, not for polish.
6. Interesting but unneeded ideas go to `parking_lot.md` instead of being studied now.

### Execution order

Phase 1 (D1, D2), then Phase 3 (D3), then Phase 2 (extras). The phase numbers are kept so other files stay valid. If a Phase 3 step turns out to need one Phase 2 lesson (for example BAC-CAB for the tensor), only that lesson is pulled in just in time.

---

## PHASE 1: Read the notebook line by line, fill gaps live

Goal: explain every line, redraw the flow, explain how a MuJoCo system is set up, and know the physics or math behind each line. One part per session; the owner reads first, then asks.

### Method

For every line ask three questions:

1. What does it do? (code behavior)
2. What physical quantity is it, with units?
3. Where does its value or formula come from? FOUNDATIONAL (chosen or measured) or DERIVED (from which equation)?

A line is **closed** only when all three are answered. Status marks: OK (understood why), WHAT (understood what, not why), UNKNOWN.

Gap rule:

- **Cheap gap** (about 10 minutes, or one short self-contained lesson using only what the owner has): taught live, at the line.
- **Expensive gap** (needs other new ideas): one row in the gap ledger (line, what is missing, where it closes), move on, return when it is taught.

Ledger (a table in the owner's notes, filled during the reading):

| Part and line | Status | Missing prerequisite | Closes at |
|---|---|---|---|
| (example) Part 5, energy check | WHAT | body angular velocity, kinetic energy | Phase 3 H4, H6 |

### The parts and the live lessons (L1 to L11)

| Part | Content | Live lessons at the line |
|---|---|---|
| 0 | imports, result folder, timestamp | none |
| 1A | constants: g, L, m, r, dt, T_max, c, f (foundational); I_COM (already taught); I_ZZ; OMEGA_UNSTABLE | **L1** I_zz by rings (redo) and its naming (I_ab = torque about axis a per unit angular acceleration about axis b; row a, column b of the 3 x 3 table). **L2** parallel axis theorem, I = I_cm + m d^2, proved (0.0833 + 1.0 x 0.5^2 = 0.3333). **L3** OMEGA_UNSTABLE: gravity torque about the pivot, small angle, theta'' = Omega^2 theta, cosh solution, Omega = sqrt(m g d / I_pivot) = sqrt(1.5 g / L) = 3.836 1/s |
| 1B | XML model: world, nested bodies, ring, hinges jx and jy, inertial, diaginertia, motors, damping, frictionloss, RK4, energy flag | **L4** inertia tensor: L = I omega built from the component formula (entries, symmetry, covariance link I = trace(S) 1 - S), using v = omega x r and the cross product formula the owner already has. **L5** diaginertia and principal axes: why "Ixx Iyy Izz" is enough for the rod, products of inertia are 0 by mirror symmetry; `inertial` is about the center of mass and MuJoCo applies the parallel-axis theorem itself. **L6** damping and Coulomb friction as torques (tau = -c q', tau = -f sign(q')), motor gear and ctrlrange clipping, why the placeholder ring needs mass. RK4 and the energy flag: what only |
| 2 | model checks: tip formula, mass matrix, straightness | **L7** rotation matrices Rx(q1), Ry(q2) (from trig). **L8** composition and the tip formula (x = L sin q2, y = -L sin q1 cos q2, z = L cos q1 cos q2). Mass matrix at upright = I_pivot (uses L2, L5). Straightness: ledger |
| 3 | run_fall | **L9** the arcsin conversion from a lean to joint angles (inverse of the tip formula) and degrees of freedom (qpos, qvel). `mj_step` vs `mj_forward`: what only |
| 4 | main run and saving | **L10** Gaussian sensor noise (two sentences) |
| 5 | extra runs: directions, growth (cosh), energy | **L11** gimbal lock: at q2 = +-90 degrees the rod lies along x, hinge jx spins it about its own long axis, so the inertia jx feels is I_zz; why I_zz = 1e-6 was a problem (flag F1) and 2e-4 is stable; why runs stop after horizontal. Growth check closes with L3. arctan2 and hypot: two sentences. Energy check: ledger |
| 6 | plots | none |
| 7 | GIF | none |

Left in the ledger on purpose (each needs body angular velocity or the equations of motion):

- energy check (kinetic energy including rotation): Phase 3 H4, H6
- straightness check (why the fall stays on the lean line): H7
- mass matrix at a general pose, hinge inertias I_pivot cos^2 q2 + I_zz sin^2 q2: H4, H5
- RK4 and numerical drift: H9

Apply pending notebook change F10 (compute I_zz from m and r) at the end of this phase.

Exit (close test): without looking at the notebook, the owner writes (1) the system diagram (ring, jx, rod, jy, motors), (2) the tip formula with its derivation, (3) the flow: build model, check, run, log, plot, and (4) the ledger has only Phase 3 items left.

---

## PHASE 2: Extra concepts (OFF-PATH, runs after Phase 3 exits; see Guardrails)

Goal: the full, rigorous version of the math the owner wants to cover, with all proofs. Runs after the hand simulator works (D3), except that single lessons are pulled in earlier if a Phase 3 step needs one. One short lesson per message, in dependency order.

| Lesson | Topic | Needs |
|---|---|---|
| E1 | T5 recap: dL/dt = tau_ext, internal torques cancel, tau_z = I alpha for any rigid body about a fixed axis. Owner writes it into the notes | torque lessons T1 to T4 |
| E2 | C1, C2: where a x b comes from (the torque formula), components forced by the rules | E1 |
| E3 | R1, R2: why a handedness convention exists, why x cross y = +z (determinant sign) | E2 |
| E4 | C3, C4, C5: anticommutative, linear, r x r = 0; perpendicular to both inputs; length |a||b| sin(theta), proved | E2 |
| E5 | R3, R4, R5: rotation-sense rule for the omega arrow, consistency of v = omega x r, pseudovector (mirror) | E3, E4 |
| E6 | C6: triple products and BAC-CAB, a x (b x c) = b (a . c) - c (a . b), proved | E4 |
| E7 | T6 (full length): torque about a new point P (tau_P = tau_O - r_P x F_total), couples, gravity torque r_cm x m g | E4 |
| E8 | Inertia tensor again with the BAC-CAB proof, and I' = R I R^T | E6, L4, L7 |

Exit: the owner can prove each cross product property and the right-hand rule claims, and has T5 in the notes.

---

## PHASE 3: Build the same system by hand (physics and math)

Goal: write the equations of motion of the gimbal rod from first principles, simulate them with hand-written code (numpy only), and match the saved MuJoCo trajectories. Each step is: derive, hand-code, compare with MuJoCo.

| Step | Topic | What is learned | Check against MuJoCo |
|---|---|---|---|
| H1 | One hinge, one angle | torque, I, theta'' = (m g d / I) sin theta, linearize, cosh, energy; hand RK4 | the 2D single-hinge case (earlier result: 1e-14 rad) |
| H2 | Hand-coded kinematics (derivation in L7, L8) | tip function with numpy only | tip position vs saved data, 1000 poses |
| H3 | Gap closing from Phase 2 as needed | revisit ledger rows that need E1 to E8 | ledger rows |
| H4 | Angular velocity of the rod from the gimbal angles | body angular velocity (q1' cos q2, q2', q1' sin q2), derived with the cross product and rotation matrices | optional numeric check |
| H5 | Rigid-body dynamics for the gimbal | hinge inertias, mass matrix at several poses (uses E8) | mass matrix at several poses |
| H6 | Energy | kinetic energy (translation m v^2 / 2 plus (1/2) omega^T I omega), potential energy m g z_cm | energy readout of the notebook |
| H7 | Equations of motion | Euler-Lagrange for two angles: M(q) q'' + C(q, q') q' + g(q) = tau (frictionless first); optional Newton-Euler cross-check using E1 and E7 | mass matrix, accelerations, straightness |
| H8 | Non-conservative terms in the simulator | Coulomb friction smooth tanh model vs MuJoCo constraint friction, motor saturation | trajectories with damping and friction on |
| H9 | Hand simulator | hand RK4 (and explicit Euler for contrast), energy drift, step size | full trajectories vs the saved .npz, tolerance stated up front |
| H10 | Linearization at upright | Jacobian, eigenvalues (expect +-3.836 1/s per axis), general form sqrt(m g d / I_pivot) | growth check of the notebook |

Exit: a hand-coded 3D simulator (no MuJoCo call) matches MuJoCo within the stated tolerance on several trajectories.

---

## Parking lot

Interesting concepts that are not needed for the project are logged in `parking_lot.md` (same folder) instead of being studied now. Claude adds a row and says "Parked: <name>" in one line, then the lesson continues. The list is reviewed after the hand simulator works (Phase 3 exit), or earlier if an item turns out to be needed.

## Not in this plan (later, only if wanted)

LQR, nondimensionalization, noise and sensors, the chapter report, and Chapters 2 and 3. They stay in `plan.md` (Stages 1.9 to 1.12).

## Status

| Item | State |
|---|---|
| Torque lessons T1 to T5, omega arrow, alpha arrow, torque arrow, 3D torque as three flat torques | taught in chat; owner's notes cover through the 3D torque formula |
| Phase 1 (notebook line by line) | NEXT: Part 0, then Part 1A with L1 to L3 |
| Phase 3 (build by hand) | after Phase 1 |
| Phase 2 (extra concepts) | after Phase 3 (D3), pull-in only if needed |
