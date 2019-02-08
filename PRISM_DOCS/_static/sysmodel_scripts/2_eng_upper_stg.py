from math import *
from prism import *

# set design constants from common Constants values
gc = 32.174 # gravitational conversion factor

DiamVeh = 33.0
LenVeh = 36.0
thkShell = 0.08
LenBosses = 1.5

LtanksAvail = LenVeh - LenBosses

ullFracOx = 0.03
ullFracFl = 0.03

engineIntletOverPc = 1.66 
Wpayload = 20.0

expulEffOx = 0.99
expulEffFl = 0.99

TminOperate = 510.0 # degR
TmaxOperate = 550.0 # degR

NumAxial = 2

NumOxTanks = 2
NumFlTanks = 2
NumHeTanks = 2

etaEREAxial = 0.97    # same as IR&D engine

cxwValves=1.0

cxw_Axial = 1.27

cxwLines = 3.5

cxwPropTank_PMD = 1.32

LchamMinAxial = 2.0


SMX_misc = Misc_Weights(name="SMX misc.", mass_lbm=0.0)

SMX_misc.add_item('Axial Transducer',.14)
SMX_misc.add_item('Axial Install',.45)
SMX_misc.add_item('Axial Engine Insulation',1.0)

SMX_misc.add_item('PSA Install',.34)
SMX_misc.add_item('Ox Tank Outlet Assembly',1.0)
SMX_misc.add_item('Ox Tank Gas Inlet Assembly',1.)
SMX_misc.add_item('Ox Tank bracket, spacer, sensor',2.)
SMX_misc.add_item('Fuel Tank Outlet Assembly',1.0)
SMX_misc.add_item('Fuel Tank Gas Inlet Assembly',1.)
SMX_misc.add_item('Fuel Tank bracket, spacer, sensor',2.)
SMX_misc.add_item('Electrical Install',1.)
SMX_misc.add_item('Cap, Weld - F&D Valves',.05)
SMX_misc.add_item('GSA Install',.24)
SMX_misc.add_item('Gas Valves (Reg, F&D, Iso, Relief, P Switch)',3.)
SMX_misc.add_item('GSA Mount & Assembly',2.)
SMX_misc.add_item('Electrical Cable Install',2.)
SMX_misc.add_item('Squib, Electrical Sep.',.09)
SMX_misc.add_item('Connector, Mech. Sep.',.1)

#SMX_misc.add_item('',)


# create system object (make sure author is correct... it's used for report)
S = SysModel(name="NTO/MMH He, PMD, Cb", type="bi-propellant", 
    author="N. Orbit")


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["PHe",10000.0, 4000.0, 10000.0, 200.0, 'psia', 'Helium Tank Pressure'],
    ["MR",    1.75,    1.0,    2.0,  0.05,    '',  'Engine Mixture Ratio'],
    ["Pc",    250.0, 100.0, 400.0,  20.0, 'psia', 'Engine Chamber Pressure'],
    ["pcentBell",    80.0, 60.0, 100.0,  5.0, '', 'Nozzle Percent Bell'],
    ["eps", 40.0, 10.0, 150., 5., '', 'Axial Nozzle Area Ratio'],
    ['WtPropAxial', 700., 50., 1000., 10.,'lbm','Usable Propellant'],
    ['Ltanks', LtanksAvail, 15., 44., 1.,'in','Tank Length'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["Isp", "sec", "Engine Specific Impulse"],
    ["Lengine",'in','Axial Engine Length'],
    ["Winert",'lbm','System Inert Mass'],
    ["WpropTotal",'lbm','Total Propellant Mass'],
    ['Itot','lbf-sec','Total Impulse'],
    ['massFrac','','Stage Propellant Mass Fraction'],
    ['massFracUsable','','Usable Propellant Mass Fraction'],
    ['geesBO','gees','Burnout Gees'],
    ['DiamPkg','in','Packaged Diameter','<',33.0],
    ['LenPkg','in','Packaged Length','<',LenVeh],
    ['burnTime','sec','Total Burn Time'],
    )


# create Mass Items that make up the system
# use scaling from reference engine
Engine = Engine_FFC(name="Axial Engine", 
    oxName='N2O4', fuelName='MMH',
    cxw=cxw_Axial, Pc=108.0, Fvac=100.0, eps=50.0, mr=1.65, 
    CR=2.5, LoverDt=2.0, LchamMin=LchamMinAxial, cxwValves=cxwValves,
    etaERE=etaEREAxial, calcEtaNoz=1, useFastCEALookup=0, Number=NumAxial)


