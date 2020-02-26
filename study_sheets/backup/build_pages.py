
import os
from dateutil import parser
from build_html_study_file import BuildHTML
from prefix import prefixD
import os
import time
from win32_setctime import setctime

here = os.path.abspath(os.path.dirname(__file__))

path_nameD = {} # index=zip_name: value=(dir_name, datetime)

dir_name = ''
for line in open('temp.txt','r'):
    
    if line.startswith(' Directory'):
        print('Dir:', line[14:].strip() )
        dir_name = line[14:].strip()
    
    if line.find('flash.zip') >= 0:
        zip_name = line[39:].strip()
        date_str = line[:22].strip()
        file_date = parser.parse( date_str )
        full_path = os.path.join( dir_name, zip_name )
        print( '    ',full_path )
        
        
        if zip_name not in path_nameD:
            path_nameD[ zip_name ] = (dir_name, file_date)
        else:            
            if file_date > path_nameD[ zip_name ][1]:
                print('Replacing:',path_nameD[ zip_name ][1],' with ',file_date)
                print('      for:', zip_name)
                path_nameD[ zip_name ] = (dir_name, file_date)
            else:
                print('Keeping:',path_nameD[ zip_name ][1],' over ',file_date)
                print('    for:', zip_name)
            
print('='*77)


for zip_name, (dir_name, file_date) in path_nameD.items():
    BH = BuildHTML()
    full_path = os.path.join( dir_name, zip_name )
    BH.load_file( full_path )
    
    if dir_name in prefixD:
        s = prefixD[ dir_name ]
        if s:
            s = s + '_'
        html_file_name = os.path.join( here, s + zip_name.split('.')[0] + '.html')
        
    else:
        html_file_name = os.path.join( here, zip_name.split('.')[0] + '.html')
    
    if 1:# os.path.isfile( html_file_name ):
    
        print( 'Saving to',html_file_name)
        BH.launch_web_browser_study_sheet( html_file_name, single_column=True, 
                                           launch_browser=False )


        modTime = time.mktime(file_date.timetuple())
        os.utime( html_file_name, (modTime, modTime) )
        setctime( html_file_name,  modTime )
        
