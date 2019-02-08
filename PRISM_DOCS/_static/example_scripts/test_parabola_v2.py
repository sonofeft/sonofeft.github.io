from prism.isp.tdk import raoContour, parabolic
from math import *
from prism.isp.cea.CEA_Isp import CEA_Isp
from prism.utils import xlChart

def sinDeg( ang ):
    return sin( ang*pi/180.0 )

def cosDeg( ang ):
    return cos( ang*pi/180.0 )

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

myTitle = "Example Parabola Contour, %s/%s, Area Ratio=%g, %%Bell=%g\nThroat Diam = %g, Entrance Ang=%g deg, Exit Ang=%g deg in"%\
    (oxName, fuelName, eps, pcentBell, Dthrt, p.theta, p.exitAng)

rs = [ ['x','Rnozzle'] ]
# make the circular arc at the throat
ang = -p.theta
while ang<=p.theta:
    rs.append( [p.Rd*sinDeg(ang)*Rthrt, (1.0 + p.Rd*(1.-cosDeg(ang)))*Rthrt] )
    ang += 1.

rs.append( ['',''] ) # separate circular throat from parabola
# add the parabola
for i, xval in enumerate( p.zContour ):
    row = [xval * Rthrt,  p.rContour[i] * Rthrt]
    rs.append(row)

xl = xlChart.xlChart()
xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message

xl.makeChart(rs, title=myTitle ,nCurves = 1,
            chartName="Parabola",sheetName="parabData",
            yLabel="Radial Position", xLabel="Axial Position")

