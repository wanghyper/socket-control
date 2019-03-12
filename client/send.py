import os
import json
import binascii


def sendTocken(s):
    # 连接验证
    print(s.recv(1024).decode('utf-8'))
    msg = {'id': "client2", 'tocken': 'iceyue'}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def sendMsg(s, words):
    # 发送消息
    msg = {'id': "client2", 'action': 'msg'}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    msg = {'msg': words, 'exit': False}
    s.sendall(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
    msg = {'target': "client1", 'msg': 'reset', 'exit': True}
    s.sendall(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def sendMsgTo(s, words, client="client1"):
    # 发送消息
    msg = {'id': "client2", 'action': 'msg'}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    msg = {'target': client, 'msg': words, 'exit': False}
    s.sendall(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

def reset(s):
    msg = {'target': "client1", 'msg': 'reset', 'exit': True}
    s.sendall(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def sendInputMsg(s):
    # 发送消息
    msg = {'id': "client2", 'action': 'msg'}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    msg = {'target': "client1", 'msg': '', 'exit': False}
    while not msg['exit']:
        msg['msg'] = input('请输入:')
        if msg['msg'] == 'exit':
            msg['exit'] = True
        s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


def sendFile(s, path, fileName):
    msg = {'id': "client2", 'action': 'file'}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    file_info = os.stat(path)
    msg = {'id': "client2", 'fileInfo': {'fileSize': file_info.st_size, 'fileName': fileName}}
    s.send(json.dumps(msg).encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))

    print('send file size:', file_info.st_size * 2)
    fo = open(path, 'rb')
    send_size = 0
    while True:
        file_data = fo.read(1024)
        print(send_size, int(send_size/file_info.st_size*100),'%')
        if not file_data:
            break
        s.sendall(binascii.b2a_hex(file_data))
        send_size+=len(file_data)
    fo.close()
    print(s.recv(1024).decode('utf-8'))
