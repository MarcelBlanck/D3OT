# bot.py

# D3OT - The Discord Dungeons & Dragons Organizational Tools Bot
# Copyright (C) 2021  Marcel Blanck | mail@marcel-blanck.de
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sqlite3
from dotenv import load_dotenv
from client.D3OTClient import D3OTClient
from client.commands.EnrolmentCheck import EnrolmentCheck
from client.commands.CharacterDataWrite import CharacterDataWrite

def printWelcomeMessage():
    with open(os.path.join(os.path.dirname(__file__), 'data/welcome.txt'), mode='r') as welcome:
        for line in welcome:
            print(line, end='')

def initDatabase(con):
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS chars
        (player_tag text, char_name text, char_level int, created text, updated text, data_url text)''')
    con.commit()

if __name__ == '__main__':
    load_dotenv()

    printWelcomeMessage()

    debugMode = bool(os.getenv('DEBUG_MODE'))

    sqliteConnection = sqlite3.connect(os.getenv('DATABASE_NAME') + '.db')
    initDatabase(sqliteConnection)

    client = D3OTClient(
        os.getenv('COMMAND'), 
        os.getenv('GUILD_NAME'), 
        debugMode
    )

    client.setCommandExecutors({
        'enrol': EnrolmentCheck(debugMode)
    })

    client.run(os.getenv('DISCORD_TOKEN'))
