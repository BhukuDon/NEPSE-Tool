import discord
import requests
import threading
import asyncio
from lib.scripts.static import _Config
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send(f'Pong! In {round(self.latency * 1000)}ms')
            
            try :
                nepsealpha = requests.get("https://nepsealpha.com/")
                await message.channel.send(f'Nepsealpha! In {round(nepsealpha.elapsed.total_seconds() * 1000)}ms')
                pass
            except:
                await message.channel.send(f'Nepsealpha! In Failed')
                pass
            try :
                nepalstock = requests.get("http://www.nepalstock.com/")
                await message.channel.send(f'Nepalstock! In {round(nepalstock.elapsed.total_seconds() * 1000)}ms')
                pass
            except:
                await message.channel.send(f'Nepalstock! In Failed')
                pass
            try :
                tms = requests.get("https://tms34.nepsetms.com.np/")
                await message.channel.send(f'TMS! In {round(tms.elapsed.total_seconds() * 1000)}ms')
                pass
            except:
                await message.channel.send(f'TMS! In Failed')
                pass
            
client = MyClient()

def _RunBot():
    """with open("./Paste Token.txt","r") as token_file:
        token = token_file.readlines()
    token_file.close()"""


    dontrun = _Config("r","ToRunBot")
    if dontrun == False:
        return

    token = _Config("r","BotToken")

    client.run(token)


def _Shutdown():
    #exit()
    print(len(asyncio.all_tasks()))
    pass