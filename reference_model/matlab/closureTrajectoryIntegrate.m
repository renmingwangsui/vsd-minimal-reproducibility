function [z,o,audit,times,states]=closureTrajectoryIntegrate(z0,command,plant,horizon,step,mode)
% HF contact-force readout, never reconstructed using surrogate phi*bf.
% Local mode is a held-body/temperature actuation-wheel slice; dynamic mode
% integrates all27 states. Both use the original independent hfVectorField.
z=z0;times=0;states=z0.';p=plant.model;cuts=unique([0,min(p.tauF,horizon),min(p.tauA,horizon),horizon]);
audit=struct('minSpeed',z(2),'minWheelOmega',min(z(10:13)),'minLoad',inf,'maxTemperature',max(z(19:22)),'valid',true,'controllerDisabled',true);
for seg=1:numel(cuts)-1
 lo=cuts(seg);hi=cuts(seg+1);n=ceil((hi-lo)/step);if n==0,continue;end;h=(hi-lo)/n;
 for k=1:n
  t=lo+(k-1)*h;right=hi-8*eps(max(1,hi));
  k1=flow(t,z);k2=flow(min(t+h/2,right),z+h*k1/2);k3=flow(min(t+h/2,right),z+h*k2/2);k4=flow(min(t+h,right),z+h*k3);
  z=z+h*(k1+2*k2+2*k3+k4)/6;
  times(end+1,1)=t+h;states(end+1,:)=z.';
  audit.minSpeed=min(audit.minSpeed,z(2));audit.minWheelOmega=min(audit.minWheelOmega,min(z(10:13)));audit.maxTemperature=max(audit.maxTemperature,max(z(19:22)));
 end
end
[~,o]=hfVectorField(z,effective(horizon),plant);audit.minLoad=min(o.Fz);
audit.valid=all(isfinite(z))&&audit.minSpeed>p.vMin&&all(o.Fz>0)&&audit.minWheelOmega>=0&&audit.maxTemperature<=p.modelValidTemperature(2)&&min(z(19:22))>=p.modelValidTemperature(1)&&abs(p.kappa*z(5))<.1;
 function u=effective(t)
  u=command;
  if t<p.tauF,u(1:4)=z0(14:17);end
  if t<p.tauA,u(5)=z0(18);end
 end
 function d=flow(t,zz)
  d=hfVectorField(zz,effective(t),plant);
  if strcmp(mode,'local'),masked=zeros(27,1);masked(10:17)=d(10:17);d=masked;end
 end
end
