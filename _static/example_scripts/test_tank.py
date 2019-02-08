from prism.tanks.Tank import Tank

oxekv = Tank(name="Divert Vehicle Propellant Tank", 
    makeCompositeTank=1, kalmod=0,  
    matlName="grEpox",   vfree=486.0,ell=1.767,rcyltd=1.445,
    ptank=1400.0,sf=1.5,cxw=1.5,
    ithcyl=1,kacqui=1,inpex=1,expefi=0.98,
    tblad=0.030,tbond=0.030,ttrspc=0.010,
    rhobnd=0.04,rhoacq=0.098,tliner=0.03,rholiner=0.098)

print oxekv.getSummary()
