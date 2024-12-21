from gtts import gTTS; import discord; from discord.ext import commands; import asyncio; import os


#perms
intents=discord.Intents.default()
intents.message_content = True  

bot=commands.Bot(command_prefix='!', intents=intents)

TARGET_VC_NAME="VOICE CHANNEL"                      #name of VC to join
TARGET_TEXT_CHANNEL_NAME="TEXT CHANNEL"     #name of chat to read

@bot.event
async def on_ready():
    print('Logged in')
    for guild in bot.guilds:
        print(f'Connected to {guild.name}')

@bot.event
async def on_message(message):
    if message.channel.name == TARGET_TEXT_CHANNEL_NAME:
        
        #find target VC
        for channel in message.guild.channels:
            if channel.name == TARGET_VC_NAME and channel.type == discord.ChannelType.voice:
                #connect to VS if not already
                voice_client = discord.utils.get(bot.voice_clients, guild=message.guild)
                if not voice_client or not voice_client.channel:
                    voice_client = await channel.connect()

                #save tts
                tts = gTTS(text=message.content, lang='en', slow=False)
                tts.save("tts_message.mp3")

                #play tts
                audio_source = discord.FFmpegPCMAudio("tts_message.mp3")
                voice_client.play(audio_source)

                #delay a sec
                while voice_client.is_playing():
                    await asyncio.sleep(1)

bot.run('TOKEN') #replace with your bot token