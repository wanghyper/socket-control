const net = require('net');
const fs = require('fs');

const client = net.createConnection({port: 8899}, () => {
    // 'connect' listener
    console.log('connected to server!');
    let msg = {'id': "client2", 'tocken': 'iceyue', 'action': 'file'};
    client.write(JSON.stringify(msg));
    sendFile('./lijianing.jpg', 'lijianing.jpg')

});
client.on('data', (data) => {
    console.log(data.toString());
    client.end();
});
client.on('end', () => {
    console.log('disconnected from server');
});

function sendFile(path, name) {
    let fileInfo = fs.statSync(path);
    let fileSize = fileInfo.size;
    client.write(JSON.stringify({'id': "client2", 'fileInfo': {'fileSize': fileSize, fileName: name}}));
    let sendSize = 0;
    let packSize = 1024;
    let fd = fs.openSync(path, 'r');
    let buf = new Buffer.alloc(packSize);
    while (sendSize < fileSize) {
        //readSync参数:文件ID,buffer对象,写入buffer起始位置,写入buffer结束位置,读取文件的起始位置
        fs.readSync(fd, buf, 0, buf.length, sendSize);
        let data = buf.toString('hex');//以十六进制传输
        client.write(data);
        sendSize += packSize;
    }
}