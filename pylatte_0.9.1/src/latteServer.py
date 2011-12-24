'''
Created on 2011. 7. 16.
dd
@author: rucifer
'''
import sys;
sys.path.append('./topy')    #Path to save uploaded files.
import os
import http.server
import methodGetGetParam     #To use GET parameter
import methodGetPostParam    #To use POST parameter
import requestHeaderInfo     #To use request Header information in pyl files.

import sessionUtil


class latteServer(http.server.CGIHTTPRequestHandler):
    
    excuteDic=tuple()
    urlMappingDic=tuple()
    databaseInfo=tuple()
    server_version="pylatte HttpServer 1.0v"
    
    isPyl=False
    
    pyFile=None;
    
    def __init__(self, request, client_address, server):

        #URL Mapping
        self.urlMap=server.urlMap

        #Database information
        self.databaseInfo=server.databaseInfo
        
        http.server.CGIHTTPRequestHandler.__init__(self, request, client_address, server)
            
        pass
    
    def do_GET(self):
        
        headerInfo=requestHeaderInfo.requestHeaderInfo(self)
        
        print(self.path)

        #get GET parameters value.
        param=methodGetGetParam.methodGetGetParam(self.path)
        
        self.pyFile=None; #no file uploaded
        
        url = self.path.split('?')[0]
        try:
            self.path=self.urlMap[url]
            moduleName=self.path.split('.')[0]
            print("moduleName : "+moduleName)
            urlTest_pyl=moduleName+'_pyl'
            
            #Checking a cookie value to know whether session exists or not.
            print("Cookie:"+headerInfo.getHeaderInfo()["Cookie"])
            
            sessionutil =sessionUtil.session
            #if there is no cookie value, make a new cookie value.
            if headerInfo.getHeaderInfo()["Cookie"] == "":
                sessionKey = sessionutil.genSessionKey(sessionutil)
            #If there is a cookie value, get the value from head information and put into sessionKey variable.
            else: 
                sessionKey = headerInfo.getHeaderInfo()["Cookie"].split('=')[1]
                
            print("session ID : "+sessionKey);
            
            try:
                sessionData = sessionutil.getSessionData(sessionutil, sessionKey)
            except IOError:
                sessionData =""
                
            sessionDic = sessionutil.sessionDataTodict(sessionutil,sessionData)
            
            #print(urlTest_pyl)
            pyl = __import__(urlTest_pyl)
            print(pyl)
            print("processing Dynamic Page")
            module=getattr(pyl, moduleName)(param.getParam(),self.pyFile,sessionDic,headerInfo.getHeaderInfo(),self.databaseInfo)
            #print("processing DynamicPage End")
            htmlcode = module.getHtml()    # completely generaged HTML
            #print(htmlcode)
            
            finalSessionDic=module.getSession()
            sessionData = sessionutil.dictToSessionData(sessionutil,finalSessionDic)
            sessionutil.setSessionData(sessionutil,sessionKey, sessionData)
            
            wf = open("temp.html","w")
            wf.write(htmlcode)
            wf.close()
            self.isPyl=True
            
        except KeyError:# If there is nothing to process dynamically, look for static thing
            self.isPyl=False
            sessionKey=None
            pass
        except TypeError:
            print('Error - Result of processing SQL is None. NoneType object is not subscriptable.')
            pass
        
        
        #if session value is same
        try:
            if sessionKey==headerInfo.getHeaderInfo()["Cookie"].split('=')[1]:
                f = self.send_head(None)#send sessionid to header
            else:
                f = self.send_head(sessionKey)
        except IndexError:
            f = self.send_head(sessionKey)
            
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        pass
       
    def do_POST(self):
       
        headerInfo=requestHeaderInfo.requestHeaderInfo(self)
        
        print(self.path)
        
        #print("Start of getting POST parameter")
        post_payload = self.rfile.read(int(headerInfo.getHeaderInfo()["Content-Length"]));
        print(post_payload)
        if post_payload.find(b'Content-Disposition: form-data')!=-1:
            print("multy-part upload");
            import postMultipartForm
            param=postMultipartForm.postMultipartForm(post_payload)
            self.pyFile=param.getFileInfo()
            
        else:
            param=methodGetPostParam.methodGetPostParam(str(post_payload))
            self.pyFile=None;
        #print("End of getting POST parameter")
        
        url = self.path
        try:
            self.path=self.urlMap[url]
            moduleName=self.path.split('.')[0]
            print("moduleName : "+moduleName)
            urlTest_pyl=moduleName+'_pyl'
            
            
            #print(urlTest_pyl)
            pyl = __import__(urlTest_pyl)#import py files which is generated from pyl files.
            
            #Checking a cookie value to know whether session exists or not.
            print("Cookie:"+headerInfo.getHeaderInfo()["Cookie"])
            
            sessionutil =sessionUtil.session
            #if there is no cookie value, make a new cookie value.
            if headerInfo.getHeaderInfo()["Cookie"] == "":
                sessionKey = sessionutil.genSessionKey(sessionutil)
            #If there is a cookie value, get the value from head information and put into sessionKey variable.
            else: 
                sessionKey = headerInfo.getHeaderInfo()["Cookie"].split('=')[1]
                
            print("session ID : "+sessionKey);
            
            try:
                sessionData = sessionutil.getSessionData(sessionutil, sessionKey)
            except IOError:
                sessionData =""
                
            sessionDic = sessionutil.sessionDataTodict(sessionutil,sessionData)
            
            print("processing Dynamic Page")
            module=getattr(pyl, moduleName)(param.getParam(),self.pyFile,sessionDic,headerInfo.getHeaderInfo(),self.databaseInfo)
            #print("processing Dynamic Page End")
            
            #세션유지시킬 값도 가져와야됨.
            
            htmlcode = module.getHtml()
            print(htmlcode)
            wf = open("temp.html","w")
            wf.write(htmlcode)
            wf.close()
            self.isPyl=True
            
        except IndexError:# If there is nothing to process dynamically, look for static thing
            
            self.isPyl=False
            pass
        except TypeError:
            print('Error - Result of processing SQL is None. NoneType object is not subscriptable.')
            pass
        
        #if session value is same
        try:
            if sessionKey==headerInfo.getHeaderInfo()["Cookie"].split('=')[1]:
                f = self.send_head(None)#send sessionid to header
            else:
                f = self.send_head(sessionKey)
        except IndexError:
            f = self.send_head(sessionKey)
            
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        pass
        
            
    def do_HEAD(self):
        http.server.CGIHTTPRequestHandler.do_HEAD(self)
        pass
    
    def send_head(self,sessionKey=None):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """
        
        if self.isPyl==True:
            path = "temp.html"
        else:
            path = self.translate_path(self.path)
            print(path)
        
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        if self.isPyl==True:
            self.send_header("Content-type", ctype + "; charset=utf-8")
        else:
            self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        if sessionKey!=None:#if sessionKey exist, the key are used
            self.send_header("Set-Cookie", "PYLATTESESSIONID="+sessionKey)
            
        self.end_headers()
        return f
