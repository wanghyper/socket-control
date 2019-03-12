import socket
import client.send as send

class mySocket:
    server = None
    def __init__(self,  host = '127.0.0.1',  port = 8899):
        self.server = socket.socket()  # 创建 socket 对象
        self.server.connect((host, port))
        self.setTocken()
    def setTocken(self):
        send.sendTocken(self.server)
    def sendMsg(self, msg):
        send.sendMsg(self.server, msg)
    def sendInputMsg(self):
        send.sendInputMsg(self.server)
    def sendFile(self, path, filename):
        send.sendFile(self.server, path, filename)
    def sendMsgTo(self, words):
        send.sendMsgTo(self.server, words)