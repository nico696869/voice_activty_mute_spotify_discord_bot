from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
import spotify_mute
from discord.ext import voice_recv
import time
from datetime import timedelta
import asyncio
import yt_dlp




last_speech_time = 0
spotify_muted = False
SILENCE_DELAY = 2
song_queue = []
is_playing = False

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

ytdl = yt_dlp.YoutubeDL({
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "default_search": "ytsearch"
})

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


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

    vc = ctx.voice_client

    if vc:
        vc.stop_listening()

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

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int):
    await member.timeout(discord.utils.utcnow() + timedelta(seconds=duration))
    await ctx.send(f"{member} has been timed out for {duration} seconds.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def remove_timeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"{member} has been removed from timeout.")
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f"{member} has been kicked from the server.")
    
@kick.error
async def kick_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
        
            
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"{member} has been banned from the server.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):

    await ctx.guild.unban(user)

    await ctx.send(f"{user} has been unbanned.")     
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"Cleared {amount} messages.")
    await msg.delete(delay=5)
        
@bot.command()
async def jarvis_play(ctx, *, query):

    global is_playing

    if not ctx.author.voice:
        await ctx.send("You must be in a voice channel.")
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    vc = ctx.voice_client

    try:

        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))

        if "entries" in info:
            info = info["entries"][0]

        url = info["url"]
        title = info["title"]

        song_queue.append((url, title))

        await ctx.send(f"Added to queue: {title}")

        if not is_playing:
            await play_next(ctx)

    except Exception as e:
        await ctx.send("Error playing the song.")
        print(e)
        
@bot.command()
async def skip(ctx):

    vc = ctx.voice_client

    if not vc:
        await ctx.send("I'm not in a voice channel.")
        return

    if not vc.is_playing():
        await ctx.send("Nothing is playing.")
        return

    vc.stop()  

    await ctx.send("Skipped the current song.")
            
@bot.command()        
async def play_next(ctx):

    global is_playing

    vc = ctx.voice_client

    if not vc:
        return
    if vc.is_playing():
        return

    if len(song_queue) > 0:

        is_playing = True

        url, title = song_queue.pop(0)

        vc.play(
            discord.FFmpegPCMAudio(url, **ffmpeg_options),
            after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        )

        await ctx.send(f"Now playing: {title}")

    else:
        is_playing = False 
           
bot.run(BOT_TOKEN)
