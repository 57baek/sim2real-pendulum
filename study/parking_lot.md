# sim2real: Parking Lot (interesting, not on the critical path)

Started 2026-10-11. Last updated: 2026-10-12 09:46:25 EDT. Things that came up while studying that are interesting but not needed for D1 to D3 (notebook understood, hand tip function, hand 3D simulator). Nothing here blocks the project. Review after the hand simulator works, or earlier if one becomes needed.

## How it works

- When a lesson raises something interesting that the project does not need, Claude adds one row here and says "Parked: <name>" in one line. The lesson then continues.
- Status: PARKED (not studied), NEEDED (turned out to be on the critical path, pull into the plan), DONE (studied).
- Rows are never deleted. Studied items are marked DONE with the date.

## Parked items

| # | Concept | Came up at | Why it is interesting | Needed for the project? | Status |
|---|---|---|---|---|---|
| 1 | Pseudovector (axial vector): omega and torque flip differently from position under a mirror | right-hand rule (E3, E5) | Explains why the right-hand rule is a convention and the physics is not | No | PARKED |
| 2 | Cross product proofs: perpendicular to both inputs, length |a||b| sin(theta), BAC-CAB identity | cross product (E2, E4, E6) | The rigorous base under torque and the tensor | No (component formula is enough) | PARKED |
| 3 | Spectral theorem: why a symmetric inertia table always has principal axes | diaginertia (L5) | Links mechanics to linear algebra | No (the rod's axes are obvious by symmetry) | PARKED |
| 4 | Covariance link: I = trace(S) 1 - S, inertia as a second-moment table | inertia tensor (L4) | Same math as PCA and covariance in statistics | No | PARKED |
| 5 | Angular momentum L need not be parallel to omega; torque-free tumbling (Euler's equations) | T5 / tensor | Why a spinning book tumbles about its middle axis | No | PARKED |
| 6 | Torque about a new point P, couples, gravity torque r_cm x m g | T6 (E7) | Shows torque depends on the chosen point | No (Lagrange route does not use it) | PARKED |
| 7 | Newton-Euler derivation of the gimbal equations, as a cross-check of Euler-Lagrange | equations of motion (H7) | Two derivations of the same equations | Optional cross-check | PARKED |
| 8 | Quaternions and other ways to avoid gimbal lock | gimbal lock (L11) | How real robots and simulators store orientation | No for this rod | PARKED |
| 9 | Finite rotations do not add or commute, only rates add | omega arrow lessons | Why Rx then Ry differs from Ry then Rx | Partly (already used in the tip formula) | PARKED |
| 10 | Symplectic integrators and why RK4 slowly loses energy | energy check (Part 5) | Why some integrators keep energy for very long runs | No | PARKED |
| 11 | Transforming the tensor to a tilted frame, I' = R I R^T | tensor again (E8) | Needed for non-symmetric bodies | No for this rod | PARKED |
| 12 | Realistic rods and edge cases (non-uniform, off-center mass) | plan.md Section 8A | Real objects are rarely uniform thin rods | No (optional, after Chapter 3) | PARKED |
| 13 | plan.md Section 9A reading list (7 papers: Muratore review, Tobin, Peng, Chebotar, BayesSim, DROPO, Gautier and Khalil) and later Chapter 3 papers | project plan v4.9 | Maps the field and the closest cousins of the covariance-guided randomization idea | No (reading is not code) | PARKED |
| 14 | RankNet bridge paper and its possible chain (Bradley-Terry, preference-based RL, DROPO, GOODE) | plan.md Section 9 | Link to the professor's paper for the class report | No | PARKED |
| 15 | Verifying the literature citations (flag F7) | plan.md Section 10 | Several descriptions and venues are from memory | No | PARKED |
| 16 | Tier 1 MPC (hand-written, short horizon) | plan.md Section 8 | Another way to control the rod without learning | No (optional) | PARKED |
| 17 | Phase 2 extras of the study plan as a group (E1 to E8) | study_plan.md | Rigorous proofs behind torque, cross product, tensor | No | PARKED |
| 18 | Tier 4 imitation learning: behavior cloning and DAgger from the LQR or MPC teacher | plan.md Section 8 | Learn a controller from demonstrations instead of rewards | No (owner decision 2026-10-12) | PARKED |

## Change log

| Date and time | Change |
|---|---|
| 2026-10-11 | File created with rows 1 to 12 |
| 2026-10-12 | Rows 13 to 17 added (reading list, RankNet bridge, citation check, MPC, study plan Phase 2 extras) |
| 2026-10-12 09:46:25 EDT | Row 18 added (tier 4 imitation, parked by the owner). Timestamp and change log added. |
