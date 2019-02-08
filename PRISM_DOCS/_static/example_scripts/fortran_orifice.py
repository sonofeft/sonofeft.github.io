from prism.fortran import orifice  # a FORTRAN DLL

wdot = 1.0 # lbm/sec
Pin = 500.0 # psia
Tin = 530.0 # degR
Pout = 400.0 # psia
gamma = 1.4 # Cp/Cv
WtMol = 28.0 # lbm/lbmmole

CdA, ImSonic = orifice.solveorificecda(wdot, Pin, Tin, Pout, gamma, WtMol)

print 'CdA =',CdA,'sqin     ImSonic=',ImSonic
