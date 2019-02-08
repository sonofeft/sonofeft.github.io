from prism.isp.cea.CEA_Isp import CEA_Isp

Pc=200.0
eps=10.0

print 'at Pc=%g psia, Area Ratio=%g'%(Pc,eps)

ispObj = CEA_Isp(propName="HAN315")
IspODE, Cstar, Tcomb = ispObj.get_IvacCstrTc(Pc=Pc, eps=eps )

print 'for propellant =',ispObj.desc 
print 'IspODE=%g sec, Cstar=%g ft/sec, Tcomb=%g degR'%(IspODE, Cstar, Tcomb)
