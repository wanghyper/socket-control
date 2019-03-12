from client import client

host = '148.70.10.149'
# host = '127.0.0.1'
port = 8899
socket = client.mySocket(host, port)

socket.sendMsg('有人吗')
socket.sendInputMsg()
# socket.sendFile('fuyao.mp4', '一爱难求.mp4')
# socket.sendFile('lijianing.jpg', 'lijianing.jpg')