'''
Created on 2011. 7. 24.

@author: rucifer
'''

class methodGetGetParam:
    dic = dict()

    def __init__(self,path):
        
        try:
            params=path.split('?')[1].split('&')
            
            for param in params:
                item = param.split('=')
                self.dic[item[0]]=item[1]
            
            print(self.dic)
        
        except IndexError:
            #print("parameter is none")
            pass
        
        self.getParam()
        pass
    
    def getParam(self):
        return self.dic

if __name__ == '__main__':
    p=methodGetGetParam("urlTest.pyl1?method=1&to=1");
    print(p.getParam())