import os, sys
import json
import zipfile

class Question( object ):
    
    def __init__(self, id=1, prompt='', answer='', hint='', big_hint='',
                   story='', image=''):

        self.id = id
        self.prompt = prompt
        self.answer = answer
        self.hint = hint
        self.big_hint = big_hint
        self.story = story
        self.image = image
        
    def summ_print(self):
        print( 'Question: %s'%self.id)
        print( '  Prompt: %s'%self.prompt)
        print( '  Answer: %s'%self.answer)
        print( '    Hint: %s'%self.hint)
        print( 'Big Hint: %s'%self.big_hint)
        print( '   Story: %s'%self.story)
        print( '   Image: %s'%str(self.image) )
        

class Question_Collection( object ):
    def __init__(self, title='US State Capitals'):
        
        self.title = title
        self.questionL = [] # list of Question objects
        self.next_id = 1 # id entries can be deleted, so there may be id gaps.
        
    def add_question(self, prompt='', answer='', hint='', big_hint='',
                       story='', image=''):
        
        if prompt:
            id = self.next_id
            self.next_id += 1
            Q =  Question(id=id, prompt=prompt, answer=answer, hint=hint, big_hint=big_hint,
                          story=story, image=image)
            self.questionL.append( Q )
        
    def summ_print(self, verbose=False):
        print( 'Question_Collection: "%s"'%self.title )
        print( '  has %i entries'%len(self.questionL) )
        
        if verbose:
            for Q in self.questionL:
                Q.summ_print()
                print( '='*50 )
        
        for Q in self.questionL:
            if Q.image:
                if not os.path.isfile(Q.image):
                    print( 'ERROR...'*5 )
                    print( '  Image file (%s) NOT found for: %s'%(Q.image ,Q.prompt) )

    def get_item_list(self, name='prompt'):
        if name=='prompt':
            return [Q.prompt for Q in self.questionL]
        elif name=='answer':
            return [Q.answer for Q in self.questionL]
        elif name=='hint':
            return [Q.hint for Q in self.questionL]
        elif name=='big_hint':
            return [Q.big_hint for Q in self.questionL]
        elif name=='story':
            return [Q.story for Q in self.questionL]
        elif name=='image':
            return [Q.image for Q in self.questionL]
        else:
            return None

    def get_json_str(self):
        
        pL = [Q.prompt for Q in self.questionL]
        aL = [Q.answer for Q in self.questionL]
        hL = [Q.hint for Q in self.questionL]
        bhL = [Q.big_hint for Q in self.questionL]
        sL = [Q.story for Q in self.questionL]
        iL = [Q.image for Q in self.questionL]
        
        D = {'title':self.title,
             'list_of_prompts':pL, 'list_of_answers':aL, 'list_of_hints':hL, 
             'list_of_big_hints':bhL, 'list_of_stories':sL, 'list_of_images':iL}
                 
        return json.dumps(D, indent=4)

    def create_zip_file(self, file_prefix=''): # if blank, use self.title as file_prefix
        
        if not file_prefix:
            file_prefix = self.title
        fname = file_prefix + '.flash.zip'
        
        zf = zipfile.ZipFile(fname, mode='w', compression=zipfile.ZIP_DEFLATED)
        
        try:
            print( 'adding flashcard_info.json')
            zf.writestr('flashcard_info.json', self.get_json_str())
            
            for Q in self.questionL:
                if Q.image:
                    if os.path.isfile(Q.image):
                        zf.write( Q.image )
            
            print( 'SUCCESS in creating zip file.')
        finally:
            print( 'closing')
            zf.close()

        print()
        print( 'Zip file (%s) contains:'%fname)
        zf = zipfile.ZipFile(fname)
        for info in zf.infolist():
            print( info.filename)
        
        


if __name__ == "__main__":
    
    
    QL = Question_Collection( title='Some Title')
    QL.add_question( prompt="First Question", answer="First Answer",  
        hint="Little Hint", big_hint="Big Hint" ,  
        story="The Little Hint leads to the Big Hint", image='' )
        
    QL.add_question( prompt="", answer="",  
        hint="", big_hint="" ,  
        story="", image='' )
        
    QL.summ_print()
    
    #print( QL.get_json_str())
    
    #QL.create_zip_file()
    