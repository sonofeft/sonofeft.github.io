from prism.utils import xlChart
from prism.utils.colebrook import colebrook_ffact, buzzelli_ffact
from math import log10

diam = 0.2  # inch diam
rough = 0.0001  # in
eod = rough / diam
ReNum = 1.0E3  # start in laminar region
rs = [['ReNum','Colbrook','Buzzelli','Haaland']]  # plot data

while ReNum < 1.0E8:
    ffColebrook = colebrook_ffact(rough, diam, ReNum)
    ffBuzz = buzzelli_ffact(eod, ReNum)
    ffHaaland = (1.0/ (-1.8*log10((eod/3.7)**1.11 + 6.9/ReNum)) )**2
    
    rs.append( [ReNum, ffColebrook, ffBuzz, ffHaaland] )
    ReNum *= 1.2
    
xl = xlChart.xlChart()
xl.makeChart(rs, title="Friction Factor", nCurves = len(rs[0])-1,
    chartName="ff", sheetName="ffData",
    yLabel="Friction Factor", xLabel="Reynolds Number")
             
xl.setXScaleType( log=1 )
xl.addTextBox(text="""Diam = %g in\nRoughness = %g in\ne/D = %g"""%(diam,rough,eod))
xl.setXrange( 1000.0, 1.0E8)