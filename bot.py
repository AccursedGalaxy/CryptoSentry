import disnake
from disnake.ext import commands
import logging

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


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

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

bot.run(TOKEN)

