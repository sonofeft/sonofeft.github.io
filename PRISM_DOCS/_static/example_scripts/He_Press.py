from prism import PressurantInteg

h = PressurantInteg(name="General Test", gas='HE',
    VpropTnk=300000.0,PGasTnkMEOP=4455.0,PpropNom=180.0,
    Nbottle=4,
    PfinGasOvPnom=0.9, heatExchangerTout=None,
    tAction=400.0,TminR=510.0,TmaxR=550.0, useDBruns=0, TbottleMatlConst=None)

print h.getSummary()
