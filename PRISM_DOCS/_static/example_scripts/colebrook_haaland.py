
from prism.utils.colebrook import colebrook_ffact, buzzelli_ffact
from math import log10

ReNum = 2.0E5
diam = 0.2
rough = 0.0001 # in
eod = rough / diam

ffColebrook = colebrook_ffact(rough,diam,ReNum)
ffBuzzelli = buzzelli_ffact(eod, ReNum)
ffHaaland = (1.0/ (-1.8*log10((eod/3.7)**1.11 + 6.9/ReNum)) )**2

print 'Colebrook:','%g'%ffColebrook
print 'Buzzelli :','%g'%ffBuzzelli, \
    '(%+.2f'%((ffBuzzelli-ffColebrook)*100.0/ffColebrook),'% Error)'
print 'Haaland  :','%g'%ffHaaland, \
    '(%+.2f'%((ffHaaland-ffColebrook)*100.0/ffColebrook),'% Error)'
