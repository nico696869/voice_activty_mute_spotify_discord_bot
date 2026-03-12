import os as _System
import dotenv as _ENV
from dotenv import load_dotenv as _Load_ENV
from src.Bot_Setup.Check_Token import _Check_Token
import src.Color_Library.Colors as _Color_library
import src.Color_Library.Colors as _Color
from src.Color_Library.Colors import *
import discord as _Discord
from discord.voice_client import VoiceClient as _VcClient
from discord.ext import commands as _BotCommandAPI

_Load_ENV()
_TOKEN = _System.getenv("BOT_TOKEN")
if _Check_Token():
    print(_Color._RED + "[!] " + "Bot Token was not Set!" + _Color._RESET)
    _System._exit(5)
else:
    print(_Color._GREEN + "[!] " + "Token Successfully Retrieved..." + _Color._RESET)


_BOT_INTENT = _Discord.Intents.default()
_BOT_INTENT.message_content = True
_BOT_INTENT.voice_states = True
_BOT = _BotCommandAPI.Bot(command_prefix="!", intents=_BOT_INTENT)


@_BOT.event
async def on_message(message):
    if message.author.bot:
        return

    if "join vc" in message.content.lower():
        if message.author.voice:
            channel = message.author.voice.channel

            if message.guild.voice_client is None:
                await channel.connect()
                await message.channel.send("Joined your VC!")
            else:
                await message.channel.send("I'm already in a voice channel.")

        else:
            await message.channel.send("You are not in a voice channel.")

    await _BOT.process_commands(message)
    
@_BOT.event
async def _IsSomeoneSpeaking(member, speaking):
    if speaking:
        print("Someone is yapping.")

        
    
    
    
    
    
    
_BOT.run(_TOKEN)