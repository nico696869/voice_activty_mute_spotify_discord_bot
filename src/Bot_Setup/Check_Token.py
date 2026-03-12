import os as _System
import dotenv as _ENV
from dotenv import load_dotenv as _Load_ENV
import src.Color_Library.Colors as _Color_library
import src.Color_Library.Colors as _Color
from src.Color_Library.Colors import *

def _Check_Token():
    print(_Color._BLUE + "[!] " + "" + "Getting Token from Environment Variable..." + _Color._RESET)
    
    # _TOKEN = _System.getenv("BOT_TOKEN")
    _TOKEN = _System.getenv("BOT_TOKEN")
    if not _TOKEN:
        print(_Color._RED + "[!] " + "Bot Token was not Set!" + _Color._RESET)
        return True
    else:
        print(_Color._GREEN + "[!] " + "Token Successfully Retrieved..." + _Color._RESET)
        return False