import discord
import DiscordBotForGreenwell as dbfg

@client.event
async def on_ready():
    print(f'Logged in as a bot {dbfg.client.user}')
    print(dbfg.client.user.name)
    print(dbfg.client.user.id)
    print('------')

    guild = discord.utils.get(dbfg.client.guilds, name=GUILD)
    print(
        f'{dbfg.client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )
