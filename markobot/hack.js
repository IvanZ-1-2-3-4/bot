const Discord = require("discord.js");
const client = new Discord.Client();
const math = require('mathjs');
var newWord = "";
let stuff;
client.on("ready", () => {
  console.log("ready");
});

String.prototype.replaceAt=function(index, replacement) {
    return this.substr(0, index) + replacement+ this.substr(index + replacement.length);
}

client.on("message", (message) => {
    
});

client.login("NDU1NTI5Mjc0ODUwNjcyNjQx.DruwsA.-1Opps");
