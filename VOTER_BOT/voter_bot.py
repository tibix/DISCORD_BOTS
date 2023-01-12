# create a bot that can take in feature requests, store them in a database, and allow users to vote on them. The bot should also be able to display the top 10 feature requests, and the top 10 feature requests that have the most votes.

import discord
from discord.ext import commands
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.presences = True
intents.members = True

BOT_PREFIX = ("!")
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

TOKEN = 'TO_BE_ADDEDE'

# log to the console when bot is logged in
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def feature_request(ctx, *, feature):
    await ctx.send(f"Feature request {feature} received!")
    
