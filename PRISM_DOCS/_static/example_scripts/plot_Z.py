
from pylab import *
#from prism.props.refprop7.n_dll_fluid import n_fluid
from engcoolprop.ec_fluid import EC_Fluid

gasL = ['N2','HE']
tL = [0., 45., 90.]  # degF
pL = range(1000, 15001, 100)

for gas in gasL:
    h = EC_Fluid(gas)
    
    for tF in tL:
        tR = tF + 460.0
        zL = []
        for p in pL:
            h.setTP(T=tR, P=p)
            zL.append( h.compressibility() )
            print gas,'%g F  '%tF,'%g psia  Z='%p,h.compressibility() 
            
        plot(pL, zL, label='%s (T=%gF)'%(gas,tF), linewidth=2)

legend(loc='best')
grid(True)
title( 'Compressibility Factor' )
xlabel( 'Pressure (psia)' )
ylabel( 'Z = (PV/nRT)' )
savefig('Z_compare2.png', dpi=120)

show()
