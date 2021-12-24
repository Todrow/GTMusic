import discord
import re


# Making Client class
class Client(discord.Client):

    actions = {} # Put here function that will execute if needed message will be received
    """
    Example:

    actions = {"!*": f}

    Function "f" will be executed if bot received a message, that starts with "!".
    Make sure that the only one argument that will be given to the function will
    be the message, that called a function.
    """

    async def on_ready(self):
        print("Started")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        text = message.content

        for item in actions:
            if re.match(item.key, text):
                item.value(message)

# Getting token
with open("C:/key/key.txt", "r") as f: token = f.read();

# Starting client
client = Client()
client.run(token)
