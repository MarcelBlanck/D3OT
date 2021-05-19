# D3OTClient.py

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

import re, discord

class D3OTClient(discord.Client):
    def __init__(self, command, guild, debugMode):
        super(D3OTClient, self).__init__()
        self.command = command
        self.guild = guild
        self.debugMode = debugMode
        self.commandRegex = re.compile(self.command + ' ([a-z]+).*')
        self.commandExecutors = {}

    def setCommandExecutors(self, commandExecutors):
        self.commandExecutors = commandExecutors
        for command in self.commandExecutors:
            commandExecutors[command].setClient(self)

    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == self.guild, self.guilds)
        print(f'{self.user} is connected to: {guild.name}(id: {guild.id})')

    async def on_message(self, msg):
        if not msg.content.startswith(self.command) or msg.author.bot:
            return

        if self.debugMode:
            print('Incomming message {0}'.format(msg.content))

        commandMatch = re.search(self.commandRegex, msg.content)
        commandExecuted = False
        if commandMatch != None:
            command = commandMatch.group(1)
            if command in self.commandExecutors:
                await self.commandExecutors[command].handleMessage(msg)
                commandExecuted = True
            else:
                await self.sendUsage(msg.author, f'Unknown command "{command}".')
        
        if not commandExecuted:
            await self.sendUsage(msg.author, f'Wrong syntax "{msg.content}"')

    async def sendUsage(self, author, errorText):
        usageText = f'Error: {errorText}\n\nD3OT Bot Usage:\n'
        for command in self.commandExecutors:
            usageText += self.commandExecutors[command].usage()
        await author.send(usageText)
