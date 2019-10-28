# @Author: Edmund Lam <edl>
# @Date:   06:50:24, 02-May-2018
# @Filename: handlers.py
# @Last modified by:   edl
# @Last modified time: 22:40:55, 27-Oct-2019

bot_data = {}
bot_prefix = '.'
public_message_handlers = {}
private_message_handlers = {}

import re
from random import randint
from bot.utils import datautils, msgutils, strutils
import discord

print("Begin Handler Initialization")

print("\tBegin Loading Files")

bot_data = datautils.load_data();

def get_data():
    return bot_data

def set_data(dat):
    bot_data = dat

print("\tLoaded files")

class message_handler:
    def add(handler, keyword):
        message_handler.add_public(handler, keyword);
        message_handler.add_private(handler, keyword);
    def add_public(handler, keyword):
        public_message_handlers[strutils.format_regex(keyword)] = handler
    def add_private(handler, keyword):
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
                    reg = re.compile(a, re.DOTALL).match(msg.content)
                    if reg:
                        await private_message_handlers[a](bot, msg, reg)
            else:
                for a in public_message_handlers:
                    reg = re.compile(a, re.DOTALL).match(msg.content)
                    if reg:
                        commandname = public_message_handlers[a].__name__;
                        if cmdutils.allowed_command(commandname,c):
                            await public_message_handlers[a](bot, msg, reg)
                            break
                        else:
                            await c.send('The {} command is disabled in this channel.'.format(commandname), deleteafter=1)
        except Exception as e:
            em = discord.Embed(title="Unknown Error",
                               description="An unknown error occurred. Trace:\n%s" % e, colour=0xd32323)
            await msgutils.send_embed(bot, msg, em)
            traceback.print_tb(e.__traceback__)

async def timed_save(Bot):
    while True:
        await asyncio.sleep(60)
        datautils.save_data()
