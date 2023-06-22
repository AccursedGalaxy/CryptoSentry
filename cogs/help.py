import disnake
from disnake.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Display the help message.")
    async def help(self, ctx):
        embed = disnake.Embed(
            title="Help",
            description="You can use commands by typing / followed by the comamnd.",
            color=disnake.Color.blue(),
        )
        embed.add_field(
            name="dca", value="Get coins that are near a level.", inline=False
        )
        embed.add_field(name="help", value="Get this message.", inline=False)

        # add another embed for information about the server
        embed2 = disnake.Embed(
            title="Server Information",
            description="Information about the server",
            color=disnake.Color.blue(),
        )
        embed2.add_field(name="Server Name", value=ctx.guild.name, inline=False)
        embed2.add_field(name="Server Owner", value=ctx.guild.owner, inline=False)
        embed2.add_field(
            name="Server Created", value=ctx.guild.created_at, inline=False
        )
        embed2.add_field(
            name="Server Members", value=ctx.guild.member_count, inline=False
        )
        embed2.add_field(
            name="Website", value="https://www.fitzocrypto.com", inline=False
        )

        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Help(bot))
