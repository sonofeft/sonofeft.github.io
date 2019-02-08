
from math import *
from prism import *

from prism.isp.tdk import TDK_Nozzle
from prism.isp.tdk import Huzel

pc=1000.0
eps=40.0 
pcBell = 80.0
gam = 1.2

# Get curve fit estimate of optimum parabolic nozzle shape.
thAng, exAng = Huzel.getHuzelThetaAlpha( eps, pcBell )

markdown_desc = """
Finding the optimum parabolic nozzle can be done in two ways within PRISM.

1. Call the curve fit within the Huzel routine.
2. Use the optimizer to call TDK to find the highest efficiency.

The parabolic nozzle is defined by the entrance angle and the exit angle.

This example demonstrates for a nozzle of 

* area ratio = {eps:g}
* Percent Bell = {pcBell:g}

the curve fit result is 

* entrance angle = {thAng:g} deg
* exit angle = {exAng:g} deg

The optimization below performs the TDK approach for comparison.

**NOTICE** the figure of merit in the optimization is not nozzle efficiency, it
is the **difference** between nozzle efficiency and a reference nozzle efficiency.
This is done so that the optimizer will see larger percent improvements as it explores the design space.

Aside from the sensitivity chart that shows how efficiency changes with the two design parameters, there is also
a contour plot of efficiency that shows the optimizers answer at approximately the center of the optimum "island"
on the plot.

""".format( **{'thAng':thAng, 'exAng':exAng, 'eps':eps, 'pcBell':pcBell} )
    

thAng += 3.0 # add an offset to see if optimizer brings it back
exAng += 3.0 # add an offset to see if optimizer brings it back


# create system object (make sure author is correct... it's used for report)
S = SysModel(programName='Nozzle Optimization Study',  type="analysis", 
             author="Skippy Rao", name="Parabolic Nozzle",
             markdown_desc=markdown_desc, constraintTolerance=0.00001) # set tol for 0.99 constrVal

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["thetaAng",thAng, 25.0, 40.0, 0.5, 'deg', 'Entrance Angle'],
    ["exitAng",  exAng, 3.0, 15.0,  0.5, 'deg', 'Exit Angle'],
    ["eps",  eps, 5.0, 100.0,  2.0, '', 'Area Ratio'],
    ["pcBell", pcBell, 60.0, 100.0,  2.0, '', 'Percent Bell'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["eta2D", "", "Nozzle Efficiency", ">", 0.99],
    ["eta2Ddiff", "", "Nozzle Efficiency - Ref Efficiency"]
    )
#    ["Lengine", "in", "Axial Engine Length", "<", 15.6],

tdk = TDK_Nozzle.TDK(  theta=thAng, exitAngle=exAng , Rthrt=1.0,
                Pc=pc, gamma=gam, eps=eps, Tc=5500., MW=20.,
                RWTU = 1.0, RWTD = 1.0, Nsegs=48,
                pcentBell=pcBell, saveFile='')
                
eta2Dref = tdk.IspMOC/tdk.IspODE

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    thetaAng, exitAng = S("thetaAng","exitAng")
    
    if exitAng > thetaAng-1.0:
        exitAng = thetaAng-1.0

    try:
        tdk = TDK_Nozzle.TDK(  theta=thetaAng, exitAngle=exitAng , Rthrt=1.0,
                Pc=pc, gamma=gam, eps=eps, Tc=5500., MW=20.,
                RWTU = 1.0, RWTD = 1.0, Nsegs=48,
                pcentBell=pcBell, saveFile='')
                
        eta2D = tdk.IspMOC/tdk.IspODE
    except:
        eta2D = 0.97
    S["eta2D"] = eta2D
    
    etaDiff = eta2D - eta2Dref + 0.001
    S["eta2Ddiff"] = etaDiff
    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine) # calls myControlRoutine as well

# now optimize the system... it should match up with the carpet plots.
optimize(S, figureOfMerit="eta2Ddiff", desVars=["thetaAng","exitAng"], findmin=0, useCOBYLA=0)

#make2DPlot(S, sysParam="eta2D", desVar="thetaAng")
makeSensitivityPlot(S,figureOfMerit="eta2D", desVars=["thetaAng","exitAng"])

S.saveShortSummary()

makeContourPlot(S, sysParam="eta2D", desVars=["thetaAng","exitAng"], 
    interval=0.0005, colorMap="hsv")

# now save summary of system
S.saveFullSummary()
    
# Be sure to wrap-up any files
S.close()

print 'original Huzel theta and exit =',Huzel.getHuzelThetaAlpha( eps, pcBell )