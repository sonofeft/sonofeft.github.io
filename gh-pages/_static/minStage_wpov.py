

from math import *
from prism import *

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Sample Case", type="liquid", 
    author="Charlie Taylor", programName="PRISM Docs")


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ['Pc',500,350,650,25,'psia','Chamber Pressure'],
    ['PHe',8000,6000,10000,200,'psia','Helium MEOP'],
    ['WtPropBurned',100,50,200,10,'lbm','Burned Propellant Mass'],
    ['eps',10,5,20,1,'','Nozzle Area Ratio'],
    ['pcentBell',70,60,90,1.5,'','Nozzle Percent Bell'],
    )


# now add any Result Variables That might be plotted
# "sysMass" is required
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ['Lstage','in','Stage Length','<',65],
    ['Dexit','in','Nozzle Diameter','<',10],
    ['deltaV','ft/sec','Ideal Delta V'],
    ['Itot','lbf-sec','Total Impulse'],
    ['sysMass','lbm','Total System Mass'],
    )



MR = 1.8 # Engine Mixture Ratio
FAxial = 3000.0 # lbf, Engine Thrust
Wpayload = 100.0 # lbm, Payload Mass
pcentACS = 5.0 # %, Percent of Propellant Used for ACS

oxName = 'N2O4'
fuelName = "MMH"

DiamVeh = 10.0 # in
clearance = 0.25 # in

# mass multipliers
cxwEngineVlv = 0.33
cxwPropTank_FFC = 1.5
cxwHeTank =  6.95 / 5.056

TminOperate = 500.0 # degR, The minimum operating temperature
TmaxOperate = 550.0 # degR, The maximum operating temperature
expulEffOx = 0.99
expulEffFl = 0.99
ullFracOx = 0.03
ullFracFl = 0.03

etaERE = 0.955

# stage axial engine
EngineAxial = Engine_FFC(name="Axial Engine", 
    oxName=oxName, fuelName=fuelName, Number=1,
    cxw=1.0, Pc=500.0, Fvac=4000.0, eps=20.0, mr=1.0, 
    CR=2.5, LoverDt=2.0, LchamMin=2.0, cxwValves=cxwEngineVlv,
    etaERE=etaERE, calcEtaNoz=1, useFastCEALookup=1,isBell=1, pcentBell=70.0,
    halfAngDeg=15.0, xlnOverLcham=0.9 )

# stage ACS engines
EngineACS = Engine_FFC(name="ACS Engines", 
    oxName=oxName, fuelName=fuelName, Number=4,
    cxw=1.0, Pc=500.0, Fvac=40.0, eps=10., mr=1.0, 
    CR=2.5, LoverDt=2.0, LchamMin=1.0, cxwValves=cxwEngineVlv,
    etaERE=0.94, calcEtaNoz=1, useFastCEALookup=1,isBell=1, pcentBell=80.0,
    halfAngDeg=15.0, xlnOverLcham=0.9 )

