import sys
import os
from prism import *


vOxTank = 150000.0
vFlTank = 100000.0
vPropTanks = vOxTank + vFlTank
ptank = 300.0
PHeTnk=2000.0

Oxtank = Tank(name="Oxidizer Tank", makeCompositeTank=0, matlName="Ti",
    kacqui=4, tliner=0.030, vfree=vOxTank, ptank=ptank)
Fltank = Tank(name="Fuel Tank", makeCompositeTank=0,
    kacqui=4, tliner=0.030, vfree=vFlTank, ptank=ptank)

he = PressurantHe(name="Helium Pressurant",
    VpropTnk=vPropTanks,PHeTnk=PHeTnk,PpropNom=159.36,
    PfinHeOvPnom=1.0,
    tAction=433.94,TminR=510.0,TmaxR=550.0)

Hetank = Tank(name="Helium Tank",  makeCompositeTank=0,
   matlName="Ti", ptank=PHeTnk,
    tliner=0.030, vfree=he.volHeTotal)

def myControlRoutine(S):
    PHe    = S.getDesignVar("PHe")
    he.PHeTnk =  PHe
    he.reCalc()
    Hetank.vfree = he.volHeTotal
    Hetank.ptank = PHe
    S.reCalcItems()
    
    S["sysMass"] = S.mass_lbm
    
Hetank.texture = Texture( colorName="Gray50" )
Oxtank.texture = Texture( colorName="Aquamarine" )
Fltank.texture = Texture( colorName="Pink" )

def myRenderControlRoutine(S):
    povItemL = []
    loc = 0.0
    for i,item in enumerate(S.items):
        povItem = item.getPOV_Item()
        if povItem:
            povItemL.append( povItem )
        
            if len(povItemL)>0:
                loc = loc + item.pov_w/2.0 + S.items[i-1].pov_w/2.0
                povItemL[-1].translate([loc,0.,0.])
        
        
    return povItemL

S = SysModel(author="I.B. Simpleton", name="simple system", type="trial baloon", 
    controlRoutine=myControlRoutine, renderControlRoutine=myRenderControlRoutine)
S.addMassItem( Oxtank )
S.addMassItem( Fltank )
S.addMassItem( he )
S.addMassItem( Hetank )

# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesignVariable( name="PHe", InitialVal=3250.0, minVal=500.0, maxVal=10000.0, step=200.0)

# result variables have: 
#    name,      units,  description
S.addResultVars( ["sysMass", "lbm", "Total System Mass"] )


print S.getMassStr()
print
print S.getShortSummary()
#print Hetank.getSummary()

S.render()

#optimize(S, figureOfMerit="mass_lbm", desVars=["PHe"])
#print S.getShortSummary()
#print Hetank.getSummary()

make2DPlot(S, sysParam="sysMass", desVar="PHe")


S.close()
