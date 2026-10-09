# Adapted from the frozen VSD plotter: portable paths/output routing only.
from pathlib import Path
import sys,json,csv,hashlib,shutil,collections
import numpy as np
from scipy.io import loadmat
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
V=Path(__file__).resolve().parents[1]
R=V/'data/records'
I=V/'data/tables';O=V/'output/figures';D=V/'output/tables'
for folder in [O,D,V/'output/audit']: folder.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,'axes.titlesize':9,'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
C=['#424b57','#c23830','#2166ac','#18815b'];L=['Uniform','Left hot','Right hot','Front hot']; provenance={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(fig,name,sources,notes):
 fig.savefig(O/(name+'.pdf'),bbox_inches='tight');fig.savefig(O/(name+'.svg'),bbox_inches='tight');fig.savefig(O/(name+'.png'),bbox_inches='tight',dpi=200);plt.close(fig)
 provenance[name]={'sources':{str(p.relative_to(V)).replace('\\','/'):sha(p) for p in sources},'notes':notes,'pdf_sha256':sha(O/(name+'.pdf'))}
def hull(p):
 q=np.unique(p,axis=0);return q[ConvexHull(q).vertices] if len(q)>2 and np.linalg.matrix_rank(q-q.mean(0))==2 else q
files=[]
def geom(ax,stage,point,T,pat,family=None):
 p=R/(f'output/fade_independence/raw/{family}/{stage}/P{point}_T{T}_pattern{pat}_main.mat' if family else f'output/thermal_authority/raw/{stage}/P{point}_T{T}_pattern{pat}_main.mat');files.append(p)
 m=loadmat(p,simplify_cells=True);q=hull(m['data'][:,4:6])/1000;q=np.vstack([q,q[0]]);ax.plot(q[:,0],q[:,1],color=C[pat-1],label=L[pat-1],lw=1.6);return m
# Fig 1 purely procedural conceptual mechanism, five panels; geometry thumbnail is real P3 local.
fig,axs=plt.subplots(1,5,figsize=(7.1,2.5),gridspec_kw={'wspace':.26});files=[]
fig.subplots_adjust(left=.015,right=.985,top=.80,bottom=.10);titles=['A  Thermal\npatterns','B  Brake\neffectiveness','C  Vehicle\nmechanics','D  Joint\nauthority','E  Dynamic\nconsequences']
for ax,title in zip(axs,titles):
 ax.set_title(title,fontweight='bold',pad=12,fontsize=8);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off');ax.add_patch(FancyBboxPatch((0,.03),1,.92,boxstyle='round,pad=0.012',facecolor='#f3f6f9',edgecolor='#607387',linewidth=.8))
axs[0].text(.5,.73,'Uniform / left hot\nRight / front hot',ha='center',va='center',fontsize=7.8);axs[0].text(.5,.40,r'$\overline{T}(0)$ matched',ha='center',fontsize=8);axs[0].text(.5,.17,'Spatial\ninformation',ha='center',fontsize=8)
axs[1].text(.5,.66,'Wheel-specific\nbrake fade',ha='center',fontsize=8);axs[1].text(.5,.39,r'$\Phi=\mathrm{diag}_j\phi_j(T_j)$',ha='center',fontsize=8);axs[1].text(.5,.17,'Location\nretained',ha='center',fontsize=8)
axs[2].text(.5,.71,'Delayed states\nWheel/contact\nCombined slip\nLoad transfer',ha='center',va='center',fontsize=7.8);axs[2].text(.5,.18,'27-state\npropagation',ha='center',fontsize=8)
small=axs[3].inset_axes([.16,.30,.77,.48]);small.set_xlabel('B',labelpad=0);small.set_ylabel(r'$M_z$',labelpad=0);small.set_xticks([]);small.set_yticks([])
for pat in [1,2,3]:geom(small,'local',3,475,pat)
axs[3].text(.5,.12,'Sampled\ncontact hulls',ha='center',fontsize=8)
axs[4].text(.5,.66,'Yaw / sideslip\nMean-lumping loss\nFeasibility',ha='center',va='center',fontsize=7.8);axs[4].text(.5,.22,'Separate\nobservables',ha='center',fontsize=8)
for i in range(4):axs[i].annotate('',xy=(1.23,.5),xytext=(1.02,.5),xycoords='axes fraction',arrowprops={'arrowstyle':'->','lw':1.3},annotation_clip=False)
save(fig,'fig1_mechanism',files,'Conceptual five-step chain; D uses real sampled F1 P3 local 475 K hulls. No generated bitmap or invented numerical curve.')
# Fig2 exact pattern grid and original local geometry.
fig,axs=plt.subplots(1,2,figsize=(7,2.9),layout='constrained',gridspec_kw={'width_ratios':[1.05,1.2]});files=[]
T=475+np.array([[0,0,0,0],[35,-35,35,-35],[-35,35,-35,35],[35,35,-35,-35]])
im=axs[0].pcolormesh(np.arange(-.5,4.5),np.arange(-.5,4.5),T,cmap='coolwarm',vmin=440,vmax=510,rasterized=False);axs[0].invert_yaxis();axs[0].set_xticks(range(4),['FL','FR','RL','RR']);axs[0].set_yticks(range(4),L);axs[0].set_title('(a) Initial surface temperatures (K)')
for i in range(4):
 for j in range(4):axs[0].text(j,i,str(T[i,j]),ha='center',va='center',color='#17202a')
cb=fig.colorbar(im,ax=axs[0],ticks=[440,475,510],shrink=.75);cb.solids.set_rasterized(False)
for pat in range(1,5): m=geom(axs[1],'local',3,475,pat); assert np.array_equal(m['z0'][18:22],T[pat-1])
axs[1].set(xlabel='Incremental braking B (kN)',ylabel=r'Incremental brake $M_z$ (kN m)',title='(b) P3, F1, held-body 0.25 s');axs[1].grid(alpha=.18);axs[1].legend(loc='upper left',fontsize=7)
save(fig,'fig2_authority',files,'Actual 475 K patterns and sampled endpoint contact hulls; matched zero-service baseline subtracted, not instantaneous or exact reachable set.')
# Fig3 exact contact readout from saved frozen trajectories, no new integration.
def contact(z,a):
 p=a['model'];vx,vy,r,delta=z[1],z[2],z[3],z[26];x=np.array([p['lf'],p['lf'],-p['lr'],-p['lr']]);y=p['y'];w=np.array([p['lr'],p['lr'],p['lf'],p['lf']])/(p['lf']+p['lr'])
 f0=p['m']*p['g']*np.cos(p['theta'])*w/2;react=a['Kroll']*z[6]+a['Droll']*z[7];fz=f0+np.array([-1,-1,1,1])*z[8]/2+np.array([-1,1,-1,1])*w*react/p['track']
 ang=np.array([delta,delta,0,0]);cw,sw=np.cos(ang),np.sin(ang);bx=vx-r*y;by=vy+r*x;wx=cw*bx+sw*by;wy=-sw*bx+cw*by
 slip=(a['R']*z[9:13]-wx)/np.maximum(np.abs(wx),1);alpha=np.arctan2(wy,np.maximum(np.abs(wx),1));cap=p['mu']*np.maximum(fz,0)*(np.maximum(fz,1)/f0)**(a['loadExponent']-1)
 stiff=np.array([p['CalphaF'],p['CalphaF'],p['CalphaR'],p['CalphaR']])/2;dx=stiff*slip;dy=-stiff*alpha;norm=np.sqrt(dx*dx+dy*dy);q=norm/np.maximum(cap,1);scale=cap*np.tanh(q)/np.maximum(norm,1e-12)
 return cw*scale*dx-sw*scale*dy
fig,axs=plt.subplots(3,2,figsize=(7,5.2),layout='constrained');files=[];export=[];checks=[]
for col,point in enumerate([2,4]):
 base=None
 for pat in range(1,5):
  p=R/f'output/final_submission_closure/trajectories/F1/P{point}_T475_pattern{pat}_main.mat';raw=R/f'output/fade_independence/raw/F1/dynamic/P{point}_T475_pattern{pat}_main.mat';files.extend([p,raw]);m=loadmat(p,simplify_cells=True);old=loadmat(raw,simplify_cells=True);t=m['times'];z=np.asarray(m['trajectories'][15]);
  assert m['endpointError']==0 and np.array_equal(z[-1],old['terminalStates'][15]) and m['controllerDisabled']==1
  if base is None:base=m
  else:
   assert np.array_equal(base['commands'],m['commands']) and np.array_equal(base['times'],t)
   mask=np.ones(27,dtype=bool);mask[18:22]=False;assert np.array_equal(base['z0'][mask],m['z0'][mask])
   for k,v in base['p'].items():
    if isinstance(v,(float,int)) or (isinstance(v,np.ndarray) and v.dtype != object): assert np.array_equal(v,m['p'][k])
  fx=np.stack([contact(s,m['plant']) for s in z]);err=float(np.max(np.abs(fx[-1]-old['contactFx'][15])));assert err<1e-9
  B=-fx.sum(1);beta=np.arctan2(z[:,2],z[:,1]);
  axs[0,col].plot(t,z[:,3],color=C[pat-1],label=L[pat-1],lw=1.6);axs[1,col].plot(t,beta,color=C[pat-1],lw=1.6);axs[2,col].plot(t,B/1000,color=C[pat-1],lw=1.6)
  for n in range(len(t)):export.append({'point':point,'family':'F1','mean_T_K':475,'pattern':L[pat-1],'command_id':16,'time_s':t[n],'yaw_rate_rad_s':z[n,3],'sideslip_rad':beta[n],'contact_braking_N':B[n]})
  checks.append({'point':point,'pattern':pat,'command_id':16,'command':m['commands'][15].tolist(),'horizon_s':m['horizon'],'step_s':m['step'],'samples':len(t),'endpoint_state_error':0,'terminal_contact_error_N':err})
 for row in range(3):
  axs[row,col].grid(alpha=.18);axs[row,col].axvline(.14,color='#888888',ls=':',lw=.7)
 axs[0,col].set_title(f'P{point}: curved, F1, 475 K, command 16');axs[2,col].set_xlabel('Time (s)')
axs[0,0].set_ylabel(r'$r$ (rad/s)');axs[1,0].set_ylabel(r'$\beta$ (rad)');axs[2,0].set_ylabel('Contact braking B (kN)');fig.legend(handles=[Line2D([0],[0],color=c,lw=2,label=l) for c,l in zip(C,L)],loc='outside lower center',ncol=4)
with (D/'VSD_FIG3_TIME_HISTORIES.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=export[0].keys());w.writeheader();w.writerows(export)
(V/'output/audit/FIG3_REPLAY_CHECKS.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');save(fig,'fig3_dynamic_response',files,'P2 and P4 curved, F1, 475 K, fixed command ID16 (all four service commands 0.05mg, auxiliary0, original held steering); 376 real stored nodes each. Actual B=-sum Fx includes zero-service contact baseline; not hull-centroid forcing. Dotted line service arrival0.14s; state/terminal contact checked.')
# Fig4 marginal strata deterministic quantiles.
rows=list(csv.DictReader((I/'THERMAL_AUTHORITY_EFFECT_SIZE.csv').open(encoding='utf-8-sig')));rows=[r for r in rows if r['family'] in ['F1','F2','F3']];dyn=list(csv.DictReader((I/'THERMAL_YAW_ENGINEERING_TRANSLATION.csv').open(encoding='utf-8-sig')));dyn=[r for r in dyn if r['stage']=='dynamic'];assert len(rows)==324 and len(dyn)==162
strata=[('family',['F1','F2','F3'],['F1','F2','F3']),('mean_T_K',['400','475','550'],['400','475','550']),('road',['straight','curved'],['Straight','Curved']),('pattern',['LEFT_HOT_RIGHT_COLD','LEFT_COLD_RIGHT_HOT','FRONT_REAR_ASYMMETRIC'],['LH','RH','FH'])]
print('pattern values',sorted({r['pattern'] for r in rows}),flush=True)
fig,axs=plt.subplots(3,4,figsize=(7.5,5),layout='constrained');stats=[]
for row,(metric,data,factor,label) in enumerate([('E_yaw',rows,100,r'$E_{yaw}$ (%)'),('E_B',rows,100,r'$E_B$ (%)'),('max_abs_delta_r',dyn,1000,r'max $|\Delta r|$ (mrad/s)')]):
 for col,(field,values,names) in enumerate(strata):
  ax=axs[row,col]
  for i,value in enumerate(values):
   a=np.array([float(r[metric])*factor for r in data if r[field]==value]);assert len(a)>0;lo,p10,med,p90,hi=np.quantile(a,[0,.1,.5,.9,1]);ax.vlines(i,lo,hi,color='#8da3b7',lw=.9);ax.vlines(i,p10,p90,color='#265879',lw=4);ax.scatter(i,med,color='#c23830',s=20,zorder=3)
   stats.append({'metric':metric,'stratum':field,'value':value,'n':len(a),'display_factor':factor,'min':lo,'P10':p10,'median':med,'P90':p90,'max':hi})
  ax.set_xticks(range(len(values)),names);ax.set_xlim(-.5,len(values)-.5);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.18)
  if row==0:ax.set_title(['Fade family','Initial mean T (K)','Road','Thermal pattern'][col])
  if col==0:ax.set_ylabel(label)
fig.text(.5,-.015,'Dots: median   |   Thick bars: P10–P90   |   Thin bars: range   |   Deterministic grid, no confidence intervals',ha='center',fontsize=8)
with (D/'VSD_STRATIFICATION_QUANTILES.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=stats[0].keys());w.writeheader();w.writerows(stats)
save(fig,'fig4_stratification',[I/'THERMAL_AUTHORITY_EFFECT_SIZE.csv',I/'THERMAL_YAW_ENGINEERING_TRANSLATION.csv'],'All324 geometry pairs; dynamic162 only for state differences. Four marginal strata preserve covarying point parameters; quantiles are deterministic summaries.')
# Fig5 frozen continuous mean projection, original straight and curved records.
fig,axs=plt.subplots(1,2,figsize=(7,2.85),layout='constrained');files=[]
for ax,point in zip(axs,[3,4]):
 for pat in [2,3]:geom(ax,'dynamic',point,475,pat)
 p=R/f'output/thermal_authority/lumped_dynamic/P{point}_T475_main.mat';files.append(p);m=loadmat(p,simplify_cells=True);q=hull(m['data'][:,3:5])/1000;q=np.vstack([q,q[0]]);ax.plot(q[:,0],q[:,1],'k--',lw=1.6,label='Continuous mean projection');ax.set(title=f'P{point}: '+('straight' if point==3 else 'curved')+', F1, 0.75 s',xlabel='Incremental B (kN)',ylabel=r'Incremental $M_z$ (kN m)');ax.grid(alpha=.18)
axs[0].legend(fontsize=7,loc='center');save(fig,'fig5_mean_lumping',files,'Existing continuously projected surface/core thermal model; exact original ablation with averaged thermal derivatives. No claim that all longitudinal metrics fail; future dynamic means need not match.')
# Fig6 all 54 real pairs, no coordinate jitter; zoom shows near-zero status changes.
pairs=list(csv.DictReader((I/'PHASE_I_RESERVE_PAIRWISE.csv').open(encoding='utf-8-sig')));assert len(pairs)==54;ct=collections.Counter((r['QP_uniform'],r['QP_asym']) for r in pairs);assert list(ct.values())==[12,6,36];assert sum(r['row_changed'].lower()=='true' for r in pairs)==18
classes=[]
def cls(r):
 labels=json.loads(r['phase_I_asym']);groups=set('Thermal' if x.startswith('thermal') else 'Load transfer' if x.startswith('LT') else 'Lane / handling' if x.startswith(('lane','yaw','beta','LTR')) else 'Speed / tyre' for x in labels)
 return 'Thermal' if 'Thermal' in groups else 'Load transfer' if 'Load transfer' in groups else 'Lane / handling' if 'Lane / handling' in groups else 'Speed / tyre'
colors={'Thermal':'#c23830','Load transfer':'#2166ac','Lane / handling':'#18815b','Speed / tyre':'#424b57'};markers={('feasible','feasible'):'o',('feasible','infeasible'):'v',('infeasible','feasible'):'^',('infeasible','infeasible'):'s'}
fig,axs=plt.subplots(1,2,figsize=(7.2,3.1),layout='constrained',gridspec_kw={'width_ratios':[1.2,1]})
for ax in axs:
 for r in pairs:
  status=(r['QP_uniform'],r['QP_asym']);c=cls(r);ax.scatter(float(r['rho_uniform']),float(r['rho_asym']),marker=markers[status],c=colors[c],s=42,edgecolors='black' if status==('feasible','infeasible') else 'white',linewidths=1.1 if status==('feasible','infeasible') else .35,zorder=3)
 ax.axhline(0,color='#555555',lw=.8);ax.axvline(0,color='#555555',lw=.8);ax.grid(alpha=.18);ax.set_xlabel(r'$\rho_{uniform}$');ax.set_ylabel(r'$\rho_{asymmetric}$')
x=np.array([float(r['rho_uniform']) for r in pairs]);y=np.array([float(r['rho_asym']) for r in pairs]);low=min(x.min(),y.min())-.8;high=max(x.max(),y.max())+.8
axs[0].plot([low,high],[low,high],'k--',lw=.7);axs[0].set(xlim=(low,high),ylim=(low,high),title='(a) All 54 pairs (overlaps retained)')
axs[1].plot([-.15,.55],[-.15,.55],'k--',lw=.7);axs[1].set(xlim=(-.15,.55),ylim=(-3.2,.55),title='(b) Six F → I transitions near zero')
handles=[Line2D([0],[0],marker=mk,ls='',color='#555555',label=f'{a[0].upper()}/{b[0].upper()} = {ct[(a,b)]}',markersize=6) for (a,b),mk in markers.items()]
axs[0].legend(handles=handles,loc='upper left',fontsize=7);fig.legend(handles=[Line2D([0],[0],marker='o',ls='',color=c,label=k,markersize=5) for k,c in colors.items()],loc='outside lower center',fontsize=7,ncol=4,title='Asymmetric limiting class (saved phase-I labels)',title_fontsize=7)
for pt in ['1','2']:
 fip=[r for r in pairs if r['point']==pt and r['QP_uniform']=='feasible' and r['QP_asym']=='infeasible'];assert len(fip)==3
 rr=fip[0];axs[1].annotate('P'+pt+' (3 overlapping pairs)',xy=(float(rr['rho_uniform']),float(rr['rho_asym'])),xytext=(.25,float(rr['rho_asym'])+.08),fontsize=7,arrowprops={'arrowstyle':'-','lw':.6})
for r in pairs:classes.append({**r,'asymmetric_limiting_class':cls(r)})
with (D/'VSD_FEASIBILITY_PLOT_RECORDS.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=classes[0].keys());w.writeheader();w.writerows(classes)
save(fig,'fig6_feasibility',[I/'PHASE_I_RESERVE_PAIRWISE.csv'],'54 unique F1 surrogate pairs at fixed positive row scales; symbols show four QP-status categories including empty I/F; colours classify saved asymmetric phase-I limiting labels with thermal/load/lane/speed-tyre priority, ties preserved in CSV; no jitter or causal attribution.')
(V/'output/audit/FIGURE_PROVENANCE.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
print('Six figures completed; Fig3 terminal contact error',max(c['terminal_contact_error_N'] for c in checks),flush=True)


