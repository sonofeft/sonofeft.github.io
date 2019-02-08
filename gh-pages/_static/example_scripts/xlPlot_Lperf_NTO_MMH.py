from prism import *
from prism.utils import xlChart

pcentFFC=15.0
etaPulse=1.0
mrBarrier=0.15
FvacGoal = 1200.0
elemDens=None # if None use d/v
Em=0.85

pc=500.0
eps=22.7
oxName= 'N2O4'
fuelName='MMH'

Tox=500.0    # Tox=None if using reference point
Tfuel=500.0  # Tfuel=None if using reference point

props = oxName + '/' + fuelName
mrLow=0.5
mrHigh=2.5
Nsteps = 25

LoverDt=0.1
LchamMin=1.5

rs = [ ['MRcore','IspODE','IspODK','IspWOFFC','IspDel','MRengine','Tcomb','CstarWOFFC','AreaRatio','Pc',
        'etaKin', 'etaDiv', 'etaBL', 'etaVap', 'etaMix', 'etaEm', 'etaFFC', 'etaPulse'] ]

delMR = (mrHigh-mrLow)/Nsteps

LprimeMin = 99999.0
LprimeMax = 0.0
elemDensMin = 99999.0
elemDensMax = 0.0

for i in range(Nsteps+1):
    mr = mrLow + i * delMR
    
    Engine = Engine_FFC(name="Est Engine",
                    oxName=oxName, fuelName=fuelName, etaERE=0.98,
                    Pc=pc, Fvac=FvacGoal, eps=eps, mr=mr, CR=2.5, LoverDt=LoverDt,  LchamMin=LchamMin,
                    pcentBell=80.0)
    
    if Engine.Lcham > LprimeMax: LprimeMax = Engine.Lcham
    if Engine.Lcham < LprimeMin: LprimeMin = Engine.Lcham
    
    LP = Lperf( engine = Engine ,Tox=Tox, Tfuel=Tfuel, elemDens=elemDens, 
        pcentFFC=pcentFFC, mrBarrier=mrBarrier, etaPulse=etaPulse, Em=Em)
    
    if LP.elemDensCalc > elemDensMax: elemDensMax = LP.elemDensCalc
    if LP.elemDensCalc < elemDensMin: elemDensMin = LP.elemDensCalc
    
    IspWOFFC = LP.IspDel / LP.etaFFC
    rs.append( [mr, LP.IspODE, LP.IspODK, IspWOFFC,   LP.IspDel,LP.mrEngine,
        LP.TcombODE, LP.CstarDel, eps, pc,
        LP.etaKin, LP.etaDiv, LP.etaBL, LP.etaVap, LP.etaMix, LP.etaEm, LP.etaFFC, LP.etaPulse] )
        
        
        
        
print Engine.getSummary()
print LP.getSummary()

xl = xlChart.xlChart()

xl.xlApp.DisplayAlerts = 0  # Allow Quick Close without Save Message
#xl.makeDataSheet( _resultsRS, sheetName="Tank Fill")

if '%.2f'%LprimeMin=='%.2f'%LprimeMax:
    LprimeStr = "%.2f"%LprimeMin
else:
    LprimeStr = "%.2f-%.2f"%(LprimeMin,LprimeMax)


if '%.1f'%elemDensMin=='%.1f'%elemDensMax:
    elemDensStr = '%.1f'%elemDensMin
else:
    elemDensStr = '%.1f-%.1f'%(elemDensMin,elemDensMax)

if elemDens:
    myTitle = "%s Performance\nFvac=%.0f lbf, Pc=%.0f psia, AR=%.1f\n%.2f elem/sqin, Em=%.2f, L'=%s, fuel film cooling=%.1f%%"%\
        (props, FvacGoal, pc, eps, elemDens, Em, LprimeStr, pcentFFC)
else:
    myTitle = "%s Performance\nFvac=%.0f lbf, Pc=%.0f psia, AR=%.1f\n%s elem/sqin, Em=%.2f, L'=%s, fuel film cooling=%.1f%%"%\
        (props, FvacGoal, pc, eps, elemDensStr,  Em, LprimeStr, pcentFFC)
    
xl.makeChart(rs,  
            title=myTitle,nCurves = 4,
            chartName="Performance",
            sheetName="FillData",yLabel="Isp (sec)", xLabel="Mixture Ratio")
            
xl.changeSeriesXValuesColumn( NColumn=6, NSeries=4)
#xl.putSeriesOnSecondary(2, y2Label="Temperature (degR)")
#xl.makeNewChartOfPlottedColumns(cols=(7,), ZeroBased=0, chartName='Quality')
#xl.changePlotTitle( 'Quality of %s'%tf.gasData.name )
#xl.labelPrimaryYAxis( 'Quality of %s (fraction gas)'%tf.gasData.name )
xl.labelXAxis( 'Mixture Ratio' )
xl.setXrange( 1.0, 2.5)
xl.setYrange( 250.0, 350.0)

       
xl.setLineThickness( NSeries=4, thickness=5)
xl.setSeriesColor( NSeries=4, red=255, green=0, blue=0)
xl.turnMarkerOnOff( NSeries=4, showPoints=0)
 