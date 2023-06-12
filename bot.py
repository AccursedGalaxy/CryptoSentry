import disnake
from disnake.ext import commands
import logging
import json
import os
import importlib
from disnake.ext import tasks

from config.settings import TOKEN

logger = logging.getLogger('disnake')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix='!', help_command=None,intents=disnake.Intents.all(), test_guilds=[1087088370250948744])

command_modules = {}


command_modules['dca'] = importlib.import_module('commands.dca')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        command_modules[filename[:-3]] = importlib.import_module(f'commands.{filename[:-3]}')



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_guild_join(guild):
    print(f'Joined {guild.name} ({guild.id})')
    await guild.system_channel.send("Hello! I'm a bot that can help you with your DCA levels.")
    await guild.system_channel.send("To get started, type `!setchannel <channel_id>` to set the channel for signals.")

@bot.event
async def on_command_error(ctx, error):
    logger.error(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have permission to use this command.")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f"Invalid input. Please try again: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\n\n{ctx.command.help}",
            color=disnake.Color.red()
        ))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention} This command is on cooldown. Please try again in {error.retry_after:.2f}s.")
    elif isinstance(error, commands.CommandNotFound):

        # If the command is not found, do nothing
        pass
    else:
        await ctx.send(f"{ctx.author.mention} An error occurred while processing the command. Please try again later.")


@bot.slash_command()
async def ping(ctx):
    await ctx.response.send_message('Pong!')

# get channel id from user input and write to channel.json
@bot.slash_command()
async def set_channel(ctx, channel_id: int):
    if ctx.author.id == 883830567219642449:
        with open('channel.json', 'w') as f:
            json.dump({'channel_id': channel_id}, f)
        await ctx.response.send_message(f"Channel set to {channel_id}.")
    else:
        await ctx.response.send_message(f"{ctx.author.mention} You don't have permission to use this command.")


@bot.slash_command()
async def dca(ctx):
    await ctx.response.send_message("Checking DCA levels...")
    await check_dca_levels(bot)

@tasks.loop(minutes=5) # one minute for testing
async def check_dca_levels(client):
    response = await command_modules['dca'].generate_dca_response()

    # try to read the old response, handle the case where the file doesn't exist or is empty
    try:
        with open('dca_response.json', 'r') as f:
            old_response = f.read()
    except (FileNotFoundError, IOError):
        old_response = ""
        logging.info("No previous response found.")

    # write the new response to the file
    with open('dca_response.json', 'w') as f:
        f.write(response)

    # send only unique lines of the response to the channel
    new_lines = [line for line in response.split('\n') if line and line not in old_response.split('\n')]
    if new_lines:
        logging.info(f"New lines found: {new_lines}")
        # get channel id from channel.json
        try:
            with open('channel.json', 'r') as f:
                channel_id = json.load(f)['channel_id']
        except (FileNotFoundError, IOError, KeyError):
            logging.error("Failed to get channel ID.")
            return
        channel = client.get_channel(int(channel_id))
        if channel is not None:
            embed = discord.Embed(title="New Levels:", description="\n".join(new_lines), color=0x00ff00)
            await channel.send(embed=embed)
    else:
        logging.info(f"No new lines found in response.")

    logging.info("Finished checking DCA levels.")





bot.run(TOKEN)

