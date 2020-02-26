import sys
import sys
import os
import io
import json
import zipfile
import time
import random
from question_obj import Question_Collection
from make_html_study_sheet import Study_Html_output
import webbrowser
import base64
#from PyQt4.QtGui import QVBoxLayout, QImage

class BuildHTML( object ):
    def __init__(self):
        self.QcollL = [] # list of Question_Collection objects
        self.zip_fileL = [] # list of zip files (for images)
        
    
    def load_file(self, full_fname):
        
        head,tail = os.path.split( full_fname )
        
        zf = zipfile.ZipFile(full_fname, 'r')
        json_data = zf.read('flashcard_info.json')
        json_obj = json.loads( json_data )
        zf.close()
        

        promptL = []
        answerL = []
        hintL = []
        big_hintL = []
        storyL = []
        imageL = []
        
        Question_Coll = Question_Collection( title=json_obj['title'] )

        #if json_obj.has_key('list_of_prompts'):
        if 'list_of_prompts' in json_obj:
            promptL = json_obj['list_of_prompts']
            answerL = json_obj['list_of_answers']
            hintL = json_obj['list_of_hints']
            big_hintL = json_obj['list_of_big_hints']
            storyL = json_obj['list_of_stories']
            imageL = json_obj['list_of_images']
                            
            for p,a,h,bh,s,i in zip(promptL,answerL,hintL,big_hintL,storyL,imageL):
                Question_Coll.add_question(prompt=p, answer=a, hint=h, big_hint=bh,
                       story=s, image=i)
                
            self.QcollL.append( Question_Coll )
            self.zip_fileL.append( full_fname )
            
    def launch_web_browser_study_sheet(self, html_file_name, single_column=False,
                                       launch_browser=True):
        
        for iq in range( len(self.QcollL) ):
            
            Qcoll = self.QcollL[iq]
            zip_file = self.zip_fileL[iq]
            questionL = Qcoll.questionL
            
            promptL = [q.prompt for q in questionL]
            answerL = [q.answer for q in questionL]
            hintL = [q.hint for q in questionL]
            big_hintL = [q.big_hint for q in questionL]
            storyL = [q.story for q in questionL]
            imageL = [q.image for q in questionL]
            

            zf = zipfile.ZipFile(zip_file, 'r')

            rightL = []
            
            for i in range( len(questionL) ):
                if answerL[i]:
                    s_ans = answerL[i]
                else:
                    s_ans = ''
                
                s_other = '<br>'.join( [hintL[i], big_hintL[i], storyL[i]] )
                    
                while s_other.startswith('<br>'):
                    s_other = s_other[4:]
                    
                #while s_other.find('<br><br>')>=0:
                #    s_other = s_other.replace('<br><br>','<br>')
                
                # maybe place img into string
                if imageL and imageL[i]:
                    # read bytes from archive
                    img_data = zf.read(imageL[i])
                    b64_img = base64.b64encode( img_data ).decode('utf-8')
                    #img = QImage()
                    #img.loadFromData( img_data )
                    #print( len( img_data ))
                    if len( img_data ) > 631: # blank img is 631
                        s = '<div>' + s_ans + '<br>' + s_other + '</div>' + \
                            '<div><img src="data:image/png;base64,' + \
                            b64_img + '" alt="%i.jpg">'%i + \
                            '</div>'
                            # '</div><div>' +s_other + '</div>'
                    else:
                        s = s_ans + '<br>' + s_other
                else:
                    s = s_ans + '<br>' + s_other
                
                
                rightL.append( s )
            zf.close()
                
            if iq == 0:
                HTML_obj = Study_Html_output( title=Qcoll.title, 
                                              leftL=promptL, 
                                              rightL=rightL, single_column=single_column )
            else:
                HTML_obj.add_table(title=Qcoll.title, 
                                   leftL=promptL, 
                                   rightL=rightL, single_column=single_column )
            
            
        head,tail = os.path.split( self.zip_fileL[-1] )
        html_file_name = os.path.join( head, html_file_name )
        print( 'html_file_name="%s"'%html_file_name)
        
        
        #fOut =  open( html_file_name, 'w' )
        fOut = io.open(html_file_name, "w", encoding="utf-8")
        
        sOut = str(HTML_obj)
        fOut.write( sOut )
        fOut.close()
        
        if launch_browser:
            webbrowser.open( html_file_name )
            
                

if __name__=="__main__":
    
    fname = r'D:\2020_py_proj\FlashList\Decision_Trees.flash.zip'
    fname = r'D:\2020_py_proj\FlashList\US State Capitals.flash.zip'
    fname = r'D:\GoProj\GoLang.flash.zip'
    
    BH = BuildHTML()
    BH.load_file( fname )
    print( BH.QcollL)
    print()
    
    html_file_name = fname[:-10] + '.html'
    print( 'Saving to',html_file_name)
    BH.launch_web_browser_study_sheet( html_file_name, single_column=True, launch_browser=True )
    