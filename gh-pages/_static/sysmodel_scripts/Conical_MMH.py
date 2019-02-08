from math import *
from prism import *

USE_CONICAL_HE = 0

oxName = 'N2O4'
fuelName = "MMH"

SPACE = 0.1
coneAngleDeg = asin( 3.0 / 20.0 ) * 180.0 / pi / 2.0
RbigOvrRsml = (8.4-1.) / (5.4-1.)

nomWtProp = 9.818
residualProp = 0.517
residualOx = residualProp * 0.9
residualFl = residualProp - residualOx

Pbottle = 10000.0

LchamMinDivert = 1.4 #in
etaERE=0.9141  # low to account for big FFC and 95% pulsing

tActionMin = 100.0 # sec
TminOperate = 510.0 # degR
TmaxOperate = 550.0 # degR

mrACS = 1.0
expulEffOx = (nomWtProp-residualOx)/nomWtProp
expulEffFl = (nomWtProp-residualFl)/nomWtProp
ullFracOx = 0.03
ullFracFl = 0.03

pressTankEllRatio = 1.6 # ponzo is using 1.6 NOT 1.7
apexTankEllRatio = 1.6 # 1.67
cxwApexRoller = 2.236
cxwHeTank =  (6.95 / 5.056) * (2.44/2.645)

LbossAndACS = 1.0 
    
tankOH = 20.0 - LbossAndACS # leave room for bosses etc.
thkOuterWall = 0.55

DiamVehAtEngines = 2.0*(8.4+5.4)/2.0
RvehAtEngines = DiamVehAtEngines / 2.0

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="%s/%s Conical KV"%(oxName,fuelName), 
             type="bi-propellant", constraintTolerance=0.005,
             author="Prymatt Conehead")


# have some wt change for blowdown system
EXTRA_misc = Misc_Weights(name="Misc. Wt", mass_lbm=0.0)
#EXTRA_misc.add_item('Harnesses and Fasteners',0.25)  included in engine model
EXTRA_misc.add_item('Ox and Fuel Service Valves',2*0.06)
EXTRA_misc.add_item('Ox and Fuel Burst Disks',2*0.055)
EXTRA_misc.add_item('Pressure Transducers',2*0.02)
EXTRA_misc.add_item('He Controls (pyro, reg, etc.)',1.659)
EXTRA_misc.add_item('Electronics & Harnesses',2.0*.219)

#EXTRA_misc.add_item('',0.)


Pay = SimpleEqnMass(name="Payload Mass", type="inert",  
    eqn="21.67", desc='Payload Mass')

Margin = SimpleEqnMass(name="Margin Mass", type="inert", eqn="0.035*20.0", desc='Margin Mass')

Tubing = SimpleEqnMass(name="Tubing", type="inert", eqn="0.19", desc='Tubing for Ox, Fuel and He')

ACS =  SimpleEqnMass(name="ACS Engines + Mounts", type="inert", eqn="0.56 + 0.26 + 0.15", desc='HLACS and LLACS Engines')

ManBlock = SimpleEqnMass(name="Manifold Block", type="inert", eqn="1.0", desc='Manifold Block')

DivStruct = SimpleEqnMass(name="Divert Structure", type="inert", eqn="1.1", desc='Divert Structure')

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description

WtPropInit = 48.0

