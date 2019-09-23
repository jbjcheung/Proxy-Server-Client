from socket import *
import sys

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# Creates a server socket, binds it to a port and starts listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serv_addr = ('192.168.1.68',int(sys.argv[1]))
tcpSerSock.bind(serv_addr)

tcpSerSock.listen(1)



while 1:
	# Start receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
        message = tcpCliSock.recv(1024)
	print(message)
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")                      
		outputdata = f.readlines()                        
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		for i in range(0, len(outputdata)):
			tcpCliSock.send(outputdata[i])
		print(outputdata)
		print('Read from cache')   
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false": 
			# Create a socket on the proxyserver
			c = socket(AF_INET,SOCK_STREAM)
			hostn = filename.replace("www.","",1)         
			print(hostn)                                   
			try:
				# Connect to the socket to port 80
				c.connect((hostn, 80))
				fileobj = c.makefile('r', 0)               
				fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")  
				buffer = fileobj.readlines()
				tmpFile = open("./" + filename,"wb")  
				for i in range(0, len(buffer)):
					tmpFile.write(buffer[i])
					tcpCliSock.send(buffer[i])
			except:
				print("Illegal request")
				
		else:
			# HTTP response message for file not found
				response = http.request('GET', filename)
	# Close the client and the server sockets
	tcpCliSock.close()
	break
	
