from prism import Engine_FFC

EngineDivert = Engine_FFC(name="Divert Engine", 
    oxName='N2O4', fuelName='MMH', Number=4,
    cxw=1.0, Pc=200.0, Fvac=1000.0, eps=10.0, mr=1.65, 
    CR=2.5, LoverDt=2.0, LchamMin=1.5, cxwValves=1.0,
    etaERE=0.97, calcEtaNoz=1, useFastCEALookup=1,isBell=1, pcentBell=80.,
    halfAngDeg=15.0, xlnOverLcham=0.9)

print EngineDivert.getSummary()
    