# make Titanium tanks for Ox, Fuel, and Helium
Oxtank = Tank(name="Oxidizer Tank", makeCompositeTank=1, kalmod=0,  Number=NumOxTanks,
        matlName="grEpox",   vfree=3490.0,ell=1.764,rcyltd=1.5,  # input vfree=3490 cuin to get 3575 total
        ptank=400.0,sf=1.5,cxw=cxwPropTank_PMD, NumExtraBaffles=0, tMinGaugeUser=0.035,
        ithcyl=1,kacqui=6,inpex=1,expefi=0.98,
        tblad=0.0,tbond=0.0,ttrspc=0.0,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
Fltank = Tank(name="Fuel Tank", makeCompositeTank=1, kalmod=0,  Number=NumFlTanks,
        matlName="grEpox",   vfree=3490.0,ell=1.764,rcyltd=1.5,  # input vfree=3490 cuin to get 3575 total
        ptank=400.0,sf=1.5,cxw=cxwPropTank_PMD, NumExtraBaffles=0, tMinGaugeUser=0.035,
        ithcyl=1,kacqui=6,inpex=1,expefi=0.98,
        tblad=0.0,tbond=0.0,ttrspc=0.0,rhoacq=0.098,tliner=0.03,rholiner=0.098)
        
Hetank = Tank(name="Helium Tank", Number=NumHeTanks,
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=1.764,rcyltd=2.0,
        ptank=5000.0,sf=2.0,cxw=1.1,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.065,rholiner=0.101)

Shell = ShellStructure(name="Stage External Shell",
        matlShell="grEpox", matlFlange="Al", 
        OD=DiamVeh, Length=LenVeh,
        thkShell=thkShell, thkFlange=0.1, widthFlange=0.5, cxw=1.0)


# use Helium as pressurant
        
# use Helium as pressurant
He = PressurantHe(name="pressurant helium",  mass_lbm=0.0,
    VpropTnk=1000.0,PHeTnk=6000.0,PpropNom=350.0,
    PfinHeOvPnom=1.1, wtHeACS=0.0,
    tAction=100.0,TminR=TminOperate,TmaxR=TmaxOperate,
    tPolyCorr=750.0, gamPolyCorr=1.4, gamLimPolyCorr=1.0, THeTnkHX=490.0)
        
        
# add propellants
Fl = Inc_liquid(symbol="MMH",T=530.0,P=14.7)
Ox = Inc_liquid(symbol="N2O4",T=530.0,P=20.0)

# Lines
FuelAxLine = Line_Liq(name="Axial Engine Fuel Line",wdot=1.0, matlName="Ti", 
        liqObj=Fl, Number=NumAxial, Kfactors=10.0, cxw=cxwLines, len_inches=24.0,
        velFPS=10.0)
OxAxLine = Line_Liq(name="Axial Engine Ox Line",wdot=1.0, matlName="Ti", 
        liqObj=Ox, Number=NumAxial, Kfactors=10.0, cxw=cxwLines, len_inches=24.0,
        velFPS=10.0)

def getLnozExtension():
    LnozExt = 0.0 # Engine.Lnoz/3.0
    return LnozExt
    

def getR1R2():
    
    clr = 0.25
    S1 = Fltank.OR + clr + Oxtank.OR
    D1 = S1 * sqrt(2.0)
    R1 = D1 / 2.0
    R2 = S1/2.0 + (Hetank.OR + clr + max(Fltank.OR , Oxtank.OR)) * sqrt(2.0) / 2.0
    return R1, R2 # propellant tank radius, HeTank Radius    

#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Oxtank, Fltank, He, Hetank, Engine, 
    Ox, Fl, FuelAxLine, OxAxLine, SMX_misc, Shell] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,PHe,MR,WtPropAxial,eps,pcentBell,Ltanks = \
        S("Pc","PHe","MR","WtPropAxial","eps","pcentBell",'Ltanks')

    Engine.Pc = Pc
    Engine.mr = MR
    Engine.eps = eps
    Engine.pcentBell = pcentBell
    
    #FvacAxial = 305.0 * WtPropAxial / 400.0 / float(Engine.Number) # appriximately 400 sec burn time
    #print 'FvacAxial=',FvacAxial
    #sys.exit()
    Engine.Fvac = 270.0 #  FvacAxial
    
    Engine.reCalc()
    S["Lengine"] = Engine.Lengine
    
    Itot = WtPropAxial * Engine.Isp
    S["Itot"] = Itot
    
    
    burnTime = WtPropAxial / Engine.wdotTot / Engine.Number
    S["burnTime"] = burnTime
    
    # set line flowrates
    FuelAxLine.wdot = Engine.wdotFl * Engine.Number
    OxAxLine.wdot = Engine.wdotOx * Engine.Number
    
        
    # calc derived parameter variables
    WtOx = WtPropAxial * MR/(1.0+MR)
    WtFl = WtPropAxial - WtOx
    
    # start assigning values to Mass Items
    WtOxResid = (WtOx) * (1.0 / expulEffOx - 1.0)
    WtFlResid = (WtFl) * (1.0 / expulEffFl - 1.0)
    Ox.setMassBreakdown( [('Burned Axial',WtOx),
        ('Residual',WtOxResid)])
    Fl.setMassBreakdown( [('Burned Axial',WtFl),
        ('Residual',WtFlResid)])
    Ox.reCalc()
    Fl.reCalc()
    
    WpropTotal = Ox.mass_lbm + Fl.mass_lbm
    
    Oxtank.vfree = Ox.Volume / (1.0-ullFracOx) / NumOxTanks
    Fltank.vfree = Fl.Volume / (1.0-ullFracFl) / NumFlTanks
    
    # get pressure schedule
    FlDeltpP =  FuelAxLine.dpLine  + Fltank.dpacq
    OxDeltpP = OxAxLine.dpLine     + Oxtank.dpacq
    maxDeltaDP = max( OxDeltpP, FlDeltpP )
    
    pcFace = Pc*(1. + 0.25/Engine.CR**1.8)
    
    ptank = pcFace * 1.35 + 75.0 + maxDeltaDP
    
    Oxtank.ptank = ptank
    Fltank.ptank = ptank
    FuelAxLine.pLine = ptank
    OxAxLine.pLine = ptank
    #print 'ptank,PHe',ptank,PHe
    
    # set all tanks to length
    Oxtank.setToLength( Ltanks )
    Fltank.setToLength( Ltanks )

    He.tAction = WtPropAxial / Engine.wdotTot / Engine.Number

    He.PHeTnk =  PHe
    He.PpropNom = ptank
    He.VpropTnk = Oxtank.vfree*NumOxTanks + Fltank.vfree*NumFlTanks
    He.reCalc()
    
    Hetank.ptank = PHe
    Hetank.vfree = He.volHeTotal / Hetank.Number
    
    Hetank.setToLength( Ltanks )
        
    S.reCalc()

    # calc packaged diameter
    R1, R2 = getR1R2()
    Dprop = 2.0 * (R1 + max( Oxtank.OD, Fltank.OD )/2.0)
    Dhe = 2.0 * (R2 + Hetank.OD/2.0)
    DiamPkg = max(Dprop, Dhe) + 2.0*thkShell
    S['DiamPkg'] = DiamPkg

    
    #print 'PHe,ptank,Pc,MR',PHe,ptank,Pc,MR
    S["sysMass"] = S.mass_lbm
    S["WpropTotal"] = WpropTotal
    S["Isp"] =  Engine.Isp
    
    Winert = S.mass_lbm -Ox.mass_lbm -Fl.mass_lbm - He.mass_lbm
    S["Winert"] = Winert
    
    massFracUsable = WtPropAxial / S.mass_lbm
    S['massFracUsable'] = massFracUsable
    
    massFrac = WpropTotal / S.mass_lbm
    S['massFrac'] = massFrac
    
    geesBO = Engine.Fvac * Engine.Number / (Wpayload + S.mass_lbm - WtPropAxial)
    S['geesBO'] = geesBO
    
    LnozExt = getLnozExtension()
    LenPkg = Ltanks + LnozExt + LenBosses
    S['LenPkg'] = LenPkg
    
    
    #print "PHe=",PHe,"Pc=",Pc,"pcentBell=",pcentBell,"eps=",eps
    #print "     massFrac=",massFrac,'Winert=',Winert

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
#optimize(S, figureOfMerit="sysMass", desVars=["PHe","Pc","eps"], findmin=1)

            
Hetank.texture = Texture( colorName="Gray50", reflection=0. )
Oxtank.texture = Texture( colorName="Aquamarine", reflection=0. )
Fltank.texture = Texture( colorName="Pink", reflection=0. )
        
