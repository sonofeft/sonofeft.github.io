
from math import *
from prism import *

DiamVeh = 50.0

NumberOxTanks = 1
NumberFuelTanks = 1

WtHeLeakage = 0.1 # lbm

NumberHeTanks = 1

simpleHe = 0 # 1=calibrate with one integ, 0=all integ, -1=skip any integration

propellant_margin_LBM = 0.0 #lbm

leakage = 0.0 # total propellant leakage
leakage_ox = leakage * 2.0 / 3.0
leakage_fuel = leakage - leakage_ox


mrACS = 1.75
etaERE=0.95

etaKinetic = 0.975  # kinetic efficiency... 

NumAxialEngines = 3
NumACSEngines = 6

oxName = 'MON25'
fuelName = 'MMH'
heObj = n_fluid('HE',T=500.0,P=1000.0)

mission = 'solar'
if mission=='solar':
    Fvac=200.0 
    ItotDescent=8424. + 7229. + 6387. + 24027.
    ItotACS=2763. + 389. + 3366.
else:
    Fvac=100.0
    ItotDescent=5312. + 4559. + 4034. + 14806.
    ItotACS=2264. + 246. + 2127.

FvacACS=5.0

cantAngleDescent=0.0 # deg
etaCant=cos(cantAngleDescent*pi/180.0)

dpLinesEst = 20.0

# using Valcor regulator as reference
dPregRef = 120.0  # Valcor dP
dPregMin = dPregRef + 20.0 + 10.0 + 10.0 # includes regulator drop, He line drop, filter, pyro vlv

tActionSec = 46.0*3 + 90.0*2

TminOperate = 460.0 - 4.0
TmaxOperate = 550.0
TmaxHe = 460.0 + 122.0 # Helium bottle is filled at 122 degF

cxwValves=1.0

expulEffOx = 0.99
expulEffFl = 0.99
ullFracOx = 0.03
ullFracFl = 0.03

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="%s/%s %s ILN"%(oxName,fuelName,mission), type="bi-propellant", 
    author="Moon Walker",programName='Lunar Lander')


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars( ["PcAxial",  230.0, 150.0, 400.0,  20.0, 'psia', 'Axial Engine Chamber Pressure'] )
S.addDesVars( ["LengLimit",  13.,  10.0, 15.0,   1.0, 'in',  'Engine Length Limit'] )
S.addDesVars( ["ItotDescent",  ItotDescent,  20000.0, 50000.0,   5000.0, 'lbf-sec',  'Total Impulse of Descent Engines'] )
S.addDesVars( ["ItotACS",  ItotACS,  4000.0, 8000.0,   500.0, 'lbf-sec',  'Total Impulse of ACS Engines'],
    ['mrAxial', 1.75 , 1.5, 1.9, 0.05,'','Divert Engine Mixture Ratio'],
    ['PmaxGas',4500.,4000.,6000.,500.,'psia','Helium Max Bottle Pressure'])


#S.addFeasibleVariable( name="VolRatioTanks", feasibleVal=1.0,   
#        units='', desc='Tank Volume Ratio',
#        controlVar="mrAxial", cvMinVal=1.4, cvMaxVal=2.0,
#        cvUnits='', cvDesc='Divert Engine Mixture Ratio')

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Total System Mass"],
    ["Isp", "sec", "Engine Specific Impulse"],
    ["IspACS", "sec", "ACS Engine Specific Impulse"],
    ["IspEff", "sec", "Effective Isp (with cant angle)"],
    ["Lengine", "in", "Engine Length"],
    ["engMass", "lbm", "Total Engine Mass"],
    ["tankMass", "lbm", "Total Tankage Mass"],
    ["feedMass", "lbm", "Valve/Line/Regulator Mass"],
    ["dPvlvMax", "psid", "Maximum Valve Pressure Drop"],
    ["dPvlvOx", "psid", "Ox Valve Pressure Drop"],
    ["dPvlvFuel", "psid", "Fuel Valve Pressure Drop"],
    ["dPinjector", "psid", "Injector Pressure Drop"],
    ["dpBalOrificeACS", "psid", "Balance Orifice Pressure Drop"],
    ["Ptank", "psia", "Propellant Tank Pressure"],
    ["PengineIn", "psia", "Engine Inlet Pressure"],
    ["PcFace", "psia", "Engine Face Pressure"],
    ["PfinalHe", "psia", "Final Helium Pressure"],
    ["AreaRatio", "", "Descent Nozzle Area Ratio"],
    ["VolRatioTanks","",'Tank Volume Ratio (Ox/Fuel)']
    )
        
