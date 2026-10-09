function [dz,o]=hfVectorField(z,u,a)
% Explicit nonlinear body/wheel/roll plant. No online tire/load helper calls.
p=a.model;vx=z(2);vy=z(3);r=z(4);delta=z(27);locx=[p.lf;p.lf;-p.lr;-p.lr];locy=p.y;
Fz0=p.m*p.g*cos(p.theta)*[p.lr;p.lr;p.lf;p.lf]/(2*(p.lf+p.lr));
react=a.Kroll*z(7)+a.Droll*z(8);w=[p.lr;p.lr;p.lf;p.lf]/(p.lf+p.lr);
Fz=Fz0+[-1;-1;1;1]*z(9)/2+[-1;1;-1;1].*w*react/p.track;
angles=[delta;delta;0;0];cw=cos(angles);sw=sin(angles);
bodyx=vx-r*locy;bodyy=vy+r*locx;wx=cw.*bodyx+sw.*bodyy;wy=-sw.*bodyx+cw.*bodyy;
slip=(a.R*z(10:13)-wx)./max(abs(wx),1);alpha=atan2(wy,max(abs(wx),1));
cap=p.mu.*max(Fz,0).*(max(Fz,1)./Fz0).^(a.loadExponent-1);
stiff=[p.CalphaF;p.CalphaF;p.CalphaR;p.CalphaR]/2;
demand=[stiff.*slip,-stiff.*alpha];normd=sqrt(sum(demand.^2,2));q=normd./max(cap,1);
scale=cap.*tanh(q)./max(normd,1e-12);Fxw=scale.*demand(:,1);Fyw=scale.*demand(:,2);
Fx=cw.*Fxw-sw.*Fyw;Fy=sw.*Fxw+cw.*Fyw;
fade=p.phiFcn(z(19:22));brakeF=fade.*z(14:17)+p.auxShare*z(18);torque=a.R*brakeF;
axContact=sum(Fx)/p.m;ay=sum(Fy)/p.m;
drag=.5*p.rhoAir*p.Cd*p.Af*vx*abs(vx);rolling=p.Cr*p.m*p.g*cos(p.theta)*tanh(vx);
dz=zeros(27,1);dz(1)=(vx*cos(z(6))-vy*sin(z(6)))/(1-p.kappa*z(5));
dz(2)=axContact-(drag+rolling)/p.m-p.g*sin(p.theta)+r*vy;
dz(3)=ay-r*vx;dz(4)=sum(locx.*Fy-locy.*Fx)/p.Iz;
dz(5)=vx*sin(z(6))+vy*cos(z(6));dz(6)=r-p.kappa*dz(1);
dz(7)=z(8);dz(8)=(p.m*p.hcg*ay-react)/a.Ix;
dz(9)=(p.m*p.hcg*axContact/(p.lf+p.lr)-z(9))/.12;
dz(10:13)=(-torque-a.R*Fxw)/a.Iw;
lag=p.tf*ones(4,1);lag(u(1:4)<z(14:17))=a.releaseLag;
dz(14:17)=(u(1:4)-z(14:17))./lag;dz(18)=(u(5)-z(18))/p.ta;
surface=z(19:22);core=z(23:26);exchange=(surface-core)/a.exchangeTime;
heat=fade.*z(14:17)*a.R.*max(z(10:13),0)./p.C;
cool=(p.convIntercept+p.convSlope*max(vx,0))*(surface-p.Tamb);
dz(19:22)=(heat-cool-exchange)/a.surfaceFraction;dz(23:26)=exchange/a.coreCapacityRatio;
dz(27)=(u(6)-delta)/a.steerLag;
o=struct('Fx',Fx,'Fy',Fy,'Fz',Fz,'tireDemand',q,'tireUtil',tanh(q),'torque',torque,'fade',fade, ...
 'LTR',(Fz(2)+Fz(4)-Fz(1)-Fz(3))/sum(Fz),'ay',ay,'axContact',axContact,'roll',z(7));
end
