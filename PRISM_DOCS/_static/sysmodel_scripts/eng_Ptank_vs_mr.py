from prism import *
from prism.isp import off_mr

S = SysModel(name="Engine Pc/MR Study", type="analysis", 
    author="O.F. Design")

# set design constants from common Constants values

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["PengInOx",277.7, 250.0, 350.0, 5.0, 'psia', 'Ox Engine Inlet Pressure'],
    ["PengInFuel",286.0, 250.0, 350.0, 5.0, 'psia', 'Fuel Engine Inlet Pressure'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["Pc", "psia", "Chamber Pressure"],
    ["MR", "", "Mixture Ratio"],
    ["Fvac", "lbf", "Vacuum Thrust"],
    )

RefEng =  off_mr.RefEngine()

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    PengInOx,PengInFuel = S("PengInOx","PengInFuel")
    
    Pc,MR = RefEng.solvePcMR_GivenPfeed(PengInOx,PengInFuel)
    Fvac = RefEng.calcThrustForPcMR( Pc, MR)

    S.reCalc()

    S["sysMass"] = S.mass_lbm
    S["Pc"] = Pc
    S["MR"] = MR
    S["Fvac"] = Fvac

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()
#S.saveShortSummary()

#make2DPlot(S, sysParam="Pc", desVar="PengInOx")
dpi = 100
make2DParametricPlot(S, sysParam="MR", desVar="PengInOx",
    paramVar=["PengInFuel",250.0,275.0,300.0,325.,350.]  ,makeHTML=1, dpi=dpi,
    ptData=[[277.7],[1.85]], ptLegend='Design Point', logX=0, logY=0)
    
make2DParametricPlot(S, sysParam="Pc", desVar="PengInOx",
    paramVar=["PengInFuel",250.0,275.0,300.0,325.,350.]  ,makeHTML=1, dpi=dpi,
    ptData=[[277.7,277.7],[150.,150.]], ptLegend='Design Point', logX=0, logY=0)
    
make2DParametricPlot(S, sysParam="Fvac", desVar="PengInOx",
    paramVar=["PengInFuel",250.0,275.0,300.0,325.,350.]  ,makeHTML=1, dpi=dpi,
    ptData=[[277.7,277.7],[7500.,7500.]], ptLegend='Design Point', logX=0, logY=0)
    

makeContourPlot(S, sysParam="MR", desVars=["PengInOx","PengInFuel"], interval=0.05, dpi=dpi)
makeContourPlot(S, sysParam="Pc", desVars=["PengInOx","PengInFuel"], interval=2.0, dpi=dpi)
makeContourPlot(S, sysParam="Fvac", desVars=["PengInOx","PengInFuel"],  dpi=dpi)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()