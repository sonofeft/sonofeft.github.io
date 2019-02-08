
from math import *
from prism import *

deltaVReqmt = 1000.0 # assumes linear expenditure of RCS propellant during mission
payload = 1000.0 # lbm

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor
payload = 1700.0 # lbm
ullFracOx = 0.03
ullFracFl = 0.03

NumAxial = 1
NumPY = 6
NumRoll = 4
NumRCS = NumPY + NumRoll

ItotPY = 6800.0 # lbf-sec from John K 12/2/2005
ItotRoll = 1050.0 # lbf-sec from John K 12/2/2005

FvacPY = 23.0 # lbf  from John K 12/2/2005
FvacRoll = 18.0 # lbf  from John K 12/2/2005
FvacAxial = 315.0 # lbf  from John K 12/2/2005

epsAxial = 50.0
epsPY = 25.0
epsRoll = 25.0
pcentBellRCS = 80.0

mrPY = 1.2
mrRoll = 1.2
mrAxial = 1.65

etaEREFine = 0.97    # same as R&D engine
etaERECoarse = 0.94  # same as PSRE RS-140

etaEREFineRCS = 0.95
etaERECoarseRCS = 0.90

cxwValves=1.0
cxwValvesFast=2.0

cxwFFC = 1.27
cxwAblative = 1.25
cxwFFC_ACS = 1.27*1.25
cxwLines = 3.5

cxwPropTank_PMD = 1.32
cxwPropTank_FFC = 1.5
cxwPropTank_PSRE = 1.02

LchamMinAxial = 2.0
LchamMinRCS = 1.5
maxLengine = 15.6 # same as PSRE engine
maxPYLengine = 1.5

engineIntletOverPc = 1.66 # Frank Lu 11/30/2005

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor
ullFracOx = 0.03
ullFracFl = 0.03

expulEffOx = 0.99
expulEffFl = 0.99
tActionMin = 200.0 # 433.94
tActionRCS = tActionMin
TminOperate = 510.0 # degR
TmaxOperate = 550.0 # degR


# use mission 1 reqmts
MissionName = "Mission 1"
deltaVReqmt = 901.2 # assumes linear expenditure of RCS propellant during mission
payload = 1700.0 # lbm

# add misc wt dependent on design constants
PSRE_misc = Misc_Weights(name="Stage Misc.", mass_lbm=50.0)


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="NTO/MMH He & COPV Tanks ", type="bi-propellant", 
    author="Elly Kepler", programName='Upper Stage Optimization')


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["PHe",5000.0, 4000.0, 9000.0, 200.0, 'psia', 'Helium Tank Pressure'],
    ["MR",    mrAxial,    1.0,    2.4,  0.05,    '',  'Engine Mixture Ratio'],
    ["Pc",    150.0, 150.0, 500.0,  20.0, 'psia', 'Engine Chamber Pressure'],
    ["pcentBell",    80.0, 60.0, 100.0,  5.0, '', 'Nozzle Percent Bell'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["Isp", "sec", "Engine Specific Impulse"],
    ["Itot", "lbf-sec", "Total Impulse"]
    )

# set Feasible Variables

S.addFeasibleVariable( name="LPYnoz", feasibleVal=maxPYLengine,
        units='in', desc='PY Engine Length',
        controlVar="epsPY", cvMinVal=1.2, cvMaxVal=150.0, cvFailValue=1.2,
        cvUnits='', cvDesc='PY Engine Area Ratio')

S.addFeasibleVariable( name="Lengine", feasibleVal=maxLengine,
        units='in', desc='Axial Engine Length',
        controlVar="eps", cvMinVal=10.0, cvMaxVal=600.0,
        cvUnits='', cvDesc='Axial Engine Area Ratio')
        
S.addFeasibleVariable( name="deltaV", 
        feasibleVal=deltaVReqmt ,
        units='ft/sec', desc='Vacuum Delta Velocity',
        controlVar="WtPropAxial", cvMinVal=10.0, cvMaxVal=600.0,
        cvUnits='lbm', cvDesc='Total Usable Axial Propellant')

# create Mass Items that make up the system
# use scaling from reference engine
Engine = Engine_FFC(name="Axial Engine", 
    oxName='N2O4', fuelName='MMH',
    cxw=cxwFFC, Pc=108.0, Fvac=FvacAxial, eps=epsAxial, mr=mrAxial, 
    CR=2.5, LoverDt=2.0, LchamMin=LchamMinAxial, cxwValves=cxwValves,
    etaERE=etaERECoarse, calcEtaNoz=1, useFastCEALookup=1)

