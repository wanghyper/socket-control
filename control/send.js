const net = require('net');
const fs = require('fs');

const client = net.createConnection({port: 8899}, () => {
    // 'connect' listener
    console.log('connected to server!');
    let msg = {'id': "client2", 'tocken': 'iceyue', 'action': 'file'};
    client.write(JSON.stringify(msg));

});
client.on('data', (data) => {
    console.log(data.toString());
    client.end();
});
client.on('end', () => {
    console.log('disconnected from server');
});
module.exports = {
    sendMsg(words){
        let msg = {'id': "client2", 'tocken': 'iceyue', 'action': 'file'};
    client.write(JSON.stringify(msg));
    }
}