
from math import *
from prism import *

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Neutral Grain", type="solid gg", 
    author="Finney Burns", programName="Grain Analysis")


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ['OR',6,5,15,1,'in','Outside Radius'],
    ['web',2,2,4,0.2,'in','Web thickness'],
    ['pcentBurned',0,0,100,5,'%','Percent Burned'],
    )


# now add any Result Variables That might be plotted
# "sysMass" is required
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ['Height','in','Grain Height'],
    ['SA','sqin','Grain Surface Area'],
    ['sysMass','lbm','Total System Mass'],
    )


# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    OR,web,pcentBurned = S("OR","web","pcentBurned")

    S.reCalc()

    Height = 4.0 * OR #- web
    
    wBurned = pcentBurned*web/100.0
    h = Height - wBurned*2.0
    r = OR - web + wBurned
    SA = 2.0*pi*r*h + 2.0*pi*(OR**2 - r**2)

    # "sysMass" is required
    S["sysMass"] = S.mass_lbm
    S["Height"] = Height
    S["SA"] = SA    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

make2DParametricPlot(S, sysParam="SA", desVar="pcentBurned",
    paramVar=["web",1.0,1.5,2.0,2.5]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="SA", desVar="pcentBurned",
    paramVar=["web",1.0,2.0,3.0,4.0,5.0]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)


# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
