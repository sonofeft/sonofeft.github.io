from prism import *
from math import *

S = SysModel(name="Optimization Test", type="misc", 
    author="C. Taylor", programName="Simple Optimization")


S.addDesignVariable( name="x", InitialVal=0.1, minVal=0.0, maxVal=2.0)

S.addResultVariable( name="y")

def myControlRoutine(S):
    
    x = S('x')
    
    S['y'] = sin(x)

S.setControlRoutine(myControlRoutine)

optimize(S, figureOfMerit="y", desVars=['x'], findmin=0, useCOBYLA=1, print_summary=True)

#print S.getShortSummary()

print 'Correct answer is: x = pi/2 =',pi/2.0