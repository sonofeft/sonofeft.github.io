from prism.utils import xlChart
from numpy import arange
from prism.isp.cea.CEA_Isp import CEA_Isp

pcL = [ 2000., 500., 70.]

topRow = ['MR']
for Pc in pcL:
    topRow.append( 'Pc=%g'%Pc )

rs = [topRow]

ispObj = CEA_Isp(propName='', 
    oxName='LOX', fuelName="LH2")
mrL = arange(2.0,8.1,0.1)

for MR in mrL:
    row = [MR]
    for Pc in pcL:
        row.append( ispObj.get_Cstar( Pc=Pc, MR=MR) )
    rs.append(row)

xl = xlChart.xlChart()
xl.makeChart(rs, title="Cstar for "+ispObj.desc, nCurves = len(pcL),
             chartName="Cstar",
             sheetName="Cstar Dataset",
             yLabel="Cstar (ft/sec)", xLabel="Mixture Ratio")
