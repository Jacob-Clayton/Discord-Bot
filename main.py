#Import packages
import discord
import requests
import json
from discord.ext import commands
from discord import Intents

#Create discord client, set prefix and store in variable
bot = commands.Bot(command_prefix = '!', intents=Intents.all())

#Private discord channel token
token = ('Insert token here')

#Bot status messages [Connected - Ready - Resumed - Disconected]
@bot.event
async def on_connect():
  print('Bot has connected to Discord')

@bot.event
async def on_ready():
  print('Bot is ready')

@bot.event
async def on_resume():
  print('Bot resumed')

@bot.event
async def on_disconnect():
  print('Bot has disconnected from Discord')


#---Wiki embeded message response in any channel---
@bot.command(name = 'wiki')
#Context = whichever channel the message is sent
async def wiki(context):
#Embed message creation
  myEmbed = discord.Embed(
  title='Ape Gang Wiki', 
  description='https://wiki.apegang.art/', 
  colour='2f3136')
  myEmbed.add_field(name='Updated', value='Nov 5th',inline=False)
#Send embeded wiki message  
  await context.message.channel.send(embed=myEmbed)

#Read !wiki and return link
@bot.event
async def on_message(message):
  if message.content == 'hi':
    general_channel = bot.get_channel(1034442573617573941)
    await general_channel.send('Hello')
  await bot.process_commands(message)

#Send embeded message
@bot.event
async def on_message(msg):
  if msg.content == 'help':
    general_channel = bot.get_channel(1034442573617573941)

    myEmbed = discord.Embed(
      title='Ape Gang Wiki', 
      description='https://wiki.apegang.art/',
      colour='2f3136')
    myEmbed.add_field(name='Updated', value='Nov 5th',inline=False)

    await general_channel.send(embed=myEmbed)


#Get nice quote from api and concatenate response with quote author
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


#Send inspirational quote when !inspire is typed
@bot.event
async def on_message(message):
  if message.content == '!inspire':
    quote = get_quote()
    await message.channel.send(quote)


bot.run(token)
