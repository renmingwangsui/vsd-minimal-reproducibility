"""Verify packaged frozen records; no new vehicle trajectory is integrated."""
from pathlib import Path
import csv, hashlib, json, collections
import numpy as np
from scipy.io import loadmat
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]

def rows(name, folder='data/tables'):
    with (ROOT/folder/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def verify_manifest():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        file = ROOT/item['path']
        assert file.is_file(), item['path']
        assert hashlib.sha256(file.read_bytes()).hexdigest() == item['sha256'], item['path']
    return len(manifest['files'])

def verify_statistics():
    geometry = rows('THERMAL_AUTHORITY_EFFECT_SIZE.csv')
    nonnull = [r for r in geometry if r['family'] in ['F1','F2','F3']]
    null = [r for r in geometry if r['family']=='F0']
    dynamic = [r for r in rows('THERMAL_YAW_ENGINEERING_TRANSLATION.csv') if r['stage']=='dynamic']
    assert len(geometry)==432 and len(nonnull)==324 and len(null)==108 and len(dynamic)==162
    key = lambda r: tuple(r[k] for k in ['family','stage','point','mean_T_K','pattern'])
    assert len({key(r) for r in geometry})==432
    assert len({key(r) for r in dynamic})==162
    assert max(abs(float(r['E_yaw'])) for r in null)==0
    assert max(abs(float(r['E_B'])) for r in null)==0
    pairs = rows('PHASE_I_RESERVE_PAIRWISE.csv')
    assert len(pairs)==len({r['case_id'] for r in pairs})==54
    count = collections.Counter((r['QP_uniform'],r['QP_asym']) for r in pairs)
    expected = {('feasible','feasible'):12,('feasible','infeasible'):6,('infeasible','feasible'):0,('infeasible','infeasible'):36}
    assert all(count[k]==v for k,v in expected.items())
    assert sum(r['row_changed'].lower()=='true' for r in pairs)==18
    assert all(r['Srow_uniform_sha256']==r['Srow_asym_sha256'] for r in pairs)
    assert all(all(x.startswith('thermal') for x in json.loads(r['phase_I_asym'])) for r in pairs if r['QP_uniform']=='feasible' and r['QP_asym']=='infeasible')
    summary = {'geometry_pairs':324,'F0_null_pairs':108,'dynamic_pairs':162,'feasibility_pairs':54,
               'phase_I_limiting_label_changes':18,'feasible_to_infeasible':6,'infeasible_to_feasible':0,
               'status_matrix':{a+'/'+b:count[(a,b)] for a,b in expected}}
    for name, data, factor in [('E_yaw_percent',nonnull,100),('E_B_percent',nonnull,100),
                               ('max_abs_delta_r_rad_s',dynamic,1),('max_abs_delta_beta_rad',dynamic,1)]:
        field={'E_yaw_percent':'E_yaw','E_B_percent':'E_B'}.get(name,name.replace('_rad_s','').replace('_rad',''))
        vals=np.array([float(r[field])*factor for r in data])
        summary[name]=dict(zip(['min','P10','median','P90','max'],np.quantile(vals,[0,.1,.5,.9,1]).tolist()))
    assert abs(summary['E_yaw_percent']['median']-3.09)<.005
    assert abs(summary['max_abs_delta_r_rad_s']['median']-.004752)<.0000005
    assert abs(summary['max_abs_delta_beta_rad']['median']-.000616)<.0000005
    lumped=rows('all_lumped.csv')
    assert len(lumped)==576
    summary['wheel_lumped_comparisons']=len(lumped)
    return summary

def verify_snapshots():
    index=rows('ALL72_FROZEN_SNAPSHOTS.csv')
    assert len(index)==len({r['case_id'] for r in index})==72
    max_lp_error=0.; max_saved_residual=0.; max_qp_residual=0.; active=[]
    for row in index:
        m=loadmat(ROOT/'data/records'/row['raw_file'],simplify_cells=True)
        s=m['set']; r=m['reserve']; p=m['p']
        A=np.asarray(s['A']); b=np.asarray(s['b']); scale=np.asarray(s['scales'])
        lo=np.asarray(s['lower']); hi=np.asarray(s['upper'])
        assert len(b)==int(row['row_count']) and np.all(scale>0) and np.all(lo<=hi)
        assert hashlib.sha256(np.ascontiguousarray(scale,dtype='<f8').tobytes()).hexdigest()==row['Srow_sha256']
        assert np.array_equal(m['u0'],np.clip(m['uNom'],p['commandMin'],p['commandMax']))
        assert np.array_equal(s['u0'],m['u0'])
        u=np.asarray(r['u']); xi=float(r['xi'])
        residual=float(np.max((A@u-b)/scale-xi))
        max_saved_residual=max(max_saved_residual,residual)
        assert residual<=1e-6 and np.all(u>=lo-1e-6) and np.all(u<=hi+1e-6)
        assert abs(float(r['rho'])+xi)<1e-12
        assert abs(float(row['rho'])-float(r['rho']))<1e-12
        objective=np.r_[np.zeros(A.shape[1]),1.]
        solved=linprog(objective,A_ub=np.column_stack([A/scale[:,None],-np.ones(len(b))]),b_ub=b/scale,
                       bounds=list(zip(lo,hi))+[(None,None)],method='highs')
        assert solved.success, row['case_id']
        error=abs(-float(solved.fun)-float(row['rho']))
        max_lp_error=max(max_lp_error,error)
        assert error<=1e-6, (row['case_id'],error)
        labels=np.asarray(s['labels']).reshape(-1)
        selected=sorted(set(str(x) for x in labels[np.abs((A@u-b)/scale-xi)<=1e-6]))
        assert selected==sorted(json.loads(row['phase_I_labels'])), (row['case_id'],selected)
        feasible=float(m['ctl']['exitflag'])>0
        assert ('feasible' if feasible else 'infeasible')==row['QP_status']
        if feasible:
            q=np.asarray(m['ctl']['uStar'])
            violation=float(np.max((A@q-b)/scale));max_qp_residual=max(max_qp_residual,violation)
            assert violation<=1e-6 and np.all(q>=lo-1e-6) and np.all(q<=hi+1e-6)
        active.append(np.asarray(m['qpActive']).size)
    assert max(active)==0
    return {'count':72,'phase_I_independent_solver':'SciPy linprog / HiGHS',
            'max_abs_recomputed_rho_error':max_lp_error,'max_saved_phase_I_row_residual':max_saved_residual,
            'max_saved_feasible_QP_row_residual':max_qp_residual,
            'saved_QP_active_label_count_max':max(active),'new_vehicle_integrations':0}

def compare_figure_tables():
    checks={}
    for name in ['VSD_FIG3_TIME_HISTORIES.csv','VSD_STRATIFICATION_QUANTILES.csv','VSD_FEASIBILITY_PLOT_RECORDS.csv']:
        actual=rows(name,'output/tables'); expected=rows(name,'expected')
        assert len(actual)==len(expected),name
        max_error=0.
        for a,b in zip(actual,expected):
            assert set(a)==set(b),name
            for k in a:
                try:
                    x,y=float(a[k]),float(b[k])
                except ValueError:
                    assert a[k]==b[k],(name,k,a[k],b[k]);continue
                assert np.isfinite(x) and np.isfinite(y), (name,k)
                max_error=max(max_error,abs(x-y))
                assert abs(x-y)<=1e-9*(1+abs(y)),(name,k,x,y)
        checks[name]={'rows':len(actual),'max_abs_numeric_difference':max_error}
    return checks
