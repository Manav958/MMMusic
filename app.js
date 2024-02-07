const express = require('express');
const app = express();
const path = require('path');
const mongoose = require('mongoose');
const Songs = require('./models/Songs');
const methodOverride = require('method-override');
const ejsMate = require('ejs-mate');
const axios = require('axios');
const cors = require('cors');
const bodyParser = require('body-parser');

app.use(cors());

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(methodOverride('_method'));
app.use(bodyParser.json());

mongoose.connect('mongodb://localhost:27017/Songs', {

});

const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => {
    console.log("database connected");
});

app.engine('ejs', ejsMate)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(methodOverride('_method'))
//_________________________________________________________
app.get('/', (req, res) => {
    res.render('home.ejs')
})
//_______________________________________________________
app.get('/songs', async (req, res) => {
    const music = await Songs.find({})
    res.render('songs/index', { music })
})

//_________________________________________________
app.get('/songs/new', (req, res) => {
    res.render('songs/new');
})
app.post('/songs', async (req, res) => {
    const music = new Songs(req.body.Songs);
    await music.save();
    res.redirect(`/songs/${music._id}`);

});

//_____________________________________________
app.get('/songs/:id', async (req, res) => {
    const mus = await Songs.findById(req.params.id)
    res.render('songs/show', { mus });

})

app.get('/text', async (req, res) => {
    res.render('songs/text');

})

app.post('/predict', (req, res) => {
    const message = req.body.message;
    const predictedMood = predictedMood(message);
    res.setHeader('Content-Type', 'application/json');

    res.json({ predictedMood })

})
let mood;
app.post('/send', (req, res) => {
    mood = req.body.predictedMood;


    res.redirect('/final_result')


})
app.get('/final_result', async (req, res) => {

    console.log(mood)
    const music = await Songs.find({ mood: mood });
    console.log(music)
    res.render('songs/result', { music, mood });
});








//_________________________________________________
app.listen(3000, () => {
    console.log("Serving on port 3000!!")
})