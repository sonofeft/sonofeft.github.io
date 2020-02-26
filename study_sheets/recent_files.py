#!/usr/bin/env python
# -*- coding: ascii -*-

import os
import sys
from config_file import ConfigInterface

USER_HOME_DIR = os.path.dirname( os.path.expanduser('~/') )

class RecentFiles( object ):
    MaxRecentFiles = 99
    
    def __init__(self, config_file_prefix='FlashList'):
        
        self.file_name = os.path.join( USER_HOME_DIR, '%s.cfg'%config_file_prefix )
        self.config_obj = ConfigInterface( config_filename=self.file_name, 
                                            sectionL=['RecentFiles'] )
        
        self.recent_fileL = []
        
        D = self.config_obj.get_dictionary()['RecentFiles']
        
        self.last_dir = D.get('last_dir',USER_HOME_DIR)
        
        for i in range(RecentFiles.MaxRecentFiles):
            fname = D.get( 'file_%i'%(i+1,), '')
            if fname:
                self.recent_fileL.append( fname )
    
    def get_full_path_list(self):
        
        return self.recent_fileL[:]  # return a copy
    
    def change_file_path(self, fname_old, fname_new):
        
        fname_old = fname_old.replace('/','\\')
        fname_new = fname_new.replace('/','\\')
                
        for i in range( RecentFiles.MaxRecentFiles ):
            if i < len( self.recent_fileL ):
                if self.config_obj['RecentFiles','file_%i'%(i+1,)] == fname_old:
                    self.config_obj['RecentFiles','file_%i'%(i+1,)] = fname_new
                    self.recent_fileL[i] = fname_new
                    
                    print( 'changed file_%i from:'%(i+1,), fname_old )
                    print( '  to:',fname_new )
                
        self.config_obj.save_file()
    
    def update(self, fname):
        
        fname = fname.replace('/','\\')
        
        head,tail = os.path.split( fname )
        
        self.config_obj['RecentFiles','last_dir'] = head
        
        while fname in self.recent_fileL:
            try:
                self.recent_fileL.remove(fname)
            except ValueError:
                break
        
        self.recent_fileL.insert(0, fname)
                
        for i in range( RecentFiles.MaxRecentFiles ):
            if i < len( self.recent_fileL ):
                self.config_obj['RecentFiles','file_%i'%(i+1,)] = self.recent_fileL[i]
            else:
                self.config_obj['RecentFiles','file_%i'%(i+1,)] = ''
                
        self.config_obj.save_file()
        
    def save(self):
        self.config_obj.save_file()
        
        
    def set_dir(self, filePath):
        self.config_obj['RecentFiles','last_dir'] = filePath
        self.config_obj.save_file()
    
    def get_dir(self):
        if self.config_obj.has_option('RecentFiles', 'last_dir'):
            filePath = self.config_obj['RecentFiles', 'last_dir']
        else:
            filePath = USER_HOME_DIR # os.getcwd()
        return filePath
    
    def chdir(self):
        filePath = self.get_dir()
        print( "Changing Directory To:",filePath )
        try:
            os.chdir( filePath )
        except:
            print( "ERROR: Path NOT Found:", filePath )
 
if __name__ == "__main__":
     
    RF = RecentFiles()
    
    #print( RF.config_obj.get_dictionary() )
    #print()
    print( RF.recent_fileL )
     