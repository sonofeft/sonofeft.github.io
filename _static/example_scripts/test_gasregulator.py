from prism import Gas_Regulator

reg = Gas_Regulator(name="gas regulator", gasSymbol='O2',  matlName="Ti", 
        wdot=1.0, TgasInit=530.0, TgasFinal=400.0,
        PgasOutlet=400.0, PgasInit=4000.0,  PgasFinal=800.0,
        Number=1, CdASF=1.5, sf=4.0, cxw=1.25)
        
print reg.getSummary()
