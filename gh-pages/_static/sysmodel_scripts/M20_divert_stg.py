
from math import *
from prism import *

DiamVeh = 9.9
DiamHeTank = DiamVeh/3.3

SPACE = 0.1
LbossAndACS = 1.0

epsMax = 30.0
Pbottle = 10000.0

oxName = 'N2O4'
fuelName = "M20"

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
apexTankEllRatio = 2.0 # 1.67
cxwApexRoller = 2.16 * (2.75/2.714)
cxwHeTank =  (6.95 / 5.056) * (2.44/2.645)

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="%s/%s Ascent Phase"%(oxName,fuelName), type="bi-propellant", constraintTolerance=0.005,
    author="I.M. Pacter")



Pay = SimpleEqnMass(name="Payload Mass", type="inert",  
    eqn="15.0*2.20462", desc='Payload Mass')

ManBlock = SimpleEqnMass(name="Manifold Block", type="inert", eqn="1.0", desc='Manifold Block')

DivStruct = SimpleEqnMass(name="Divert Structure", type="inert", eqn="1.1", desc='Divert Structure')

# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ["PHe",Pbottle, 4000.0, Pbottle, 200.0, 'psia', 'Helium Tank Pressure'],
    ["Pc",    375.0, 300.0, 500.0,  20.0, 'psia', 'Engine Chamber Pressure'],
    ["MR",    1.0, 0.8, 2.0,  0.02, '', 'Engine Mixture Ratio'],
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
    ["LcylOx", "in", "Cylinder Length of Ox Tank"],
    ["OxTankOD",'in','Ox Tank Diameter','>',DiamVeh-.1],
    ['rhoBulk','lbm/cuin','Propellant Bulk Density'],
    )


# create Mass Items that make up the system
# make reference engine


EngineRef = Engine_FFC(name="Divert Engine",
                oxName=oxName, fuelName=fuelName, etaERE=etaERE,
                Pc=500.0, Fvac=300.0, eps=25.0, mr=1.0, CR=2.0, LoverDt=0.01,  LchamMin=1.03,
                pcentBell=80.0, Pamb=14.7)
    


# setup routine that will calc vacuum thrust for different area ratios


Oxtank = Tank(name="Oxidizer Tank", 
        makeCompositeTank=0, kalmod=0,  #RinsidMax=7.0,
        matlName="grEpox",   vfree=486.0,ell=apexTankEllRatio,rcyltd=0.1,
        ptank=1400.0,sf=1.5,cxw=cxwApexRoller,
        ithcyl=1,kacqui=1,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.1,tliner=0.03,rholiner=0.1)
        
        
Fltank = Tank(name="Fuel Tank",  
        makeCompositeTank=0, kalmod=0,  #RinsidMax=7.0,
        matlName="grEpox",   vfree=486.0,ell=apexTankEllRatio,rcyltd=0.1,
        ptank=1400.0,sf=1.5,cxw=cxwApexRoller , 
        ithcyl=1,kacqui=1,inpex=1,expefi=0.98,
        tblad=0.030,tbond=0.030,ttrspc=0.010,
        rhobnd=0.04,rhoacq=0.1,tliner=0.03,rholiner=0.1)
        