# create Mass Items that make up the system
# use scaling from reference engine

EngineAxial = Engine_FFC(name="Axial Engine w/o Valves", 
    oxName=oxName, fuelName=fuelName, Number=NumAxialEngines,
    cxw=1.0, Pc=500.0, Fvac=Fvac, eps=25.0, mr=1.9, 
    CR=2.5, LoverDt=2.0, LchamMin=1.25, cxwValves=0.0,
    etaERE=etaERE, calcEtaNoz=1, useFastCEALookup=0,isBell=1, pcentBell=80.0,
    halfAngDeg=15.0, xlnOverLcham=0.9, valvesMassInput=0.000001 )

    
EngineACS = Engine_Fixed_Design( name="R-6D with valves",  mass_lbm=1.0, 
        oxName=oxName, fuelName=fuelName, Number=NumACSEngines,
        Pc=92.0, Dt=0.2066, eps=100.0, mr=mrACS, CR=2.5, xlcOxln=1.0, Lprime=3.0,
        etaERE=0.97, etaNoz=0.99, isBell=1, pcentBell=80.0,
        halfAngDeg=15.0, useFastCEALookup=0, etaKinInp=1.0,
        calcEtaNoz=1, inputIspDel=1, IspDel=280.0)    
#print Engine.getSummary()


Oxtank = Tank(name="Ox Tank", Number=NumberOxTanks,
        makeCompositeTank=0, kalmod=0,  tMinGaugeUser=0.010,
        matlName="Ti",   vfree=486.0,ell=1.0,rcyltd=0.,
        ptank=1400.0,sf=1.5,cxw=1.5,
        ithcyl=1,kacqui=6,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.16,tliner=0.0,rholiner=0.04)
        
        
Fltank = Tank(name="Fuel Tank", Number=NumberFuelTanks,
        makeCompositeTank=0, kalmod=0,    tMinGaugeUser=0.010,
        matlName="Ti",   vfree=486.0,ell=1.0,rcyltd=0.,
        ptank=1400.0,sf=1.5,cxw=1.5,
        ithcyl=1,kacqui=7,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.04,tliner=0.0,rholiner=0.04)
        
        
Hetank = Tank(name="COPV Helium Tank",   tMinGaugeUser=0.050,
        makeCompositeTank=1, kalmod=0,  Number=NumberHeTanks,
        matlName="grEpox",   vfree=160.0, ell=1.764,rcyltd=1.45,
        ptank=10000.0,sf=2.0,cxw=1.25,
        ithcyl=1,kacqui=0,inpex=0,
        inpTblad=0, tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.1,tliner=0.04,rholiner=0.1)
        
# add propellants
Fl = Inc_liquid(symbol=fuelName,T=TmaxOperate,P=14.7)
Ox = Inc_liquid(symbol=oxName,T=TmaxOperate,P=100.0)

# add main propellant lines
FlLine = Line_Liq_inpD( name="Fuel Line", liqObj=Fl,  matlName="Ti", 
        wdot=0.1, pLine=400.0, OD=0.5, thkWall=0.045,
        len_inches=50.0, Kfactors=5.0,  Number=1,
        cxw=1.25, roughness=5.0E-6 )
OxLine = Line_Liq_inpD( name="Ox Line", liqObj=Ox,  matlName="Ti", 
        wdot=0.1, pLine=400.0, OD=0.5, thkWall=0.045,
        len_inches=50.0, Kfactors=5.0,  Number=1,
        cxw=1.25, roughness=5.0E-6 )

