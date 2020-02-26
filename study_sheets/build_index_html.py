
import os
import glob
from datetime import datetime
from index_template import top, bottom

html_fileL = glob.glob( '*.html' )

sL = []

date_nameL = sorted([ (os.path.getctime(path_to_file), path_to_file) for path_to_file in html_fileL  ], reverse=True)
for d,n in date_nameL:
    if n != 'index.html':
        date_time = datetime.fromtimestamp( d )

        sdate = date_time.strftime("%m/%d/%Y")
        #print( sdate, n )
        
        sL.append( '''<TR><TD> %s </TD><TD><BUTTON Class="prompt" onclick="window.location.href = '%s';">%s</BUTTON></TD></TR>'''%( sdate, n, n) )
  
content = '\n'.join(sL)

fOut = open('index.html', 'w')
fOut.write( top + content + bottom )
fOut.close()