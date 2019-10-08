import discord
import asyncio
import logging
import re

import bot.client.getkey as _getkey
import bot.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class BotClientClass(discord.Client):
    async def on_ready(self):
        await self.change_presence(game=discord.Game(name='.help', url='https://github.com/UnsignedByte/Coconut-Milk', type=2))
        await asyncio.gather(bot.handlers.timed_msg(self), bot.handlers.timed_save(self))
    async def on_message(self, message):
        await bot.handlers.on_message(self, message)
    async def on_message_edit(self, before, after):
        await bot.handlers.on_message(self, after)
Bot = BotClientClass()

def runBot():
    Bot.run(_getkey.key())

if __name__ == "__main__":
    print("Auth key is %s" % _getkey.key())
