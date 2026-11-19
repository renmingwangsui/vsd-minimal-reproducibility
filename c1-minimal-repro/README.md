# C1 finite saved-history minimax demonstration

**Public-safe method demonstration; synthetic data only.**

This small package demonstrates the finite saved-history minimax identity used in the W49/S01 C1 analysis. It is separate from the paper's controlled C1 reviewer archive.

## Run

Python 3.10+; standard library only:

```bash
python scripts/minimax_saved_history.py data/synthetic_histories.csv --output output/minimax_summary.csv
```

Input columns: `descriptor_class,history_id,output,node,time_s,value`.

For a finite descriptor class C of saved histories h_i in R^K:

`inf_p max_i ||h_i-p||_infinity = 0.5 * max_{i,j} ||h_i-h_j||_infinity`.

The equality is for unrestricted predictions over the finite saved-history vector. For causal, physical, dynamically constrained or learned predictors, the half-diameter remains a lower bound; attainability is not asserted.

## Scope limitation

The included CSV is synthetic. This package does **not** reproduce the paper's 864 matched groups, 3,456 histories, 13919/14191 diagonal witness, reported yaw-rate/sideslip values, or R8.4–R8.7 force/moment results.

The exact C1 reviewer archive and its file-level rights/external reviewer access were recorded as pending. Accordingly, this public-safe package excludes exact C1 response arrays, MAT files, unpublished source/configuration, manuscript text/PDF and third-party records. It demonstrates the calculation only; it does not resolve external access to the exact numerical evidence. A separate rights-holder-approved reviewer-access arrangement is still required.

## Rights

No new licence grant is made for these new files by this notice. The parent repository's existing rights register explicitly says that newly added files do not automatically inherit its existing code/data grants. Obtain rights-holder approval before reuse or redistribution.
