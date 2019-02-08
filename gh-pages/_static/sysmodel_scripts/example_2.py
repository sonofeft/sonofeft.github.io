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
    PHe    = S("PHe")
    he.PHeTnk =  PHe
    he.reCalc()
    Hetank.vfree = he.volHeTotal
    Hetank.ptank = PHe
    S.reCalcItems()
    
    S["HeSysMass"] = he.mass_lbm + Hetank.mass_lbm
    S["HeMass"] = he.mass_lbm
    S["HeTankMass"] = Hetank.mass_lbm
    
    S["HePVoverW"] = Hetank.PburstVoverW
    S["HeVolume"] = he.volHeTotal / 1728.0
    
Hetank.texture = Texture( colorName="Gray50" )
Oxtank.texture = Texture( colorName="Aquamarine" )
Fltank.texture = Texture( colorName="Pink" )


S = SysModel(author="I.B. Simpleton", name="simple system", type="trial baloon", 
    controlRoutine=myControlRoutine, renderControlRoutine=None)
S.addMassItem( Oxtank )
S.addMassItem( Fltank )
S.addMassItem( he )
S.addMassItem( Hetank )


# design vars have: 
#     name, value, minVal, maxVal, step,  units,  description
S.addDesignVariable( name="PHe", InitialVal=3250.0, minVal=500.0, maxVal=8000.0, step=200.0)

# result variables have: 
#    name,      units,  description
S.addResultVars( ["HeSysMass", "lbm", "Helium System Mass"] )
S.addResultVars( ["HeMass", "lbm", "Helium Gas Mass"] )
S.addResultVars( ["HeTankMass", "lbm", "Helium Tank Mass"] )
S.addResultVars( ["HePVoverW", "", "Helium Tank PV/W"] )
S.addResultVars( ["HeVolume", "cuft", "Helium Tank Volume"] )

print S.getShortSummary()

make2DPlot(S, sysParam="HePVoverW", desVar="PHe")

make2DPlot(S, sysParam="HeVolume", desVar="PHe")

make2DPlot(S, sysParam=["HeMass","HeTankMass","HeSysMass"], desVar="PHe")

makeMassItemSensitivityPlot(S, makeHTML=1,desVar="PHe", showDelta=0,
    excludePropellant=0, dpi=70)
    
S.saveFullSummary()

S.close()