def myRenderControlRoutine(S):
    S.reCalcItems()
    
    R1, R2 = getR1R2()
    
    fl = Fltank.getPOV_Item()
    radj = R1
    domeHt = Fltank.OR/Fltank.ell
    fl.translate([radj,domeHt,0.])
    
    fl2 = Fltank.getPOV_Item()
    fl2.translate([radj,domeHt,0.])
    fl2.rotate( [0.,180.,0.] )
        
    
    ox = Oxtank.getPOV_Item()
    radj = R1
    domeHt = Oxtank.OR/Oxtank.ell
    ox.translate([radj,domeHt,0.])
    ox.rotate( [0.,90.,0.] )

    ox2 = Oxtank.getPOV_Item()
    ox2.translate([radj,domeHt,0.])
    ox2.rotate( [0.,270.,0.] )

    he = Hetank.getPOV_Item()
    radj = R2
    domeHt = Hetank.OR/Hetank.ell
    he.translate([radj,domeHt,0.])
    he.rotate( [0.,45.,0.] )
        
    he2 = Hetank.getPOV_Item()
    he2.translate([radj,domeHt,0.])
    he2.rotate( [0.,225.,0.] )
    
    engs=[]
    ang = 360.0 / NumAxial
    for i in range(NumAxial):
        eng = Engine.getPOV_Item()
        eng.rotate([180,0,0])
        
        hNest = Engine.Lcham + Engine.Lnoz - getLnozExtension() -LenBosses/2.0
        eng.translate( [DiamVeh/2-Engine.Dexit/2. ,hNest,0.] )
        
        eng.rotate( [0.,ang*i-45.,0.0] )
        
        #eng.translate([0.0,heightEng,0])
        #eng.rotate( [0.,90.*i+45.0,0.] )
        engs.append(eng)
        
    Lpackage = max( fl.h, ox.h, he.h ) 
    
    #box = POV_Items.Box(corner1=[10,10,10], corner2=[0,0,0])
    #shell = POV_Items.HollowCylinder( OD=DiamVeh + .2, thickness=0.1, height=LenVeh,
    #        texture = Texture( colorName="White", transmit=0.9, reflection=0. )    )
    
    shell = Shell.getPOV_Item()
    
    shell.translate([0,-LenBosses/2.0,0])
    
    #shell2 = POV_Items.HollowCylinder( OD=DiamVeh + .2 + 12.0, thickness=0.1, height=Lpackage,
    #        texture = Texture( colorName="White", transmit=0.9 )    )

    
    povItemL = [he, fl, ox, shell, he2, fl2, ox2]
        
    for eng in engs:
        povItemL.append( eng )
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)


