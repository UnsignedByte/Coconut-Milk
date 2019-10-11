import discord
import asyncio
import logging
import re

import from bot.client.getkey import readKey
import bot.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class BotClientClass(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(name='.help', url='https://github.com/UnsignedByte/Persimmon', type=discord.ActivityType.listening))
        await bot.handlers.timed_save(self)
    async def on_message(self, message):
        await bot.handlers.on_message(self, message)
    async def on_message_edit(self, before, after):
        await bot.handlers.on_message(self, after)
Bot = BotClientClass()

keys = readKey()

def runBot():
    Bot.run(keys[0])
