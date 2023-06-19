import disnake
from disnake.ext import commands
import requests
import json
from config.settings import X_RAPIDAPI_KEY

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="Get the global crypto stats.")
    async def stats(self, ctx):
        # Defer the response as soon as possible
        await ctx.response.defer()
        # Then do the slow operations
        response = await self.generate_stats_response()
        embed = disnake.Embed(title="Global Crypto Stats", description=response, color=disnake.Color.blue())
        # Edit the deferred response
        await ctx.edit_original_message(embed=embed)

    async def generate_stats_response(self):
        """Generate the response for the DCA command."""
        url = "https://coinranking1.p.rapidapi.com/stats"
        querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}
        headers = {
            "X-RapidAPI-Key": X_RAPIDAPI_KEY,
            "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()['data']
        # send as embed
        # format numbers with commas and decimals
        total_coins = "{:,}".format(data['totalCoins'])
        total_markets = "{:,}".format(data['totalMarkets'])
        total_exchanges = "{:,}".format(data['totalExchanges'])
        total_market_cap = "{:,}".format(int(data['totalMarketCap']))
        total_24h_volume = "{:,}".format(int(data['total24hVolume']))
        btc_dominance = "{:.2f}".format(data['btcDominance'])
        # format best coins
        best_coins = ""
        for coin in data['bestCoins']:
            best_coins += f"{coin['name']} ({coin['symbol']})\n"
        # format newest coins
        newest_coins = ""
        for coin in data['newestCoins']:
            newest_coins += f"{coin['name']} ({coin['symbol']})\n"
        # format response
        response = f"""
        **Total Coins:** {total_coins}
        **Total Markets:** {total_markets}
        **Total Exchanges:** {total_exchanges}
        **Total Market Cap:** ${total_market_cap}
        **Total 24h Volume:** ${total_24h_volume}\n
        **BTC Dominance:** {btc_dominance}%\n
        **Best Coins:**\n {best_coins}
        **Newest Coins:**\n {newest_coins}
        """
        return response



def setup(bot):
    bot.add_cog(InfoCog(bot))


