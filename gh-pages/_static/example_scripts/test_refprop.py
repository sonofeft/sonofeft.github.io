#from prism.props.refprop7.n_dll_fluid import n_fluid
from engcoolprop.ec_fluid import EC_Fluid

h = EC_Fluid("N2")

h.setPD( P=50.0, D=0.1)
h.printTPD()
h.setTP(T=400.0, P=500.0)
h.printTPD()
h.constS_newP(P=1000.0)
h.printTPD()
