from prism import Gas_Orifice

orf = Gas_Orifice(name="gas orifice", gasSymbol='O2',  matlName="Ti", 
        CdAInp=0.1, wdot=1.1, TgasDegR=530.0,
        usePinlet=0, PgasOutlet=400.0, PgasInlet=400.0, 
        Number=1, sf=4.0, cxw=1.25)
        
print orf.getSummary()
