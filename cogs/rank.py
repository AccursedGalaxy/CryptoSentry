import disnake
import requests
from disnake.ext import commands

class RankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get the market cap rank of a coin.")
    async def rank(self, ctx, coin: str):
        # Defer the response as soon as possible
        await ctx.response.defer()

        # Fetch the coin data from Coinranking API
        coin_data = self.fetch_coin_data(coin)

        # Check if the API returned data
        if coin_data:
            rank = coin_data['rank']
            embed = disnake.Embed(title=f"Rank of {coin}", description=f"{coin} is currently ranked {rank} by market cap.", color=disnake.Color.blue())
        else:
            embed = disnake.Embed(title=f"Error", description=f"Could not fetch data for {coin}.", color=disnake.Color.red())

        # Edit the deferred response
        await ctx.edit_original_message(embed=embed)

    def fetch_coin_data(self, coin):
        """Fetch the data for a coin from Coinranking API."""
        url = f"https://api.coinranking.com/v2/coin/{coin}"
        headers = {
            "Accepts": "application/json",
            "X-Coinranking-API-Key": "YOUR_COINRANKING_API_KEY",
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()['data']['coin']
            return data
        except Exception as e:
            return None

def setup(bot):
    bot.add_cog(RankCog(bot))