HeLine = Line_Gas( name="Helium line", gasSymbol='HE',  matlName="Ti", 
        calcVelFromDiamInp=1, DiamInp=0.25, thkWallInp=0.045,
        wdot=0.1, velFPS=20.0, TgasDegR=530.0, designWithVout=1,
        usePinlet=0, PgasOutlet=400.0, PgasInlet=400.0, 
        len_inches=50.0, Kfactors=5.0,  Number=1,
        sf=4.0, cxw=1.25, roughness=5.0E-6, mass_lbm=0.0 )
# use Helium as pressurant

PpropNomEst = 400.0
#PfOvPref = dPregMin / (dPregMin + PpropNomEst)
PfOvPref = 0.8  # assume a blow down at end

He = PressurantHe(name="pressurant helium",  mass_lbm=0.0,
    VpropTnk=4800.0,PHeTnk=3000.0,PpropNom=PpropNomEst,
    PfinHeOvPnom=PfOvPref, wtHeACS=WtHeLeakage,
    tAction=tActionSec,TminR=TminOperate,TmaxR=TmaxHe)

if simpleHe>=0:
    HeInteg = PressurantInteg( name="Helium Pressurant",  mass_lbm=0.0, gas='HE',
        timeProfileL=[0.0, tActionSec], pcentLiqExpelledL=[0.0, 100.0],
        VpropTnk=5000.0,PGasTnkMEOP=3000.0,PpropNom=PpropNomEst,
        PfinGasOvPnom=PfOvPref, 
        tAction=tActionSec,TminR=TminOperate,TmaxR=TmaxHe, ullageFrac=(ullFracOx+ullFracFl)/2.0,
        PVoW_Bottle=500000., PVoW_Tank=100000.,
        AccGees=1.0,
        Nbottle=1, ellBottle=1.4, LcylOvDBottle=1.0, Cp_effBottle=0.15, # Cp Ti=.125, Al=.2, Monel=.1
        Ntank=NumberFuelTanks+NumberOxTanks, ellTank=1.414, LcylOvDTank=1.0, Cp_effTank=0.15,
        CdARegMax=None, dPregulator=dPregMin, NtimeSteps=400, heatExchangerTout=None,
        WtHeLLACS=WtHeLeakage, QexternalIntoBottle=0.0, velMultTank=1.0, useDBruns=1)
        
if simpleHe==1:
    He.calibrate( TfBottle=HeInteg.TfinalGasBot, TfProp=HeInteg.TfinalPropGas )
elif simpleHe==0:
    He = HeInteg

# make valve objects
if 0:
    vlvFl = ValveFixedDesign(  name="Moog Axial Fuel valve", liqObj=Fl,  matlName="Stainless Steel", 
            wdot=0.232, refWaterWdot=0.358, refWaterDP=166.0, refName="MOOG MKV valve",  Number=1,
            mass_lbm=0.9, cxw=1.0)
    
    vlvOx = ValveFixedDesign(  name="Moog Axial Oxidizer valve", liqObj=Ox,  matlName="Stainless Steel", 
            wdot=0.441, refWaterWdot=0.358, refWaterDP=166.0, refName="MOOG MKV valve",  Number=1,
            mass_lbm=0.9, cxw=1.0)
else:
    vlvFl = ValveFixedDesign(  name="Axial Fuel valve", liqObj=Fl,  matlName="Stainless Steel, Teflon", 
            wdot=0.232, refWaterWdot=0.214, refWaterDP=30.0, refName="MOOG Spacebus valve, Model 53-203",  Number=1,
            mass_lbm=0.9, cxw=1.0)
    vlvOx = ValveFixedDesign(  name="Axial Ox valve", liqObj=Ox,  matlName="Stainless Steel, Teflon", 
            wdot=0.441, refWaterWdot=0.214, refWaterDP=30.0, refName="MOOG Spacebus valve, Model 53-203",  Number=1,
            mass_lbm=0.9, cxw=1.0)