S.addDesVars(
    ["PHe",Pbottle, 4000.0, Pbottle, 200.0, 'psia', 'Helium Tank Pressure'],
    ["Pc",    375.0, 350.0, 1000.0,  20.0, 'psia', 'Engine Chamber Pressure'],
    ["MR",    1.68, 0.8, 2.0,  0.02, '', 'Engine Mixture Ratio'],
    ["Wpayload",21.67,5.0,40.0,2.0,'lbm','Payload Mass'],  # 2.0*16.54
    ["pcentACS",5.0,0.0,10.0,0.2,'%','HLACS Percent of Total Impulse'],
    ["pcentBell",80.0,60.0,80.0,2.0,'%','Percent Bell Nozzle Contour'],
    ["WtProp",WtPropInit,nomWtProp,80.0,2.0,'lbm','Usable Divert Propellant Mass'],
    ["Fdivert",202.0,50.0,250.0,10.0, "lbf", "Divert Thrust"],
    ['apexTankEllRatio',apexTankEllRatio,1.4,3.0,.1,'','Apex Tank Ellipse Ratio'],
    ['pressTankEllRatio',pressTankEllRatio,1.4,3.0,.1,'','Pressure Tank Ellipse Ratio'],
    )

    #["Fdivert",200.0,50.0,250.0,10.0, "lbf", "Divert Thrust"],
    #["geesEnd",nomGeesEnd,1.0,8.0,1.0, "gees", "Desired Divert Gees"],

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Propulsion System Mass"],
    ["Isp", "sec", "Divert Engine Specific Impulse"],
    ["IspAxial", "sec", "Axial Engine Specific Impulse"],
    ["Itot", "lbf-sec", "Total Impulse"],
    ["Lpackage", "in", "Total KV Length"],
    ["Ptank", "psia", "Propellant Tank Pressure"],
    ["deltaV", "ft/sec", "Total Vacuum Delta V"],
    ["deltaV_SI", "m/sec", "Total Vacuum Delta V"],
    ["deltaV_Divert", "ft/sec", "Divert Vacuum Delta V"],
    ["deltaV_SI_Divert", "m/sec", "Divert Vacuum Delta V"],
    ["deltaV_Axial", "ft/sec", "Axial Vacuum Delta V"],
    ["deltaV_SI_Axial", "m/sec", "Axial Vacuum Delta V"],
    ['AreaRatioDivert', '', 'Divert Nozzle Area Ratio'],
    ['AreaRatioAxial', '', 'Axial Nozzle Area Ratio'],
    ["DACSMass",  'lbm', 'DACS Mass','<',81.0],
    ["endGameGeesPhi45",'gees','End Game Gees at phi=45'],
    ['lcylOvDox','','Lcyl/Diam Ox Tank'],
    ['lcylOvDfuel','','Lcyl/Diam Fuel Tank'],
    ['htBlock','in','Height of IVA Block'],
    ['tBurnAxial','sec','Total Axial Engine Burn Time'],
    ['LenEngineGoal','in','Divert Nozzle + Chamber Length'],
    )


#S.addFeasibleVariable( name="geesOverGoal", 
#        feasibleVal=1.0 ,
#        units='', desc='Gees / Gees Desired',
#        controlVar="Fdivert", cvMinVal=1.0, cvMaxVal=800.0,
#        cvUnits='lbf', cvDesc='Divert Engine Thrust')


# create Mass Items that make up the system
# use scaling from reference engine
EngineDivert = Engine_FFC(name="Divert Engine", matlInj="Ti",
    oxName=oxName, fuelName=fuelName, Number=4,
    cxw=0.9, Pc=516.0, Fvac=200.0, eps=25.0, mr=1.0, 
    CR=2.5, LoverDt=2.0, LchamMin=LchamMinDivert, cxwValves=1.0,
    etaERE=etaERE*297.68/290.074, calcEtaNoz=1, useFastCEALookup=0,isBell=1, pcentBell=70.0,
    halfAngDeg=15.0, xlnOverLcham=0.9, valvesMassInput=0.36/4.0,
    inputIspDel=0, IspDel=300.)

EngineAxial = Engine_FFC(name="Axial Engine", matlInj="Ti",
    oxName=oxName, fuelName=fuelName, Number=2,
    cxw=0.9, Pc=516.0, Fvac=200.0, eps=25.0, mr=1.0, 
    CR=2.5, LoverDt=2.0, LchamMin=LchamMinDivert, cxwValves=1.0,
    etaERE=etaERE*297.68/290.074, calcEtaNoz=1, useFastCEALookup=0,isBell=1, pcentBell=70.0,
    halfAngDeg=15.0, xlnOverLcham=0.9, valvesMassInput=0.36/4.0,
    inputIspDel=0, IspDel=300.)


