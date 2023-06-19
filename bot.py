# bot.py
import disnake
from disnake.ext import commands
import logging
import json
from disnake.ext import tasks

from config.settings import TOKEN, TEST_GUILD_IDS, SIGNAL_CHANNEL_ID

# Create logger
logger = logging.getLogger('dca-bot')
# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Add formatter to ch
ch.setFormatter(formatter)
# Add ch to logger
logger.addHandler(ch)

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix='!', help_command=None,intents=disnake.Intents.all(), test_guilds=TEST_GUILD_IDS, command_sync_flags=command_sync_flags)

# Load cogs
bot.load_extension("cogs.dca")
bot.load_extension("cogs.setchannel")
bot.load_extension("cogs.info")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_guild_join(guild):
    logger.info(f'Joined {guild.name} ({guild.id})')
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
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"{ctx.author.mention} An error occurred while invoking the command. Please try again later.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"{ctx.author.mention} An error occurred while processing the command. Please try again later.")


bot.run(TOKEN)

