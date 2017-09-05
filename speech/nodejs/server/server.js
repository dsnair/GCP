var express         = require('express');
var app             = express();                    // create our app w/ express
var morgan          = require('morgan');            // log requests to the console (express4)
var bodyParser      = require('body-parser');       // pull information from HTML POST (express4)
var path            = require('path');
var methodOverride  = require('method-override');   // simulate DELETE and PUT (express4)
var speech          = require('@google-cloud/speech')({
    projectId: 'billion-taxi-rides',
    keyFilename: './server/springml-speech-api-key.json'
});
var Promise         = require('bluebird');
var port            = process.env.PORT || 8080;

// -------------------------------------------------------------------------
// Configuration -----------------------------------------------------------
// -------------------------------------------------------------------------
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.use(bodyParser.json({
    type: 'application/vnd.api+json'
}));
app.use(methodOverride());
app.use('/js', express.static(path.join(__dirname, '../public/js')))

// -------------------------------------------------------------------------
// Application -------------------------------------------------------------
// -------------------------------------------------------------------------
app.get('/', function(req, res){
    res.sendFile(path.join(__dirname, '../public/', 'index.html'));
});

app.post('/posts', function(req, res){
    var aux = {
        gsUri: req.body.uri,
        fileType: {
            encoding: 'LINEAR16',
            sampleRate: 16000,
            verbose: true
        }
    }
    var transcribe = function(){
        return new Promise(function(resolve, reject){
            speech.startRecognition(aux.gsUri, aux.fileType, function(err, operation, res) {
                if (err) {
                    console.error(err);
                } else {
                    operation.on('error', function(err){
                        console.error(err);
                    }).on('complete', function(transcript){
                        console.log(transcript)
                        var returnAllTranscripts = [];
                        transcript.forEach(function(block){
                            returnAllTranscripts.push(block.transcript);
                        });
                        resolve(returnAllTranscripts);
                    });
                }
            });
        })
    }
    transcribe().then(function(data){
        res.end(JSON.stringify({transcriptArray: data, size: data.length}))
    });
});


app.listen(port, function() {
    console.log("Listening to port: " + port);
});

// gs://billion-taxi-rides-ml-gr/speech_test/audio.raw
// gs://billion-taxi-rides-ml-gr/speech_test/async.raw
