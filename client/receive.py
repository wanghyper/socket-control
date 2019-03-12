import socket
import json

s = socket.socket()         # 创建 socket 对象
host = 'iceyue.top'
# host = '127.0.0.1'
port = 8899                # 设置端口号

s.connect((host, port))

msg = {'id': "client1", 'tocken': 'iceyue'}
s.send(json.dumps(msg).encode('utf-8'))
print(s.recv(1024).decode('utf-8'))


while True:
    msg = s.recv(1024)
    print(msg.decode('utf-8'))
