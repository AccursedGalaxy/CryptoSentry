import disnake
from disnake.ext import commands
import logging
import json
import requests
from disnake.ext import tasks

from config.settings import TOKEN, CMC_API_KEY, TEST_GUILD_IDS, SIGNAL_CHANNEL_ID
from config.setup import coins, near_percentage

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

channel_id = SIGNAL_CHANNEL_ID

last_signals = {}


@bot.event
async def on_ready():
    global channel_id
    print(f'We have logged in as {bot.user}')
    # Load channel_id from JSON file
    try:
        with open('channel.json', 'r') as f:
            data = f.read()
            if data:
                data_json = json.loads(data)
                channel_id = data_json.get('channel_id', None)
            else:
                channel_id = None
    except FileNotFoundError:
        channel_id = None
    # Start the background task only if the channel_id is set and the channel exists in the guild
    if channel_id is not None:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            # Check if the task is running before trying to start it
            if not signal_task.is_running():
                signal_task.start()




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


async def send_signals():
    global last_signals
    # Get the channel
    channel = bot.get_channel(channel_id)
    # Only send signals if the channel_id is set and the channel exists
    if channel_id is not None and channel is not None:
        # Generate the DCA response
        response = await generate_dca_response()
        # Split the response into lines
        lines = response.split('\n')
        # Iterate over the lines
        for i in range(2, len(lines)):
            # Check if ' Hit a ' is in the line
            if ' Hit a ' in lines[i]:
                # Get the coin and the signal
                coin, signal = lines[i].split(' Hit a ')
                # If the signal is different from the last one, send it
                if last_signals.get(coin) != signal:
                    # Create an embed message
                    embed = disnake.Embed(
                        title=f"Signal for {coin}",
                        description=f"{coin} has hit a {signal}",
                        color=disnake.Color.green() if 'DCA Level' in signal else disnake.Color.red()
                    )
                    await channel.send(embed=embed)
                    # Update the last signal
                    last_signals[coin] = signal


# Create a background task that runs every 15 minutes
@tasks.loop(minutes=2)
async def signal_task():
    await send_signals()




def fetch_prices(coins):
    """Fetch the prices for multiple coins from CoinMarketCap."""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }
    parameters = {
        "symbol": ','.join(coins),
        "convert": "USD"
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()['data']
        prices = {coin: float(data[coin]['quote']['USD']['price']) for coin in coins}
        logger.info(f"Prices: {prices}")
        return prices
    except Exception as e:
        logger.error(f"Could not fetch prices: {e}")
        return None


def check_levels(coin, levels, price):
    """Check if the price is near a DCA or profit level."""
    logger.info(f"Checking levels for {coin} at {price}")
    level_hits = {}
    for level_type, level_values in levels.items():
        for level in level_values:
            if (1 - near_percentage) * level <= price <= (1 + near_percentage) * level:
                level_hits[level_type] = level
    return level_hits if level_hits else None


async def generate_dca_response():
    """Generate the DCA response."""
    logger.info("Generating DCA response")

    # Initialize dictionaries to store coins that hit each level
    dca_hits = {}
    target_hits = {}
    bullrun_hits = {}

    try:
        prices = fetch_prices(coins.keys())
        if prices is not None:
            for coin, levels in coins.items():
                price = prices.get(coin)
                if price is not None:
                    result = check_levels(coin, levels, price)

                    # Check which level was hit and add to the appropriate dictionary
                    if result:
                        if 'DCA' in result:
                            dca_hits[coin] = result['DCA']
                        if 'Target' in result:
                            target_hits[coin] = result['Target']
                        if 'BullRunTarget' in result:
                            bullrun_hits[coin] = result['BullRunTarget']

                else:
                    response = f"Could not fetch price for {coin}.\n"

        # Add DCA hits to the response
        if dca_hits:
            response = "**DCA Targets Hit On These Coins:**\n"
            for coin, info in dca_hits.items():
                response += f"{coin} Hit a DCA Level: {info}\n"

        # Add Target hits to the response
        if target_hits:
            response = "\nProfit Target Hit On These Coins:\n"
            for coin, info in target_hits.items():
                response += f"{coin} Hit a Target Level: {info}\n"

        # Add BullRunTarget hits to the response
        if bullrun_hits:
            response = "\nBull Run Target Hit On These Coins:\n"
            for coin, info in bullrun_hits.items():
                response += f"{coin} Hit a Bull Run Target Level: {info}\n"

        return response
    except Exception as e:
        logger.error(f"Could not generate DCA response: {info}\n")
        return None





@bot.slash_command(description="Get coins that are near a level.")
async def dca(ctx):
    # Defer the response as soon as possible
    await ctx.response.defer()
    # Then do the slow operations
    response = await generate_dca_response()
    embed = disnake.Embed(title="Levels Update", description=response, color=disnake.Color.blue())
    # Edit the deferred response
    await ctx.edit_original_message(embed=embed)



@bot.slash_command(description="Ping the bot for latency.")
async def ping(ctx):
# pong back with the latency
    await ctx.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')



@bot.slash_command(description="Set the channel for the bot to send messages in.")
async def set_channel(ctx: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
    # Defer the response as soon as possible
    await ctx.response.defer()
    # Then do the slow operations
    global channel_id
    channel_id = channel.id
    with open('channel.json', 'w') as f:
        json.dump({'channel_id': channel_id}, f)
    await ctx.edit_original_message(content=f"Channel set to {channel.id}.")
    # Send a test message to the specified channel
    await channel.send("Channel set.")


bot.run(TOKEN)