vlvFl.Number = EngineAxial.Number
vlvOx.Number = EngineAxial.Number


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Oxtank, Fltank,  EngineAxial, EngineACS, Ox, Fl, Hetank,He, OxLine, FlLine, HeLine,
    vlvFl, vlvOx] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    PcAxial,LengLimit,ItotDescent,ItotACS,mrAxial,PmaxGas=\
        S("PcAxial","LengLimit","ItotDescent","ItotACS","mrAxial","PmaxGas")

    EngineAxial.etaKinInp = etaKinetic
    EngineAxial.Pc = PcAxial
    EngineAxial.mr = mrAxial
                    
    def newLeng( e ):
        EngineAxial.eps = e
        EngineAxial.reCalc()
        return EngineAxial.Lnoz + EngineAxial.Lcham + EngineAxial.Dcham
        
    epsMax = 150.0 # limit area ratio 
    G = Goal(goalVal=LengLimit, minX=2.0, maxX=epsMax, 
        funcOfX=newLeng, tolerance=1.0E-5, maxLoops=40, failValue=epsMax)
    eps, ierror = G()
    EngineAxial.eps = eps
    EngineAxial.reCalc()



    #EngineACS.etaKinInp = etaKinetic
    #EngineACS.Pc = Pc
    #EngineACS.mr = mrACS
    #EngineACS.reCalc()
    
    vlvFl.wdot = EngineAxial.wdotFl
    vlvOx.wdot = EngineAxial.wdotOx
    
    S["Lengine"] = EngineAxial.Lengine
    S["AreaRatio"] = eps
    
    wdotOxTot = NumAxialEngines * EngineAxial.wdotOx + NumACSEngines * EngineACS.wdotOx
    wdotFlTot = NumAxialEngines * EngineAxial.wdotFl + NumACSEngines * EngineACS.wdotFl
    wdotTot = wdotFlTot + wdotOxTot
    
    # split margin mass by flow demand
    margin_ox_LBM = propellant_margin_LBM * wdotOxTot / wdotTot
    margin_fuel_LBM = propellant_margin_LBM * wdotFlTot / wdotTot
    
    WtPropAxial = ItotDescent/EngineAxial.Isp/etaCant
    WtPropACS = ItotACS/EngineACS.Isp
    
    # calc derived parameter variables
    WtOx = WtPropAxial*mrAxial/(1.0+mrAxial) + margin_ox_LBM + leakage_ox + WtPropACS*mrACS/(1.0+mrACS)
    WtFl = WtPropAxial/(1.0+mrAxial)         + margin_fuel_LBM + leakage_fuel + WtPropACS/(1.0+mrACS)
    
    # get pressure schedule
    
    dPInjector = PcAxial*0.5
    pcFace = PcAxial*(1. + 0.25/EngineAxial.CR**1.8)
    
    dpVlvMax = max(vlvFl.deltaP,  vlvOx.deltaP)
    S["dPvlvMax"] = dpVlvMax
    dpFeed = dpVlvMax + dpLinesEst
    
    pRegOutlet = pcFace + dPInjector + dpFeed
    
    if pRegOutlet > 400.0:
        dpBalOrificeACS =  pRegOutlet - 400.0
    else:
        dpBalOrificeACS = 0.0
        pRegOutlet = 400.0

    S["dPvlvOx"] = vlvOx.deltaP
    S["dPvlvFuel"] = vlvFl.deltaP
    S["dPinjector"] = dPInjector
    S["dpBalOrificeACS"] = dpBalOrificeACS
    

    # start assigning values to Mass Items
    # start assigning values to Mass Items
    WtOxResid = WtOx * (1.0 / expulEffOx - 1.0)
    WtFlResid = WtFl * (1.0 / expulEffFl - 1.0)
    Ox.setMassBreakdown( [('Burned Axial',WtPropAxial*mrAxial/(1.0+mrAxial)),
        ('Burned ACS',WtPropACS*mrACS/(1.0+mrACS)),('Margin',margin_ox_LBM),
        ('Leakage',leakage_ox),('Residual',WtOxResid)])

    Fl.setMassBreakdown( [('Burned Axial',WtPropAxial/(1.0+mrAxial)),
        ('Burned ACS',WtPropACS/(1.0+mrACS)),('Margin',margin_fuel_LBM),
        ('Leakage',leakage_fuel),('Residual',WtFlResid)])

    Ox.reCalc()
    Fl.reCalc()
    
    Oxtank.vfree = Ox.Volume / (1.0-ullFracOx)/ NumberOxTanks
    Fltank.vfree = Fl.Volume / (1.0-ullFracFl)/ NumberFuelTanks
    
    Oxtank.ptank = pRegOutlet
    Fltank.ptank = pRegOutlet
    
    Oxtank.reCalc()
    Fltank.reCalc()

    S["VolRatioTanks"] = Oxtank.vfree/Fltank.vfree 

    # calculate final deltaP across regulator orifice
    #if simpleHe: # works for -1 and 1
    #    He.PfinHeOvPnom = (pRegOutlet + dPregMin) / pRegOutlet
    #else:
    #    He.PfinGasOvPnom = (pRegOutlet + dPregMin) / pRegOutlet

    if simpleHe: # works for -1 and 1
        He.PHeTnk =  PmaxGas
    else:
        He.PGasTnkMEOP =  PmaxGas
    
    He.PpropNom = pRegOutlet
    He.VpropTnk = (Oxtank.vfree*NumberOxTanks + Fltank.vfree*NumberFuelTanks) 
    #He.tAction = WtProp / EngineAxial.wdotTot / EngineAxial.Number
    He.reCalc()
    
    Hetank.ptank = PmaxGas
    if simpleHe: # works for -1 and 1
        Hetank.vfree = He.volHeTotal / Hetank.Number
        HeLine.TgasDegR = He.TfinalHeBot
    else:
        Hetank.vfree = He.Vbottle / Hetank.Number
        HeLine.TgasDegR = He.TfinalGasBot
    Hetank.reCalc()
    
    # give helium line its inputs
    HeLine.PgasOutlet = pRegOutlet
    heObj.setTP(T=HeLine.TgasDegR, P=HeLine.PgasOutlet)

    vdotHe = wdotOxTot/Ox.rho + wdotFlTot/Fl.rho

    HeLine.wdot = vdotHe * heObj.rho
    
    # do main propellant lines
    OxLine.wdot = wdotOxTot
    FlLine.wdot = wdotFlTot
    OxLine.pLine = pRegOutlet
    FlLine.pLine = pRegOutlet
    
    S.reCalc()
    
    S["sysMass"] = S.mass_lbm
    S["engMass"] = EngineAxial.mass_lbm
    S["Isp"] =  EngineAxial.Isp
    S["IspACS"] =  EngineACS.Isp
    S["IspEff"] =  EngineAxial.Isp*etaCant
    
    
    S["engMass"] = EngineAxial.mass_lbm + EngineACS.mass_lbm
    S["tankMass"] = Oxtank.mass_lbm + Fltank.mass_lbm + Hetank.mass_lbm

    S["feedMass"] =  OxLine.mass_lbm + FlLine.mass_lbm + HeLine.mass_lbm
    
    S["Ptank"] =  pRegOutlet
    S["PengineIn"] =  PcAxial + dPInjector
    S["PcFace"] = pcFace
    
    try:
        S["PfinalHe"] = He.PfinalGasBot
    except:
        S["PfinalHe"] = He.PfinalHeBot
    


# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.

#optimize(S, figureOfMerit="sysMass", desVars=["PcAxial","LengLimit",
#    "dpLowFeed","dpHighFeed","CdAhiPvlvOx","CdAhiPvlvFl","CdAloPvlvOx","CdAloPvlvFl"], findmin=1)

#optimize(S, figureOfMerit="sysMass", desVars=["PcAxial","PmaxGas"], findmin=1)


Oxtank.texture = Texture( colorName="Aquamarine" )
Fltank.texture = Texture( colorName="Pink" )
        
def myRenderControlRoutine(S):
    S.reCalcItems()
    Lpackage = max( Fltank.OH, Oxtank.OH )
    
    rVeh = (Fltank.OD + Oxtank.OD)/1.5
    rVeh = 100.0
    
    
    heL = []
    ORmax = max(Hetank.OR, Fltank.OR, Oxtank.OR)
    for i in range( NumberHeTanks ):
        he = Hetank.getPOV_Item()
        height = Hetank.OR/Hetank.ell
        he.translate([0.0,height,(-ORmax-1.0)*(i+1)])
        heL.append(he)
    
    flL = []
    for i in range( NumberFuelTanks ):
        fl = Fltank.getPOV_Item()
        height = Fltank.OR/Fltank.ell
        fl.translate([(ORmax+1.0)*(i+1),height,0.])
        flL.append(fl)
    
    oxL = []
    for i in range( NumberOxTanks ):
        ox = Oxtank.getPOV_Item()
        height = Oxtank.OR/Oxtank.ell
        ox.translate([(-ORmax-1.0)*(i+1),height,0.])
        oxL.append(ox)
    
    
    
    Linjff = EngineAxial.Lengine - EngineAxial.Dcham
    hadj = Linjff
    
    engs=[]
    for N in range(EngineAxial.Number):
        # place axial engines
        axial_eng = EngineAxial.getPOV_Item()
        axial_eng.rotate( [180.0, 0.0, 0.0] )
        #axial_eng.translate( [0.0,-EngineAxial.Dcham,0.0] )
        
        
        if EngineAxial.Number>1:
            dang = 360.0 / EngineAxial.Number
            radj = (DiamVeh - max(EngineAxial.Dcham, EngineAxial.Dexit))/2.0
            axial_eng.rotate( [0.0, 0.0, cantAngleDescent] )
            axial_eng.translate( [radj,hadj,0.0] )
            axial_eng.rotate( [0.0, N*dang + 45., 0.0] )
        else:
            yNest = 0.0
        
        engs.append(axial_eng)

    for i in range(3):
        for j in range(2):
            eng = EngineACS.getPOV_Item()
            eng.rotate([90,0,0])
            
            heightEng = EngineAxial.Lengine
            
            if j==1:
                eng.rotate([180,0,0])
                eng.translate([0,0,-1])
            else:
                eng.translate([0,0,1])
        
            radLoc = radj
            
            eng.translate([radLoc,heightEng,0])
            eng.rotate( [0.,120.*i + 45.,0.] )
            engs.append(eng)


    povItemL = [ ]
    povItemL.extend( engs )
    povItemL.extend( oxL )
    povItemL.extend( flL )
    povItemL.extend( heL )
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)
#S.render(view='front',ortho=0,clockX=30, clockY=30, background="Quartz", viewMargin=0.8, lookAtOffset=[0,-25,0])
S.render(view='front',ortho=0,clockX=30, clockY=30, background="Quartz")
#S.render(view='back',ortho=1, clockX=15, clockY=15, background="Quartz")

