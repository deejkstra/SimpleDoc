var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
    res.sendFile('/home/mkrupin/dev/nodejs/html/doc.html');
});

io.on('connection', function(socket) {


    sample_py = function(op, msg) {

        console.log('sample');
        var spawn = require('child_process').spawn;
        var spawn_data = ['/home/mkrupin/dev/nodejs/sample.py', op, msg];
        var py = spawn('python3', spawn_data);

        var child_status = '1';

        py.stdout.on('data', function(data) {
            console.log('data');
            var str = data.toString('utf8');
            console.log(str);
            io.emit('python', str);
        });

        py.stdout.on('end', function(data) {
            console.log('end');
        });

        py.stderr.on('data', function(data) {
            console.log('Failed to start child process: ' + data.toString());
            child_status = '0';
        });

        return child_status;
    }

    socket.on('create', function(msg) {

    });

    socket.on('update', function(msg) {
        console.log('update');

        sample_py(msg);

        io.emit('update', msg);
    });

    socket.on('save', function(msg) {
        io.emit('save', '1');
        //io.emit('python', py_sample('save'));
        //console.log(msg);
    });

    socket.on('disconnect', function() {
        // disconnect
        console.log("disconnected");
        //py.stdin.end();
    });
});

http.listen(8080, function() {
    console.log('listening on *:8080');
});
