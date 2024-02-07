const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const SongsSchema = new Schema({
    name: String,
    artist:String,
    image: String,
    link: String,
    mood: String
});

module.exports = mongoose.model('Songs',SongsSchema);