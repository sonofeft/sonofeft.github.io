from prism.utils.InterpProp import InterpProp
from pylab import *

mrL = [3,3.75,4.5,5.25,6,6.75]
isptdkL = [273.2843,286.8167,293.3783,293.5222,289.6593,284.6533]
plot(mrL, isptdkL, 'o', label='TDK Data', linewidth=2)

ispTerp = InterpProp(mrL, isptdkL, extrapOK=1, linear=0)
ispTerp2= InterpProp(mrL, isptdkL, extrapOK=0, linear=1)

mr = 2.6
mL = []
iL = [];  i2L = []
while 1:
    isp = ispTerp( mr ) # use quadratic interpolation with extrapolation
    isp2 = ispTerp2( mr ) # use linear interpolation w/o extrapolation
    
    mL.append( mr )  # save values
    iL.append( isp )
    i2L.append( isp2 )
    
    mr += 0.02 # increment or terminate loop
    if mr > 8.0:
        break

plot(mL, iL, label='TDK Quadratic', linewidth=2)
plot(mL, i2L,label='TDK Linear', linewidth=2)

legend(loc='best')
grid(True)
title( 'Interpolation Test' )
xlabel( 'Mixture Ratio' )
ylabel( 'TDK Isp (sec)' )
savefig('test_terp.png', dpi=120)

show()
