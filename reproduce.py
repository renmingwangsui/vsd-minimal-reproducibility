"""One-command frozen-result reproduction and independent snapshot checks."""
from pathlib import Path
import json, subprocess, sys, platform
from scripts.verify_records import verify_manifest, verify_statistics, verify_snapshots, compare_figure_tables
import numpy, scipy, matplotlib

def main():
    root=Path(__file__).resolve().parent
    files=verify_manifest()
    statistics=verify_statistics()
    snapshots=verify_snapshots()
    subprocess.run([sys.executable,str(root/'scripts/make_figures.py')],cwd=root,check=True)
    comparison=compare_figure_tables()
    report={'status':'PASS','scope':'Frozen result reproduction; independent phase-I LP check; no new vehicle integration',
            'verified_manifest_files':files,'summary':statistics,'snapshot_verification':snapshots,
            'figure_table_comparison':comparison,
            'environment':{'Python':platform.python_version(),'NumPy':numpy.__version__,
                           'SciPy':scipy.__version__,'Matplotlib':matplotlib.__version__}}
    (root/'output/verification_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
