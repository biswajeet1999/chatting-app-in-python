import socket
import threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('172.138.138.138',1234))
username = input("Enter username: ")
s.send(username.encode())

msg = s.recv(1024)
print(msg.decode())

active = True

def recvMsg():
  global active 
  while active:
    try:  
        recvmsg = s.recv(1024)
        print(recvmsg.decode())
    except:
      print('Server down')
      active =False

threading.Thread(target=recvMsg).start()


while active:
    sendmsg = input()
    s.send(sendmsg.encode())
    if(sendmsg == 'logout'):
        active = False
        

s.close()
