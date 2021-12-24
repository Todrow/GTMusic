import discord
import re


TEXT_SERVER_ID = 924019353203142736


# Making Client class
class Client(discord.Client):
    async def docommand(self, message):
        await self.sent_message(message.content)

    async def sent_message(self, text):
        await self.get_channel(TEXT_SERVER_ID).send(text)

    async def on_ready(self):
        print("Started")

    async def on_message(self, message):

        self.actions = {"^!*": self.docommand} # Put here function that will execute if needed message will be received
        """
        Example:

        actions = {"!*": f}

        Function "f" will be executed if bot received a message, that starts with "!".
        Make sure that the only one argument that will be given to the function will
        be the message, that called a function.
        """

        text = message.content

        for key, value in self.actions.items():
            if re.match(key, text) != '':
                await value(message)

# Getting token
with open("C:/key/key.txt", "r") as f: token = f.read();

# Starting client
client = Client()
client.run(token)
