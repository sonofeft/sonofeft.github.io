from prism.isp.tdk import raoContour, parabolic
from math import *
from prism.isp.cea.CEA_Isp import CEA_Isp
from prism.utils import xlChart

def sinDeg( ang ):
    return sin( ang*pi/180.0 )

def cosDeg( ang ):
    return cos( ang*pi/180.0 )

def isFloat(s):
    '''is the given string a float'''
    try: float(s)
    except ValueError: return 0
    else: return 1

pc=400.0
pcentBell=80.0

eps=40.0
oxName= 'N2O4'
fuelName='M20'
mr = 1.0
Dthrt = 0.65
Rthrt = Dthrt/2.

ispObj = CEA_Isp(oxName=oxName, fuelName=fuelName)
IspODE, Cstar, Tcomb, mw, gam = ispObj.get_IvacCstrTc_ChmMwGam( Pc=pc, MR=mr, eps=eps)
print 'Using gamma =',gam

rao = raoContour.RaoContour2( eps=eps, gam=gam, molWt=mw,
    Pc=pc, Tc=Tcomb, THETAB=25.0,
    RWTU = 2.0, RWTD = 0.5, RSTAR = 1.0, 
    pcentBell=pcentBell, Lnoz=0.0, saveFile="testRao",  
    useRao95=0, odeObj=None, useDBruns=0)

myTitle = "Example Rao Nozzle Contour, %s/%s, Area Ratio=%g, %%Bell=%g\nThroat Diam = %g, Entrance Ang=%g deg, Exit Ang=%g deg in"%\
    (oxName, fuelName, eps, pcentBell, Dthrt, rao.entranceAngle, rao.exitAngle )

rs = [ ['x','Rnozzle'] ]
# make the circular arc at the throat
ang = -rao.entranceAngle
while ang<=rao.entranceAngle:
    rs.append( [rao.RWTD*sinDeg(ang)*Rthrt, (1.0 + rao.RWTD*(1.-cosDeg(ang)))*Rthrt] )
    ang += 1.

rs.append( ['',''] ) # separate circular throat from detailed contour
# add the nozzle
for ZStar,RStar,MachNumber,Theta in rao.contourStar[3:]:
    if isFloat(RStar) and isFloat(ZStar):
        rs.append( [float(ZStar)*Rthrt, float(RStar)*Rthrt] )

xl = xlChart.xlChart()
xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message

xl.makeChart(rs, title=myTitle ,nCurves = 1,
            chartName="Rao",sheetName="raoData",
            yLabel="Radial Position", xLabel="Axial Position")