PYEngines = Engine_FFC(name="PY Engines", 
    oxName='N2O4', fuelName='MMH',
    cxw=cxwFFC_ACS, Pc=100.0, Fvac=FvacPY, eps=epsPY, mr=mrPY, 
    CR=2.5, LoverDt=2.0, pcentBell=pcentBellRCS, cxwValves=cxwValves,
    etaERE=etaERECoarseRCS, calcEtaNoz=1, Number=NumPY, useFastCEALookup=1)

RollEngines = Engine_FFC(name="Roll Engines", 
    oxName='N2O4', fuelName='MMH',
    cxw=cxwFFC_ACS, Pc=100.0, Fvac=FvacRoll, eps=epsRoll, mr=mrRoll, 
    CR=2.5, LoverDt=2.0, pcentBell=pcentBellRCS, cxwValves=cxwValves,
    etaERE=etaERECoarseRCS, calcEtaNoz=1, Number=NumRoll, useFastCEALookup=1)


Oxtank = Tank(name="Oxidizer Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=486.0,ell=1.767,rcyltd=1.445,
        ptank=1400.0,sf=1.5,cxw=cxwPropTank_FFC,
        ithcyl=1,kacqui=1,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
        
Fltank = Tank(name="Fuel Tank",  
        matlName="grEpox",   vfree=486.0,ell=1.767,rcyltd=1.445,
        ptank=1400.0,sf=1.5,cxw=cxwPropTank_FFC,
        ithcyl=1,kacqui=1,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
Hetank = Tank(name="Helium Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=1.764,rcyltd=1.142,
        ptank=5000.0,sf=1.5,cxw=1.0,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.065,rholiner=0.101)

# use Helium as pressurant
He = PressurantHe(name="Helium Pressurant",
        PfinHeOvPnom=1.1,
        tAction=tActionMin,TminR=TminOperate,TmaxR=TmaxOperate)
        
# add propellants
Fl = Inc_liquid(symbol="MMH",T=530.0,P=14.7)
Ox = Inc_liquid(symbol="N2O4",T=530.0,P=20.0)

# Lines
FuelRCSLines = Line_Liq(name="RCS Fuel Lines",wdot=1.0, matlName="Ti", 
        liqObj=Fl, Number=NumRCS, Kfactors=10.0, cxw=cxwLines, len_inches=60.0)
OxRCSLines = Line_Liq(name="RCS Ox Lines",wdot=1.0, matlName="Ti", 
        liqObj=Ox, Number=NumRCS, Kfactors=10.0, cxw=cxwLines, len_inches=60.0)
FuelAxLine = Line_Liq(name="Axial Engine Fuel Line",wdot=1.0, matlName="Ti", 
        liqObj=Fl, Number=NumAxial, Kfactors=10.0, cxw=cxwLines, len_inches=24.0)
OxAxLine = Line_Liq(name="Axial Engine Ox Line",wdot=1.0, matlName="Ti", 
        liqObj=Ox, Number=NumAxial, Kfactors=10.0, cxw=cxwLines, len_inches=24.0)


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Oxtank, Fltank, He, Hetank, Engine, PYEngines, RollEngines, 
    Ox, Fl, FuelRCSLines, OxRCSLines, FuelAxLine, OxAxLine, PSRE_misc] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,PHe,MR,WtPropAxial,eps,pcentBell,epsPY = S("Pc","PHe","MR","WtPropAxial","eps","pcentBell","epsPY")

    Engine.Pc = Pc
    Engine.mr = MR
    Engine.eps = eps
    Engine.pcentBell = pcentBell
    Engine.reCalc()
    S["Lengine"] = Engine.Lengine
    
    Itot = WtPropAxial * Engine.Isp
    S["Itot"] = Itot
    
    PYEngines.Pc = Pc
    PYEngines.eps = epsPY
    PYEngines.reCalc()
    S["LPYnoz"] = PYEngines.Lnoz
    RollEngines.Pc = Pc
    RollEngines.eps = epsPY
    RollEngines.reCalc()
    
    ItotRCS = ItotPY + ItotRoll
    WpPY = ItotPY / PYEngines.Isp 
    WpRoll = ItotRoll / RollEngines.Isp
    WpRCS = WpPY + WpRoll
    
    WtOxRCS = WpPY * PYEngines.mr/(1.0+PYEngines.mr) + WpRoll * RollEngines.mr/(1.0+RollEngines.mr)
    WtFlRCS = WpRCS - WtOxRCS
    
    # set line flowrates
    FuelRCSLines.wdot = max( PYEngines.wdotFl, RollEngines.wdotFl )
    OxRCSLines.wdot =   max( PYEngines.wdotOx, RollEngines.wdotOx )
    FuelAxLine.wdot = Engine.wdotFl
    OxAxLine.wdot = Engine.wdotOx
    
        
    # calc derived parameter variables
    WtOx = WtPropAxial * MR/(1.0+MR)
    WtFl = WtPropAxial - WtOx
    
    # start assigning values to Mass Items
    WtOxResid = (WtOx + WtOxRCS) * (1.0 / expulEffOx - 1.0)
    WtFlResid = (WtFl + WtFlRCS) * (1.0 / expulEffFl - 1.0)
    Ox.setMassBreakdown( [('Burned Axial',WtOx),
        ('Burned RCS',WtOxRCS),('Residual',WtOxResid)])
    Fl.setMassBreakdown( [('Burned Axial',WtFl),
        ('Burned RCS',WtFlRCS),('Residual',WtFlResid)])
    Ox.reCalc()
    Fl.reCalc()
    
    Oxtank.vfree = Ox.Volume / (1.0-ullFracOx)
    Fltank.vfree = Fl.Volume / (1.0-ullFracFl)
    
    # get pressure schedule
    FlDeltpP = max( FuelRCSLines.dpLine, FuelAxLine.dpLine ) + Fltank.dpacq
    OxDeltpP = max( OxRCSLines.dpLine, OxAxLine.dpLine )     + Oxtank.dpacq
    maxDeltaDP = max( OxDeltpP, FlDeltpP )
    
    ptank = Pc * 1.25 + 50.0 + maxDeltaDP
    Oxtank.ptank = ptank
    Fltank.ptank = ptank
    FuelRCSLines.pLine = ptank
    OxRCSLines.pLine = ptank
    FuelAxLine.pLine = ptank
    OxAxLine.pLine = ptank
    #print 'ptank,PHe',ptank,PHe
    
    He.PHeTnk =  PHe
    He.PpropNom = ptank
    He.VpropTnk = Oxtank.vfree + Fltank.vfree
    He.reCalc()
    
    Hetank.vfree = He.volHeTotal
    Hetank.ptank = PHe
    S.reCalc()
    #print 'PHe,ptank,Pc,MR',PHe,ptank,Pc,MR
    S["sysMass"] = S.mass_lbm
    S["Isp"] =  Engine.Isp
    
    # treat RCS propellant as inert flow for axial engine Isp (i.e. linear over mission)
    fracIsp = WtPropAxial / (WtPropAxial + WpRCS)
    
    Winit = S.mass_lbm + payload
    Wfinal = S.mass_lbm - WtPropAxial - WpRCS + payload  # RCS propellant is inert loss
    deltaV = gc * Engine.Isp * log( Winit / Wfinal) * fracIsp
    S["deltaV"] = deltaV

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
optimize(S, figureOfMerit="sysMass", desVars=["PHe","Pc"], findmin=1, useCOBYLA=0)

#makeSensitivityPlot(S,figureOfMerit="Lengine", desVars=["PHe","Pc","eps"])
makeSensitivityPlot(S,figureOfMerit="sysMass", desVars=["PHe","Pc","pcentBell"])
S.saveShortSummary()
            
Hetank.texture = Texture( colorName="Gray50" )
Oxtank.texture = Texture( colorName="Aquamarine" )
Fltank.texture = Texture( colorName="Pink" )
        
def myRenderControlRoutine(S):
    rVeh = 20.0
    he = Hetank.getPOV_Item()
    r = rVeh - Hetank.pov_d/2
    he.translate([0,0,r])
    
    fl = Fltank.getPOV_Item()
    r = rVeh - Fltank.pov_d/2
    fl.translate([r*cos(30.*pi/180),0.,-r*sin(30.*pi/180)])
    
    
    ox = Oxtank.getPOV_Item()
    r = rVeh - Oxtank.pov_d/2
    ox.translate([-r*cos(30.*pi/180),0.,-r*sin(30.*pi/180)])
    
    eng = Engine.getPOV_Item()
    eng.rotate([180,0,0])
    eng.translate([0,Engine.Lnoz + Engine.Lcham,0])
    
    #box = POV_Items.Box(corner1=[10,10,10], corner2=[0,0,0])
    #shell = POV_Items.HollowCylinder( OD=rVeh*2. + .2, thickness=0.1, height=18.0,
    #        texture = Texture( colorName="White", transmit=0.7 )    )
    
    povItemL = [he, fl, ox, eng]#, shell]
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)
S.render(view='front',ortho=0)
S.render(view='back',ortho=1, clockX=15, clockY=15)


if 1:
    makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=0, showDelta=0)
    makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=1, showDelta=0)
    # start making carpet plots, etc. of system
    #make2DPlot(S, sysParam="sysMass", desVar="pcentBell")
    makeContourPlot(S, sysParam="sysMass", desVars=["PHe","Pc"])
    #makeContourPlot(S, sysParam="sysMass", desVars=["eps","Pc"])
    makeMassPieCharts(S)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
