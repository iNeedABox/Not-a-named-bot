import discord
import datetime
from discord.utils import utcnow
import requests
import os
from colorama import Fore, Style
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

key = os.getenv('DISCORD_TOKEN')

if key is None:
    raise ValueError('Discord Token doesnt exist.')

URL = 'http://127.0.0.1:5000'

response = requests.get(URL)

if response.status_code == 200:
    slurs = response.json()
    slur_glosary = slurs
else:
    print("Error while requesting API ", response.status_code)
    slur_glosary = []

async def time_out_last_resource(message):
    mute_role = discord.utils.get(message.guild.roles, name='Muted')

    if mute_role is None:
        mute_role = await message.guild.create_role(name='Muted')

        for channel in message.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)
                    
    await message.author.add_roles(mute_role)

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f"Message from {message.author}: {message.content}")

        for i in slurs:
            if message.content == i:
                print(f"Slur from {Fore.GREEN}{message.author}{Fore.RESET}: {Fore.RED}{message.content}{Style.RESET_ALL}")

        if message.content.startswith(':img'):
            graph_file_path = 'C:\\Users\\pajd4\\Documents\\Proyecto Madlass\\Assets\\descarga.jpg'

            if os.path.exists(graph_file_path):
                
                await message.channel.send("Funny image lol: ", file=discord.File(graph_file_path))
            else:
                await message.channel.send(f"No image found, {message.author}")
        
        for slur in slur_glosary:
            if message.content == slur:

                time_end = datetime.timedelta(seconds=20)

                try:
                    await message.author.timeout(time_end)
                except discord.Forbidden:
                    await time_out_last_resource(message)
                except discord.HTTPException as e:
                    await time_out_last_resource(message)

                if message.author.timed_out_until:
                    embed = discord.Embed(
                        title="Time Out",
                        description=f"{message.author.id} was timed out for saying **{message.content}**!",
                        color=discord.Color.red()
                    )
                    await message.channel.send(embed=embed)

        if message.content.startswith(':shutdown') and message.author.id == 1320119829142966272:
            await message.channel.send('Restarting...')
            await client.close()
            raise Exception('Restarting...')
            pass

client = Client(intents=intents)
client.run(key)