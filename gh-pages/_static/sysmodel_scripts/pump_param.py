
from math import *
from prism import *


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Pump model exercise", type="analysis", 
    author="H.P. Shaft")

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["wdot",1.0, 0.5, 3.0, 0.1, 'lbm/sec', 'Pump Flow Rate'],
    ["deltaP",200.0,100.0,500.0,20.0,'psid', 'Pump Pressure Rise'],
    ["rpm",10000.0,10000.0, 50000.0, 2000.0, 'rpm', "Pump Speed"]
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["effCalc", "", "Pump Efficiency"],
    ["effInp", "", "Assumed Pump Efficiency"],
    ["hp", "", "Pump Horsepower"]
    )

# set Feasible Variables
S.addFeasibleVariable( name="effError", 
        feasibleVal=0.0 ,
        units='', desc='Pump Efficiency Error',
        controlVar="eff", cvMinVal=0.01, cvMaxVal=1.0,
        cvUnits='', cvDesc='Pump Assumed Efficiency')

myPump = Pump(name="Fuel Pump",  fluName="MMH", mass_lbm=0.0, pStages=2)

#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [myPump] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    wdot,deltaP,eff,rpm = S("wdot","deltaP","eff","rpm")

    myPump.eff = eff
    myPump.rpm = rpm
    myPump.wdot = wdot
    myPump.deltaP = deltaP

    S.reCalc()

    S["sysMass"] = S.mass_lbm
    
    S["effError"] = eff - myPump.effCalc
    S["effCalc"] = myPump.effCalc
    S["effInp"] = eff
    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()
makeSensitivityPlot(S,figureOfMerit="effCalc", desVars=["wdot","deltaP","eff","rpm"])


S.saveShortSummary()

make2DPlot(S, sysParam="effCalc", desVar="deltaP")
make2DPlot(S, sysParam="effCalc", desVar="rpm")
if 1:
    makeContourPlot(S, sysParam="effCalc", desVars=["wdot","deltaP"])
    makeContourPlot(S, sysParam="effCalc", desVars=["wdot","rpm"])
    makeContourPlot(S, sysParam="effCalc", desVars=["deltaP","rpm"])
    
make2DParametricPlot(S, sysParam="effCalc", desVar="deltaP", dpi=100,
        paramVar=["rpm",10000, 20000, 30000])
        
# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()