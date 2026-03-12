import os as _System
import dotenv as _ENV
from dotenv import load_dotenv as _Load_ENV
from src.Bot_Setup.Check_Token import _Check_Token
import src.Color_Library.Colors as _Color_library
import src.Color_Library.Colors as _Color
from src.Color_Library.Colors import *
import discord as _Discord
from discord.voice_client import VoiceClient as _VcClient

_Load_ENV()
if _Check_Token():
    print(_Color._BLUE + "[!] " + _Color._GREEN + "Bot TOken Configured...")
vi = _Discord.version_info