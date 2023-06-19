import disnake
from disnake.ext import commands
import requests
import json
from config.settings import X_RAPIDAPI_KEY

# Embed comand handler class
# Create a new Embed object from the user's input
# Send the embed to the channel
# Also get color and other options from the user's input

# different commands
# /embed create title|description|color
# /embed create title|description
# /embed create title
# /embed edit <message_id> title|description|color
# /embed edit <message_id> title|description
# /embed edit <message_id> title
# /embed delete <message_id>
# /embed view <message_id>

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

class EditEmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='edit', help='Edits an embed from the user\'s input.')
    async def edit_embed(self, ctx, message_id, *, args):
        # Split the user's input into a list
        args = args.split('|')

        # Get the message object
        message = await ctx.fetch_message(message_id)

        # Create the embed
        embed = disnake.Embed(title=args[0], description=args[1], color=0x3498db)

        # Edit the message
        await message.edit(embed=embed)


class DeleteEmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete', help='Deletes an embed from the user\'s input.')
    async def delete_embed(self, ctx, message_id):
        # Get the message object
        message = await ctx.fetch_message(message_id)

        # Delete the message
        await message.delete()

class ViewEmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='view', help='Views an embed from the user\'s input.')
    async def view_embed(self, ctx, message_id):
        # Get the message object
        message = await ctx.fetch_message(message_id)

        # Get the embed
        embed = message.embeds[0]

        # Send the embed
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CreateEmbedCog(bot))
    bot.add_cog(EditEmbedCog(bot))
    bot.add_cog(DeleteEmbedCog(bot))
    bot.add_cog(ViewEmbedCog(bot))

