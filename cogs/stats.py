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
        return f"Total Coins: {data['totalCoins']}\nTotal Markets: {data['totalMarkets']}\nTotal Exchanges: {data['totalExchanges']}\nTotal Market Cap: {data['totalMarketCap']}\nTotal 24h Volume: {data['total24hVolume']}\nBTC Dominance: {data['btcDominance']}"


def setup(bot):
    bot.add_cog(InfoCog(bot))

# import requests

# url = "https://coinranking1.p.rapidapi.com/stats"

# querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

# headers = {
# 	"X-RapidAPI-Key": "d272cbb83emshafd80a0ad2aebbfp1e6fa8jsne11ab7615f57",
# 	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# {
#   "status": "success",
#   "data": {
#     "referenceCurrencyRate": 1,
#     "totalCoins": 26551,
#     "totalMarkets": 36198,
#     "totalExchanges": 162,
#     "totalMarketCap": "1066266148534",
#     "total24hVolume": "21903993683",
#     "btcDominance": 47.64691898420519,
#     "bestCoins": [
#       {
#         "uuid": "OmNBhJZXb",
#         "symbol": "LYXE",
#         "name": "LUKSO Token",
#         "iconUrl": "https://cdn.coinranking.com/fx00fqI63/LUKSO.png",
#         "coinrankingUrl": "https://coinranking.com/coin/OmNBhJZXb+luksotoken-lyxe"
#       },
#       {
#         "uuid": "NfeOYfNcl",
#         "symbol": "FTT",
#         "name": "FTX Token",
#         "iconUrl": "https://cdn.coinranking.com/WyBm4_EzM/ftx-exchange.svg",
#         "coinrankingUrl": "https://coinranking.com/coin/NfeOYfNcl+ftxtoken-ftt"
#       },
#       {
#         "uuid": "Hm3OlynlC",
#         "symbol": "TWT",
#         "name": "Trust Wallet Token",
#         "iconUrl": "https://cdn.coinranking.com/cZ5j4jiOk/trust-wallet-token.svg",
#         "coinrankingUrl": "https://coinranking.com/coin/Hm3OlynlC+trustwallettoken-twt"
#       }
#     ],
#     "newestCoins": [
#       {
#         "uuid": "qzJ8ZzTOx",
#         "symbol": "AI",
#         "name": "AiDoge",
#         "iconUrl": "https://cdn.coinranking.com/z3GlZbEDa/K0a_Qyot_400x400.PNG",
#         "coinrankingUrl": "https://coinranking.com/coin/qzJ8ZzTOx+aidoge-ai"
#       },
#       {
#         "uuid": "udQY9DoxDk",
#         "symbol": "SAW",
#         "name": "SAW",
#         "iconUrl": "https://cdn.coinranking.com/NfucOpRP2/1_20230615013144.PNG",
#         "coinrankingUrl": "https://coinranking.com/coin/udQY9DoxDk+saw-saw"
#       },
#       {
#         "uuid": "g2I6Dp3et",
#         "symbol": "BM",
#         "name": "Bullishman",
#         "iconUrl": "https://cdn.coinranking.com/Rg6vW4QjX/1_20230615013658.PNG",
#         "coinrankingUrl": "https://coinranking.com/coin/g2I6Dp3et+bullishman-bm"
#       }
#     ]
#   }
# }
