
from math import *
from prism import *

DiamVeh = 9.9

SPACE = 0.1
LbossAndACS = 1.0

epsMax = 30.0
Pbottle = 10000.0

oxName = 'N2O4'
fuelName = "MMH"

LchamMinDivert = 1.4 #in
etaERE=0.916 # like Common DACS engine

tActionMin = 100.0 # sec
TminOperate = 510.0 # degR
TmaxOperate = 550.0 # degR

mrACS = 1.0
expulEffOx = 0.98
expulEffFl = 0.98
ullFracOx = 0.03
ullFracFl = 0.03

heliumTankEllRatio = 1.6 # ponzo is using 1.6 NOT 1.7
cxwHeTank =  (6.95 / 5.056) * (2.44/2.645)


Pay = SimpleEqnMass(name="Payload Mass", type="inert",  
    eqn="15.0*2.20462", desc='Payload Mass')

ManBlock = SimpleEqnMass(name="Manifold Block", type="inert", eqn="1.0", desc='Manifold Block')

DivStruct = SimpleEqnMass(name="Divert Structure", type="inert", eqn="1.1", desc='Divert Structure')

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="%s/%s He, Piston Ascent Phase"%(oxName,fuelName), type="bi-propellant", 
    author="Wally Seal")


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["PHe",Pbottle, 4000.0, Pbottle, 200.0, 'psia', 'Helium Tank Pressure'],
    ["Pc",    375.0, 300.0, 500.0,  20.0, 'psia', 'Engine Chamber Pressure'],
    ["eps",    9.0, 2.0, 20.0,  0.5, '', 'Nozzle Area Ratio'],
    ["Wpayload",33.0693,5.0,40.0,2.0,'lbm','Payload Mass'],
    ["pcentWpACS",10.0,0.0,10.0,0.5,'%','HLACS Percent of Propellant'],
    ["pcentBell",80.0,70.0,120.0,2.0,'%','Percent Bell Nozzle Contour'],
    ["ThrustVac",300.0,200.,400.,25.,'lbf','Engine Vacuum Thrust'],
    ["WtProp",20.,6.,12.,1.,'lbm','Usable Divert+ACS Propellant Mass'],
    )

# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ["sysMass", "lbm", "Propulsion System Mass"],
    ["Isp", "sec", "Engine Specific Impulse"],
    ["Itot", "lbf-sec", "Total Impulse"],
    ["IspSL", "sec", "Sea Level Isp"],
    ["ItotSL", "lbf-sec", "Sea Level Total Impulse"],
    ["Lpackage", "in", "Total KV Length"],
    ["Ptank", "psia", "Propellant Tank Pressure"],
    ['AreaRatio', '', 'Divert Nozzle Area Ratio'],
    ["DACSMass",  'lbm', 'DACS Mass'],
    ['FdivertSL','lbf','Sea Level Divert Thrust'],
    ['FdivertVac','lbf','Vacuum Divert Thrust'],
    ['Vhelium','cuin','Total Helium Volume'],
    ["OxTankOD",'in','Ox Tank Diameter'],
    ["MR","","Equal Volume Mixture Ratio"],
    ['rhoBulk','lbm/cuin','Propellant Bulk Density'],
    )

# make feasible variable for nesting tanks optimally
S.addFeasibleVariable( name="nestError", 
        feasibleVal=0.0 ,
        units='in', desc='Helium Tank Nesting Quality',
        controlVar="IDpiston", cvMinVal=DiamVeh/10.0, cvMaxVal=DiamVeh/2.5,
        cvUnits='in', cvDesc='ID of Piston Tanks')


# create Mass Items that make up the system
# make reference engine


EngineRef = Engine_FFC(name="Divert Engine",
                oxName=oxName, fuelName=fuelName, etaERE=etaERE,
                Pc=500.0, Fvac=300.0, eps=25.0, mr=1.6, CR=2.0, LoverDt=0.01,  LchamMin=1.03,
                pcentBell=80.0, Pamb=14.7)
    
