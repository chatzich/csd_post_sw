# -*- coding: utf-8 -*- 
import formFile
class index:
	result=""
	sessionDic=dict()
	def __init__(self,param,pyFile,session,headerInfo,lattedb):
		self.generate(param,pyFile,session,headerInfo,lattedb)

	def generate(self,param,pyFile,session,headerInfo,lattedb):

		self.result+=str("""<!DOCTYPE html>
		 """)
		self.result+=str("""<html>
			 """)
		self.result+=str("""<head>
				 """)
		self.result+=str("""<meta charset="utf-8">
				 """)
		self.result+=str("""<title>This message printed by filter """)
		self.result+=str("""</title>	
			 """)
		self.result+=str("""</head>
			
			 """)
		self.result+=str("""<body>
		
		 """)
		h = "Hello"
		p = "Pylatte"
		result = h + " " + p
		
		self.result+=str("""
		
				 """)
		self.result+=str("""<h1> """)
		self.result+=str(result)
		self.result+=str("""</h1>	
				 """)
		self.result+=str("""<h2>Founder """)
		self.result+=str("""</h2>
				 """)
		self.result+=str("""<ul>
		 """)
		founder = ['Sangkeun Park', 'Hwanseong Lee', 'Heegeun Park']
		for person in founder:
		
			self.result+=str("""
					 """)
			self.result+=str("""<li> """)
			self.result+=str(person)
			self.result+=str("""</li>
		 """)
			pass
		
		self.result+=str("""
				 """)
		self.result+=str("""</ul>
		
		 """)
		import datetime
		time=datetime.datetime.now()
		
		self.result+=str("""
		
				 """)
		self.result+=str("""<p>You Accessed at :  """)
		self.result+=str(time)
		self.result+=str("""</p>
				 """)
		self.result+=str("""<p>Contact to @pylatte(Twitter) or http://www.pylatte.org/ """)
		self.result+=str("""<p>
				
				 """)
		self.result+=str("""<form name="form" method="post" action="http://localhost:8000/">
					 """)
		self.result+=str("""</br>
					 """)
		self.result+=str("""<p>Check POST & GET parameter """)
		self.result+=str("""</p>
					 """)
		self.result+=str("""<p>
					name	:  """)
		self.result+=str("""<input type="text" name="name">
					 """)
		self.result+=str("""<input type="submit" value="CLICK">
					 """)
		self.result+=str("""</p>
				 """)
		self.result+=str("""</form>
		 """)
		if param=={}:
			pass	
		else:
		
			self.result+=str("""
			 """)
			self.result+=str("""<p> """)
			self.result+=str("Parameter is : "+param['name'])
			self.result+=str("""</p>
		 """)
			pass
		
		self.result+=str("""
			 """)
		self.result+=str("""</body>
		 """)
		self.result+=str("""</html>
		
		
		 """)
		self.sessionDic=session
		pass
	def getHtml(self):
		return self.result
		pass
	def getSession(self):
		return self.sessionDic
		pass
