from math import *
from prism import *


Tref = 527.67
ASSUMESATURATION = 1
PRESS = 1000.0

markdown_desc = """
When designing the tanks for a liquid propellant system, it is necessary to know the worst-case
propellant density, (usually max storage temperature) so that the tanks can be large enough at 
that condition.

There are a number ways to get propellant density in PRISM.

1. correlations from literature in the routind **dsat**
2. extrapolation from corresponding states (i.e. critical properties) in **prolib**
3. the open source code **CoolProp** via **EngCoolProp**
4. the commercial code **Refprop**

Each of the above approaches is constrained to just those propellants included in each of the models.

The graph below uses *dsat* to calculate saturated density for:

* IRFNA
* N2O4
* MON15
* MON25
* Water (H2O)
* MMH

Notice that the freezing point is shown for each propellant.

**dsat** continues to estimate density for the frozen condition, even though it is outside the limits of the correlations.
The code uses an anchored method of corresponding states to do the extrapolation.

If the stage is not intended to experience frozen propellants, that constraint must be imposed by the user.

"""

# create system object (make sure author is correct... it's used for report)
S = SysModel(programName="Propellant Properties Comparison", type="Liquid", 
    author="Scooter Rho", name="Propellant Properties Comparison",
    markdown_desc=markdown_desc)


# add design variables to the system (these variables may be used to
# optimize the system or to create plots)
# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesVars(
    ['Temperature',Tref,384.67,589.67,4.88095,'degR','Temperature of fluid'],
    )


# now add any Result Variables That might be plotted
# "sysMass" is required
# result variables have: 
#    name,      units,  description
S.addResultVars(
    ['MMH','lbm/cuft','Density of Monomethyl Hydrazine'],
    ['N2O4','lbm/cuft','Density of Nitrogen Tetroxide'],
    ['MON15','lbm/cuft','Density of MON-15'],
    ['MON25','lbm/cuft','Density of MON-25'],
    ['IRFNA','lbm/cuft','Density of Inhibited Red Fuming Nitric Acid'],
    ['H2O','lbm/cuft','Density of Water'],
    ['sysMass','lbm','Total System Mass'],
    )


MMH = Inc_liquid(symbol="MMH",T=Tref,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)
N2O4 = Inc_liquid(symbol="N2O4",T=None,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)
MON15 = Inc_liquid(symbol="MON15",T=None,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)
MON25 = Inc_liquid(symbol="MON25",T=None,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)
IRFNA = Inc_liquid(symbol="IRFNA",T=None,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)
H2O = Inc_liquid(symbol="Water",T=None,P=None, assumeSaturation=ASSUMESATURATION, mass_lbm=1)


#=====  after they have been created, add the Mass Items to the system object ====
#  if in addMassItem, then one call to S.reCalc() will recalc all of them
S.addMassItem( [MMH, N2O4, MON15, MON25, IRFNA, H2O] )

# the following control routine ties together the system components
#  with the system design variables
def myControlRoutine(S):
    # get current values of design variables    
    Temperature = S("Temperature")

    MMH.setTP(T=Temperature,P=PRESS)
    N2O4.setTP(T=Temperature,P=PRESS)
    MON15.setTP(T=Temperature,P=PRESS)
    MON25.setTP(T=Temperature,P=PRESS)
    IRFNA.setTP(T=Temperature,P=PRESS)
    H2O.setTP(T=Temperature,P=PRESS)

    S.reCalc() # All added MassItem objects are recalculated.

    # set all result variables
    S["MMH"] = MMH.D
    S["N2O4"] = N2O4.D
    S["MON15"] = MON15.D
    S["MON25"] = MON25.D
    S["IRFNA"] = IRFNA.D
    S["H2O"] = H2O.D

# need to tell system the name of the control routine
S.setControlRoutine(myControlRoutine)

S.reCalcItems()


S.saveShortSummary() # if no mass items, then do not call

if ASSUMESATURATION:
    yLabel = 'Saturated Liquid Density (lbm/cuft)'
else:
    yLabel = 'Liquid Density at P=%g psia (lbm/cuft)'%PRESS

propL = ['IRFNA','N2O4','MON15','MON25','H2O','MMH']
freezeL = [get_freezing_pt(prop, 'degR') for prop in propL]

dobjL = [IRFNA,N2O4,MON15,MON25,H2O,MMH]
satdL = []
for dobj,T in zip(dobjL, freezeL):
    dobj.setTP(T=T,P=PRESS)
    satdL.append( dobj.D )

make2DPlot(S, sysParam=['IRFNA','N2O4','MON15','MON25','H2O','MMH'], 
    desVar='Temperature', makeHTML=1, dpi=120, linewidth=2,
    ptData=[freezeL, satdL], ptLegend='Freeze Pts', 
    logX=0, logY=0, xResultVar=None, colorL=None, yLabel=yLabel,
    legendOnLines=0, titleStr=' ')

# now save summary of system
S.saveFullSummary()

# Be sure to wrap-up any files
S.close()
