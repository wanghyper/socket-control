const http = require('http')

http.createServer(function (request, response) {
    console.log(request.url)
    response.write('收到')

    response.end('继续')
}).listen(8080)