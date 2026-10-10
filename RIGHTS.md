# Rights and licence scope — v1.0.0

The author explicitly authorised these grants on 10 October 2026.
Copyright holder and original simulation-data rights holder: **任林祥**.
Only the original code and original simulation numerical data below are
licensed by this release. Public repository visibility is not a licence for
other materials. The per-file register is [docs/RIGHTS_SCOPE.json](docs/RIGHTS_SCOPE.json).

| Path / material | Effective licence | Basis and boundary |
|---|---|---|
| reproduce.py; scripts/*.py | MIT, LICENSE | Original reproduction, plotting and numerical verification code; portable adaptation lineage is recorded in SOURCE_LINEAGE.json. |
| reference_model/matlab/*.m (three files) | MIT, LICENSE | Original research vector-field/integrator excerpts; preserved source hashes. These are not MathWorks toolbox implementations or a complete simulation runner. |
| .github/workflows/reproduce.yml; requirements.txt; .gitattributes; .gitignore | MIT, LICENSE | Original declarative build/environment configuration only. Imported actions/packages are excluded. |
| data/records/**/*.mat (98 numerical exports) | CC BY 4.0, DATA_LICENSE.md | Original simulation numerical values, exported from retained records; not external experimental data. |
| data/tables/*.csv (seven files) | CC BY 4.0, DATA_LICENSE.md | Original frozen simulation numerical tables. |
| expected/*.csv (three files) | CC BY 4.0, DATA_LICENSE.md | Original numerical reference readouts used for reproduction comparison. |
| expected/LOCAL_VERIFICATION_REPORT.json; docs/*.json and *.md; README.md; MANIFEST.json; rights/legal notices | No new MIT/CC BY grant for their prose or metadata | Documentation/provenance/legal notices are separately identified. The code/data grant does not automatically cover their text. Licence notices explain the grants; their inclusion does not relicense unrelated content. |
| Generated figures/images; manuscript or article text; PDFs | Not covered by this release's code/data grants | Not tracked or attached to this release. Plotting code is MIT and input numerical data CC BY 4.0; image rights are not inferred from those grants. |
| Third-party code, external datasets, packages and actions | Their original terms | No implementation or external data is vendored in the inspected package. NumPy/SciPy/Matplotlib and pinned dependencies, GitHub actions and MATLAB/Optimization Toolbox retain their respective licences. References/DOIs/links do not transfer rights. |
| Full unpublished historical research archive, private records, AI logs | Excluded | Not deposited, redistributed or licensed by v1.0.0. Access arrangements require a separate decision. |

## Items excluded pending a separate rights decision

No blanket permission is asserted for documentation prose/metadata, rendered
images, manuscript text, employer/funder-owned or subsequently supplied
third-party material, or the complete historical archive. The original
code/data grants above are explicit; the excluded classes do not inherit
those grants. If a file cannot be assigned confidently to an authorised
original-code or original-numerical-data class, exclude it and record it here
before any future release. Newly added files do not inherit a licence merely
by directory proximity.

The retained source lineage and inspected contents support the listed
original-code/data scope; they are not an independent legal determination of
all possible rights. No third-party paper PDFs, manufacturer documents,
commercial binaries or external measured datasets are redistributed. Do not
represent these scenario simulations as target-vehicle measurements or a
physical safety certificate.
