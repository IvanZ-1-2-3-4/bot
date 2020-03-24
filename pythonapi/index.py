import discord as d
from discord.ext import commands

class Client(d.Client):
    async def on_ready(self):
        print("Logged on as {0}".format(self.user))

    async def on_message(self, message):
        print("message from {0.author}: {0.content}".format(message))

c = Client()
c.run("NjkyMDQ2MDM5NzI4NzgzMzYw.Xno73A.PAlIq53K53xAiYO5Y5NBv5-oIa0")