# now optimize the system... it should match up with the carpet plots.
if 0:
    optimize(S, figureOfMerit="Itot", 
        desVars=["Ltanks",'WtPropAxial','Pc'], findmin=0, useCOBYLA=1)

    
# now calibrate the simple He model
HeInteg = PressurantInteg( name="Helium Pressurant",  mass_lbm=0.0, gas='HE',
        VpropTnk=He.VpropTnk,PGasTnkMEOP=He.PHeTnk,PpropNom=He.PpropNom,
        PfinGasOvPnom=He.PfinHeOvPnom, 
        tAction=He.tAction,TminR=TminOperate,TmaxR=TmaxOperate, ullageFrac=0.03,
        PVoW_Bottle=500000., PVoW_Tank=100000.,
        AccGees=1.0,
        Nbottle=1, ellBottle=1.4, LcylOvDBottle=1.0, Cp_effBottle=0.15, # Cp Ti=.125, Al=.2, Monel=.1
        Ntank=1, ellTank=1.414, LcylOvDTank=1.0, Cp_effTank=0.15,
        CdARegMax=None, dPregulator=50.0, NtimeSteps=400, heatExchangerTout=None,
        WtHeLLACS=He.wtHeACS, QexternalIntoBottle=0.0, velMultTank=1.0, useDBruns=1)

He.calibrate( TfBottle=HeInteg.TfinalGasBot, TfProp=HeInteg.TfinalPropGas )
S.reCalcItems()

S.saveShortSummary()

S.render(view='front',ortho=1,clockX=0, clockY=15)
#S.render(view='back',ortho=1, clockX=15, clockY=15)
S.render(view='top',ortho=0)#,clockX=0, clockY=16)

if 0:
    #makeSensitivityPlot(S,figureOfMerit="Lengine", desVars=["PHe","Pc","eps"])
    makeSensitivityPlot(S,figureOfMerit="massFrac", desVars=["PHe","Pc","pcentBell","eps"], omitViolPts=0)
    makeSensitivityPlot(S,figureOfMerit="Winert", desVars=["PHe","Pc","pcentBell","eps"], omitViolPts=0)
    
    makeSensitivityPlot(S,figureOfMerit="sysMass", desVars=["PHe","Pc","pcentBell","eps"], omitViolPts=0)
    makeSensitivityPlot(S,figureOfMerit="Itot", desVars=["PHe","Pc","pcentBell","eps"], omitViolPts=0)

if 0:
    makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=0, showDelta=0)
    makeMassItemSensitivityPlot(S, desVar="Pc", excludePropellant=0, showDelta=1)
    # start making carpet plots, etc. of system
    #make2DPlot(S, sysParam="sysMass", desVar="pcentBell")
    #makeContourPlot(S, sysParam="sysMass", desVars=["PHe","Pc"])
    #makeContourPlot(S, sysParam="sysMass", desVars=["eps","Pc"])
    makeMassPieCharts(S)

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
