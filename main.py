import json
import discord
import re
from youtube_dl import YoutubeDL
from asyncio import sleep
import os
from FindMusic import get_video


BASE_DIR = os.path.split(os.path.abspath(__file__))[0] + "\\"


# TEXT_SERVER_ID = 760581470565433425

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

PLAYLISTS = {}

def readJSON():
    with open('./playlists/playlists.json', 'r') as read_file:
        return json.load(read_file)

def writeJSON(playlists):
    with open('./playlists/playlists.json', 'w') as write_file:
        json.dump(playlists, write_file)

PLAYLISTS = readJSON()
queue = []


def compare(r, text):
    match = re.match(r, str(text))
    if match is not None:
        if match.group(0) != '': return True
    return False

# Making Client class
class Client(discord.Client):
    async def queue(self, url):
        # try:
        #     if queue[0] == url:
        #         await self.sent_message("This song is already on queue.")
        #         return
        # except: pass
        queue.append(url)

    async def play(self, voice_channel):
        global vc, queue

        print(f"[INFO] playing to {voice_channel}")

        try:
            vc = await voice_channel.connect()
        except:
            print('[WARNING] Already have connected or cannot connect to the server.')
            if not vc: return

        if vc.is_playing():
            pass
        else:
            while len(queue) > 0:
                try:
                    URL = queue[0]
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(URL, download=False)

                    url = info['formats'][0]['url']

                    vc.play(discord.FFmpegPCMAudio(executable=BASE_DIR+"ffmpeg\\ffmpeg.exe", source = url, **FFMPEG_OPTIONS))

                    await self.sent_message(f"Now playing: {URL}")
                    self.now_playing = URL

                    while vc.is_playing() or vc.is_paused():
                        await sleep(1)
                except:
                    await self.sent_message("I can`t do this!")
                finally:
                    try:
                        queue = queue[1:]
                    except:
                        pass
            try:
                if not vc.is_paused():
                    await vc.disconnect()
            except:
                await self.sent_message("I can`t do this!")

    async def docommand(self, message):
        global queue, vc

        if compare("^!play ", message.content) or compare("^!p ", message.content):
            if compare("^!play http*", message.content) or compare("^!p http*", message.content):
                url = message.content.split()[1]
                await self.queue(url)
            else:
                try:
                    playlist = PLAYLISTS[" ".join(message.content.split()[1:])]
                    for song in playlist:
                        await self.queue(song)
                except:
                    # https://www.youtube.com/results?search_query=
                    name = " ".join(message.content.split()[1:])
                    song = get_video(name)
                    await self.queue(song)
                    # Here we put finding song by name
                    #await self.sent_message("No such playlist")
            try:
                if not vc.is_playing():
                    await self.play(message.author.voice.channel)
            except:
                await self.play(message.author.voice.channel)

        elif compare("^!queue", message.content):
            if len(queue) == 0:
                await self.sent_message("Queue is empty")
            else:
                await self.sent_message("Queue:\n" + "\n".join([str(i+1)+". "+name for i, name in enumerate(queue[:5])]))

        elif compare("^!dis", message.content):
            try:
                await vc.stop()
                await vc.disconnect()
                queue = []
            except:
                pass

        elif compare("^!skip", message.content):
            try:
                await vc.stop()
                queue = queue[1:]
            except:
                pass

        elif compare("^!pause", message.content):
            try:
                await vc.pause()
            except:
                pass

        elif compare("^!resume", message.content):
            try:
                await vc.resume()
            except:
                pass

        elif compare("^!help", message.content):
            await self.sent_message(
"""I know such commands as:
1. !play smth - {!p - is the same} I will add the song you want to the queue. Instead of 'smth' you should write the url to a video on YouTube, or the name of the playlist, or the name of the song.
2. !queue - I will show the queue.
3. !skip - I will skip the current song.
4. !help - It's a help.
5. !dis - I will disconnect from server and clear queue.
6. !playlists - {!pls is the same} I will show all playlists that I know.
6.1 !playlists name - I will show the list of songs of necessary playlist. Instead of 'name' put the name of playlist.
6.2 !playlists add name - I will make a new playlist. Instead of 'name' put the name of playlist.
6.3 !playlists update url name - I will add a song to a playlist. Instead of 'url' put the url to a song, instead of 'name' put the name of playlist.
7. !pause - I will pause the current song.
8. !resume - I will resume the current song."""
            )
        elif compare("^!playlists", message.content) or compare("^!pls", message.content):
            if compare("^!playlists add *", message.content) or compare("^!pls add *", message.content):
                try:
                    playlist = " ".join(message.content.split()[2:])
                    if playlist[:6] == "https:": a=1/0
                    PLAYLISTS.update({playlist: []})

                    writeJSON(PLAYLISTS)
                except:
                    print("[ERROR] Something got wrong while adding a playlist.")

            elif compare("^!playlists update *", message.content) or compare("^!pls update *", message.content):
                try:
                    url = message.content.split()[2]
                    playlist = " ".join(message.content.split()[3:])
                    PLAYLISTS[playlist].append(url)

                    writeJSON(PLAYLISTS)
                except:
                    print("[ERROR] Something got wrong while adding a song to a playlist.")

            elif compare("^!playlists \w*", message.content) or compare("^!pls \w*", message.content):
                try:
                    playlist = " ".join(message.content.split()[1:])
                    plst = PLAYLISTS[playlist]
                    result = " \n".join([str(i+1)+". "+name for i, name in enumerate(plst)])
                    await self.sent_message(f"In {playlist} there are:\n" + result)

                except:
                    print("[ERROR] Something got wrong while showing a playlist.")

            else:
                result = "\n".join([str(i+1)+". "+name for i, name in enumerate(PLAYLISTS.keys())])
                await self.sent_message("I know such playlists as:\n" + result)

        else:
            await self.sent_message("Нихуя не понял, но очень интересно. Что бы узнать какие есть комманды введи !help.")

    async def sent_message(self, text):
        try:
            await self.text_channel.send(text)
        except:
            print("[ERROR] Cannot connect to unidentified text channel.")

    async def on_ready(self):
        print("Hello")

    async def on_message(self, message):
        if (message.author != self.user):
            self.actions = {r"^!*": self.docommand} # Put here function that will execute if needed message will be received
            self.text_channel = message.channel
            """
            Example:

            actions = {"!*": f}

            Function "f" will be executed if bot received a message, that starts with "!".
            Make sure that the only one argument that will be given to the function will
            be the message, that called a function.
            """
            text = message.content
            for key, value in self.actions.items():
                if compare(key, text):
                        await value(message)

# Getting token
with open("C:/key/key.txt", "r") as f: token = f.read();

# Starting client
client = Client()
client.run(token)