# oxidizer tank
Oxtank = Tank(name="Oxidizer Tank", Number=1,
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=486.0,ell=1.6,rcyltd=1.445,
        ptank=1400.0,sf=1.5,cxw=cxwPropTank_FFC,
        ithcyl=1,kacqui=6,inpex=1,expefi=expulEffOx,
        tblad=0.0,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
# fuel tank
Fltank = Tank(name="Fuel Tank",  Number=1,
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=486.0,ell=1.6,rcyltd=1.445,
        ptank=1400.0,sf=1.5,cxw=cxwPropTank_FFC,
        ithcyl=1,kacqui=6,inpex=1,expefi=expulEffFl,
        tblad=0.0,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
# helium tank
Hetank = Tank(name="Helium Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=1.6,rcyltd=1.142,
        ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=1,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.065,rholiner=0.101)
        
        
# use Helium as pressurant
He = PressurantHe(name="pressurant helium",  mass_lbm=0.0,
    VpropTnk=1000.0,PHeTnk=6000.0,PpropNom=350.0,
    PfinHeOvPnom=1.1, wtHeACS=0.0,
    tAction=100.0,TminR=TminOperate,TmaxR=TmaxOperate,
    tPolyCorr=750.0, gamPolyCorr=1.4, gamLimPolyCorr=1.0, THeTnkHX=490.0)
        
# add propellants
Fl = Inc_liquid(symbol=fuelName,T=TmaxOperate,P=14.7)
Ox = Inc_liquid(symbol=oxName,T=TmaxOperate,P=30.0)


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( Oxtank, Fltank,  He, Hetank,  EngineAxial, EngineACS, Ox, Fl )



# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,PHe,WtPropBurned,eps,pcentBell = S.getDesVars("Pc","PHe","WtPropBurned","eps","pcentBell")

    # start ENGINEERING logic here (like a PRISM control routine)
    # calc axial and acs propellants
    WpRCS = WtPropBurned * pcentACS / 100.0
    WpAxial = WtPropBurned - WpRCS
    # calc Ox and Fuel portions of axial and acs propellants
    WtOxRCS = WpRCS / 2.0
    WtFlRCS = WpRCS - WtOxRCS
    WtOxAxial = WpAxial * MR/(1.0+MR)
    WtFlAxial = WpAxial - WtOxAxial
    # calc residual propellants  (can you explain the eqn?)
    WtOxResid = (WtOxAxial + WtOxRCS) * (1.0 / expulEffOx - 1.0)
    WtFlResid = (WtFlAxial + WtFlRCS) * (1.0 / expulEffFl - 1.0)
    # tell propellant objects about the breakdown
    Ox.setMassBreakdown( [('Burned Axial',WtOxAxial),
        ('Burned RCS',WtOxRCS),('Residual',WtOxResid)])
    Fl.setMassBreakdown( [('Burned Axial',WtFlAxial),
        ('Burned RCS',WtFlRCS),('Residual',WtFlResid)])
    Ox.reCalc()    # <=== need current values, so reCalc
    Fl.reCalc()    # <=== need current values, so reCalc

    # set engine parameters (both axial and acs)
    EngineAxial.Pc = Pc
    EngineAxial.mr = MR
    EngineAxial.eps = eps
    EngineAxial.Fvac = FAxial
    EngineAxial.pcentBell = pcentBell
    EngineAxial.reCalc()    # <=== need current values, so reCalc

    EngineACS.Pc = Pc

    Itot = WpAxial * EngineAxial.Isp # Total Impulse lbf-sec
    Dexit = EngineAxial.Dexit

    # inside FORTRAN tank routine...
    #  Vtank = Vfree + Vresid + Vacqui + Vliner, so Vfree is...
    Oxtank.vfree = (ullFracOx + expulEffOx) * Ox.Volume / Oxtank.Number
    Fltank.vfree = (ullFracFl + expulEffFl) * Fl.Volume / Fltank.Number    

    # get pressure schedule
    ptank = Pc * 1.3 + 150.0
    Oxtank.ptank = ptank
    Fltank.ptank = ptank

    # size tanks to fit diameter envelope
    Fltank.setToMaxOD( ODmax=DiamVeh)
    Oxtank.setToMaxOD( ODmax=DiamVeh)

    # give pressurization routine what it needs
    He.PHeTnk =  PHe
    He.PpropNom = ptank
    He.VpropTnk = Oxtank.vfree*Oxtank.Number + Fltank.vfree*Fltank.Number
    He.tAction = WpAxial / EngineAxial.wdotTot
    He.reCalc()

    # Set helium tank sizes based on helium volume
    Hetank.vfree = He.volHeTotal / Hetank.Number
    Hetank.ptank = PHe
    # size helium tank to fit diameter envelope
    Hetank.setToMaxOD( ODmax=DiamVeh)

    S.reCalc()

    # figure out package Length
    Lstage =  Fltank.OH + Oxtank.OH + Hetank.OH  + EngineAxial.Lengine + clearance*3.0
    MassStage = S.mass_lbm
    
    massFraction = WtPropBurned / MassStage

    Winit = MassStage + Wpayload
    Wfinal = MassStage + Wpayload - WtPropBurned

    fracIsp = WpAxial / WtPropBurned

    deltaV = 32.174 * fracIsp * EngineAxial.Isp * log( Winit / Wfinal )


    # "sysMass" is required
    S.setResultVar("sysMass", S.mass_lbm)
    S.setResultVar("Lstage", Lstage)
    S.setResultVar("Dexit", Dexit)
    S.setResultVar("deltaV", deltaV)
    S.setResultVar("Itot", Itot)    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

    
Hetank.texture = Texture( colorName="Gray50", reflection=0. )
Oxtank.texture = Texture( colorName="Aquamarine", reflection=0. )
Fltank.texture = Texture( colorName="Pink", reflection=0. )

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
optimize(S, figureOfMerit="deltaV", desVars=['Pc', 'PHe', 'WtPropBurned', 'eps', 'pcentBell'], findmin=0)

S.saveShortSummary()

def myRenderControlRoutine(S):
    S.reCalcItems()
    Lstage = S.getResultVar("Lstage")

    rVeh = DiamVeh / 2.0
    
    eng = EngineAxial.getPOV_Item()
    eng.rotate([180,0,0])
    hadj = EngineAxial.Lengine - EngineAxial.Dcham
    eng.translate([0.,hadj,0.])

    # calculate dome and cyl heights
    hdomeFl = Fltank.OR/Fltank.ell    
    hdomeOx = Oxtank.OR/Oxtank.ell    
    hdomeHe = Hetank.OR/Hetank.ell    
    
    hcylFl = Fltank.OH - hdomeFl*2.
    hcylOx = Oxtank.OH - hdomeOx*2.
    
    # position all three tanks
    fl = Fltank.getPOV_Item()
    domeHt = Fltank.OR/Fltank.ell
    hadj = EngineAxial.Lengine + domeHt
    fl.translate([0.,hadj,0.])
    
    ox = Oxtank.getPOV_Item()
    hadj += hdomeFl + hcylFl + hdomeOx + clearance
    ox.translate([0.,hadj,0.])

    he = Hetank.getPOV_Item()
    hadj += hdomeOx + hcylOx + hdomeHe + clearance
    he.translate([0.,hadj,0.])
    
    
    shell = POV_Items.HollowCylinder( OD=DiamVeh+clearance, thickness=clearance/4.0, height=Lstage,
            texture = Texture( colorName="White", transmit=0.9, reflection=0. )    )

    return [ eng, fl, ox, he, shell ]
    
    
S.setRenderControlRoutine(myRenderControlRoutine)
S.render(view='front')

makeSensitivityPlot(S, 
    figureOfMerit="deltaV", desVars=['Pc', 'PHe', 'WtPropBurned', 'eps', 'pcentBell'],
    makeHTML=1, dpi=100, linewidth=2)


make2DParametricPlot(S, sysParam="deltaV", desVar="Pc",
    paramVar=["eps",5.,10.,15.,20.]  ,makeHTML=1, dpi=100, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)


# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
