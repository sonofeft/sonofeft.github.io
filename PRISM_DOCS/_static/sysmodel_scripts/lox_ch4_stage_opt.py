
from math import *
from prism import *

# for LOX/CH4
rhoBulk = 0.0301 #lbm/cuin

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="LOX/CH4 stage optimization", type="study", 
    author="M.E. Thane", programName='Stage Example')

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["Diam", 78.0, 56., 84., 1., 'in', 'Stage Diameter'],
    ["Pc",    2000.0, 500.0, 3000.0,  50.0, 'psia', 'Engine Chamber Pressure'],
    ["Fvac",    50000.0, 10000.0, 100000.0,  1000.0, 'lbf', 'Engine Thrust'],
    ["Wp",    50000.0, 10000.0, 100000.0,  1000.0, 'lbm', 'Propellant Load'],
    ["eps",    100.0, 50.0, 200.0,  5.0, '', 'Engine Area Ratio'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["sysMassK", "Klbm", "Total System Mass"],
    ["Isp", "sec", "Engine Specific Impulse"],
    ["D/Dmax", "in", "Minimum L/D Stage Diameter","<",1.0]
    )
#    ["Lengine", "in", "Axial Engine Length", "<", 15.6],

S.addFeasibleVariable( name="deltaV", 
        feasibleVal=16000.0 ,
        units='ft/sec', desc='Vacuum Delta Velocity',
        controlVar="Wp", cvMinVal=10000.0, cvMaxVal=100000.0,
        cvUnits='lbm', cvDesc='Total Usable Propellant')    

S.addFeasibleVariable( name="FoverWt", 
        feasibleVal=0.75 ,
        units='lbf/lbm', desc='Initial Thrust to Weight',
        controlVar="Fvac", cvMinVal=10000.0, cvMaxVal=100000.0,
        cvUnits='lbf', cvDesc='Engine Thrust')    


# create Mass Items that make up the system

Payload = MassItem(name="payload", type="inert", mass_lbm=5000.0)

Tankage = SimpleEqnMass(name="Stage Burnout Mass", type="inert", eqn="3.0",
    desc="curve fits from ELES runs")

EngineHdwr = SimpleEqnMass(name="Engine Hardware", type="inert", eqn="3.0",
    desc="Engine/Mount/Gimbal/Lines")

AftSkirt = SimpleEqnMass(name="Aft Skirt", type="inert", eqn="3.0",
    desc="curve fits from ELES runs")

Propellant = SimpleEqnMass(name="Usable Propellant", type="propellant", eqn="3.0",
    desc="Usable Propellant")

def ln(x):
    return log(x)
#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [  Tankage, EngineHdwr, Propellant, AftSkirt,Payload ] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,Dmotor,ThrustTCA,WpropUsable,eps = S("Pc","Diam","Fvac","Wp","eps")

    WengStuff = exp(4.24824 + 0.00582539*sqrt(ThrustTCA) + 500.54/Pc + 0.00292917*eps - 12880.6/ThrustTCA + 3.84994e-005*Pc)
    WtankStuff = exp(9.56478 + 3.9034e-006*WpropUsable - 0.0278607*Dmotor - 4917.22/WpropUsable + 0.000118555*Dmotor**2)
    WaftSkirt = exp(3.17581 + 0.348021*ln(ThrustTCA) - 0.426844*ln(Pc) + 0.0616475*sqrt(eps) + 0.00666201*sqrt(Pc))
    
    Tankage.eqn = str( WtankStuff )
    EngineHdwr.eqn = str( WengStuff )
    AftSkirt.eqn = str( WaftSkirt )
    Propellant.eqn = str( WpropUsable )
    
    Ispdel = 309.686 + 14.4186*ln(eps) - 270367/ThrustTCA - 1.86425e-007*Pc**2
    
    S.reCalc()
    
    Wbo = S.mass_lbm - WpropUsable
    deltaV = 32.174 * Ispdel * log( S.mass_lbm / Wbo )
    
    FoverWt = ThrustTCA / S.mass_lbm
    
    # minimum diameter based on L/D propellant=2
    Dmin = (WpropUsable*4.0/pi/2.0/rhoBulk)**(1./3.)
    
    S["sysMass"] = S.mass_lbm
    S["sysMassK"] = S.mass_lbm/1000.0
    S["Isp"] =  Ispdel
    S["deltaV"] =  deltaV
    S["FoverWt"] =  FoverWt
    S["D/Dmax"] =  Dmotor/Dmin
    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
#optimize(S, figureOfMerit="sysMassK", desVars=["Diam","Pc","eps"], findmin=1)
makeSensitivityPlot(S,figureOfMerit="sysMassK", desVars=["Diam","Pc","eps"])

S.saveShortSummary()
if 1:
    # start making carpet plots, etc. of system
    #make2DPlot(S, sysParam="sysMassK", desVar="Pc")
    #make2DPlot(S, sysParam="Isp", desVar="Pc")
    makeContourPlot(S, sysParam="sysMassK", desVars=["eps","Pc"])
    makeContourPlot(S, sysParam="sysMassK", desVars=["Diam","eps"])
    #makeContourPlot(S, sysParam="Isp", desVars=["eps","Pc"])
    #makeMassPieCharts(S)
    
    makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=0, showDelta=0)
    #makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=0, showDelta=1)
    makeMassItemSensitivityPlot(S, desVar="eps", excludePropellant=0, showDelta=0)
    makeMassItemSensitivityPlot(S, desVar="Diam", excludePropellant=0, showDelta=0)
    #makeMassItemSensitivityPlot(S, desVar="eps", excludePropellant=0, showDelta=1)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()