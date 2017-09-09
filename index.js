const express = require('express')
const http = require('http')
const PythonShell = require('python-shell')
const bodyParser = require('body-parser')
const path = require('path')
const app = express()
const port = 8000;

app.use(express.static(path.join(__dirname,'/public')));
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

var options = {
    pythonPath: '/usr/local/Cellar/python3/3.6.2/Frameworks/Python.framework/Versions/3.6/bin/python3.6',
    pythonOptions: ['-u']
};

var pyshell = new PythonShell('runWizard.py', options);

var latestXValue = 50;

var clicks = [];

// html render engine
app.set('view engine', 'ejs');


//screen one, is the game canvas
app.get('/', (request, response) => {
    response.sendFile(path.join(__dirname, '/views/calibration.html'))
})

app.post('/click', (request, response) => {
    clicks.push({xpos: JSON.parse(request.body.x), ypos: JSON.parse(request.body.y)});
    console.log(clicks);
})

app.post('/game', (request, response) => {
    response.sendFile(path.join(__dirname, '/views/test.html'))
    pyshell.on('message', function(message) {
        latestXValue = message;
    })
})

app.get('/game/data', (request, response) => {
    response.json({xcoord: latestXValue});
})

app.listen(port, (err) => {
    if (err) {
        return console.log('something bad happened', err)
    }

    console.log(`server is listening on ${port}`)
})
