const net = require('net');
const fs = require('fs');
const socketServer = net.createServer();

socketServer.listen(8899, function () {
    console.log('开始监听:' + JSON.stringify(socketServer.address()));
}).on('error', function (e) {
    throw e;
});
socketServer.maxConnections = 2;
let clients = {};
socketServer.on('connection', (socket) => {
    socket.write('你好');
    socketServer.getConnections((err, count) => {
        console.log('当前连接数状态：' + count + '/' + socketServer.maxConnections);
    });
    // console.log('socket端口对象信息：' + JSON.stringify(socketServer.address()));

    socket.setEncoding('utf8');
    socket.setTimeout(500000);
    socket.on('data', (data) => {
        if (!socket.action) {
            try {
                let obj = JSON.parse(data);
                if (!obj.tocken || obj.tocken !== 'iceyue') {
                    console.log('no tocken');
                    socket.destroy();
                } else {
                    clients[obj.id] = socket;
                    socket.id = obj.id;
                    socket.write(getTime() + ': set ' + obj.id);
                    socket.action = obj.action || 'reset';
                }
            } catch (e) {
                console.log('unrecognized client');
                socket.destroy();
            }
        }
        else {
            try {
                switch (socket.action) {
                    case 'reset':
                        let {action} = JSON.parse(data);
                        socket.action = action || 'reset';
                        socket.write('set action: ' + socket.action);
                        if (action === 'close') {
                            socket.destroy()
                        }
                        break;
                    case 'msg':
                        let obj = JSON.parse(data);
                        if (obj.exit) {
                            socket.action = 'reset';
                            socket.write('msg action close');
                            break
                        }
                        if (!obj.target) {
                            console.log('msg: ' + obj.msg);
                            socket.write('receive: ' + obj.msg);
                        }
                        else if (clients[obj.target]) {
                            clients[obj.target].write(obj.msg)
                        } else {
                            socket.write('no target: ' + obj.target);
                            console.log('no target: ' + obj.target);
                        }
                        break;
                    case 'file':
                        if (!socket.file_info) {
                            socket.file_info = JSON.parse(data).fileInfo;
                            socket.hasSend = 0;
                            socket.hasWrite = 0;
                            socket.buf = '';
                            socket.fd = fs.openSync(socket.file_info.fileName, 'w+');
                            socket.write('set file info');
                        } else {
                            socket.buf += data;
                            socket.hasSend = socket.hasSend + data.length;
                            while (socket.buf.length >= 2048) {
                                let pack = socket.buf.slice(0, 2048);
                                socket.buf = socket.buf.slice(2048);
                                pack = Buffer.from(pack, 'hex');
                                fs.appendFileSync(socket.fd, pack);
                            }
                            // console.log(socket.hasSend,
                            //     parseInt(socket.hasSend / 2 / socket.file_info.fileSize * 100) + '%');
                            if (socket.hasSend >= socket.file_info.fileSize * 2) {
                                let buf = Buffer.from(socket.buf, 'hex');
                                fs.appendFileSync(socket.fd, buf);
                                fs.closeSync(socket.fd);
                                console.log('file transfer completed');
                                socket.write('file transfer completed');
                                socket.file_info = null;
                                socket.action = 'reset';
                            }
                        }

                }

            } catch (e) {
                console.error(e);
                if (socket.fd)
                    fs.closeSync(socket.fd);
            }
        }


    })
        .on('timeout', () => {
            console.log('客户端连接已超时！');
            socket.destroy();
        })
        .on('end', () => {
            if (clients[socket.id] === socket) {
                delete clients[socket.id];
            }
            console.log(socket.id + ' 连接已关闭');
        })
        .on('error', (error) => {
            console.log(error);
        });
});
socketServer.on('close', function () {
    console.log('服务器关闭');
});
module.exports = clients;

function getTime() {
    let time = new Date();
    let date = time.getFullYear() + '-' + (time.getMonth() + 1) + '-' + time.getDate() +
        ' ' + time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds();
    return date;
}