# Scientific boundaries and preserved negative results

## Models and comparisons

- The reduced coupled-command surrogate and independent 27-state nonlinear scenario plant have different roles. Saved surrogate feasibility is not a plant-level robust safety certificate.
- Initial mean surface temperatures are matched while spatial patterns vary. Future wheel-resolved and continuously mean-projected thermal histories need not have identical means.
- The local 0.25-s slice holds body/thermal states. The 0.75-s dynamic experiment propagates the 27-state plant. Local state differences are zero by construction.
- Fig. 3 contact braking is `B = -sum(Fx)` with the actual contact baseline; authority hulls use incremental contact quantities relative to the saved zero-service baseline. A hull centroid is not an applied torque trajectory.
- F0 is a no-fade null control; F1/F2/F3 are scenario fade families. No physical identification of a target truck is supplied.
- Phase-I row scales are fixed and strictly positive within each matched pair. Limiting-label changes are separate from QP-active-label changes; the saved QP-active lists are empty.
- Deterministic marginal quantiles retain covarying scenario parameters and do not establish a causal effect of an individual stratum.

## Historical controller/theory results retained as limitations

The manuscript candidate dated 9 October 2026, discussion section, reports the following. They are stated here to preserve interpretation; their full controller/theory archives are not packaged or rerun by this repository.

| Historical finding | Interpretation |
|---|---|
| 224 diagnostic cases: 99.0796% joint residual coverage against required 100% | Failed coverage; protocol fixed after exposure to baseline results |
| 16 confirmation cases: 3 completed trajectories, 13 hard-QP stops, 98.7633% coverage | Failed coverage; not robust remainder validation |
| 96 full/no-reserve comparisons coincide; event-matched lead advantages zero | No demonstrated reserve-controller benefit |
| Alarm occupancy 72.30% / 100% | Preserved historical result |
| Serial MATLAB mean/P95 runtime 0.200 / 0.309 s vs 0.1-s cycle | Target timing not established |
| Coherent velocity amplification peak 1.794951 near 1.232223 rad/s | Nonamplification not established |
| Full 256-corner common-storage search numerically unresolved | Not proved feasible or infeasible |

The minimal package's `PASS` denotes file integrity, reproducibility of included frozen numerical readouts and the declared LP checks. It does not turn these historical failures into successes or validate a physical vehicle.

## Reference source excerpts

`hfVectorField.m` defines the explicit body/wheel/roll/contact and surface/core thermal vector field. `closureTrajectoryIntegrate.m` and `thermalAuthorityIntegrateLumped.m` preserve the original integration/projection implementations for inspection. The minimal numerical exports intentionally omit MATLAB function handles and configuration dependencies. These excerpts do not constitute an end-to-end MATLAB regeneration workflow.
