from pylab import *
from prism.utils.colebrook import colebrook_ffact, buzzelli_ffact

e = 5.0e-6
diam = 1.0
eList = [.03, .01, .003, .001, .0003, .0001, .00001, .000001]

cycle = [1.0]
while cycle[-1]<10.0:
    cycle.append( cycle[-1] * 1.1 )
cycle = cycle[:-1]

ReList = [1.E3, 1.E4, 1.E5, 1.E6, 1.E7]

for e in eList:
    xRe = []
    yFF = []

    for ReBase in ReList:
        for cyVal in cycle:
            ReNum = ReBase * cyVal
            ff = colebrook_ffact(e,diam,ReNum)
            #print ReNum, ff
            xRe.append( ReNum )
            yFF.append( ff )
            
    #p.add( biggles.Curve(xRe, yFF, color="red") )
    
    semilogx(xRe,yFF,linewidth=3, label='Ce/D=%G'%e )

legend(loc='best')

grid(True)
title( "Colebrook Friction Factor" )
xlabel( "Reynolds Number" )
ylabel( "Friction Factor" )

ax = axes()
ax.set_xlim( (1.0E3, 1.0E8) )

show()
