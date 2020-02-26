from HTMLTags import *


class Study_Html_output( object ):
    
    def __init__(self, title='Study List', leftL=None, rightL=None, single_column=False ):
        
        self.head = HEAD()
        self.head <= STYLE( STYLE_Str )
        self.head <= SCRIPT( BTN_SCRIPT_Str )        
        
        self.body = BODY()
        
        self.body <= '''<div  Class="Header">'''
        
        self.body <=  BUTTON("Show All Answers", Class="topbtns", onclick="showAllAnswers( %i );"%len(leftL))
        self.body <= BUTTON("Hide All Answers", Class="topbtns", onclick="hideAllAnswers( %i );"%len(leftL))
        #self.body <= BUTTON("Click Prompt to Toggle Answer", Class="topbtns", style="color:b7410e; font-weight:bold;")
        self.body <= '''</div><br>\n<div  Class="Content">'''
        
        self.add_table( title=title, leftL=leftL, rightL=rightL, single_column=single_column )
        self.body <= '''</div>'''
        
        #table = TABLE( width="100%")
        
        #table <= TR( TD(CENTER(H3(title)), Class="oompf", colspan="2")   )
        
        #for left,right in zip(leftL, rightL):
        #    table <= TR( TD(SPAN(left, Class="oompf"), align="right", Class="col_one") + \
        #             TD(SPAN(right, Class="oompf"), align="left", Class="col_two") )
        #self.body <= table
        
    def add_table(self, title='Study List', leftL=None, rightL=None, single_column=False ):
        
        table = TABLE( width="100%")
        
        if single_column:
            table <= TR( TD(CENTER(H3(title)), Class="oompf")   )
        else:
            table <= TR( TD(CENTER(H3(title)), Class="oompf", colspan="2")   )
        
        i_cell = 1 # number of each cell in table
        for left,right in zip(leftL, rightL):
            if single_column:
                                
                table <= TR( TD( BUTTON(left, Class="prompt", onclick="toggleAnswer('answer%i');"%(i_cell, )) + #'<br>' + 
                                 SPAN(right, Class="oompf", id="answer%i"%i_cell, style="display: none;"), 
                                 align="left", Class="col_one", tabindex="%i"%i_cell),
                                 onkeypress="toggleAnswer('answer%i');"%i_cell, Class="row" )
                #table <= TR( TD( SPAN(left, Class="prompt", onclick="toggleAnswer('answer%i');"%(i_cell, )) + #'<br>' + 
                #                 SPAN(right, Class="oompf", id="answer%i"%i_cell, style="display: none;"), 
                #                 align="left", Class="col_one", tabindex="%i"%i_cell),
                #                 onkeypress="toggleAnswer('answer%i');"%i_cell, Class="row" )
                                
            else:
                table <= TR( TD( SPAN(left, Class="prompt"), align="right", valign="top", Class="col_one", onclick="toggleAnswer('answer%i');"%i_cell) + \
                             TD( SPAN(right, Class="oompf", id="answer%i"%i_cell, style="display: none;"), 
                                 align="left", Class="col_two"), tabindex="%i"%i_cell,
                                 onkeypress="toggleAnswer('answer%i');"%i_cell, Class="row" )
            i_cell += 1
        
        self.body <= table
        
    
    def __str__( self ):
        
        return str( HTML(self.head + self.body) )

BTN_SCRIPT_Str = """
function toggleAnswer(id) {
    if (document.getElementById(id).style.display == 'none'){
        document.getElementById(id).style.display = 'block';
    } else {
        document.getElementById(id).style.display = 'none';
    }
}

function hideAllAnswers( N ){

    for(i = 1; i <= N; i++)
    {
        document.getElementById( "answer" + i ).style.display = 'none';
    }
}

function showAllAnswers( N ){

    for(i = 1; i <= N; i++)
    {
        document.getElementById( "answer" + i ).style.display = 'block';
    }
}
"""


STYLE_Str = """
table {
    border-collapse: collapse;
}

table, th, td {
    border: 1px solid black;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 15px;
    padding-right: 15px;
}

tr:nth-child(even) {background-color: #E3E8EA}
tr:nth-child(odd) {background-color: #F6F7F8}

tr:hover, td:hover { background-color: #ffffff;}


.prompt {
    font-size: 18px;
    color: #123945;
    background-color: #ECF0F1;
    font-weight: bold;
    line-height: 18px;
    margin-bottom: 8px;
}

.topbtns {
    font-size: 18px;
    color: #10323E;
    background-color: #E8ECED;
    font-weight: bold;
    line-height: 18px;
    margin-bottom: 8px;
}

.oompf {
    font-size: 18px;
    color: #10323E;
    font-weight: bold;
    line-height: 18px;
    margin-bottom: 8px;
}

@media print
 {
    table {width: 100%;}
    td.col_one { width: 50%; }
    td.col_two { width: 50%; }
    .col_one { width: 50%; }
    .col_two { width: 50%; }
    
    img { max-width:3.0in !important;} 
    tr    { page-break-inside:avoid; page-break-after:auto }    
    
 }

.Header
{
  position: fixed;
  background-color: #ffffff;
  top: 0;
  left: 0;
  width: 100%;
  height: 30px;}
  
.Content
{
    top: 30px;
    background-color: #ffffff;
    overflow-y:auto;
    padding-top: 30px;
}


"""


if __name__ == '__main__':
    from question_obj import Question_Collection    
    
    QL = Question_Collection( title='Some Title')
    QL.add_question( prompt="First Question", answer="First Answer",  
        hint="Little Hint", big_hint="Big Hint" ,  
        story="The Little Hint leads to the Big Hint", image='' )
    QL.add_question( prompt="Second Question", answer="Second Answer",  
        hint="Second Little Hint", big_hint="Second Big Hint" ,  
        story="The Second Little Hint leads to the Second Big Hint", image='' )
        
    QL.add_question( prompt="", answer="",  
        hint="", big_hint="" ,  
        story="", image='' )
    
    EO = Study_Html_output( title=QL.title, 
                            leftL=QL.get_item_list(name='prompt'), 
                            rightL=QL.get_item_list(name='hint'), single_column=False )
    print( EO )
    