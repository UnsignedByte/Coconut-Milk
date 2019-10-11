# @Author: Edmund Lam <edl>
# @Date:   18:59:11, 18-Apr-2018
# @Filename: utilities.py
# @Last modified by:   edl
# @Last modified time: 18:45:07, 10-Oct-2019

# from pprint import pformat
import json
import asyncio
import pickle
from bot.utils import msgutils, strutils, datautils, userutils, objutils
from bot.handlers import add_message_handler, add_private_message_handler
from discord import Embed, NotFound, HTTPException
import requests as req
import re
import traceback
from bs4 import BeautifulSoup
import greenlet

async def info(bot, msg, reg):
    em = Embed(title="Who am I?", colour=0x9542f4)
    em.description = "Hi, I'm [Persimmon](https://github.com/UnsignedByte/Persimmon), a discord bot created by <@418827664304898048>.\nOn this server, I am known as "+nickname(bot.user, msg.server)+'.'
    em.add_field(name="Features", value="For information about my features do `"+bot_prefix+"help` or take a look at [our readme](https://github.com/UnsignedByte/Persimmon/blob/master/README.md)!")
    await msgutils.send_embed(bot, msg, em)

async def execute(bot, msg, reg):
    if is_mod(bot, msg.author):
        #From https://stackoverflow.com/a/46087477/5844752
        class GreenAwait:
            def __init__(self, child):
                self.current = greenlet.getcurrent()
                self.value = None
                self.child = child

            def __call__(self, future):
                self.value = future
                self.current.switch()

            def __iter__(self):
                while self.value is not None:
                    yield self.value
                    self.value = None
                    self.child.switch()

        def gexec(code):
            child = greenlet.greenlet(exec)
            gawait = GreenAwait(child)
            child.switch(code, {'gawait': gawait, 'bot': bot, 'msg': msg})
            yield from gawait

        async def aexec(code):
            green = greenlet.greenlet(gexec)
            gen = green.switch(code)
            for future in gen:
                await future

        try:
            out = await aexec('import asyncio\nasync def run_exec():\n\t'+'\t'.join(re.search(r'`(?P<in>``)?(?P<body>(.?\s?)*)(?(in)```|`)', msg.content).group("body").strip().splitlines(True))+'\ngawait(run_exec())')
        except Exception:
            await msgutils.send_embed(bot, msg, Embed(title="Output", description=traceback.format_exc(), colour=0xd32323))

async def quote(bot, msg, reg):
    try:
        m = await (msg.channel if len(msg.channel_mentions) == 0 else msg.channel_mentions[0]).send(strutils.strutils.strip_command(msg.content).split(" ")[0])
        em = Embed(title="Message Quoted by "+msg.author.display_name+":", colour=0x3b7ce5)
        desc = m.content
        print(desc)
        log = reversed([a async for a in bot.logs_from(m.channel, limit=20, after=m)])
        print(log)
        for a in log:
            if a.author == m.author:
                if a.content:
                    desc+="\n"+a.content
            else:
                break
        async for a in bot.logs_from(m.channel, limit=20, before=m):
            if a.author == m.author:
                if a.content:
                    desc=a.content+"\n"+desc
            else:
                break
        em.description = desc
        print(desc)
        await bot.delete_message(msg)
        await msgutils.send_embed(bot, msg, em, time=m.timestamp, usr=m.author)
    except NotFound:
        em = Embed(title="Unable to Find Message", description="Could not find a message with that id.", colour=0xd32323)
        await msgutils.send_embed(bot, msg, em)

