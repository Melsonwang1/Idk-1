import discord
import os 
import requests
from discord import FFmpegPCMAudio
import json
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")



status = cycle (["idk", "hello",  "hows your day"])

@client.event
async def on_ready():
   change_status.start()
   print("bot is ready")
    
@tasks.loop(minutes=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
  

  
   
@client.event
async def on_member_join(member):
    print(f'{member} have joined a server')
    
@client.event
async def on_member_remove(member):
    print(f'{member}have left the server')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("hey,this command does not work sry")
  


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
  await ctx.channel.purge(limit=amount)
  
@clear.error
async def clear_error(ctx, error):
   if isinstance (error, commands.MissingRequiredArgument):
    await ctx.send("pls specify the amount of messages you want to delete")

def is_it_me(ctx):
  return ctx.author.id == 846240977806295080

@client.command()
@commands.check(is_it_me)
async def example(ctx):
  await ctx.send(f"hi im {ctx.author}")
    
  
@client.command()
async def kick(ctx , member : discord.Member, *, reason=None ):
  await member.kick(reason=reason)
  await ctx.send(f'you have been kicked{member.mention}')

@client.command()
async def ban(ctx , member : discord.Member, *, reason=None ):
  await member.ban(reason=reason)
  await ctx.send(f'you have been banned{member.mention}')

@client.command()
async def unban(ctx , *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
  
    for ban_entry in banned_users:
      user = ban_entry.user
    
    
    if(user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'you have been unbanned{user.name}#{user.discriminator}')
      return
  
@client.command()
async def load(ctx , extension):
  client.load_extension(f'Cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'Cogs.{extension}')
    


for filename in os.listdir("./Cogs"):
  if filename.endswith('.py'):
    client.load_extension(f"Cogs.{filename[:-3]}")
    

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
      channel = ctx.message.author.voice.channel
      await channel.connect()
      source = FFmpegPCMAudio("song.mp3")
      player = voice.play(source)
   
    else:
      await ctx.send('you are not in a voice channel')

@client.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):
      await ctx.guild.voice_client.disconnect()
      await ctx.send("i left the voice channel")
    else:
      await ctx.send("i am not inside a voice channel")


@client.command(pass_context = True)
async def play(ctx, url:str):
  if(ctx.author.voice):
      channel = ctx.message.author.voice.channel
      voice = await channel.connect()
      ydl_opts = {
     'format':'bestaudio/best',
      'postprocesses': [{
        'key' : "FFmpegExtractAudio", 
        'preferedcodec' : "mp3", 
        'preferredquality': "192"
      }],
    }
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
       ydl.download([url])
      for file in os.listdir("./"):
        if file.endswith(".mp3"):
          os.rename(file, "song.mp3")
      source = FFmpegPCMAudio("song.mp3")
      player = voice.play(source)
  else:
      await ctx.send('you are not in a voice channel')





client.run("ODgyMjExODMzNzc4NDM0MDU5.YS4Fyw.t5tniWTyqjWJqUgf9KSo4EWx9-s")      
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
client.run(os.getenv('TOKEN'))






