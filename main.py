import os

import discord

from dotenv import load_dotenv
load_dotenv()

import logging

intents = discord.Intents.all()
intents.message_content = True

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#discord.opus.load_opus('/lib/x86_64-linux-gnu/libopus.so.0')

class URandom(discord.Bot):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print("Screaming into VC...")

bot = URandom()
connection = None

@bot.slash_command()
async def urandom(ctx: discord.ApplicationContext):
    global connection

    await ctx.respond(str(os.urandom(100).decode('latin1')))
    
    voice = ctx.author.voice
    if not voice:
        await ctx.respond(f"You need to join a channel, you {str(os.urandom(5).decode('latin1'))}")        


    if connection != None:
        print("Connection exists")
        await connection.disconnect(force=True)
        connection = None

    pipe = discord.FFmpegOpusAudio("/dev/urandom", before_options="-f s16le", options="-map 0", codec="copy", bitrate=150)

    connection = await voice.channel.connect()
    connection.play(pipe, after=lambda x: pipe.cleanup())

bot.run(os.getenv("BOT_TOKEN"))
