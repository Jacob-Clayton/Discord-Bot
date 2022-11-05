#Discord Bot
import os
import discord
from discord.ext import commands, tasks

bot = commands.Bot(commands_prefix='!')


@bot.command()
async def wiki(ctx):
  await ctx.send('https://wiki.apegang.art/')


my_secret = os.getenv('token')
bot.run(my_secret)
