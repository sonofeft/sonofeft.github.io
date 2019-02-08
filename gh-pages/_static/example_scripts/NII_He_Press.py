from prism import TankPress

# simulation of NII Delta He pressurization

Vfull = 5.69 * 1728.0
Voull = 5.0 * 1728.0
Vftank = 78.66 * 1728.0
Votank = 95.11 * 1728.0
Vtanks = Vftank + Votank
Vullage = Vfull + Voull
Vliq = Vtanks - Vullage
tburn = 400.0
Vbottle = 8.7 * 1728.0
Pbottle=4455.0

Peff = (Vftank*184.4 + Votank*171.0)/Vtanks

tf = TankPress(gas="HE", Vbottle=Vbottle, Vullage=Vullage, Vliq=Vliq, vdotLiq=Vliq/tburn,
    Pbottle=Pbottle, Ptank=Peff,
    Tbottle=530.0, Tullage=530.0, initTullage=1, AccGees=1.0,
    PVoW_Bottle=500000., PVoW_Tank=100000.,
    Nbottle=3, ellBottle=1.0, LcylOvDBottle=0.0, Cp_effBottle=0.125, # Cp Ti=.125, Al=.2, Monel=.1
    Ntank=2, ellTank=1.414, LcylOvDTank=1.0, Cp_effTank=0.15,
    CdARegMax=None,  NtimeSteps=100, 
    QexternalIntoBottle=2.4, dPregulator=2.0 )
    
tf.makeExcelPlots( title='NII Delta' )
