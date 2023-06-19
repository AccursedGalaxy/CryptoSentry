import disnake
from disnake.ext import commands
import requests
import json
from config.settings import X_RAPIDAPI_KEY

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get detailed information about a specific cryptocurrency.")
    async def info(self, inter: disnake.ApplicationCommandInteraction, coin_name: str):
        coin_info = self.fetch_coin_info(coin_name)
        if coin_info is None:
            await inter.response.send_message(f"Could not find a cryptocurrency with the name {coin_name}.")
            return

        # Format and send the information as a message
        embed = self.format_info_message(coin_info)
        await inter.response.send_message(embed=embed)

    def fetch_coin_info(self, coin_name):
        url = "https://coinranking1.p.rapidapi.com/coins"
        headers = {
            "X-RapidAPI-Key": X_RAPIDAPI_KEY,
            "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        coins = response.json()["data"]["coins"]
        for coin in coins:
            if coin["name"].lower() == coin_name.lower():
                return coin

        return None

    def format_info_message(self, coin_info):
        # Format the information about the coin into an embed
        embed = disnake.Embed(title=f"{coin_info['name']} ({coin_info['symbol']})", color=0x3498db)
        embed.description = coin_info['description']
        embed.add_field(name="Price", value=coin_info['price'], inline=True)
        embed.add_field(name="Market Cap", value=coin_info['marketCap'], inline=True)
        embed.add_field(name="24h Volume", value=coin_info['24hVolume'], inline=True)
        embed.add_field(name="Change (24h)", value=f"{coin_info['change']}%", inline=True)
        embed.add_field(name="Rank", value=coin_info['rank'], inline=True)
        embed.add_field(name="Website", value=coin_info['websiteUrl'], inline=True)
        embed.set_thumbnail(url=coin_info['iconUrl'])
        return embed

def setup(bot):
    bot.add_cog(InfoCog(bot))

