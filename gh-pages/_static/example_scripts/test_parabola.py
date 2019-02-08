from prism.isp.tdk import raoContour, parabolic
from math import *
from prism.isp.cea.CEA_Isp import CEA_Isp


pc=400.0
pcentBell=70.0

eps=7.0
oxName= 'N2O4'
fuelName='M20'
mr = 1.0
Dthrt = 0.65
Rthrt = Dthrt/2.

ispObj = CEA_Isp(oxName=oxName, fuelName=fuelName)
IspODE, Cstar, Tcomb, mw, gam = ispObj.get_IvacCstrTc_ChmMwGam( Pc=pc, MR=mr, eps=eps)
print 'Using gamma =',gam

p = parabolic.Parabola(Rt=Rthrt, eps=eps, pcentBell=pcentBell, gam=gam,  Rd=0.5, showPlot=0)

myTitle = "Example Nozzle Contour, %s/%s, Area Ratio=%g, %%Bell=%g\nThroat Diam = %g, Entrance Ang=%g deg, Exit Ang=%g deg in"%\
    (oxName, fuelName, eps, pcentBell, Dthrt, p.theta, p.exitAng)
p.makeExcelPlots( title=myTitle, absUnits=1)

