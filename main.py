#Import packages
import discord
import requests
import json
import asyncio
import os
#from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import Bot, Context

#.env file to safely assign the token value
#load_dotenv('.env')
#token = os.getenv('TOKEN')

#Allow intents so the bot can access all features
intents = discord.Intents.all()

#Setup bot prefix
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#Private discord channel token. Move this to a .env file when going live to hide the token
token = ('Enter Token Here')


#-------------------------------------Events----------------------------------------

#Bot status messages [Connected - Ready - Resumed - Disconected]
@bot.event
async def on_connect():
  print('Bot has connected to Discord')

#Get the info/ rules channel id here too
@bot.event
async def on_ready():
  print('Bot is ready')
  for guild in bot.guilds:
    for channel in guild.text_channels:
      if str(channel).strip() == 'info':
        #id of the channel I have set up as info/ rules channel
        global verify_channel_id
        verify_channel_id = channel.id
        break

@bot.event
async def on_resume():
  print('Bot resumed')

@bot.event
async def on_disconnect():
  print('Bot has disconnected from Discord')


#Verify user when a green tick reaction is added to a message
@bot.event
async def on_raw_reaction_add(reaction):
  #Check if the reaction came from the correct channel
  if reaction.channel_id == verify_channel_id:
    #Check what emoji was reacted as
    if str(reaction.emoji) == '✅':
      #Add user role
      verified_role = get(reaction.member.guild.roles, name = 'Verified')
      await reaction.member.add_roles(verified_role)
      await reaction.member.send(f'Welcome to Bridgr {reaction.member.name}, you are now verified.')


#Get quotes from API and concatenate response with quote author
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)


#Send inspirational quote when a user types !inspire
@bot.event
async def on_message(message):
  if message.content == '!inspire':
    quote = get_quote()
    await message.channel.send(quote)

#Return an embeded message with a link to the Ape Gang Wiki when a user types '!wiki'
@bot.event
async def on_message(message):
    if message.content == '!wiki':
        embedVar = discord.Embed(title="Ape Gang Wiki", url='https://wiki.apegang.art', description="The official resource", color=0x2f3136)
        await message.channel.send(embed=embedVar)


bot.run(token)
