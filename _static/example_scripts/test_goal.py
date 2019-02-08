from prism import Goal
from prism import Engine_FFC

EngineDivert = Engine_FFC(name="Divert Engine", 
    oxName='N2O4', fuelName='MMH', Number=4,
    cxw=1.0, Pc=200.0, Fvac=1000.0, eps=10.0, mr=1.65, 
    CR=2.5, LoverDt=2.0, LchamMin=1.5, cxwValves=1.0,
    etaERE=0.97, calcEtaNoz=1, useFastCEALookup=1,isBell=1, pcentBell=80.,
    halfAngDeg=15.0, xlnOverLcham=0.9)
    
    
print 'Find Area Ratio that has Exit Diameter = 5.0 inches'
print
print 'Initial AR =',EngineDivert.eps,' Dexit =',EngineDivert.Dexit
                    
def newDexit( e ):
    EngineDivert.eps = e
    EngineDivert.reCalc()
    return EngineDivert.Dexit
                
G = Goal(goalVal=5.0, minX=2.0, maxX=80.0, 
    funcOfX=newDexit, tolerance=1.0E-5, maxLoops=40, failValue=80.0)
eps, ierror = G()
print
print 'Area Ratio =',eps,'for Dexit =',EngineDivert.Dexit

print EngineDivert.getSummary()
