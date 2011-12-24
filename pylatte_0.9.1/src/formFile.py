'''
Created on 2011. 10. 7.

@author: pylatte
'''

import shutil

class formFile:
    
    error=""
    formFile=dict()
    def __init__(self,formFile):
        self.formFile=formFile
        pass
        
    def moveUploadFile(self,name,dir,fileName):
        """
        name는 <input> 태그의 name
        dir는 이동시킬 폴더의 이름(미리 존재해야됨) 그렇지 않음 오류
        fileName은 저장시킬 파일이름. 구별할수 있어야됨.
        
        성공시 return 0
        실패시 return -1
        
        오류 내용은 getError으로 받으면 됨.
        """
        print(name)
        print(self.formFile[name])
        print("/tmp/pylatte_tmp/"+self.formFile[name]["tmpFileName"])
        shutil.move("/tmp/pylatte_tmp/"+self.formFile[name]["tmpFileName"],dir+"/"+fileName)
        
        
        self.error="success"
        return 0
        pass
    
    def getError(self):
        return self.error
        pass
    
    pass

