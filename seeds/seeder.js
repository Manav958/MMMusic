const path =require('path');
const mongoose = require('mongoose');
const songs = require('../models/Songs');
 
mongoose.connect('mongodb://localhost:27017/Songs',{
    
});

const db = mongoose.connection;
db.on("error", console.error.bind(console,"connection error:"));
db.once("open",() => { 
    console.log("database connected");
});

const seedDB = async () =>{
    await songs.deleteMany({});
    
    const mus =new songs({
        name: 'Confident',
        artist: 'Justin Bieber',
        mood: 'cool',
        link: '',
        image:''
    })
    await mus.save()
    
    
}

seedDB();