Oxtank = Tank_Conical( name="Oxidizer Tank",  mass_lbm=0.0, 
        coneAngleDeg=coneAngleDeg, RbigOvrRsml=RbigOvrRsml,
        makeCompositeTank=0,kalmod=0, matlName="Ti",  Cp_eff=0.15, # Cp Ti=.125, Al=.2, Monel=.1
        tMinGaugeUser=0.0,
        vfree=1000.0,ell=1.414,ptank=350.0,
        sf=1.5,cxw=1.25,  NumExtraBaffles=0,
        ithcyl=1,kacqui=1,inpex=0,expefi=0.99, Number=2,
        inpTblad=1, tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.28,tliner=0.0,rholiner=0.1)

Fltank = Tank_Conical( name="Fuel Tank",  mass_lbm=0.0, 
        coneAngleDeg=coneAngleDeg, RbigOvrRsml=RbigOvrRsml,
        makeCompositeTank=0,kalmod=0, matlName="Ti",  Cp_eff=0.15, # Cp Ti=.125, Al=.2, Monel=.1
        tMinGaugeUser=0.0,
        vfree=1000.0,ell=1.414,ptank=350.0,
        sf=1.5,cxw=1.25,  NumExtraBaffles=0,
        ithcyl=1,kacqui=1,inpex=0,expefi=0.99, Number=2,
        inpTblad=1, tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.28,tliner=0.0,rholiner=0.1)


if USE_CONICAL_HE:
    Hetank = Tank_Conical( name="Perimeter Helium Tank",  mass_lbm=0.0, 
        coneAngleDeg=coneAngleDeg, RbigOvrRsml=1.4,
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=pressTankEllRatio,
        ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=4,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.035,rholiner=0.101)
else:        
    Hetank = Tank(name="Helium Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=pressTankEllRatio,rcyltd=1.142,
        ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=4,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.035,rholiner=0.101)

HetankCenter    = Tank(name="Center Helium Tank", 
    makeCompositeTank=1, kalmod=0,  
    matlName="grEpox",   vfree=160.0, ell=pressTankEllRatio,rcyltd=1.142,
    ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=1,
    ithcyl=1,kacqui=0,inpex=0,
    tbond=0.030,rhobnd=0.04,tliner=0.035,rholiner=0.101)

# use Helium as pressurant
He = PressurantHe(name="Helium Pressurant", THeTnkHX=450.0, # results of TankPressurize
        PfinHeOvPnom=1.0,  tPolyCorr=200.0, gamPolyCorr=1.2, gamLimPolyCorr=1.18,
        tAction=tActionMin,TminR=TminOperate,TmaxR=TmaxOperate)
        
