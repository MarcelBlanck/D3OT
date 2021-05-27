# EnrolmentCheck.py

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



import re
from discord.utils import find
from discord import NotFound, Forbidden, HTTPException

class CharacterDataWrite():
    def __init__(self, databaseConnection, debugMode):
        self._client = None
        self._databaseConnection= databaseConnection
        self._debugMode = debugMode
        self._commandRegex = re.compile('.* wchar "([^"]+)" ([0-9]+) (.+)') 

    def setClient(self, client):
        self._client = client

    async def handleMessage(self, msg):
        if self._client == None:
            raise 'Client not set on command handler.'

        commandMatch = re.search(self._commandRegex, msg.content)

        if commandMatch == None:
            await msg.author.send("Invalid command in " + msg.content)
            
        charName, charLevel, charUrl = (commandMatch.group(1), commandMatch.group(2), commandMatch.group(3))
        '''CREATE TABLE IF NOT EXISTS chars 
        (player_tag text, char_name text, char_level int, created text, updated text, data_url text)'''

#         cur = self._databaseConnection.cursor()
#         cur.execute('''REPLACE INTO positions (player_tag, char_name)
#             (player_tag text, char_name text, char_level int, created text, updated text, data_url text)''')
#         con.commit()

#         REPLACE INTO positions (title, min_salary)
# VALUES('Full Stack Developer', 140000);

    def usage(self):
        return """Usage:
        The **wchar** command lets players store or update character data

        Syntax:
        /d3ot wchar "[char name]" [char level] [char sheet URL]

        Example:
        /d3ot wchar "Drizzt Do'Urden" 8 https://media.wizards.com/2018/dnd/dragon/19/DRA19_5_Drizzt.pdf
        """
