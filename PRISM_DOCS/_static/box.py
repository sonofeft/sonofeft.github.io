from prism import *
from math import *

markdown_desc = """
This example is taken from the [ParaSol](http://parasol.readthedocs.io/en/latest/index.html) program's 
[Example #3](http://parasol.readthedocs.io/en/latest/example3.html)

The purpose of this example is to maximize the volume of an open topped box starting with a rectangle of cardboard measuring (10 x 20).

The image below shows the basic cardboard shape, after the (h x h) squares have been removed from all four corners of the original rectangle.

![Box Dimensions](./box.jpg)
"""

# create system object (make sure author is correct... it's used for report)
S = SysModel(name="Box Design", type="misc", 
    author="C.N. Tainer", programName="Simple Optimization",
    markdown_desc=markdown_desc)


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ['Lmatl',20,10,30,1,'in','Length of Material'],
    ['Wmatl',10,8,12,0.2,'in','Width of Material'],
    ['hbox',1,0.2,3.8,0.18,'in','Height of Box'],
    )


# now add any Result Variables That might be plotted
# "boxMass" is required
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ['Volume','cuin','Box Volume'],
    ['boxMass','lbm','Box Mass'],
    )


SimpleEqnMass_1 = SimpleEqnMass(name="Simple Mass", type="inert",  mass_lbm=0.0,  eqn="1.2*1.1", desc='mass = simple eqn')


#=====  after they have been created, add the Mass Items to the system object ====
S.addMassItem( SimpleEqnMass_1 )



# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Lmatl,Wmatl,hbox = S("Lmatl","Wmatl","hbox")

    S.reCalc()

    # cut a Wmatl x Lmatl sheet to make a box.
    Volume = (Wmatl-2*hbox)*(Lmatl-2*hbox)*hbox
    
    boxMass = Wmatl*Lmatl - 4*hbox**2

    # "boxMass" is required
    S["boxMass"] = boxMass
    S["Volume"] = Volume

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()



# now optimize the system... it should match up with the carpet plots.
optimize(S, figureOfMerit="Volume", desVars=['hbox'], findmin=0, useCOBYLA=0)

makeSensitivityPlot(S, 
    figureOfMerit="Volume", desVars=['hbox'],
    makeHTML=1, dpi=70, linewidth=2)


makeCarpetPlot(S, sysParam="Volume", 
    desVarL=[["hbox",1,1.3,1.6,2.5,3.3],["Lmatl",20,25,30]],
    xResultVar="boxMass",
    makeHTML=1, dpi=100, linewidth=2, smallLegend=1,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', 
    haLabel='center', vaLabel='center')

if 0:
    makeSensitivityPlot(S, 
        figureOfMerit="Volume", desVars=['Lmatl', 'Wmatl', 'hbox'],
        makeHTML=1, dpi=70, linewidth=2)


    makeContourPlot(S, sysParam="Volume", desVars=["Wmatl","hbox"],
            interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
            dpi=70, colorMap="summer")


    make2DParametricPlot(S, sysParam="Volume", desVar="hbox",
        paramVar=["Wmatl",1.0,1.5,2.0,2.5]  ,makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0)


    makeContourPlot(S, sysParam="Volume", desVars=["Lmatl","hbox"],
            interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
            dpi=70, colorMap="summer")


    make2DPlot(S, sysParam=['Volume'], desVar='Lmatl', makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='')


# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
