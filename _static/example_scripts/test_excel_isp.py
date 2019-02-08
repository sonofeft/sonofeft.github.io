from prism.utils import xlChart
from numpy import arange
from prism.isp.cea.CEA_Isp import CEA_Isp

Pc = 500.0
epsL = [ 50., 20., 10.]

topRow = ['MR']
for eps in epsL:
    topRow.append( 'AR=%g'%eps )

rs = [topRow]

ispObj = CEA_Isp(propName='', oxName='LOX', fuelName="LH2")
mrL = arange(2.0,8.1,0.1)

for MR in mrL:
    row = [MR]
    for eps in epsL:
        IspODE, Cstar, Tcomb = ispObj.get_IvacCstrTc(Pc=Pc, MR=MR, eps=eps )
        row.append( IspODE )
    rs.append(row)

xl = xlChart.xlChart()
xl.makeChart(rs, title="IspODE for "+ispObj.desc+" (NASA CEA Code)", nCurves=len(epsL),
             chartName="IspODE",
             sheetName="IspODE Dataset",
             yLabel="IspODE (sec)", xLabel="Mixture Ratio")
