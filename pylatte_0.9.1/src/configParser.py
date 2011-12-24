from xml.dom.minidom import parse

class pyLatteConfigPaser():
    
    mappingExcute=dict();
    mappingUrl=dict();
    urlMap=dict();
    
    databaseInfo=tuple();
    
    filterPyl=dict();
    filterUrl=dict();
    filterMap=dict();
    
    def __init__(self):
        self.doc=parse("pylatte_config.xml")
        self.parseUrlMapingExcute()#xml에서 실행될 위치를 가져온다.
        self.parseUrlMappingUrl()#xml에서 요청하는 url를 가져온다.
        
        self.makeUrlMap()#위의 두함수에서 가져온 값을 조합하여 하나의 dictionary로 만든다.
        print(self.urlMap)
        
        self.parseFilterPyl()
        #print(self.filterPyl);
        self.parseFilterUrl()
        #print(self.filterUrl);
        self.makeFilterMap()#위의 두함수에서 가져온 값을 조합하여 하나의 dictionary로 만든다.
        print(self.filterMap)
        
        pass
    
    
    
    def parseUrlMapingExcute(self):
        mappingList=self.doc.getElementsByTagName("pylatte");
        for item in mappingList:
            for item1 in item.childNodes:
                if(item1.nodeName=="pylatte-name"):
                    name=item1.firstChild.nodeValue
                if(item1.nodeName=="pylatte-pyl"):
                    pyName=item1.firstChild.nodeValue
            self.mappingExcute[name]=pyName
        pass
    
    def parseUrlMappingUrl(self):
        mappingList=self.doc.getElementsByTagName("pylatte-mapping");
        for item in mappingList:
            for item1 in item.childNodes:
                if(item1.nodeName=="pylatte-name"):
                    name=item1.firstChild.nodeValue
                if(item1.nodeName=="url-mapping"):
                    urlName=item1.firstChild.nodeValue
            self.mappingUrl[name]=urlName
        pass
    
    def makeUrlMap(self):
        for item in self.mappingExcute.keys():
            self.urlMap[self.mappingUrl[item]]=self.mappingExcute[item]
        
        pass
    
    def parseFilterPyl(self):
        mappingList=self.doc.getElementsByTagName("filter");
        for item in mappingList:
            for item1 in item.childNodes:
                if(item1.nodeName=="filter-name"):
                    name=item1.firstChild.nodeValue
                if(item1.nodeName=="filter-pyl"):
                    pyName=item1.firstChild.nodeValue
            self.filterPyl[name]=pyName
        pass
    
    def parseFilterUrl(self):
        mappingList=self.doc.getElementsByTagName("filter-mapping");
        for item in mappingList:
            filterUrlList=[];
            for item1 in item.childNodes:
                if(item1.nodeName=="filter-name"):
                    name=item1.firstChild.nodeValue
                if(item1.nodeName=="filter-url"):
                    filterUrlList.append(item1.firstChild.nodeValue)
            self.filterUrl[name]=filterUrlList
        pass
    
    def makeFilterMap(self):
        for item in self.filterUrl.keys():
            self.filterMap[self.filterPyl[item]]=self.filterUrl[item]
        
        pass

    
    def getUrlMap(self):
        return self.urlMap
    def getDataBaseInfo(self):
        return self.databaseInfo
    def getFilterMap(self):
        return self.filterMap
    pass


if __name__ == '__main__':
    #f = open("pylatte_config.xml","r",encoding="utf-8")
    
    p = pyLatteConfigPaser();
    #p.Parse(f.read())
    pass
    