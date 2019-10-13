# @Author: Edmund Lam <edl>
# @Date:   18:59:11, 18-Apr-2018
# @Filename: utilities.py
# @Last modified by:   edl
# @Last modified time: 21:44:31, 12-Oct-2019

# from pprint import pformat
import asyncio
from bot.utils import msgutils, userutils, miscutils
from bot.handlers import message_handler, bot_prefix, strutils
from discord import Embed, NotFound, HTTPException
import re
from PyDictionary import PyDictionary
from googletrans import Translator
import urbandict

dictionary = PyDictionary()
translator = Translator()

async def info(bot, msg, reg):
    em = Embed(title="Who am I?", colour=miscutils.colours['orange'])
    em.description = "Hi, I'm [Persimmon](https://github.com/UnsignedByte/Persimmon), a discord bot created by "+(await userutils.get_owner(bot)).mention+"."
    em.add_field(name="Features", value="For information about my features do `"+bot_prefix+"help` or take a look at [my github](https://github.com/UnsignedByte/Persimmon/)!")
    await msgutils.send_embed(bot, msg, em)

async def urban(bot, msg, reg):
    x = reg.group('word')
    try:
        res = urbandict.define(x)
        res = res[0]
        em = Embed(title=res['word'], description=strutils.escape_markdown(res['def']), colour=miscutils.colours['orange'])
        if res['example']:
            em.add_field(name='Example', value=res['example'])
        await msgutils.send_embed(bot, msg, em)
    except Exception:
        await msg.channel.send('Could not find `{}` in the urban dictionary. Make sure the phrase is spelled correctly.'.format(x))

async def define(bot, msg, reg):
    x = reg.group('word')
    meaning = dictionary.meaning(x);
    if not meaning:
        await msg.channel.send('Could not find `{}` in the dictionary. Make sure the word is spelled correctly.'.format(x))
        return
    em = Embed(title=x.title(), colour=miscutils.colours['orange'])
    for type in meaning:
        desc = ''.join('{}. {}\n'.format(i, meaning[type][i]) for i in range(len(meaning[type])));
        em.add_field(name=type, value=desc, inline=False)
    await msgutils.send_embed(bot, msg, em)

async def translate(bot, msg, reg):
    x = reg.group('word')
    lang = reg.group('lang')
    em = Embed(title='Translation', colour=miscutils.colours['orange'])
    if lang:
        if lang.lower() in miscutils.lang_shortcuts:
            lang = miscutils.lang_shortcuts[lang.lower()]
        try:
            res = translator.translate(x, dest=lang)
        except ValueError:
            em.description = 'Invalid language specified. Translating to english.'
            res = translator.translate(reg.group(1))
    else:
        em.description = 'No language specified. Translating to english.'
        res = translator.translate(x)
    em.add_field(name=miscutils.lang_codes[res.src], value=res.origin, inline=True)
    em.add_field(name=miscutils.lang_codes[res.dest], value=res.text, inline=True)
    await msgutils.send_embed(bot, msg, em)

message_handler.add(info, r'hi|info')
message_handler.add(urban, r'urban(?:dict)? (?P<word>.+)')
message_handler.add(define, r'(?:define|dictionary) (?P<word>.+)')
message_handler.add(translate, r'(?:trans(?:late)?) ((?P<word>.+?) (?P<lang>[a-zA-Z\-]+?)?)')
