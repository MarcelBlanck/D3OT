# bot.py
import os, re, discord
from discord.utils import find
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')
COMMAND = os.getenv('COMMAND')

class MGToolBotClient(discord.Client):
    def __init__(self):
        super(MGToolBotClient, self).__init__()
        self.commandRegex = re.compile(r'/mg ([a-z]+).*')
        self.messageUrlRegex = re.compile(r'/mg eval https://discord.com/channels/([0-9]+)/([0-9]+)/([0-9]+)')


    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})')


    async def on_message(self, msg):
        if not msg.content.startswith(COMMAND) or msg.author.bot:
            return

        print('Incomming message ' + msg.content)
        commandMatch = re.search(self.commandRegex, msg.content)
        if commandMatch != None:
            command = commandMatch.group(1)
            if command == 'eval':
                await self.cmd_evaluateGameEnrolement(msg)
            else:
                await self.sendUsage(msg.author)


    async def cmd_evaluateGameEnrolement(self, msg):
        urlMatch = re.search(self.messageUrlRegex, msg.content)
        if urlMatch != None:
            guildID, channelID, checkMsgID = (urlMatch.group(1), urlMatch.group(2), urlMatch.group(3))
            
            guild = self.get_guild(int(guildID))
            if guild == None:
                await msg.author.send("Invalid guild id " + guildID)
                return
            
            channel = find(lambda c: c.id == int(channelID), guild.channels)
            if channel == None:
                await msg.author.send("Invalid channel id " + channelID)
                return
            
            try:
                checkMsg = await channel.fetch_message(int(checkMsgID))
            except discord.NotFound:
                await msg.author.send('The message with ID {0} has not been found.'.format(checkMsgID))
                return
            except discord.Forbidden:
                await msg.author.send('Access to message ID {0} is forbidden.'.format(checkMsgID))
                return
            except discord.HTTPException:
                await msg.author.send('Retrieving the message failed.')
                return
            
            result = ''
            for reaction in checkMsg.reactions:
                users = await reaction.users().flatten()
                for user in users:
                    result += "\n" + '{0} has reacted with {1.emoji}!'.format(user, reaction)
            await msg.author.send(result)
            await msg.author.send("Done!")
        else:
            await self.sendUsage(msg.author)


    async def sendUsage(self, author):
        await author.send("Usage...")

client = MGToolBotClient()

client.run(TOKEN)