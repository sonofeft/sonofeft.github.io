from prism.isp.tdk import TDKwrap

tdk = TDKwrap.TDK( oxName='O2', fuelName='CH4',raoNozzle=0, varGammaRao=0,
    fracFuelL=None, fracOxL=None,
    MR=3.0, eps=150.0, Rthrt=1.0,
    Pc=250.0,  THETAB=25.0,
    RWTU = 1.0, RWTD = 1.0, calcBL=1,  IWALL=4, THETAI=30.0, ScarfAng=0.0,
    SkewParabTheta=None, SkewParabExitAng=None,
    pcentBell=74.0, Pamb=0.0, findOptParab=0, saveFile='ame_nom', useDBruns=1,
    inpNozContour=None)
                 
print    'tdk.Isp ', tdk.Isp 
print    'tdk.Cstar',tdk.Cstar 
print    'tdk.etaKin1D',tdk.etaKin1D
print    'tdk.etaKin2D',tdk.etaKin2D

print 'Pexit=',tdk.Pexit
print 
print 'IspTDK_wBL=',tdk.IspTDK_wBL
print 'IspODE=',tdk.IspODE

