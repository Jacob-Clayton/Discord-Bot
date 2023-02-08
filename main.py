#Import packages
import discord
import requests
import json
import asyncio
import os
import random
#from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import Bot, Context

#.env file to safely assign the token value (uncomment two lines below to set up .env)
#load_dotenv('.env')
#token = os.getenv('TOKEN')

#Allow all intents so the bot can access all features
intents = discord.Intents.all()

#Setup command bot prefix
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=intents)

#Private discord channel token. Move this to a .env file when going live to hide the token
token = ('MTAzODE0NjY1MzcyODgwOTEzMQ.GnnAxA.9HgZBvkXsgmNaZRrlHYrQWt62IUj_q_R2rSPCQ') #this token is expired, don't get too excited :)


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

#Sad words + Encouragements
sad_words = ['sad', 'depressed', 'lonely', 'kms', 'depressing', 'miserable', 'i feel shit', 'i feel like shit']
encouragements = ['Cheer up!', 'You are a great person', 'You are part of the family!', 'You always have the community to talk to :)', 'Hang in there']


#Get quotes from API and concatenate quote + author
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return (quote)


#Send uplifting quote when a user types !inspire
@bot.event
async def on_message(message):
  msg = message.content
  if msg == '!inspire':
    quote = get_quote()
    #embedQ = discord.Embed(title=(quote), color=0x2f3136)
    await message.channel.send(quote)
  
  #Send random message of encouragement if bot detects a sad word
  if any (word in msg for word in sad_words):
    await msg.channel.send(random.choice(encouragements))


#Return an embeded message with a link to the Ape Gang Wiki when a user types '!wiki'
@bot.event
async def on_message(message):
  if message.content == '!wiki':
    embedVar = discord.Embed(title="Ape Gang Wiki", url='https://wiki.apegang.art', description="The official AG resource", color=0x2f3136)
    await message.channel.send(embed=embedVar)


bot.run(token)
