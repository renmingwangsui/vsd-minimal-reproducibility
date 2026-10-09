# VSD minimal reproducibility package

Frozen numerical evidence for **Wheel-Resolved Thermal Heterogeneity and Coupled Braking-Yaw Authority of Heavy-Duty Vehicles on Curved Downgrades**, submission candidate dated 9 October 2026.

This package reproduces the six main-paper figures from selected saved numerical records, recomputes summary statistics from the frozen comparison tables, and independently solves the phase-I linear programmes for all 72 saved surrogate snapshots. It does not regenerate the complete simulation archive. No manuscript, third-party paper, account credential or AI conversation log is required.

## Run

Use Python 3.12 (tested with 3.12.14). From the repository directory:

```sh
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell, or `source .venv/bin/activate` on Linux/macOS. Then:

```sh
python -m pip install -r requirements.txt
python reproduce.py
```

The script resolves all data paths relative to its own location. It uses the noninteractive Matplotlib backend and requires neither MATLAB nor a commercial optimisation licence. A successful run prints `"status": "PASS"` and writes:

| Output | Contents |
|---|---|
| `output/figures/` | Six figures, each in PDF, SVG and PNG |
| `output/tables/` | 3,008 trajectory readouts, 33 stratified summaries, 54 feasibility plot records |
| `output/verification_report.json` | Input hash checks, statistics, LP errors, comparisons, library versions |
| `output/audit/` | Figure provenance and contact/terminal-state checks |

GitHub Actions also runs this command and uploads the generated outputs as a workflow artifact. Rendered PDF metadata and appearance can vary with software versions; verification compares numerical values, rather than demanding identical rendered PDF bytes.

## What is reproduced

| Evidence | Packaged population / check |
|---|---|
| Authority geometry | 324 non-null F1–F3 uniform/asymmetric pairs; 108 F0 null pairs |
| Dynamic state differences | 162 dynamic pairs; median maximum yaw-rate difference 0.0047523521 rad/s, sideslip difference 0.0006155940 rad |
| Fig. 3 trajectories | Eight saved 27-state trajectories for command 16, P2/P4, F1, 475 K; 376 nodes each |
| Mean projection | 576 frozen wheel/lumped comparison rows; Fig. 5 uses saved P3/P4 F1 hulls |
| Coupled feasibility | 54 pairs drawn from 72 saved F1 snapshots: F/F 12, F/I 6, I/F 0, I/I 36; 18 phase-I limiting-label changes |
| Independent optimisation check | SciPy/HiGHS solves the saved phase-I LPs; checks positive row scales, saved solutions, command projection and feasible QP solutions |

Figures 1/2/5 use selected frozen endpoint data; Fig. 3 recomputes contact-force readouts from saved states, without integrating new trajectories. Figures 4/6 use the full frozen comparison tables. The aggregate comparison tables are inputs: their complete upstream simulation generation is outside this minimal package. The QP check verifies stored successful solutions; it does not rerun the full online controller.

## Files and provenance

- `data/records/`: selected numerical MAT fields, including 72 affine constraint snapshots. MATLAB function handles and opaque workspace fields are omitted; retained values were checked exactly against their original values when exported.
- `data/tables/`: byte-identical frozen CSV tables.
- `expected/`: original figure readouts and the initial local verification report.
- `scripts/`: the original plotting calculations adapted for portable paths, plus verification code.
- `reference_model/matlab/`: three unchanged model/integrator files for inspection. These are reference source excerpts, not a complete configured MATLAB simulation runner.
- `docs/SOURCE_LINEAGE.json`: original relative paths, original SHA-256, packaged SHA-256, and export/adaptation descriptions.
- `MANIFEST.json`: package file sizes and SHA-256 values, checked at runtime.

Original-source hashes document provenance; the full original archive is not included. Package hashes validate the supplied files, not an independently authenticated signature. Source CSV fields such as `raw_sha256` refer to the original full MAT files; exported MAT hashes are recorded separately in the lineage file.

## Scientific scope

These are scenario-model results for non-articulated rigid heavy vehicles. Initial thermal patterns and scenario bounds are prescribed. Sampled contact hulls are not exact reachable sets; deterministic quantiles are not confidence intervals. Authority geometry, actual state response and surrogate feasibility are distinct observables. Target-vehicle calibration, experimental validation, real-road safety certification and controller superiority are not established. See [scientific boundaries](docs/SCIENTIFIC_SCOPE.md).

OpenAI Codex assisted with preparation of this package, script adaptation and verification. Numerical inputs were taken from the retained research records. The published workflows use conventional scientific plotting software; no generative image model is used.

No publication DOI or open-source licence is asserted. See [rights status](RIGHTS.md).

## 中文说明

这是已有数值记录的最小复现包：安装依赖后运行 `python reproduce.py`，即可重绘主文六幅图、复算汇总统计，并用独立 LP 求解器检查 72 个保存的快照。输入文件均带 SHA-256 校验，输出集中写入 `output/`。

本包保留 324 个非空几何配对、108 个 F0 空效应配对、162 个动态配对、576 个均温投影比较以及 54 个可行性配对。完整上游仿真、整套在线控制器及物理试验不在本包运行范围内；其中的失败结果与科学结论边界没有因本次发布而改变。
