from flask import Flask
from client import client

host = '148.70.10.149'
# host = '127.0.0.1'
port = 8899
socket = client.mySocket(host, port)

socket.sendMsg('有人吗')
# socket.sendFile('fuyao.mp4', '一爱难求.mp4')
# socket.sendFile('lijianing.jpg', 'lijianing.jpg')
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/open')
def open_light():
    socket.sendMsgTo('open')
    return 'Hello World!'
@app.route('/close')
def close_light():
    socket.sendMsgTo('close')
    return 'Hello World!'

sign = 1
@app.route('/toggle')
def toggle():
    global sign
    if sign == 1:
        close_light()
        sign=0
    else:
        open_light()
        sign=1
    return str(sign)

if __name__ == '__main__':
    app.run()