Hetank = Tank(name="Helium Tank", 
        makeCompositeTank=1, kalmod=0,  
        matlName="grEpox",   vfree=160.0, ell=heliumTankEllRatio,rcyltd=1.142,
        ptank=5000.0,sf=2.0,cxw=cxwHeTank, Number=4,
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

def calcNestingValues():
    
    # use elliptical dome logic to get package length
    hOffsetOx = ellNest.hOffset(Oxtank.OR, Oxtank.OR/Oxtank.ell, Hetank.OR, Hetank.OR/Hetank.ell, 
        DiamVeh/2.-Hetank.OR-SPACE, clearance=SPACE)

    hOffsetFl = ellNest.hOffset(Fltank.OR, Fltank.OR/Fltank.ell, Hetank.OR, Hetank.OR/Hetank.ell, 
        DiamVeh/2.-Hetank.OR-SPACE, clearance=SPACE)
        
    yDeltaMaxOx = Oxtank.OR/Oxtank.ell + Hetank.OR/Hetank.ell
    yNestOx = yDeltaMaxOx - hOffsetOx
    
    yDeltaMaxFl = Fltank.OR/Fltank.ell + Hetank.OR/Hetank.ell
    yNestFl = yDeltaMaxFl - hOffsetFl
    
    
    #print 'hOffsetOx',hOffsetOx,'   yDeltaMaxOx',yDeltaMaxOx, '   yNestOx',yNestOx
    #print 'hOffsetFl',hOffsetFl,'   yDeltaMaxFl',yDeltaMaxFl, '   yNestFl',yNestFl
    
    # figure out package Length
    htBlock = 2.0 * EngineRef.Dcham
    
    gapAvailable = Hetank.OH - yNestOx - yNestFl
    if htBlock > gapAvailable:
        banner( 'WARNING... Block Height dictates tank spacing.  htBlock=%g'%htBlock, 0,just='center')
        hOffsetOx += (htBlock-gapAvailable)/2.0
        hOffsetFl += (htBlock-gapAvailable)/2.0
        gapAvailable = htBlock
        
    return hOffsetOx, hOffsetFl, gapAvailable, htBlock

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Pc,PHe,MR,pcentBell,Wpayload,WtProp,pcentWpACS,pcentBell,eps, ThrustVac = \
        S("Pc","PHe", "MR",'pcentBell','Wpayload','WtProp',\
        'pcentWpACS','pcentBell','eps','ThrustVac')

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
        
    # estimate vehicle diameter using ox tank
    Oxtank.rcyltd = 0.0375
    
    WtOx = WtProp * MR/(1.0+MR)
    WtFl = WtProp - WtOx
    Oxtank.vfree = WtOx / Ox.rho
    
    #Oxtank.reCalc()
    Oxtank.setToMaxOD( DiamVeh )
    

    Fltank.vfree =  WtFl / Fl.rho
    Fltank.setToMaxOD( DiamVeh )
    
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
    
    He.PHeTnk =  PHe
    He.PGasTnkMEOP = PHe
    He.PpropNom = ptank
    He.VpropTnk = Oxtank.vfree*Oxtank.Number + Fltank.vfree*Fltank.Number
    He.reCalc()
    
    # figure out He tank geom
    Hetank.vfree = He.Vbottle / Hetank.Number
    Hetank.ptank = PHe
    Hetank.setToMaxOD( DiamHeTank )
    if Hetank.rcyltd < 0.5:
        Hetank.rcyltd = 0.5
        Hetank.reCalc()
    #Hetank.reCalc()  # reCalc done in setToMaxID
    
    # use elliptical dome logic to get package length
    hOffsetOx, hOffsetFl, gapAvailable, htBlock = calcNestingValues()
    
    wBlock = htBlock * 2.25/2.5
    #volBlock = htBlock * wBlock**2
    ManBlock.eqn = '%g * %g**2 * 0.16 / 2.0'%(htBlock, wBlock)
    
    # include boss and ACS additions to Lpackage 
    
    
    Lpackage = (Fltank.OR/Fltank.ell + Fltank.cyl) + hOffsetOx + hOffsetFl + Hetank.cyl + LbossAndACS +\
               (Oxtank.OR/Fltank.ell + Oxtank.cyl)
    
    #print 'gapAvailable=',gapAvailable
    DivStruct.eqn = '1.1 * (%g/10.0) * (%g/5.3)'%(DiamVeh, gapAvailable)
    #print 'Lpackage =',Lpackage
    #Lpackage = 3.9*(DiamVeh/10.0) + Oxtank.OH + Fltank.OH + Hetank.OH - Fltank.OR
 
    S.reCalc()
    
    #print 'PHe,ptank,Pc,MR',PHe,ptank,Pc,MR
    S["sysMass"] = S.mass_lbm
    
    S['DACSMass'] = S.mass_lbm - Wpayload
    S['Vhelium'] = Hetank.vfree*Hetank.Number
    
    S["Isp"] =  EngineRef.Isp
    S["IspSL"] =  EngineRef.IspAmb
    S['AreaRatio'] = EngineRef.eps
    
    
    S["Lpackage"] = Lpackage
    
    S["FdivertSL"] = EngineRef.Famb 
    S["FdivertVac"] = EngineRef.Fvac 
    S["LcylOx"] = Oxtank.cyl
    S["OxTankOD"] = Oxtank.OD
    
    rhoBulk = Ox.rho * Fl.rho * (MR+1.0) / (Ox.rho + Fl.rho*MR)
    S['rhoBulk'] = rhoBulk
    
    
    

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()

# now optimize the system... it should match up with the carpet plots.
#optimize(S, figureOfMerit="SizeWtLimit", desVars=['WtProp'], findmin=0)

            
Hetank.texture = Texture( colorName="Gray50", reflection=0. )
Oxtank.texture = Texture( colorName="Aquamarine", reflection=0.)
Fltank.texture = Texture( colorName="Pink", reflection=0. )
        
def myRenderControlRoutine(S):
    S.reCalcItems()
    
    HeightVeh = S.getResultVar('Lpackage')

    # use elliptical dome logic to get package length
    hOffsetOx, hOffsetFl, gapAvailable, htBlock = calcNestingValues()


    rVeh = DiamVeh / 2.0
    
    ox = Oxtank.getPOV_Item()
    heightOx =  Oxtank.OR/Oxtank.ell + LbossAndACS/2.0 
    ox.translate([0.,heightOx,0.])
    
    heightHe =  heightOx + Oxtank.cyl + hOffsetOx
    hetnkL = []
    for i in range( Hetank.Number ):
        he = Hetank.getPOV_Item()
        
        he.translate([rVeh-Hetank.OR-.2, heightHe, 0.0])
            
        he.rotate( [0.,90.*i,0.] )
        hetnkL.append( he )
    
    
    fl = Fltank.getPOV_Item()
    heightFl = heightHe +   Hetank.cyl + hOffsetFl
    fl.translate([0.,heightFl,0.])
    
    heightEng = ( (heightFl+Fltank.cyl/2.) + (heightOx+Oxtank.cyl/2.) ) / 2.0
    
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
    shell = POV_Items.HollowCylinder( OD=DiamVeh+SPACE/2., height=HeightVeh, thickness=SPACE/8.,
            texture = Texture( colorName="White", transmit=0.9, reflection=0. )    )
    
    povItemL = [he, fl, ox, eng, shell, engs[0], engs[1], engs[2], engs[3]]
    povItemL.extend( hetnkL )
    return povItemL

S.setRenderControlRoutine(myRenderControlRoutine)

if 1:
    S.render(view='back',ortho=1, clockX=15, clockY=15)
    S.render(view='back',ortho=0, clockX=0, clockY=0)
    Oxtank.texture = Texture( colorName="Aquamarine", reflection=0., transmit=1.0 )

    S.render(view='bottom',ortho=0)

#S.render(view='front',ortho=0,clockX=0, clockY=15)
#S.setDesignVar("WtProp", 100.)
#S.evaluate()
#S.render(view='top',ortho=0)#,clockX=0, clockY=16)
#S.render(view='bottom',ortho=0)#,clockX=0, clockY=16)


#makeSensitivityPlot(S,figureOfMerit="IspSL", desVars=["PHe"])

S.saveShortSummary()

if 1:
        
    make2DPlot(S, sysParam="Lpackage", desVar="WtProp", makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='')
        


# now save summary of system
S.saveFullSummary()


S.picklePrism()
# Be sure to wrap-up any files
S.close()
