from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
import spotify_mute
from discord.ext import voice_recv
import time
import asyncio

last_speech_time = 0
spotify_muted = False
SILENCE_DELAY = 2

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

speaking_users = set()

class VoiceReceiver(voice_recv.AudioSink):

    def wants_opus(self):
        return True

    def write(self, user, data):
        global last_speech_time, spotify_muted

        last_speech_time = time.time()

        if not spotify_muted:
            print(f"{user} muting Spotify")
            spotify_mute.mute_spotify(True)
            spotify_muted = True

    def cleanup(self):
        pass
    
async def silence_monitor():

    global last_speech_time, spotify_muted

    while True:

        await asyncio.sleep(0.5)

        if spotify_muted:
            if time.time() - last_speech_time > SILENCE_DELAY:

                print("umuting spotify")

                spotify_mute.mute_spotify(False)
                spotify_muted = False

@bot.event
async def on_ready():
    print("Bot logged in as:", bot.user)

    bot.loop.create_task(silence_monitor())

@bot.command()
async def join(ctx):

    if ctx.author.voice:

        channel = ctx.author.voice.channel

        if ctx.voice_client:
            await ctx.voice_client.disconnect()

        vc = await channel.connect(cls=voice_recv.VoiceRecvClient)

        await ctx.send(f"Joined {channel.name}")

    else:
        await ctx.send("You are not in a voice channel.")
        
        
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
        await ctx.message.delete()
    else:
        await ctx.send("I am not in a voice channel.")
        await ctx.message.delete()        

@bot.command()
async def listen(ctx):

    global listening

    vc = ctx.voice_client

    if not vc:
        await ctx.send("I'm not in a voice channel.")
        return

    listening = True

    sink = VoiceReceiver()
    vc.listen(sink)

    await ctx.send("Started listening for voices.")

@bot.command()
async def stop_listen(ctx):

    global listening

    listening = False

    spotify_mute.mute_spotify(False)

    await ctx.send("Stopped listening.")


@bot.command()
async def mute_spotify(ctx):
    spotify_mute.mute_spotify(True)
    await ctx.send("Spotify has been muted.")
    await ctx.message.delete()
    
@bot.command()
async def unmute_spotify(ctx):
    spotify_mute.mute_spotify(False)
    await ctx.send("Spotify has been unmuted.")
    await ctx.message.delete()


bot.run(BOT_TOKEN)
