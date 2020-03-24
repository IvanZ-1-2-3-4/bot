import discord as d
from dsicord.ext import commands

class Client(d.Client):
    async def on_ready(self):
        print("Logged on as {0}".format(self.user))

    async def on_message(self, message):
        print("message from {0.author}: {0.content}".format(message))

c = Client()
c.run("qmo56QXiXhq4KV_GIg2rR8pSLkZ956ky")