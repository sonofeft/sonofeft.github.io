from prism import Engine_Regen

regenEng = Engine_Regen( name="regen engine",  oxName='N2O', fuelName='Ethanol',
        cxw=1.25, Pc=519.0, Fvac=76894.0, eps=32.0, mr=5.25, DtInp=None,
        CR=2.5, LoverDt=1.0, LchamMin=17.8, xlnOverLcham=1.0,
        etaERE=0.97, etaNoz=0.99, matlInj="SS", cxwInj=1.0, cxwValves=1.0, isBell=1, pcentBell=80.0,
        halfAngDeg=15.0, useFastCEALookup=0, Number=1, etaKinInp=0.984,
        calcEtaNoz=1, thkNozExtMin=0.03, matlNozExt="Cb103", minBipropValveWt=0.2,
        valvesMassInput=None, Pamb=2.0,
        epsNozExt=60.0, SFcloseout=2.0, matlCloseout='Ni', matlGasWall="CuZr",
        thkMinCloseout=0.05, thkMinGasWall=0.05, aveLandWidth=0.05, aveChannelWidth=0.05,
        aveChannelHeight=0.05)

print regenEng.getSummary()
    
