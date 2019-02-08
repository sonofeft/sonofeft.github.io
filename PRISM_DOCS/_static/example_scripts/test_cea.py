from prism.isp.cea.CEA_Isp import CEA_Isp

Pc=200.0
MR=1.0
eps=10.0

print 'at Pc=%g psia, MR=%g, Area Ratio=%g'%(Pc,MR,eps)

ispObj = CEA_Isp(propName='', oxName='LOX', fuelName="CH4")
IspODE, Cstar, Tcomb = ispObj.get_IvacCstrTc(Pc=Pc, MR=MR, eps=eps )

print 'for propellant =',ispObj.desc 
print 'IspODE=%g sec, Cstar=%g ft/sec, Tcomb=%g degR'%(IspODE, Cstar, Tcomb)