#S.setDesignVar("Wprop", 100.)
#S.evaluate()
#S.render(view='top',ortho=0)#,clockX=0, clockY=16, background="Quartz")



#makeSensitivityPlot(S,figureOfMerit="Lengine", desVars=["PHe","PcAxial","LengLimit"])
if 1:
    makeSensitivityPlot(S,figureOfMerit="sysMass", desVars=["PcAxial","LengLimit","PmaxGas"])
#makeSensitivityPlot(S,figureOfMerit="sysMass", desVars=["CdAhiPvlvOx","CdAhiPvlvFl","CdAloPvlvOx","CdAloPvlvFl"])
#makeMassPieCharts(S)

S.saveShortSummary()

if 1:
    makeMassItemSensitivityPlot(S, desVar="PcAxial", excludePropellant=0, showDelta=0)
    makeMassItemSensitivityPlot(S, desVar="PcAxial", excludePropellant=0, showDelta=1)

    make2DPlot(S, sysParam=["AreaRatio"], desVar="PcAxial")
    make2DPlot(S, sysParam=["Isp","IspEff"], desVar="PcAxial")
    make2DPlot(S, sysParam=["feedMass","engMass","tankMass"], desVar="PcAxial")
    
    make2DPlot(S, sysParam=["PfinalHe", "Ptank","PengineIn","PcFace"], 
               desVar="PcAxial", legendOnLines=1)
    make2DPlot(S, sysParam=["dPinjector", "dPvlvOx","dPvlvFuel", "dpBalOrificeACS"], 
               desVar="PcAxial", legendOnLines=1)
    

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()

if simpleHe == -1:
    print '================================'
    print 'WARNING... simpleHe is set to -1'
    print '================================'
 