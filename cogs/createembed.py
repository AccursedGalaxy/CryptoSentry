import disnake
from disnake.ext import commands

# Embed comand handler
# Create a new Embed object from the user's input
# Send the embed to the channel
# Also get color and other options from the user's input

class CreateEmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='embed', help='Creates an embed from the user\'s input.')
    async def create_embed(self, ctx, *, args):
        # Split the user's input into a list
        args = args.split('|')

        # Create the embed
        embed = disnake.Embed(title=args[0], description=args[1], color=0x3498db)

        # Send the embed
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(CreateEmbedCog(bot))
