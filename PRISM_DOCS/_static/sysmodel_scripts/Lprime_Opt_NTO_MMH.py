from math import *
from prism import *
from prism.isp import ffc_engine_Dt


etaPulse=1.0
mrBarrier=0.15
FvacGoal = 1250.0
elemDens=None # if None use d/v
MRengine=1.8
etaERE=0.955412  # from MKV-R study

Em=0.85
pc=500.0

oxName= 'N2O4'
fuelName='MMH'

Tox=530.0    # Tox=None if using reference point
Tfuel=530.0  # Tfuel=None if using reference point

props = oxName + '/' + fuelName


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Chamber Length Optimization", type="liquid", 
    author="Percy Bell", programName="Generic "+props+' at MR=%g'%MRengine+', Pc=%g'%pc )


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ['Lprime',1.5,1.,2.,0.1,'in','Chamber Length'],
    ['pcentBell',70.,70.,90.,2.,'','Percent Bell of Nozzle'],
    ['LinjToExit',7.0,6.0,9.0,0.5,'in','Lprime + Lnoz'],
    ['pc',500.,300,500,50,'psia','Chamber Pressure'],
    ['ko',0.035,0.035,0.05,0.005,'','Entrainment Constant'],
    )

Engine = Engine_FFC(name="Est Engine",
            oxName=oxName, fuelName=fuelName, etaERE=etaERE,
            Pc=pc, Fvac=FvacGoal, eps=25.0, mr=MRengine, CR=2.5, LoverDt=0.01,  LchamMin=2.0,
            pcentBell=80.)

# now add any Result Variables That might be plotted
# "sysMass" is required
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ['IspDel','sec','Delivered Isp'],
    ['sysMass','lbm','Total System Mass'],
    ['eps','','Nozzle Area Ratio'],
    ['pcentFFC','','Percent Fuel Film Cooling'],
    )


# set Feasible Variable


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( Engine )



# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Lprime,pcentBell,LinjToExit,pc,ko = S("Lprime","pcentBell","LinjToExit",'pc','ko')


    Engine.mr = MRengine
    Engine.pcentBell = pcentBell
    Engine.LchamMin = Lprime
    Engine.Pc = pc
    

                    
    def newLeng( e ):
        Engine.eps = e
        Engine.reCalc()
        return Engine.Lnoz + Engine.Lcham
                    
    G = Goal(goalVal=LinjToExit, minX=2.0, maxX=50.0, 
        funcOfX=newLeng, tolerance=1.0E-5, maxLoops=40, failValue=None)
    eps, ierror = G()
    Engine.eps = eps
    Engine.reCalc()

    S.reCalc()

    perfD = ffc_engine_Dt.getFFC_EngPerf(Twall = 3000.0 ,etaPulse=1.0,Lcham=Lprime, Lengine=LinjToExit,
        Dthrt = Engine.Dt,elemDens=250.0,MRengine=MRengine,ko=ko, Em=Em,DorfMin=0.006,pc=500.0,
        CR=2.0,oxName= 'N2O4',fuelName='MMH',Tox=530.0,Tfuel=530.0,pcentBell=pcentBell,
        xlnOverLcham=0.1)
    
    pcentFFC = perfD['pcentFFC']


    LP = Lperf( engine = Engine ,Tox=Tox, Tfuel=Tfuel, elemDens=elemDens,
        pcentFFC=pcentFFC, mrBarrier=mrBarrier, etaPulse=etaPulse, Em=Em)
    IspDel = LP.IspDel


    # "sysMass" is required
    S["sysMass"] = S.mass_lbm
    S["IspDel"] = IspDel
    S["eps"] = eps
    S["pcentFFC"] = pcentFFC

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()




make2DParametricPlot(S, sysParam="IspDel", desVar="pc", titleStr=props + ' Lcham Optimization',
    paramVar=["pcentBell",60.,70.,80.]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)


make2DParametricPlot(S, sysParam="IspDel", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["pcentBell",60.,70.,80.]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="eps", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["pcentBell",60.,70.,80.]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="pcentFFC", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["pcentBell",60.,70.,80.]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)


make2DParametricPlot(S, sysParam="IspDel", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["LinjToExit",6,7,8]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="eps", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["LinjToExit",6,7,8]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="pcentFFC", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["LinjToExit",6,7,8]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="pcentFFC", desVar="Lprime", titleStr=props + ' Lcham Optimization',
    paramVar=["ko",0.035,0.040,0.045,0.05]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

make2DParametricPlot(S, sysParam="IspDel", desVar="pc", titleStr=props + ' Lcham Optimization',
    paramVar=["ko",0.035,0.040,0.045,0.05]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
