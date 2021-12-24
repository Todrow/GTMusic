import discord


class Client(discord.Client):
    async def on_ready(self):
        print("Started")

    async def on_ready(self, message):
        print(f'Message from {message.author}: {message.content}')

client = MyClient()
client.run()
