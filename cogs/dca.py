# cogs/dca.py
import disnake
import requests
from disnake.ext import commands, tasks
from config.settings import CMC_API_KEY
from config.setup import coins, near_percentage
import os  # Added for environment variable usage


class DCACog(commands.Cog):
    """A cog that handles DCA signals."""

    def __init__(self, bot):
        self.bot = bot
        self.last_signals = {}

    @tasks.loop(minutes=15)
    async def signal_task(self):
        """A task that runs every 15 minutes to send signals."""
        await self.send_signals()

    async def send_signals(self):
        """Send signals if the channel_id is set and the channel exists."""
        # Get the channel
        channel = self.bot.get_channel(self.bot.channel_id)
        # Only send signals if the channel_id is set and the channel exists
        if self.bot.channel_id is not None and channel is not None:
            # Generate the DCA response
            response = await self.generate_dca_response()
            # Split the response into lines
            lines = response.split("\n")
            # Iterate over the lines
            for i in range(2, len(lines)):
                # Check if ' Hit a ' is in the line
                if " Hit a " in lines[i]:
                    # Get the coin and the signal
                    coin, signal = lines[i].split(" Hit a ")
                    # If the signal is different from the last one, send it
                    if self.last_signals.get(coin) != signal:
                        # Create an embed message
                        embed = disnake.Embed(
                            title=f"Signal for {coin}",
                            description=f"{coin} has hit a {signal}",
                            color=disnake.Color.green()
                            if "DCA Level" in signal
                            else disnake.Color.red(),
                        )
                        await channel.send(embed=embed)
                        # Update the last signal
                        self.last_signals[coin] = signal

    @commands.slash_command(description="Get coins that are near a level.")
    async def dca(self, ctx):
        """Handle the '/dca' command."""
        # Defer the response as soon as possible
        await ctx.response.defer()
        # Then do the slow operations
        response = await self.generate_dca_response()
        embed = disnake.Embed(
            title="Levels Update", description=response, color=disnake.Color.blue()
        )
        # Edit the deferred response
        await ctx.edit_original_message(embed=embed)

    def fetch_prices(self, coins):
        """Fetch the prices for multiple coins from CoinMarketCap."""
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": os.getenv("CMC_API_KEY"),  # Use environment variable
        }
        parameters = {"symbol": ",".join(coins), "convert": "USD"}
        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()["data"]
            prices = {
                coin: float(data[coin]["quote"]["USD"]["price"]) for coin in coins
            }
            return prices
        except requests.exceptions.RequestException as e:  # More specific exception
            print(f"Error occurred: {e}")
            return None

    def check_levels(self, coin, levels, price):
        """Check if the price is near a DCA or profit level."""
        level_hits = {}
        for level_type, level_values in levels.items():
            for level in level_values:
                if (
                    (1 - near_percentage) * level
                    <= price
                    <= (1 + near_percentage) * level
                ):
                    level_hits[level_type] = level
        return level_hits if level_hits else None

    async def generate_dca_response(self):
        """Generate the DCA response."""
        # Initialize dictionaries to store coins that hit each level
        dca_hits = {}
        target_hits = {}
        bullrun_hits = {}

        try:
            prices = self.fetch_prices(coins.keys())
            if prices is not None:
                for coin, levels in coins.items():
                    price = prices.get(coin)
                    if price is not None:
                        result = self.check_levels(coin, levels, price)

                        # Check which level was hit and add to the appropriate dictionary
                        if result:
                            if "DCA" in result:
                                dca_hits[coin] = result["DCA"]
                            if "Target" in result:
                                target_hits[coin] = result["Target"]
                            if "BullRunTarget" in result:
                                bullrun_hits[coin] = result["BullRunTarget"]

            # Add DCA hits to the response
            response = ""
            if dca_hits:
                response += "**DCA Targets Hit On These Coins:**\n"
                for coin, info in dca_hits.items():
                    response += f"{coin} Hit a DCA Level: {info}\n"

            # Add Target hits to the response
            if target_hits:
                response += "\nProfit Target Hit On These Coins:\n"
                for coin, info in target_hits.items():
                    response += f"{coin} Hit a Target Level: {info}\n"

            # Add BullRunTarget hits to the response
            if bullrun_hits:
                response += "\nBull Run Target Hit On These Coins:\n"
                for coin, info in bullrun_hits.items():
                    response += f"{coin} Hit a Bull Run Target Level: {info}\n"

            return response
        except Exception as e:
            print(f"Error occurred: {e}")  # Print the error message
            return None


def setup(bot):
    """Add the DCACog to the bot."""
    bot.add_cog(DCACog(bot))
