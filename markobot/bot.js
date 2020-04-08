const Discord = require('discord.js')
const client = new Discord.Client()

function echo(input) {
  console.log(input);
}

client.login("NDU1NTI5Mjc0ODUwNjcyNjQx.DruwsA.tJpQPP3Mr4E01ftQZaKZq-1Opps") 

client.on('ready', () => {
    console.log("Connected as " + client.user.tag)

    client.user.setActivity("with AK-47")

    client.guilds.forEach((guild) => {
        console.log(guild.name)
        guild.channels.forEach((channel) => {
            console.log(` - ${channel.name} ${channel.type}  ${channel.id}  `) //General id - 411249827469328387

        })
    })

    let generalChannel = client.channels.get("411249827469328387")
    const attachment = new Discord.Attachment("https://evarazdin.hr/upload/media/k2/items/src/bf9cef73a47a11e9cfaa23d267525911.jpg")
    generalChannel.send("Za dom Spremni!")
    generalChannel.send(attachment)
})

client.on('message', (receivedMessage) =>{
     if (receivedMessage.author == client.user){
        return
    }
    if (receivedMessage.content.startsWith("%")){
        proccessCommand(receivedMessage)
    }
})

///Splits the message

function proccessCommand(receivedMessage){
    let fullCommand = receivedMessage.content.substr(1)
    let splitCommand = fullCommand.split(" ")
    let primaryCommand = splitCommand[0]
    let arguments = splitCommand.slice(1)

    if (primaryCommand == "help"){
        helpCommand(arguments, receivedMessage)
    }
    if (primaryCommand == "pomoc"){
        pomocCommand(arguments,receivedMessage)
    }
}

//Help commands

function helpCommand(arguments, receivedMessage) {
    if (arguments.length > 0) {
        receivedMessage.channel.send("Ja ti neznan ti englenski")
    } else {
        receivedMessage.channel.send("Ja ti neznan ti englenski")
    }
}

function pomocCommand(arguments,receivedMessage){
    receivedMessage.channel.send("Cinimise da ti triba malo pomoci, naci ovako:...") // ADD THE HELP COMMANDS
}

client.on('message', msg => {
    if (msg.content === 'Za dom!') {
      msg.reply('Spremni!');
    }
  });

///////////////////////////////////////////////PLAY A SONG\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

//connect to voice
client.on('message', message => {
    // Voice only works in guilds, if the message does not come from a guild,
    // we ignore it
    if (!message.guild) return;
  
    if (message.content === '%join') {
      // Only try to join the sender's voice channel if they are in one themselves
      if (message.member.voiceChannel) {
        message.member.voiceChannel.join()
          .then(connection => {
         })

          .catch(console.log);
      } else {
        message.reply('You need to join a voice channel first!');
      }
    }

  if (message.content === '%zasviraj') {
    // Only try to join the sender's voice channel if they are in one themselves
    if (message.member.voiceChannel) {
      message.member.voiceChannel.join()
        .then(connection => {
          const dispatcher = connection.playFile('jasenovac.mp3');
          dispatcher.on("end", end => {echo("done");})
       })

        .catch(console.log);
    } else {
      message.reply('You need to join a voice channel first!');
    }
  }
});