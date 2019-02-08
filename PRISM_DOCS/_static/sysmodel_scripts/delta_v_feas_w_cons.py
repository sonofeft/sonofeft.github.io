from prism import *
from math import *


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Mass Fraction Study", type="analysis", 
    author="C Taylor", programName='Delta V Study')

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor

#  deltaVReqmt - assumes linear expenditure of RCS propellant during mission

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["Isp",300.0, 250.0, 350.0, 2.0, 'sec', 'Engine Specific Impulse'],
    ["pcentACS",5.,0.,10.,1.,'','% ACS Propellant of Total'],
    ["Wpayload", 300., 250., 450., 10., 'lbm', 'Payload Mass'],
    ["GLOW", 900., 600., 1200., 50., 'lbm', 'Gross Liftoff Mass'],
    ["deltaVReqmt", 3000., 2000., 4000., 100., 'ft/sec', 'Delta V Requirement'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["massFraction", "", "Stage Propellant Mass Fraction","<",0.45],
    ["WtPropAxial", "lbm", "Burned Axial Propellant"],
    ["deltaV", 'ft/sec', 'Delta V Requirement'],
    ["Itot", 'lbf-sec', 'Total Impulse'],
    )

# set Feasible Variables
S.addFeasibleVariable( name="deltaV_FOM", 
        feasibleVal=1.0 ,
        units='', desc='deltaV figure of merit',
        controlVar="stgPropFrac", cvMinVal=0.0001, cvMaxVal=0.999,
        cvUnits='', cvDesc='Stage Propellant Mass Fraction')

# use base mass object to model system mass items (MassItem)
# (most simple of all mass items)
Fl = MassItem(name="Propellant", type="propellant", mass_lbm=170.0)
Payload = MassItem(name="Payload Weight", type="inert", mass_lbm=100.0)
PropulsionSys = MassItem(name="Propulsion system", type="inert", mass_lbm=0.0)

#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Payload, PropulsionSys, Fl] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Isp,stgPropFrac,pcentACS,Wpayload,GLOW,deltaVReqmt = \
        S("Isp","stgPropFrac","pcentACS","Wpayload","GLOW","deltaVReqmt")
    
    Payload.mass_lbm = Wpayload
    
    WtPropTotal = stgPropFrac * (GLOW - Wpayload)
    
    fracACS = pcentACS / 100.0
    WpRCS = fracACS * WtPropTotal
    WtPropAxial = WtPropTotal - WpRCS
    
    PropulsionSys.mass_lbm = GLOW - WtPropTotal - Payload.mass_lbm 
    
    Fl.mass_lbm = WpRCS + WtPropAxial

    S.reCalc() # recalulates all of the mass items in system

    S["sysMass"] = S.mass_lbm
    
    massFraction = stgPropFrac
    
    # treat RCS propellant as inert flow for axial engine Isp (i.e. linear over mission)
    fracIsp = WtPropAxial / (WtPropAxial + WpRCS)
    
    Winit = S.mass_lbm 
    Wfinal = S.mass_lbm - WtPropTotal
    deltaV = gc * Isp* fracIsp * log( Winit / Wfinal) 
    
    S["deltaV"] = deltaV
    S["massFraction"] = massFraction
    S["deltaV_FOM"] = deltaV/deltaVReqmt
    S["WtPropAxial"] = WtPropAxial
    S["Itot"] = WtPropAxial * Isp

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()
S.saveShortSummary()

make2DPlot(S, sysParam="massFraction", desVar="Isp")


makeSensitivityPlot(S,figureOfMerit="massFraction", desVars=["Isp","GLOW","pcentACS","Wpayload","deltaVReqmt"], omitViolPts=0)
makeSensitivityPlot(S,figureOfMerit="Itot", desVars=["Isp","GLOW","pcentACS","Wpayload","deltaVReqmt"], omitViolPts=0)

make2DParametricPlot(S, sysParam="massFraction", desVar="Isp",
    paramVar=["GLOW", 600., 900., 1200.]  ,makeHTML=1, dpi=70,
    ptData=None, ptLegend='', logX=0, logY=0)


make2DParametricPlot(S, sysParam="massFraction", desVar="deltaVReqmt",
    paramVar=["GLOW", 600., 900., 1200.]  ,makeHTML=1, dpi=70,
    ptData=None, ptLegend='', logX=0, logY=0)


makeContourPlot(S, sysParam="massFraction", desVars=["Wpayload","GLOW"],
        interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
        dpi=70, colorMap="summer")



makeCarpetPlot(S, sysParam="massFraction", 
    desVarL=[["Isp",250.,300.,350.],["GLOW",600., 900., 1200.]], 
    xResultVar="Itot",
    makeHTML=1, dpi=70, linewidth=2, smallLegend=1,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', 
    haLabel='center', vaLabel='center')


makeMassItemSensitivityPlot(S, desVar="Isp", excludePropellant=0, showDelta=0)
makeMassItemSensitivityPlot(S, desVar="Isp", excludePropellant=0, showDelta=1)
makeMassPieCharts(S)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()