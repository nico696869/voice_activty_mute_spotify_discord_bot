import keyboard 
import comtypes
from pycaw.pycaw import AudioUtilities

#print(AudioUtilities.GetAllSessions())

muted = False

def mute_spotify(muted):
    comtypes.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == "Spotify.exe":
            volume = session.SimpleAudioVolume
            volume.SetMute(muted, None)
            comtypes.CoUninitialize()

#while True:
        #keyboard.wait('x')
       # muted = not muted
       # mute_spotify(muted)
        
        