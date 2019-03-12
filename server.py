import socket  # 导入 socket 模块
import time
import threading

s = socket.socket()  # 创建 socket 对象
host = '0.0.0.0'
port = 8899  # 设置端口
s.bind((host, port))  # 绑定端口
print('server start')
s.listen(2)

client1 = None
client2 = None


def recvData(client):
    while True:
        global client1
        global client2
        msg = client.recv(1024)
        msg = msg.decode('utf-8')
        print(msg)
        if msg == 'client1':
            client1 = client
            print('set  client1')
        elif msg == 'client2':
            client2 = client
            print('set  client2')
        else:
            client1.send(msg.encode('utf-8'))
    # c.close()


def sendData(client):
    client.send("收到".encode('utf-8'))


while True:
    c, addr = s.accept()
    print("连接地址：", addr)
    t1 = threading.Thread(target=recvData, args=(c,))
    t1.start()
