function [z,o]=thermalAuthorityIntegrateLumped(z0,command,plant,horizon,step)
% Continuous mean-temperature ablation of the same HF field, not a new
% actuator/tire model. Project both initial and every stage thermal state.
p=plant.model;z=z0;z(19:22)=mean(z(19:22));z(23:26)=mean(z(23:26));
initial=z;cuts=unique([0,min(p.tauF,horizon),min(p.tauA,horizon),horizon]);
for seg=1:numel(cuts)-1
 lo=cuts(seg);hi=cuts(seg+1);n=ceil((hi-lo)/step);if n==0,continue;end;h=(hi-lo)/n;
 for k=1:n
  t=lo+(k-1)*h;right=hi-8*eps(max(1,hi));
  k1=flow(t,z);k2=flow(min(t+h/2,right),z+h*k1/2);k3=flow(min(t+h/2,right),z+h*k2/2);k4=flow(min(t+h,right),z+h*k3);
  z=z+h*(k1+2*k2+2*k3+k4)/6;z(19:22)=mean(z(19:22));z(23:26)=mean(z(23:26));
 end
end
[~,o]=hfVectorField(z,effective(horizon),plant);
 function u=effective(t)
  u=command;if t<p.tauF,u(1:4)=initial(14:17);end;if t<p.tauA,u(5)=initial(18);end
 end
 function d=flow(t,zz)
  zz(19:22)=mean(zz(19:22));zz(23:26)=mean(zz(23:26));d=hfVectorField(zz,effective(t),plant);
  d(19:22)=mean(d(19:22));d(23:26)=mean(d(23:26));
 end
end
