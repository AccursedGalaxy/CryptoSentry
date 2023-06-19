import requests
import json
import disnake
from disnake.ext import commands
from config.settings import X_RAPIDAPI_KEY


class TradingViewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tradingview', help='Fetches the latest popular ideas for Bitcoin trading from TradingView.')
    async def fetch_tradingview_ideas(self, ctx):
        url = "https://trading-view.p.rapidapi.com/ideas/list"
        querystring = {"page":"1","per_page":"5","category":"popular","sort":"latest_popular","market":"bitcoin","stock_country":"us","locale":"en"}
        headers = {
            "X-RapidAPI-Key": "X_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "trading-view.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        embed = disnake.Embed(title="Latest Popular Bitcoin Trading Ideas", description="Here are the latest popular ideas for Bitcoin trading from TradingView:", color=0x3498db)

        for idea in data['results']:
            embed.add_field(name=idea['name'], value=f"[Read More]({idea['chart_url']})", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TradingViewCog(bot))
