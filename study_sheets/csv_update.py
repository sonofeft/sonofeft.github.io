import csv
import os
from recent_files import RecentFiles
from build_html_study_file import BuildHTML
from win32_setctime import setctime
from datetime import datetime
from index_template import top, bottom

RF = RecentFiles()

study_sheet_dir = r'D:\GoogleDrive\2018_py_proj\GitHub_Blog\study_sheets'

needs_updateD = {} # index=zip_name: value=dir_name

# ============= read data into csv_date_nameL ================
csv_date_nameL = [] # lists of [file date, directory, zip file name, html_fname]

with open('_study_sheet.csv', 'rt', newline='') as f:
    csv_reader = csv.reader(f, skipinitialspace=True)

    for row in csv_reader:
        (file_date, dir_name, zip_name) = row
        full_path = os.path.join( dir_name, zip_name )
        
        # ignore any zip files that no longer exist
        if os.path.isfile( full_path ):
            csv_date_nameL.append( row )

# ============= see if recent files have changed from CSV ===========
csv_replacementD = {} # index=full_path: value=c_time  # used to recreate CSV with current info
for (file_date, dir_name, zip_name) in csv_date_nameL:
    full_path = os.path.join( dir_name, zip_name )
    
    csv_replacementD[ full_path ] = file_date
    if full_path in RF.recent_fileL:
        #print( 'Recent:', full_path )

        c_time_now = os.path.getctime( full_path )
        c_time_csv = float( file_date )
        if c_time_now != c_time_csv:
            #print('    ', c_time_now, c_time_csv, c_time_now - c_time_csv)
            
            # recent is newer than CSV, so add it to needs_updateD dictionary
            needs_updateD[ zip_name ] = dir_name

# ============== check that HTML files exist =============
# if CSV zip file has no HTML file add it to needs_updateD dictionary
for (file_date, dir_name, zip_name) in csv_date_nameL:
    html_fname = os.path.join( study_sheet_dir, zip_name.split('.')[0] + '.html')
    if not os.path.isfile( html_fname ):
        needs_updateD[ zip_name ] = dir_name
        
# if Recent zip file has no HTML file add it to needs_updateD dictionary
for full_path in RF.recent_fileL:
    
    # ignore any zip files that no longer exist
    if os.path.isfile( full_path ):
        dir_name, zip_name = os.path.split( full_path )
        html_fname = os.path.join( study_sheet_dir, zip_name.split('.')[0] + '.html')
        if not os.path.isfile( html_fname ):
            needs_updateD[ zip_name ] = dir_name

# =========== start building new pages ==============
def build_html_file( dir_name, zip_name ):
    BH = BuildHTML()
    full_path = os.path.join( dir_name, zip_name )
    BH.load_file( full_path )
    
    html_file_name = os.path.join( study_sheet_dir, zip_name.split('.')[0] + '.html')
    
    print( 'Saving to',html_file_name)
    BH.launch_web_browser_study_sheet( html_file_name, single_column=True, 
                                       launch_browser=False )

    c_time_now = os.path.getctime( full_path )
    
    os.utime( html_file_name, (c_time_now, c_time_now) )
    setctime( html_file_name,  c_time_now )
    
    csv_replacementD[ full_path ] = c_time_now
        
    

for zip_name, dir_name in needs_updateD.items():
    print( '%-50s %s'%(dir_name, zip_name) )
    
    build_html_file( dir_name, zip_name )

# ==================== rebuild CSV file ==============
index_htmlL = []
with open('_study_sheet.csv', 'wt', newline='') as f:
    csv_writer = csv.writer(f)

    #csv_writer.writerow(['Directory','Date','zip_name']) # write header

    #for zip_name, (dir_name, file_date) in path_nameD.items():
    for full_path, file_date in csv_replacementD.items():
        dir_name, zip_name = os.path.split( full_path )
        
        row = [ float(file_date), dir_name, zip_name ]
        #print( row )
        csv_writer.writerow(row)
        
        index_htmlL.append( row )

# ================= create new index.html ========================
index_htmlL = sorted( index_htmlL, reverse=True )
    
sL = []

for (file_date, dir_name, zip_name) in index_htmlL:
    
    date_time = datetime.fromtimestamp( float(file_date) )
    sdate = date_time.strftime("%m/%d/%Y")

    html_fname =  zip_name.split('.')[0] + '.html'
    
    s_dir = dir_name.replace('D:\\GoogleDrive\\_OnLineClasses','')
    s_dir = s_dir.replace('D:\\GoogleDrive\\','')
    s_dir = s_dir.replace('D:\\Charlie\\Documents','')
    s_dir = s_dir.replace('D:\\GoogleDrive\\','')
    s_dir = s_dir.replace('D:\\','')
    s_dir = s_dir.replace('\\','/')
    if s_dir.startswith('/'):
        s_dir = s_dir[1:]
    
    sL.append( '''<TR><TD> %s </TD><TD><BUTTON Class="prompt" '''%sdate +\
               '''onclick="window.location.href = '%s';">%s</BUTTON></TD>'''%( html_fname, html_fname[:-5]) +\
               '''<TD>%s</TD></TR>'''%s_dir    )
  
content = '\n'.join(sL)

fOut = open('index.html', 'w')
fOut.write( top + content + bottom )
fOut.close()

