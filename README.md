# Discord D&D Orga Tools Bot - D3OT

## Setup
1. Install python3 on your system, then
2. ```pip3 install -U discord.py```
3. ```pip install -U python-dotenv```

## Run

### Configure the runtime environment
Create the environment file in the same folder as bot.py. The filename must be ```.env``` and the content must be the following: 

```
# .env
DISCORD_TOKEN=Your token
GUILD_NAME=Your guild name
COMMAND=/d3ot
```

### Run the bot
```python3 bot.py ```
