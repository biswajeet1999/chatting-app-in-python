import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((socket.gethostbyname(socket.gethostname()),1234))
server.listen()
print('Server strated...')

clients = {}

def handleclient(clnt,uname):
    active = True
    while active:
      try:
        msg = clnt.recv(1024)
        msg = msg.decode()
      
        if(msg == 'help'):
            clnt.send('+------------------------------------------------------+\n|msg >> name:           Message send to name           |\n|name >> msg:           Message send by name           |\n|msg >> send all:       Message send to all clients    |\n|*active clients:       Display all active clients     |\n|logout:                Exit chatting program          |\n+------------------------------------------------------+\n'.encode())
       
        elif(msg == '*active clients'):
            for u in clients.keys():
                clnt.send(u.encode())

        elif(' >> send all' in msg):
            if(len(clients) > 1):
                msg = msg.replace(' >> send all','')
                msg = uname+' >> '+ msg
                for u,c in clients.items():
                    if(u != uname):
                        c.send(msg.encode())
            else:
                clnt.send("No active user except you")
        elif(msg == 'logout'):
            active = False
            clients.pop(uname)
            print(uname+' logout')
            clnt.close()
        
        else: 
            flag = 0
            for u,c in clients.items():
                if(' >> '+u in msg):
                    msg = msg.replace(' >> '+u,'')
                    c.send((uname+' >> '+msg).encode())
                    flag = 1
                    break
            if(flag == 0):
                clnt.send('Invallid username'.encode())
      except:
          print(uname+' logout')
          clients.pop(uname)
          clnt.close()
          active = False
        
while True:
    client,adr = server.accept()
    username = client.recv(1024)  #recv user name
    username = username.decode()
    print(username+" login")
    if(username not in clients.keys()):
        clients[username] = client
    client.send('Welcome to chatting program\npress help to know more'.encode())    
    threading.Thread(target = handleclient,args = (client,username)).start()