# add propellants
Fl = Inc_liquid(symbol=fuelName,T=530.0,P=14.7)
Ox = Inc_liquid(symbol=oxName,T=530.0,P=20.0)


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Oxtank, Fltank,  He, Hetank, HetankCenter,  EngineDivert, EngineAxial,
    Margin, Pay, Tubing, ACS, ManBlock, DivStruct,
    Ox, Fl, EXTRA_misc] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,PHe,WtProp,MR,pcentBell,Wpayload,Fdivert,pcentACS,pcentBell,\
        apexTankEllRatio,pressTankEllRatio = \
        S("Pc","PHe", "WtProp", "MR",'pcentBell','Wpayload',\
        'Fdivert','pcentACS','pcentBell','apexTankEllRatio',\
        'pressTankEllRatio')

    
    # get pressure schedule
    ptank = Pc * 1.6 + 400.0
    S["Ptank"] = ptank
    
    Oxtank.ptank = ptank
    Fltank.ptank = ptank
    
    Oxtank.ell = apexTankEllRatio
    Fltank.ell = apexTankEllRatio
    Hetank.ell = pressTankEllRatio
    HetankCenter.ell = pressTankEllRatio
        
    # calc derived parameter variables
    WtOx = WtProp * MR/(1.0+MR)
    WtFl = WtProp - WtOx
    
    # estimate vehicle diameter
    Fltank.vfree = (1.0 + pcentACS/100.0) * WtFl / Fl.rho / (1.0-ullFracFl) / Fltank.Number / expulEffFl
    #Fltank.setToOH( tankOH )

    Oxtank.vfree = (1.0 + pcentACS/100.0) * WtOx / Ox.rho / (1.0-ullFracOx) / Oxtank.Number / expulEffOx
    #Oxtank.setToOH( tankOH )

    # calc engine performance and size
    EngineDivert.LchamMin = 1.4 
    EngineDivert.Pc = Pc
    EngineDivert.mr = MR
    EngineDivert.Fvac = Fdivert
    EngineDivert.pcentBell = pcentBell
    
    #EngineDivert.valvesMassInput = (0.36/4.0) * (Fdivert/225.0)**0.5 # let valve mass scale a little
    EngineDivert.valveMassInput = 40.0/454.0 
    EngineDivert.reCalc()    
    
    # set up axial engine
    EngineAxial.LchamMin = 1.4 
    EngineAxial.Pc = Pc
    EngineAxial.mr = MR
    EngineAxial.Fvac = Fdivert
    EngineAxial.pcentBell = 80.0
    EngineAxial.valveMassInput = 40.0/454.0 
    EngineAxial.reCalc()    

    # calc axial engine area ratio
    def newLengAxial( e ):
        EngineAxial.eps = e
        EngineAxial.reCalc()
        return EngineAxial.Dexit
        
    epsMax = 50.0
    G = Goal(goalVal=3.3, minX=1.1, maxX=epsMax, 
        funcOfX=newLengAxial, tolerance=1.0E-5, maxLoops=40, failValue=epsMax)
    eps, ierror = G()
    EngineAxial.eps = eps
    EngineAxial.reCalc()
    
    
    Pay.eqn = '%g'%Wpayload
    Margin.eqn = '0.0'

    # calc divert engine area ratio
    def newLeng( e ):
        EngineDivert.eps = e
        EngineDivert.reCalc()
        return EngineDivert.Lnoz + EngineDivert.Lcham

    
    wBlock = 1.5 * EngineDivert.Dcham  # 2.25
    LenEngineGoal = (DiamVehAtEngines - wBlock)/2.0
    

    epsMax = 30.0
    G = Goal(goalVal=LenEngineGoal, minX=1.1, maxX=epsMax, 
        funcOfX=newLeng, tolerance=1.0E-5, maxLoops=40, failValue=epsMax)
    eps, ierror = G()
    EngineDivert.eps = eps
    
    EngineDivert.reCalc()
    
    
    Itot = WtProp * EngineDivert.Isp
    S["Itot"] = Itot
    
    WpRCS = pcentACS * Itot / 200.0 / 100.0
    
    WtFlRCS = WpRCS/(1.0 + mrACS)
    WtOxRCS =  WpRCS-WtFlRCS
    
    
    # start assigning values to Mass Items
    WtOxResid = (WtOx + WtOxRCS) * (1.0 / expulEffOx - 1.0)
    WtFlResid = (WtFl + WtFlRCS) * (1.0 / expulEffFl - 1.0)
    Ox.setMassBreakdown( [('Burned Divert',WtOx),
        ('Burned RCS',WtOxRCS),('Residual',WtOxResid)])
    Fl.setMassBreakdown( [('Burned Divert',WtFl),
        ('Burned RCS',WtFlRCS),('Residual',WtFlResid)])
    Ox.reCalc()
    Fl.reCalc()
    
    # size tanks with all propellant 
    Oxtank.vfree = Ox.Volume / (1.0-ullFracOx) / Oxtank.Number
    Fltank.vfree = Fl.Volume / (1.0-ullFracFl) / Fltank.Number    
    
    
    #Fltank.setToOH( tankOH )
    #Oxtank.setToOH( tankOH )
    
    S['lcylOvDox'] = Oxtank.cyl / Oxtank.dinsid
    S['lcylOvDfuel'] = Fltank.cyl / Fltank.dinsid

        
    # Itot of helium LLACS (if bowtie, make sure to degrade Isp from 140 to 140*cos45 )
    He.wtHeACS = 0.0 #ItotLLACS / 140.0
    
    He.PHeTnk =  PHe
    He.PpropNom = ptank
    He.VpropTnk = (Oxtank.vfree*Oxtank.Number + Fltank.vfree*Fltank.Number) * 1.03 # SF
    He.reCalc()
    
    # figure out He tank geom
    Hetank.vfree = He.volHeTotal / (Hetank.Number + 1.5*HetankCenter.Number)
    HetankCenter.vfree = Hetank.vfree * 1.5
    Hetank.ptank = PHe
    HetankCenter.ptank = PHe
    if USE_CONICAL_HE:
        Hetank.reCalc()  # reCalc done in setToMaxID
        HetankCenter.cxw = 0.0
    else:
        Hetank.setToMaxOH( 8.5 )
        #Hetank.setToMaxOD( ODmax=3.6, rcyltdMin=0.0)
        HetankCenter.setToMaxOD( ODmax=3.8, rcyltdMin=0.0)
    

    # figure out package Length
    htBlock = 2.746 * EngineDivert.Dcham
    wBlock = htBlock * 2.25/2.5
    #volBlock = htBlock * wBlock**2
    ManBlock.eqn = '%g * %g**2 * 0.16 / 2.0'%(htBlock, wBlock)
    
        
    # include fwd and aft bosses and ACS additions to Lpackage 
    Lpackage =  Oxtank.OH + LbossAndACS
    
    DivStruct.eqn = '3.449  * (%g/9.0) '%(DiamVehAtEngines, )
    #print 'Lpackage =',Lpackage
    #Lpackage = 3.9*(DiamVehAtEngines/10.0) + Oxtank.OH + Fltank.OH + Hetank.OH - Fltank.OR
    
    # create simple equations
    Tubing.eqn = '0.19 * (%g + %g) / (10.0 + 18.0)'%(DiamVehAtEngines, Lpackage )
    
    ACS.eqn = '1.333' # '(0.56 + 0.26 + 0.15) * (%g/225.0)**0.5'%Fdivert
 
    S.reCalc()
    Margin.eqn = '0.058*%g'%(S.mass_lbm-Wpayload-Fl.mass_lbm-Ox.mass_lbm-He.mass_lbm,)
    S.reCalc()
    
    #print 'PHe,ptank,Pc,MR',PHe,ptank,Pc,MR
    S["sysMass"] = S.mass_lbm
    
    WtExpended = (WtProp + WpRCS + He.wtHeACS)
    fracIsp = WtProp / WtExpended
    Wburnout = (S.mass_lbm-WtExpended)
    
    deltaV = 32.174 * fracIsp * EngineDivert.Isp * log( S.mass_lbm / Wburnout )
    deltaV_SI = deltaV / 3.281    
    S['deltaV'] = deltaV
    S['deltaV_SI'] = deltaV_SI
    
    WiDivert = Wburnout * exp(500.0*3.281/32.174/fracIsp/EngineDivert.Isp)
    WpDivert = WiDivert - Wburnout
    WpAxial = S.mass_lbm - WiDivert
    tBurnAxial = WpAxial * fracIsp / EngineAxial.wdotTot / 2.0

    deltaV_Divert = 32.174 * fracIsp * EngineDivert.Isp * log( WiDivert / Wburnout )
    deltaV_SI_Divert = deltaV_Divert / 3.281    
    
    deltaV_Axial = 32.174 * fracIsp * EngineAxial.Isp * log( S.mass_lbm / WiDivert )
    deltaV_SI_Axial = deltaV_Axial / 3.281    

    S['deltaV_Divert'] = deltaV_Divert
    S['deltaV_SI_Divert'] = deltaV_SI_Divert
    S['deltaV_Axial'] = deltaV_Axial
    S['deltaV_SI_Axial'] = deltaV_SI_Axial
    S['tBurnAxial'] = tBurnAxial

    S['DACSMass'] = S.mass_lbm - Wpayload
    
    S["Isp"] =  EngineDivert.Isp
    S['AreaRatioDivert'] = EngineDivert.eps

    S["IspAxial"] =  EngineAxial.Isp
    S['AreaRatioAxial'] = EngineAxial.eps

    endGameGeesPhi45 = sqrt(2.0) * Fdivert / (S.mass_lbm - WtProp )
    
    S["endGameGeesPhi45"] = endGameGeesPhi45
    #S["GeeRatio"] = GeeRatio
    
    S["Lpackage"] = Lpackage
    
    S['htBlock'] = htBlock
    S['LenEngineGoal'] = LenEngineGoal
    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
