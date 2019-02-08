
from prism.isp.cea.CEA_Isp import CEA_Isp
from pylab import *

Pc = 500.0
pcL = [ 2000., 500., 70.]

ispObj = CEA_Isp(propName='', oxName='LOX', fuelName="LH2")

for Pc in pcL:
    cstarArr = []
    MR = 2.0
    mrArr = []
    while MR < 8.0:
        cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR) )
        mrArr.append(MR)
        MR += 0.05
    plot(mrArr, cstarArr, label='Pc=%g psia'%Pc)

legend(loc='best')
grid(True)
title( ispObj.desc )
xlabel( 'Mixture Ratio' )
ylabel( 'Cstar (ft/sec)' )
savefig('cea_cstar_plot.png', dpi=120)

show()