async def dictionary(bot, msg):
    link="https://www.merriam-webster.com/dictionary/"
    x = strutils.strutils.strip_command(msg.content).replace(' ', '%20')
    em = Embed(title="Definition for "+x+".", description="Retrieving Definition...", colour=0x4e91fc)
    dictm = await msgutils.send_embed(bot, msg, em)

    try:
        response = req.get(link+x)
        response.raise_for_status()
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
    except req.exceptions.HTTPError as err:
        e = err.response.text
        try:
            em.description = "Could not find "+x+" in the dictionary. Choose one of the words below, or type 'cancel' to cancel."
            soup = BeautifulSoup(e.read(), 'html.parser')
            words = soup.find("ol", {"class":"definition-list"}).get_text().split()
            for i in range(0, len(words)):
                em.description+='\n**'+str(i+1)+":** *"+words[i]+'*'
            dictm = await msgutils.send_embed(bot, dictm, em)
            while True:
                vm = await bot.wait_for_message(timeout=600, author=msg.author, channel=msg.channel)
                if not vm:
                    return
                v = vm.content
                if v == 'cancel':
                    em.description = "*Operation Cancelled*"
                    await bot.delete_message(vm)
                    dictm = await msgutils.send_embed(bot, dictm, em)
                    return
                elif objutils.integer(v):
                    if int(v)>=1 and int(v) <=len(words):
                        x = words[int(v)-1].replace(' ', "%20")
                        await bot.delete_message(vm)
                        break
                else:
                    if v in words:
                        x = v.replace(' ', "%20")
                        await bot.delete_message(vm)
                        break
            html_doc = req.get(link+x).text
            soup = BeautifulSoup(html_doc, 'html.parser')
            em.title = "Definition for "+x+"."
            em.description = "Retrieving Definition..."
            dictm = await msgutils.send_embed(bot, dictm, em)
        except AttributeError:
            em.description = "Could not find "+x+" in the dictionary."
            dictm = await msgutils.send_embed(bot, dictm, em)
            return

    em.description = ""
    txts = soup.find("div", {"id" : "entry-1"}).find("div", {"class":"vg"}).findAll("div", {"class":["sb", "has-sn"]}, recursive=False)
    for x in txts:
        l = list(filter(None,map(lambda x:x.strip(), x.get_text().split("\n"))))
        st = ""
        for a in l:
            if a.startswith(":"):
                st+=' '.join(a.strip().split())
            else:
                v1 = a.split()
                if objutils.integer(v1[0]):
                    st+="\n**__"+v1[0]+"__**"
                    v1 = v1[1:]
                for n in v1:
                    if objutils.integer(n.strip("()")):
                        st+="\n\t\t***"+n+"***"
                    elif len(n)==1:
                        st+="\n\t**"+n+"**"
                    else:
                        st+=" *"+n+"*"

        em.description+= '\n'+st
    em.description+="\n\nDefinitions retrieved from [The Merriam-Webster Dictionary](https://www.merriam-webster.com/) using [Dictionary](https://github.com/UnsignedByte/Dictionary) by [UnsignedByte](https://github.com/UnsignedByte)."
    dictm = await msgutils.send_embed(bot, dictm, em)


async def purge(bot, msg):
    perms = msg.channel.permissions_for(msg.author)
    if perms.manage_messages or is_mod(bot, msg.author):
        num = int(strutils.parse_command(msg.content, 1)[1].split(' ')[0])+1
        if num < 2:
            await msg.channel.send("There is no reason to delete 0 messages!")
        deletechunks = []
        def check(message):
            return not msg.mentions or msg.mentions[0].id == message.author.id
        try:
            await bot.purge_from(msg.channel, limit=num, check=check)
            m = await msg.channel.send(strutils.format_response("**{_mention}** has cleared the last **{_number}** messages!", _msg=msg, _number=num-1))
        except HTTPException:
            m = await msg.channel.send(strutils.format_response("You cannot bulk delete messages that are over 14 days old!!"))

        await asyncio.sleep(2)
        await bot.delete_message(m)
    else:
        em = Embed(title="Insufficient Permissions", description=strutils.format_response("{_mention} does not have sufficient permissions to perform this task.", _msg=msg), colour=0xd32323)
        await msgutils.send_embed(bot, msg, em)

async def save(bot, msg, reg):
    if await userutils.is_mod(bot, msg.author):
        await msg.channel.trigger_typing();
        datautils.save_data();
        await msg.channel.send('Data saved!', delete_after=0.5);

async def getData(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        await msgutils.send_large_message(bot, msg.channel, json.dumps(datautils.get_data(), indent=1), prefix='```json\n',suffix='```')

async def find(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        if reg.group('key'):
            await msg.channel.send('`' + str(list(datautils.get_data().keys())) + '`')
            return
        await msgutils.send_large_message(bot, msg.channel, json.dumps(datautils.get_data()[reg.group('key')], indent=1), prefix='```json\n',suffix='```')

async def delete_data(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        keys = reg.group('path').split()
        if isinstance(datautils.nested_get(*keys[:-1]), dict):
            datautils.nested_pop(*keys)
        elif isinstance(datautils.nested_get(*keys[:-1]), list):
            datautils.nested_remove(keys[-1], *keys[:-1])

async def mod(bot, msg, reg):
    if msg.author == (await userutils.get_owner(bot)):
        if msg.mentions[0] not in datautils.nested_get('moderators', default=[]):
            if reg.group('sub') == 'add':
                datautils.nested_append(msg.mentions[0], 'global', 'moderators')
            else:
                datautils.nested_remove(msg.mentions[0], 'global', 'moderators')

add_message_handler(info, r'(?:hi|info)')
add_message_handler(purge, "purge")
add_message_handler(purge, "clear")
add_message_handler(quote, "quote")
add_message_handler(dictionary, "define")
add_message_handler(dictionary, "dictionary")

add_private_message_handler(save, r'save')
add_private_message_handler(execute, r'exec [.\n]+')
add_private_message_handler(getData, r'getdata')
add_private_message_handler(delete_data, r'(?:remove|delete) (?P<path>.*)')
add_private_message_handler(find, r'find (?P<key>.*)')
add_private_message_handler(mod, r'mod (?P<sub> add|del) user_mention')
