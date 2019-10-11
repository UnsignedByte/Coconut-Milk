# @Author: Edmund Lam <edl>
# @Date:   18:59:11, 18-Apr-2018
# @Filename: utilities.py
# @Last modified by:   edl
# @Last modified time: 11:21:30, 11-Oct-2019

# from pprint import pformat
import asyncio
from bot.utils import msgutils, userutils
from bot.handlers import message_handler, bot_prefix
from discord import Embed, NotFound, HTTPException
import re
from PyDictionary import PyDictionary

dictionary = PyDictionary()

async def info(bot, msg, reg):
    em = Embed(title="Who am I?", colour=0x9542f4)
    em.description = "Hi, I'm [Persimmon](https://github.com/UnsignedByte/Persimmon), a discord bot created by "+(await userutils.get_owner(bot)).mention+"."
    em.add_field(name="Features", value="For information about my features do `"+bot_prefix+"help` or take a look at [my github](https://github.com/UnsignedByte/Persimmon/)!")
    await msgutils.send_embed(bot, msg, em)

async def define(bot, msg, reg):
    x = reg.group('word')
    meaning = dictionary.meaning(x);
    em = Embed(title=x)
    for type in meaning:
        desc = ''.join('{}. {}\n'.format(i, meaning[type][i]) for i in range(len(meaning[type])));
        em.add_field(name=type, value=desc)
    await msgutils.send_embed(bot, msg, em)

message_handler.add(info, r'hi|info')
message_handler.add(define, r'(?:define|dictionary) (?P<word>.+)')
