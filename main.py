import discord
import re
from youtube_dl import YoutubeDL
from asyncio import sleep


TEXT_SERVER_ID = 924019353203142736

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# Making Client class
class Client(discord.Client):
    async def play(self, message):
        global vc

        try:
            voice_channel = message.author.voice.channel
            print(voice_channel)
            vc = await voice_channel.connect()
        except:
            print('Already have connected or cannot connect to the server.')

        if vc.is_playing():
            await ctx.send(f'{message.author}, music is already playing.')
        else:


    async def docommand(self, message):
        await self.sent_message(message.content[1:])

    async def sent_message(self, text):
        await self.get_channel(TEXT_SERVER_ID).send(text)

    async def on_ready(self):
        print("Started.")

    async def on_message(self, message):
        if (message.author != self.user):
            self.actions = {r"^!play": self.play} # Put here function that will execute if needed message will be received
            """
            Example:

            actions = {"!*": f}

            Function "f" will be executed if bot received a message, that starts with "!".
            Make sure that the only one argument that will be given to the function will
            be the message, that called a function.
            """

            text = message.content
            for key, value in self.actions.items():
                match = re.match(key, str(text))
                if match is not None:
                    if match.group(0) != '':
                        await value(message)

# Getting token
with open("C:/key/key.txt", "r") as f: token = f.read();

# Starting client
client = Client()
client.run(token)
