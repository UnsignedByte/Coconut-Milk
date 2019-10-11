# @Author: Edmund Lam <edl>
# @Date:   06:50:24, 02-May-2018
# @Filename: handlers.py
# @Last modified by:   edl
# @Last modified time: 19:01:01, 10-Oct-2019

bot_data = {}
bot_prefix = '.'
message_handlers = {}
private_message_handlers = {}

import re
from random import randint
from bot.utils import datautils, msgutils, strutils
import discord

print("Begin Handler Initialization")

print("\tBegin Loading Files")

bot_data = datautils.load_data();
print(bot_data)

def get_data():
    return bot_data

def set_data(dat):
    bot_data = dat

print("\tLoaded files")

def add_message_handler(handler, keyword):
    message_handlers[strutils.format_regex(keyword)] = handler

def add_private_message_handler(handler, keyword):
    private_message_handlers[strutils.format_regex(keyword)] = handler

print("Handler initialized")
print("Begin Command Initialization")
# Add modules here
from bot.utils import cmdutils
from commands import *
print("Command Initialization Finished")

import asyncio

async def on_message(bot, msg):
    #implement mention count later
    if not msg.author.bot:
        c = msg.channel;
        try:
            if isinstance(c, discord.abc.PrivateChannel):
                for a in private_message_handlers:
                    reg = re.compile(a).match(msg.content)
                    if reg:
                        await private_message_handlers[a](bot, msg, reg)
            else:
                for a in message_handlers:
                    reg = re.compile(a).match(msg.content)
                    if reg:
                        commandname = message_handlers[a].__name__;
                        if cmdutils.allowed_command(commandname,c):
                            await message_handlers[a](bot, msg, reg)
                            break
                        else:
                            await c.send('The {} command is disabled in this channel.'.format(commandname))
        except Exception as e:
            em = discord.Embed(title="Unknown Error",
                               description="An unknown error occurred. Trace:\n%s" % e, colour=0xd32323)
            await msgutils.send_embed(bot, msg, em)
            traceback.print_tb(e.__traceback__)

async def timed_save(Bot):
    while True:
        await asyncio.sleep(60)
        datautils.save_data()
