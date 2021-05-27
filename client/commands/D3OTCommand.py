# D3OTCommand.py
"""This is the base class for all commands"""

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

class D3OTCommand():
    def __init__(self, debugMode, commandRegex):
        self._client = None
        self._debugMode = debugMode
        self._commandRegex = re.compile(commandRegex)

    def setClient(self, client):
        self._client = client

    def handleMessage(self, msg):
        if self._client == None:
            raise 'Client not set on command handler.'

    def usage(self):
        pass

    async def _getCommandParameters(self, msg):
        if self._commandRegex == None:
            raise ValueError('CommandRegex has not been set in subclass')

        match = re.search(self._commandRegex, msg.content)

        return match.groups()