#optimize(S, figureOfMerit="endGameGeesPhi45", desVars=["Fdivert"], findmin=1)
#optimize(S, figureOfMerit="SizeWtLimit", desVars=['WtProp'], findmin=0)

# ============== find design point for 1000 ft/sec ==============
if 0:
    def getDeltaV( Wp ):
        S.setDesignVar('WtProp', Wp)
        S.evaluate()
        print 'dv=',S.getResultVar('deltaV'),'   for Wp=',Wp
        return S.getResultVar('deltaV')
                    
    G = Goal(goalVal=1000.0, minX=1.1, maxX=4.0, 
        funcOfX=getDeltaV, tolerance=1.0E-5, maxLoops=40, failValue=4.0)
    Wp, ierror = G()
    S.setDesignVar('WtProp', Wp)
# ============  set to discovered deltaV point ========

            
Hetank.texture = Texture( colorName="Gray50", reflection=0. )
HetankCenter.texture = Texture( colorName="Gray50", reflection=0. )

Oxtank.texture = Texture( colorName="Aquamarine", reflection=0. )
Fltank.texture = Texture( colorName="Pink", reflection=0. )
        
def myRenderControlRoutine(S):
    S.reCalcItems()
    
    HeightVeh = S.getResultVar('Lpackage')

    rVeh = DiamVehAtEngines / 2.0
    rVehMax = 8.4
    
    fl = Fltank.getPOV_Item()
    radj = rVehMax - Fltank.OR + SPACE/2.0
    hadj = Fltank.OR / Fltank.ell  + LbossAndACS/2.
    fl.rotate( [0.,0.,coneAngleDeg] )
    fl.translate([radj,hadj,0.])
    
    fl2 = Fltank.getPOV_Item()
    fl2.rotate( [0.,0.,coneAngleDeg] )
    fl2.translate([radj,hadj,0.])
    fl2.rotate( [0.,180.,0.] )
    
    heightEng = 1.0 + HeightVeh / 2.0
    
    ox = Oxtank.getPOV_Item()
    radj = rVehMax - Oxtank.OR + SPACE/2.0
    hadj = Oxtank.OR / Oxtank.ell + LbossAndACS/2.
    ox.rotate( [0.,0.,coneAngleDeg] )
    ox.translate([radj,hadj,0.])
    ox.rotate( [0.,90.,0.] )

    ox2 = Oxtank.getPOV_Item()
    ox2.rotate( [0.,0.,coneAngleDeg] )
    ox2.translate([radj,hadj,0.])
    ox2.rotate( [0.,270.,0.] )


    # make the helium tanks
    heTankL = []
    dAng = 360.0 / Hetank.Number
    ang = 45.0
    for N in range(Hetank.Number):
        he = Hetank.getPOV_Item()
        radj = 8.4 - Hetank.OR - SPACE/2.0
        domeHt = Hetank.OR/Hetank.ell #+ (HeightVeh-Hetank.OH)
        if USE_CONICAL_HE:
            he.rotate( [0.,0.,coneAngleDeg] )
        else:
            he.rotate( [0.,0.,2.0*coneAngleDeg] )
        he.translate([radj,domeHt,0.])
        he.rotate( [0.,ang,0.] )
        ang += dAng
        heTankL.append( he )
    
    if not USE_CONICAL_HE:
        he = HetankCenter.getPOV_Item()
        hadj = HeightVeh - HetankCenter.OH + HetankCenter.OR/HetankCenter.ell
        he.translate([0.,hadj,0.])
        heTankL.append( he )


    engs=[]
    for i in range(4):
        eng = EngineDivert.getPOV_Item()
        eng.rotate([180,0,0])
        
        #radLoc = EngineDivert.Dcham/2.0 #- EngineDivert.Lengine  + EngineDivert.Dt/1.414/2.0 - 0.2
        radLoc = EngineDivert.Dcham # DiamVehAtEngines/2.0 - EngineDivert.Lengine
        #radLoc =  DiamVehAtEngines/2.0 - EngineDivert.Lengine + EngineDivert.Lnoz
        radLoc = EngineDivert.Dcham + max(0.0, rVeh-EngineDivert.Dcham-EngineDivert.Lnoz-EngineDivert.Lcham)
        
        eng.rotate( [0.,0.,90.] )
        eng.translate([radLoc,heightEng,0])
        eng.rotate( [0.,90.*i+45.0,0.] )
        engs.append(eng)

    for i in range(EngineAxial.Number):
        eng = EngineAxial.getPOV_Item()
        eng.rotate([180,0,0])
        radLoc = 3.5 / 2.0
        #eng.rotate( [0.,0.,90.] )
        eng.translate([radLoc,-1,0])
        eng.rotate( [0.,180.0*i,0.] )
        engs.append(eng)

    #box = POV_Items.Box(corner1=[10,10,10], corner2=[0,0,0])
    shell = POV_Items.HollowCylinder( OD=3.5*2.0, height=7.0,
            texture = Texture( colorName="White", transmit=0.9, reflection=0. )    )
    shell.translate([0,-7,0])
    cone = POV_Items.Cone( Rbottom=8.4, Rtop=5.4, top=[0,20.,0],
            texture = Texture( colorName="White", transmit=0.9, reflection=0.0 )    )
    
    povItemL = [he, fl, ox, fl2, ox2,  shell, cone]
    povItemL.extend( heTankL )
    povItemL.extend( engs )
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)