Oxtank = Tank_Piston(name="Oxidizer Tank",  mass_lbm=0.0,
        inputLoverD=0, metalName="Ti", overwrapName="grEpox",
        vfree=4.0,ptank=1400.0,
        sf=1.5,cxw=1.0,Number=2,
        inpex=0,expefi=0.99, dPpiston=10.0, LoDpiston=0.45,
        LoverD=5.0,Dinside=3.0, thkMetal=0.010 )
        
Fltank = Tank_Piston(name="Fuel Tank",  mass_lbm=0.0,
        inputLoverD=0, metalName="Ti", overwrapName="grEpox",
        vfree=4.0,ptank=1400.0,
        sf=1.5,cxw=1.0,Number=2,
        inpex=0,expefi=0.99, dPpiston=10.0, LoDpiston=0.45,
        LoverD=5.0,Dinside=3.0, thkMetal=0.010 )
                
        
Hetank = Tank(name="Helium Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=heliumTankEllRatio,rcyltd=1.142,
        ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=2,
        ithcyl=1,kacqui=0,inpex=0,
        tbond=0.030,rhobnd=0.04,tliner=0.035,rholiner=0.101)

# use Helium as pressurant
He = PressurantInteg( name="Helium Pressurant",  mass_lbm=0.0, gas='HE',
        VpropTnk=1000.0,PGasTnkMEOP=Pbottle,PpropNom=1000.0,
        PfinGasOvPnom=1.1, 
        tAction=100.0,TminR=TminOperate,TmaxR=TmaxOperate, ullageFrac=0.03,
        PVoW_Bottle=500000., PVoW_Tank=100000.,
        AccGees=1.0,
        Nbottle=2, ellBottle=1.4, LcylOvDBottle=1.0, Cp_effBottle=0.15, # Cp Ti=.125, Al=.2, Monel=.1
        Ntank=2, ellTank=1.414, LcylOvDTank=1.0, Cp_effTank=0.15,
        CdARegMax=None, dPregulator=5.0, NtimeSteps=400, heatExchangerTout=None,
        WtHeLLACS=0.0, QexternalIntoBottle=0.0, velMultTank=1.0, useDBruns=1)

        
# add propellants
Fl = Inc_liquid(symbol=fuelName,T=530.0,P=14.7)
Ox = Inc_liquid(symbol=oxName,T=530.0,P=20.0)


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( [Oxtank, Fltank,  He, Hetank,  EngineRef, 
    Pay, ManBlock, DivStruct,
    Ox, Fl] )


#htBlock = calcValveBlockHt()
def calcValveBlockHt():
    
    # figure out package Length
    htBlock = 2.0 * EngineRef.Dcham
        
    return  htBlock


# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    Pc,PHe,pcentBell,Wpayload,WtProp,pcentWpACS,pcentBell,eps, ThrustVac, IDpiston = \
        S("Pc","PHe",'pcentBell','Wpayload','WtProp',\
        'pcentWpACS','pcentBell','eps','ThrustVac', 'IDpiston')

    MR = Ox.rho / Fl.rho

    # figure out engine 
    EngineRef.eps = eps
    EngineRef.Pc = Pc
    EngineRef.mr = MR
    EngineRef.pcentBell = pcentBell
    EngineRef.Fvac = ThrustVac
    EngineRef.reCalc()
    
    # calculate propellant load
    
    Pface = Pc * (1. + 0.25/2.**1.8)
    # get pressure schedule
    ptank = Pface + Pc*0.5 + 380.0
    S["Ptank"] = ptank
    
    Oxtank.ptank = ptank
    Fltank.ptank = ptank
    Oxtank.Dinside = IDpiston
    Fltank.Dinside = IDpiston
        
    # calc derived parameter variables
    WtOx = WtProp * MR/(1.0+MR)
    WtFl = WtProp - WtOx
    Oxtank.vfree = WtOx / Ox.rho / Oxtank.Number
    
    #Oxtank.reCalc()
    Fltank.vfree =  WtFl / Fl.rho / Fltank.Number
    
    # calc derived parameter variables
    
    
    WpropDiv = WtProp * (100.0-pcentWpACS)/100.0
    WpACS = WtProp - WpropDiv
    
    
    Pay.eqn = '%g'%Wpayload
    
    
    Itot = WpropDiv * EngineRef.Isp 
    S["Itot"] = Itot
    
    ItotSL = WpropDiv * EngineRef.IspAmb
    S["ItotSL"] = ItotSL
    
    WtFlRCS = WpACS/(1.0 + mrACS)
    WtOxRCS =  WpACS-WtFlRCS
    
    
    # start assigning values to Mass Items
    WtOxResid = (WtOx ) * (1.0 / expulEffOx - 1.0)
    WtFlResid = (WtFl ) * (1.0 / expulEffFl - 1.0)
    Ox.setMassBreakdown( [('Burned Divert',WtOx* (100.0-pcentWpACS)/100.0),
        ('Burned RCS',WtOxRCS),('Residual',WtOxResid)])
    Fl.setMassBreakdown( [('Burned Divert',WtFl* (100.0-pcentWpACS)/100.0),
        ('Burned RCS',WtFlRCS),('Residual',WtFlResid)])
    Ox.reCalc()
    Fl.reCalc()
    
    
    # Itot of helium LLACS (zero for Hover test)
    He.wtHeACS = 0.0
    
    Oxtank.reCalc()
    Fltank.reCalc()
    
    
    # figure out package Length
    Lpackage = max( Fltank.OH, Oxtank.OH ) + LbossAndACS
    S['Lpackage'] = Lpackage
    #LvehError = Lpackage - Lpackage
    #S['LvehError'] = LvehError
    
    He.PHeTnk =  PHe
    He.PpropNom = ptank
    He.VpropTnk = Oxtank.vfree*Oxtank.Number + Fltank.vfree*Fltank.Number
    He.reCalc()
    
    He.PGasTnkMEOP = PHe
    Hetank.vfree = He.Vbottle / Hetank.Number
    Hetank.ptank = PHe
    #Hetank.setToLength( Lpackage / 2.0 )

    DHe = DiamVeh - 2.0*(Oxtank.OD + 2.0*SPACE)
    Hetank.setToMaxOD( DHe )
    
    # height of valve block
    htBlock = calcValveBlockHt()
    
    nestError = htBlock + 4*SPACE + Hetank.OH*Hetank.Number + LbossAndACS - Lpackage

    
    wBlock = htBlock * 2.25/2.5
    #volBlock = htBlock * wBlock**2
    ManBlock.eqn = '%g * %g**2 * 0.16 / 2.0'%(htBlock, wBlock)
    
    DivStruct.eqn = '1.1 * (%g/10.0) * (%g/5.3)'%(DiamVeh, htBlock)
    
    S.reCalc()
    #print 'PHe,ptank,Pc,MR',PHe,ptank,Pc,MR
    S["sysMass"] = S.mass_lbm

    S['DACSMass'] = S.mass_lbm - Wpayload
    S['Vhelium'] = Hetank.vfree*Hetank.Number
    
    S["Isp"] =  EngineRef.Isp
    S["IspSL"] =  EngineRef.IspAmb
    S['AreaRatio'] = EngineRef.eps
    
    
    S["Lpackage"] = Lpackage
    S["MR"] = MR
    
    S["FdivertSL"] = EngineRef.Famb 
    S["FdivertVac"] = EngineRef.Fvac 
    S["OxTankOD"] = Oxtank.OD
    S['nestError'] = nestError
    
    rhoBulk = Ox.rho * Fl.rho * (MR+1.0) / (Ox.rho + Fl.rho*MR)
    S['rhoBulk'] = rhoBulk


# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
#optimize(S, figureOfMerit="SizeWtLimit", desVars=['WtProp'], findmin=0)

            
Hetank.texture = Texture( colorName="Gray50", reflection=0. )
Oxtank.texture = Texture( colorName="Aquamarine", reflection=0. )
Fltank.texture = Texture( colorName="Pink", reflection=0. )
        
def myRenderControlRoutine(S):
    S.reCalcItems()
    Lpackage = S.getResultVar("Lpackage")
    Ltanks = Lpackage - LbossAndACS
    
    rVeh = DiamVeh / 2.0
    
    fl = Fltank.getPOV_Item()
    radj = rVeh - Fltank.OR + SPACE/2.0
    LadjPiston = LbossAndACS/2.0
    fl.translate([radj,LadjPiston,0.])
    
    fl2 = Fltank.getPOV_Item()
    fl2.translate([radj,LadjPiston,0.])
    fl2.rotate( [0.,180.,0.] )
    
    heightEng = Lpackage / 2.0
    
    ox = Oxtank.getPOV_Item()
    radj = rVeh - Oxtank.OR + SPACE/2.0
    ox.translate([radj,LadjPiston,0.])
    ox.rotate( [0.,90.,0.] )

    ox2 = Oxtank.getPOV_Item()
    ox2.translate([radj,LadjPiston,0.])
    ox2.rotate( [0.,270.,0.] )


    # make the helium tanks
    heTankL = []
    #dAng = 360.0 / Hetank.Number
    #ang = 45.0
    for N in range(Hetank.Number):
        he = Hetank.getPOV_Item()
        radj = 0.0 #rVeh - Hetank.OR - SPACE/2.0
        domeHt = Hetank.OR/Hetank.ell + N*(Ltanks-Hetank.OH) + LbossAndACS/2.0
        he.translate([radj,domeHt,0.])
        #he.rotate( [0.,ang,0.] )
        #ang += dAng
        heTankL.append( he )
    
    
    engs=[]
    for i in range(4):
        eng = EngineRef.getPOV_Item()
        eng.rotate([180,0,0])
        
        #radLoc = EngineRef.Dcham/2.0 #- EngineRef.Lengine  + EngineRef.Dt/1.414/2.0 - 0.2
        radLoc = 1.25 * EngineRef.Dcham # DiamVeh/2.0 - EngineRef.Lengine
        
        eng.rotate( [0.,0.,90.] )
        eng.translate([radLoc,heightEng,0])
        eng.rotate( [0.,90.*i+45.0,0.] )
        engs.append(eng)
    
    #box = POV_Items.Box(corner1=[10,10,10], corner2=[0,0,0])
    shell = POV_Items.HollowCylinder( OD=DiamVeh+SPACE/2., height=Lpackage, thickness=SPACE/8.,
            texture = Texture( colorName="White", transmit=0.9, reflection=0. )    )


    povItemL = [ fl, ox, fl2, ox2, eng, shell] 
    povItemL.extend( engs )
    povItemL.extend( heTankL )
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)
S.render(view='front',ortho=0,clockX=0, clockY=15)
S.render(view='back',ortho=1, clockX=15, clockY=15)

#S.setDesignVar("Wprop", 100.)
#S.evaluate()
#S.render(view='top',ortho=0)#,clockX=0, clockY=16)
Hetank.texture = Texture( colorName="Gray50", reflection=0., transmit=0.8 )
S.render(view='bottom',ortho=0)#,clockX=0, clockY=16)


#makeSensitivityPlot(S,figureOfMerit="Itot", desVars=["MR","Fdivert"])

S.saveShortSummary()

if 1:
        
    make2DPlot(S, sysParam="Lpackage", desVar="WtProp", makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='')
    
    

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
