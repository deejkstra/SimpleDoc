var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
    //res.send('<h1>Hello, world!</h1>');
    res.sendFile('/home/mkrupin/dev/nodejs/html/index.html');
});

io.on('connection', function(socket) {

    socket.on('chat message', function(msg) {
        io.emit('chat message', msg);
    });

/*
    console.log('a user connected');
    socket.on('disconnect', function() {
        console.log('user disconnected');
    });
*/
});

http.listen(8080, function() {
    console.log('listening on *:8080');
});
