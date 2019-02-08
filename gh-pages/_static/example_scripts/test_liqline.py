from prism import Line_Liq, Inc_liquid

Fl = Inc_liquid( symbol="N2H4",T=530.0,P=240.0, mass_lbm=10.0)

h = Line_Liq(name="Fuel Line",wdot=2.0, matlName="Ti", velFPS=40.0,
    liqObj=Fl, Number=10, Kfactors=5.0, pLine=400.0)

print h.getSummary()
