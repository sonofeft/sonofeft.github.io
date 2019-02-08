
from prism.isp.cea.CEA_Isp import CEA_Isp, propCards

Pc=1000.0; eps=14.5

print 'at Pc=%g psia, Area Ratio=%g'%(Pc,eps)

propCards['myNewProp'] = \
    [' name R-45(FROM_RPL_DATA) C 7.0517 H 10.5754 O 0.2321 N 0.0662    wt%=12.00',
    ' h,cal= 9773.8 t(k)=298.15 rho=0.9220',
    ' name RDX            C 1.3506 H 2.7011 O 2.7011 N 2.7011           wt%=88.00',
    ' h,cal=6610.     t(k)=298.15   rho=1.8200]']

ispObj = CEA_Isp(propName="myNewProp")
IspODE, Cstar, Tcomb = ispObj.get_IvacCstrTc(Pc=Pc, eps=eps )

print 'for propellant =',ispObj.desc 
print 'IspODE=%g sec, Cstar=%g ft/sec, Tcomb=%g degR'%(IspODE, Cstar, Tcomb)
