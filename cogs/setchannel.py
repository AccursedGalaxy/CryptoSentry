# cogs/setchannel.py
import json
import disnake
from disnake.ext import commands

class SetChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Set the channel for the signals.")
    async def set_channel(self, ctx: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        # Defer the response as soon as possible
        await ctx.response.defer()
        # Then do the slow operations
        self.bot.channel_id = channel.id
        with open('channel.json', 'w') as f:
            json.dump({'channel_id': self.bot.channel_id}, f)
        await ctx.edit_original_message(content=f"Channel set to {channel.id}.")
        # Send a test message to the specified channel
        await channel.send("Channel set.")
        # Start the signal_task if it's not already running
        if not self.bot.get_cog('DCACog').signal_task.is_running():
            self.bot.get_cog('DCACog').signal_task.start()

    @commands.slash_command(description="View the current channel setup for signals")
    async def view_channel(self, ctx: disnake.ApplicationCommandInteraction):
        # Defer the response as soon as possible
        await ctx.response.defer()
        # Then do the slow operations
        await ctx.edit_original_message(content=f"Channel set to {self.bot.channel_id}.")

def setup(bot):
    bot.add_cog(SetChannelCog(bot))

