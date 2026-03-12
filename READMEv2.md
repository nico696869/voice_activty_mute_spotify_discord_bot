# Voice Activity
A Discord Bot that utilizes Voice intent to do stuff

## Features

#### Join
 - You can use ```!join``` to make the bot join the Voice Channel.

#### Leave
 - Type in ```!leave``` to make the bot leave the channel.

#### Listen
 - ```!listen``` to make the bot start the listening and auto mute spotify

#### Stop Listening
 - ```!stop_listen``` to stop listening to the vc.

#### Mute Spotify Player
 - ```!mute_spotify``` mutes spotify.

#### Unmute Spotify Player
 - ```!umute_spotify``` to unmute.

<hr>

## Miscellaneous

#### Voice Detection
- Detects when users join voice channels
- Triggers actions based on activity

#### Spotify Integration
- Automatically mutes Spotify when someone speaks
- Restores audio after inactivity

<hr>

### USAGE

* Put your **Bot Token** from the Discord Developer Portal into the `./.env` file.

Example:

```env
BOT_TOKEN=your_discord_bot_token_here
```

* Install the required dependencies:

```bash
pip install -r requirements.txt
```

* Start the bot:

```bash
python main.py
```

Once the bot starts, invite it to your Discord server and it will come online.

<hr>

<p align="center">
  <b>END OF DOCUMENT</b>
</p>