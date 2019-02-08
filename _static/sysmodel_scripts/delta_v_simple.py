from prism import *
from math import *


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Mass Fraction Study", type="analysis", 
    author="C Taylor", programName='Delta V Study')

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor

#  deltaV - assumes linear expenditure of RCS propellant during mission

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["Isp",300.0, 250.0, 350.0, 2.0, 'sec', 'Engine Specific Impulse'],
    ["pcentACS",5.,0.,10.,1.,'','% ACS Propellant of Total'],
    ["Wpayload", 100., 50., 150., 10., 'lbm', 'Payload Mass'],
    ["massFraction",0.5,0.3,0.9,0.02, "", "Stage Propellant Mass Fraction"],
    ["WtPropAxial",200.,100.,500.,25., "lbm", "Burned Axial Propellant"],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["GLOW", 'lbm', 'Gross Liftoff Mass'],
    ["deltaV", 'ft/sec', 'Delta V'],
    ["Itot", 'lbf-sec', 'Total Impulse'],
    )

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
    Isp,pcentACS,Wpayload,massFraction,WtPropAxial = \
        S("Isp","pcentACS","Wpayload","massFraction","WtPropAxial")
    
    Payload.mass_lbm = Wpayload
    
    
    fracACS = pcentACS / 100.0
    WtPropTotal = WtPropAxial * (1.0 + fracACS)
    
    WpRCS = fracACS * WtPropTotal
    WtPropAxial = WtPropTotal - WpRCS
    
    GLOW = Payload.mass_lbm + WtPropTotal/massFraction
    
    PropulsionSys.mass_lbm = GLOW - WtPropTotal - Payload.mass_lbm 
    
    Fl.mass_lbm = WtPropTotal

    S.reCalc() # recalulates all of the mass items in system

    S["sysMass"] = S.mass_lbm
    
    # treat RCS propellant as inert flow for axial engine Isp (i.e. linear over mission)
    fracIsp = WtPropAxial / (WtPropAxial + WpRCS)
    
    Winit = S.mass_lbm 
    Wfinal = S.mass_lbm - WtPropTotal
    deltaV = gc * Isp* fracIsp * log( Winit / Wfinal) 
    
    S["deltaV"] = deltaV
    S["GLOW"] = GLOW
    S["Itot"] = WtPropAxial * Isp

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()
S.saveShortSummary()

make2DPlot(S, sysParam="deltaV", desVar="Isp")


makeSensitivityPlot(S,figureOfMerit="deltaV", desVars=["Isp","pcentACS","Wpayload","WtPropAxial","massFraction"], omitViolPts=0)

make2DParametricPlot(S, sysParam="deltaV", desVar="Isp",
    paramVar=["massFraction", 0.1,0.3,0.5,0.7,0.9]  ,makeHTML=1, dpi=70,
    ptData=None, ptLegend='', logX=0, logY=0)


make2DParametricPlot(S, sysParam="deltaV", desVar="WtPropAxial",
    paramVar=["massFraction", 0.1,0.3,0.5,0.7,0.9]  ,makeHTML=1, dpi=70,
    ptData=None, ptLegend='', logX=0, logY=0)


makeContourPlot(S, sysParam="deltaV", desVars=["Wpayload","massFraction"],
        interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
        dpi=70, colorMap="summer")



makeCarpetPlot(S, sysParam="deltaV", 
    desVarL=[["Isp",250.,300.,350.],["massFraction", 0.1,0.3,0.5,0.7,0.9]], 
    xResultVar="Itot",
    makeHTML=1, dpi=70, linewidth=2, smallLegend=1,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', 
    haLabel='center', vaLabel='center')


# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()