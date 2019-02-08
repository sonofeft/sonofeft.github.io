from prism import Line_Liq_inpD, Inc_liquid

Fl = Inc_liquid( symbol="N2H4",T=530.0,P=240.0, mass_lbm=10.0)

h = Line_Liq_inpD(name="Fuel Line",wdot=2.0, matlName="Ti", OD=0.5,
    liqObj=Fl, Number=10, Kfactors=5.0, pLine=400.0, thkWall=0.045)

print h.getSummary()
