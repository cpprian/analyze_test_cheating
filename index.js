require('@tensorflow/tfjs-node');

const express = require('express');
const cors = require('cors');

const app = express();

const faceLandmarksDetection = require('@tensorflow-models/face-landmarks-detection');

app.use(express.static(__dirname), cors({ origin: "*" }));


app.listen(2020, () => {
    app.get('/', async (req, res) => {
        console.log("hello");
        res.sendFile(__dirname + '/index.html');
        res.sendFile(__dirname + '/cyprian1.mp4');
        
        const model = await faceLandmarksDetection.load(
        faceLandmarksDetection.SupportedPackages.mediapipeFacemesh);
    
        const video = document.querySelector("video");
        const faces = await model.estimateFaces({input: video});
    
        console.log(faces);
        console.log(faces.length);
        console.log("done");
    });
});