# -*- coding: utf-8 -*-

class session:
    
    ''' Pylatte 세션과 관련된 메소드 모음 @박희근  '''
    
    # 주어진 세션키가 유효한지 확인 @박희근
    # 기본으로 15 분 (=900초) 이상 지난 세션 파일은 False 가 반환되며 그 파일은 삭제된다.
    def checkAvailableSession(self, key, limit=900):
        
        import os.path
        import time
        
        if os.path.isfile('session/' + key) != True:
            return False
        
        if int(os.path.getmtime('session/' + key)) + limit < int(time.time()):
            os.remove('session/' + key)
            return False
        else:
            return True 
    
    
    # 서버에 세션 파일을 만드는 함수 @박희근
    # 클라이언트에 쿠키를 심으려면 HTTP 헤더에 Set-Cookie: PYLSESSION=pylsession_rjdidkoawe3il2q39njklszdfjoi ... 형태로 지정해주면 됨.
    def genSessionKey(self):
        
        import hashlib
        import time
        
        timestamp = int(time.time())
        timestr = str(timestamp)
        
        return 'pylsession_' + hashlib.md5(b'pylatte' + str.encode(timestr) ).hexdigest()
    
    # 생성한 키 스트링으로 파일 저장하기 @박희근
    # 선택적으로 파일 내용에 무언가를 써 넣을 수도 있다. 
    def setSessionData(self, key, content=None):
        f = open('session/' + key, mode='w', encoding='utf-8')
        if content != None:
            f.write(content)
        f.close()
        pass
    
    #해당 세션키로 세션의 데이터를 가져온다. @이환승    
    def getSessionData(self,key):
        
        f = open('session/' + key, mode='r', encoding='utf-8')
        content=f.read();
        print (content)
        
        return content    
    
    # dictionary 를 세션데이터형태로 변형 @이환승    
    def dictToSessionData(self,dicData):
        dataStr = "";
        for item in dicData.keys():
            dataStr+=item+":"+dicData[item]+"/"
        
        return dataStr
        pass
    
    # 세션데이터형태를 dictionary 로 변형 @이환승
    def sessionDataTodict(self,data):
        splitedData=data.split('/')
        resultDic = dict();
        
        try:
            for item in splitedData:
                resultDic[item.split(':')[0]]=item.split(':')[1]
        
        except IndexError:#indexError를 받으면 그냥 넘기도록 설정
            pass
            
        return resultDic
        pass
            
if __name__ == '__main__':
    str1 = "key:value/key1:value1/key2:value2/"
    result = session.sessionDataTodict(session,str1)
    print (result)
    
    resultStr = session.dictToSessionData(session, result)
    print (resultStr)
    
    