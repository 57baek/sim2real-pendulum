# sim2real: Parking Lot (interesting, not on the critical path)

Started 2026-10-11. Things that came up while studying that are interesting but not needed for D1 to D3 (notebook understood, hand tip function, hand 3D simulator). Nothing here blocks the project. Review after the hand simulator works, or earlier if one becomes needed.

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
