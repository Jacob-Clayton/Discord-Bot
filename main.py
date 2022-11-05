import os
import discord
import requests
import json

client = discord.Client(intents=discord.Intents.default())


#Get nice quote from api and concatenate response with quote author
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


#Insert private discord channel token
my_secret = os.environ['token']


#Bot logged in and working message
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


#Read !wiki and return link
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == '!wiki':
    await message.channel.send('https://wiki.apegang.art/')


#Send inspirational quote when !inspire is typed
@client.event
async def on_message(message):
  if message.content == '!inspire':
    quote = get_quote()
    await message.channel.send(quote)

client.run(os.getenv('token'))
