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

class EnrolmentCheck():
    def __init__(self, debugMode):
        self.client = None
        self.debugMode = debugMode
        self.messageUrlRegex = re.compile('.* enrol https://discord.com/channels/([0-9]+)/([0-9]+)/([0-9]+)') 

    def setClient(self, client):
        self.client = client

    async def handleMessage(self, msg):
        if self.client == None:
            raise 'Client not set on command handler.'

        urlMatch = re.search(self.messageUrlRegex, msg.content)

        if urlMatch == None:
            await msg.author.send("Invalid url in " + msg.content)
            
        guildID, channelID, checkMsgID = (urlMatch.group(1), urlMatch.group(2), urlMatch.group(3))
        
        guild = self.client.get_guild(int(guildID))
        if guild == None:
            await msg.author.send("Invalid guild id " + guildID)
            return
        
        channel = find(lambda c: c.id == int(channelID), guild.channels)
        if channel == None:
            await msg.author.send("Invalid channel id " + channelID)
            return

        waitMsg = await msg.author.send('The execution of the enrol command may take a while to fetch all data...')
        
        try:
            checkMsg = await channel.fetch_message(int(checkMsgID))
        except NotFound:
            await msg.author.send('The message with ID {0} has not been found.'.format(checkMsgID))
            return
        except Forbidden:
            await msg.author.send('Access to message ID {0} is forbidden.'.format(checkMsgID))
            return
        except HTTPException:
            await msg.author.send('Retrieving the message failed.')
            return
        
        result = ''

        for reaction in checkMsg.reactions:
            users = await reaction.users().flatten()
            if self.debugMode:
                print('reaction: ', reaction)
                print('users: ', users)
            for user in users:
                result += "\n" + '{0} has reacted with {1.emoji}!'.format(user, reaction)
        await msg.author.send(result)
        await waitMsg.delete()
        return True

    def usage(self):
        return """Usage:
        The **enrol** command helps with simple enrolment to anounced games via emojis.
        
        All reactions on the given message are counted and evaluated in a special way to allow 
        an oversight about level, tier, class as well as newbie and long time not played status
        ofall reacting users. The values to identify certain recognizable emojis can be adjusted
        in data/enrol_emojis.txt in form of absolute match strings or even regex.

        The bot needs read access to the specified guild, channel and message.

        Syntax:
        /d3ot enrol [message link]

        Example:
        /d3ot enrol https://discord.com/channels/429385869271629825/429385870252965899/842403833896632360
        """
