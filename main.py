import os
import discord 
from discord.ext import commands, tasks
import requests
import random
import datetime as dt
from sub_compare import get_subcount
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN =  os.environ.get("BOT_TOKEN")

url1 = 'https://www.youtube.com/@SeanCityNavy'
url2 = 'https://www.youtube.com/@clubpenguin_radio'

intents = discord.Intents.all()
intents.message_content = True
intents.typing = True
intents.presences = True
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)
utc = dt.timezone.utc
time = dt.time(hour=19, minute=00, tzinfo=utc)

@bot.command(name='compare', help='Compares sean\'s subcount with emote\'s subcount')
async def compare(ctx):
  sean_subcount = get_subcount(url1)
  emote_subcount = get_subcount(url2)
  await ctx.send(f'Sean currently has {sean_subcount}, and emote currently has {emote_subcount}')

@bot.command(name='quran', help='Displays a quote from the quran, bismillah')
async def send_quran_quote(ctx):
  response = requests.get('https://api.alquran.cloud/v1/quran/en.asad')
  response.raise_for_status()
  text = response.json()
  quote = text['data']['surahs'][random.randint(0, 20)]['ayahs'][random.randint(0,
                                                                  20)]['text']
  await ctx.send(quote)

@bot.event
async def on_presence_update(before, after):
    guild_id = int(os.getenv('GUILD_ID')) 
    if after.guild.id != int(guild_id):
        return
    if isinstance(after.activity, discord.Spotify):
       channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
       try:
         embed = discord.Embed(title=f"{after.name}'s Spotify",
                                description=f"Listening to {after.activity.title} by {after.activity.artist}",
                                color=0x1db954)
         embed.set_thumbnail(url=after.activity.album_cover_url)
         if after.activity.title != before.activity.title:
          await channel.send(embed=embed)
         else: 
           return 
       except discord.HTTPException as e:
         print(f"Error sending message: {e}")

@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
    f'Hey CUNT! Welcome to the server {member.mention}')
  
@tasks.loop(time=time)
async def its_friday_night():
  current_day = dt.datetime.now().weekday()
  if current_day == 5:
    channel = bot.get_channel(os.getenv('ANNOUNCEMENTS_CHANNEL'))
    await channel.send(
'https://cdn.discordapp.com/attachments/874254207958528000/1000146177951535194/FridayNight.mp4'
    )

if __name__ == '__main__':
  @bot.event
  async def on_ready():
    try:
      channel = bot.get_channel(os.getenv('TESTING_CHANNEL_ID'))
      print(f'Logged in as {bot.user.name}')
      await bot.change_presence(status=discord.Status.online,
                                activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name='you sleep'))
      its_friday_night.start()
    except Exception as e:
      await channel.send(f"Yo dumbass! {e}")

  bot.run(BOT_TOKEN)
