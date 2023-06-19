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
        coin_id = self.fetch_coin_id(coin_name)
        if coin_id is None:
            await inter.response.send_message(f"Could not find a cryptocurrency with the name {coin_name}.")
            return

        coin_info = self.fetch_coin_info(coin_id)
        if coin_info is None:
            await inter.response.send_message(f"Could not fetch information for the cryptocurrency {coin_name}.")
            return

        # Format and send the information as a message
        info_message = self.format_info_message(coin_info)
        await inter.response.send_message(info_message)

    def fetch_coin_id(self, coin_name):
        url = "https://coinranking1.p.rapidapi.com/coins"
        headers = {
            "X-RapidAPI-Key": "X_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        coins = response.json()["data"]["coins"]
        for coin in coins:
            if coin["name"].lower() == coin_name.lower():
                return coin["uuid"]

        return None

    def fetch_coin_info(self, coin_id):
        url = f"https://coinranking1.p.rapidapi.com/coin/{coin_id}"
        headers = {
            "X-RapidAPI-Key": "X_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        return response.json()["data"]["coin"]

    def format_info_message(self, coin_info):
        # Format the information about the coin into a string
        info_message = f"**{coin_info['name']} ({coin_info['symbol']})**\n"
        info_message += f"Description: {coin_info['description']}\n"
        info_message += f"Price: {coin_info['price']}\n"
        info_message += f"Market Cap: {coin_info['marketCap']}\n"
        info_message += f"24h Volume: {coin_info['24hVolume']}\n"
        info_message += f"Change (24h): {coin_info['change']}%\n"
        info_message += f"Rank: {coin_info['rank']}\n"
        info_message += f"Website: {coin_info['websiteUrl']}\n"
        return info_message

def setup(bot):
    bot.add_cog(InfoCog(bot))

