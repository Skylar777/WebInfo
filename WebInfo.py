#!/usr/bin/python

import sys
import socket
import ssl
exter=""
urlservice = sys.argv[1]
if(urlservice[0:7]!="http://"):
	if(urlservice.find("/")!=-1):
		exter=urlservice[(urlservice.find("/"))+1:]
		urlservice = urlservice[0:urlservice.find("/")]	
		#print(exter)
	httpservice = "http://"+urlservice
else:


	httpservice = sys.argv[1]
	urlservice = sys.argv[1][7:]


#print(sys.argv[1])
#print(httpservice)
#print(urlservice)

#webrequest = http.client.HTTPSConnection(sys.argv[1])
#webrequest.request('GET', '/3/')
print("website: "+ httpservice)
checker=0

#code find http2



createcontext = ssl.create_default_context()
createcontext.set_alpn_protocols(["h2"])
wrap = createcontext.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=urlservice)
wrap.connect((urlservice, 443))
if wrap.selected_alpn_protocol() == "h2":
	print("1. Supports http2: yes")
	checker=1
else:
	print("1. Supports http2: no")

cookiearray = []
cookiearray2 = []


socketget=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketget.connect((urlservice, 80))
socketget.sendall(("GET /"+exter+" HTTP/1.1\r\nHost: "+urlservice+"\r\nConnection: Keep-Alive\r\n\r\n").encode('utf-8'))
response = socketget.recv(5000)


returnedresponse=response.decode('utf-8')

checker=0



print("2. List of Cookies:")
if("302 Moved Temporarily"==returnedresponse[9:30] or returnedresponse[9:30]=="301 Moved Permanently"):
	#print("443")
	createcontext=ssl.create_default_context()
	socketget=createcontext.wrap_socket(socket.socket(socket.AF_INET), server_hostname=urlservice)
	socketget.connect((urlservice, 443))
	socketget.sendall(("GET /"+exter+" HTTP/1.1\r\nHOST: "+urlservice+"\r\nConnection: Keep-Alive\r\n\r\n").encode('utf-8'))
	response = socketget.recv(5000)
	returnedresponse=response.decode('utf-8')
	if(returnedresponse[9:25]=="401 Unauthorized"):
		checker=1



cookiearray=returnedresponse.split("\n")

for i in cookiearray:
	
	if i[0:10]=="Set-Cookie":
		
		basic1=""
		basic2=""
		basic3=""
		if(i.find(" ")!=-1):
			basic1 = i[i.find(" ")+1:]
			if(basic1.find("=")!=-1):
				basic1 = basic1[0:basic1.find("=")]
		

		if(i.find("Domain=")!=-1):
			basic2 = i[i.find("Domain=")+7:]
			if(basic2.find(";")!=-1):
				basic2 = basic2[0:basic2.find(";")]
		if(i.find("domain=")!=-1):
			basic2 = i[i.find("domain=")+7:]
			if(basic2.find(";")!=-1):
				basic2 = basic2[0:basic2.find(";")]
		

		if(i.find("expires=")!=-1):
			basic3 = i[i.find("expires=")+8:]
			if(basic3.find(";")!=-1):
				basic3 = basic3[0:basic3.find(";")]
		if(i.find("Expires=")!=-1):
			basic3 = i[i.find("Expires=")+8:]
			if(basic3.find(";")!=-1):
				basic3 = basic3[0:basic3.find(";")]

		if basic1!="" and basic2!="" and basic3!="":
			print("cookie name: "+basic1+", expires time: "+basic3+"; domain name: "+basic2)
		elif basic1!=""and basic3!="":
			print("cookie name: "+basic1+", expires time: "+basic3)
		elif basic1!=""and basic2!="":
			print("cookie name: "+basic1+", domain name: "+basic2)
		elif basic1!="":
			print("cookie name: "+basic1)

		


#coding time again?
if checker==1:
	print("3. Password-protected: yes")
else:
	print("3. Password-protected: no")