if 0:
    S.render(view='back',ortho=1, clockX=15, clockY=15)

    S.render(view='front',ortho=0,clockX=0, clockY=15)

if 0:
    S.setDesignVar("WtProp", 3.)
    S.evaluate()
    S.render(view='front',ortho=0,clockX=0, clockY=15)
#S.render(view='top',ortho=0)#,clockX=0, clockY=16)
#S.render(view='bottom',ortho=0)#,clockX=0, clockY=16)


#makeSensitivityPlot(S,figureOfMerit="deltaV", desVars=["PHe"])

#S.saveDesVarSummary()
S.saveShortSummary()


if 0:
    makeCarpetPlot(S, sysParam="Lpackage", 
        desVarL=[["apexTankEllRatio",1.6, 1.8, 2.0],["MR",1.0,1.2,1.45]], 
        makeHTML=1, dpi=70, linewidth=2, smallLegend=1,  xResultVar="Itot",
        titleStr='',
        ptData=None, ptLegend='', logX=0, logY=0, yLabelStr='', colorL=['aqua','green'],
        haLabel='center', vaLabel='bottom', iLabelsX=0, iLabelsY=1000, alphaInLineLabels=0.7)



#S.setDesignVar("MR", 1.65)
#S.setDesignVar("apexTankEllRatio", 2.4)
S.evaluate()
S.render(view='front',ortho=1)#,clockX=1, clockY=15)
S.render(view='front',ortho=0,clockX=1, clockY=15)
#S.render(view='bottom',ortho=0)#,clockX=0, clockY=16)
HetankCenter.texture = Texture( colorName="Gray50", reflection=0., transmit=0.7 )
S.render(view='top',ortho=0)#,clockX=0, clockY=16)
#S.saveDesVarSummary()


if 0:
        
    make2DPlot(S, sysParam="deltaV", desVar="WtProp", makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='Vacuum Delta V for Fvac=%g'%(S('Fdivert'),))
        
    make2DPlot(S, sysParam="DACSMass", desVar="WtProp", makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='Vacuum Delta V for Fvac=%g'%(S('Fdivert'),))

        
    make2DPlot(S, sysParam="Lpackage", desVar="WtProp", makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='Vacuum Delta V for Fvac=%g'%(S('Fdivert'),))

# now save summary of system
S.saveFullSummary()


S.picklePrism()
# Be sure to wrap-up any files
S.close()
