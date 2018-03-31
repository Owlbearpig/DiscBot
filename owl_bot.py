import discord
import asyncio
import csv
from bot_extensions.extension_class import BotExtensionFunctions
from bot_extensions.utils import BotUtilities

#
# Owlbot, a Discord bot by Owlbearpig and Inarius, based on discord.py and its command
#                             extension
#
#
#
#
#
#
#
#
#

client = discord.Client()
token = 'NDE2NTY4NjQ2MTUyODgwMTI5.DXGXbw.vDjD6z_CFE-M7NbSiwZXVlvbfMc'
loop = asyncio.get_event_loop()

async def print_channels():
    await client.wait_until_ready()
    channels = client.get_all_channels()
    print([(str(channel),str(channel.id)) for channel in list(channels)])

async def send_msg():
    await client.wait_until_ready()
    await client.send_message(discord.Object(id="407911597017661450"), content="#wave")

@client.event
#@asyncio.coroutine
async def on_ready():
    await send_msg()
    print('Logged in. Reading chat')

def destination(channel):
    id = str(channel.id)
    return discord.Object(id=id)

@client.event
async def on_message(message):
    extensions = BotExtensionFunctions(loop=loop)
    utils = BotUtilities(loop=loop)

    if message.author == client.user:
        return
    if message.content.startswith('%%sheet'):
        await client.send_message(destination(message.channel), "generating spreadsheet")
        await extensions.dungeonator_main()
        await client.send_message(destination(message.channel), "done. Attaching file...")
        await client.send_file(destination(message.channel), "out.csv")
    elif message.content.startswith("%%m++"):
        disc_id = await utils.get_user_id(message=message)
        await extensions.altinator_main(disc_id=disc_id)
        await client.send_file(message.author, extensions.altinator_png_path)

async def _run():
    await client.login(token)
    await client.connect()

async def logout():
    await client.logout()


try:
    loop.run_until_complete(_run())
except Exception as e:
    print(e)
    loop.run_until_complete(logout())
finally:
    loop.close()


