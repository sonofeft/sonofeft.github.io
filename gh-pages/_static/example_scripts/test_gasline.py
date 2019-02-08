from prism import Line_Gas

h = Line_Gas(name="Ox Line",wdot=1.0, matlName="Ti", thkWallInp=0.083,
    calcVelFromDiamInp=1, DiamInp=1.0,
    usePinlet=1, velFPS=20.0, PgasInlet=1000.0, TgasDegR=530.0,
    gasSymbol='O2', Number=10, Kfactors=2.0)

print h.getSummary()
