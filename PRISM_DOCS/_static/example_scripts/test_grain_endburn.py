from prism import Grain_EndBurn

grain = Grain_EndBurn(name="grain(end burner)",  
        WpropBurned=200.0, propName='ARC448', 
        cxw=1.0, Pc=500.0, FvacMaxPerGG=300.0, IspVacDel=238.6)
        
print grain.getSummary()
