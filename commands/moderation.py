# @Author: Edmund Lam <edl>
# @Date:   11:04:49, 05-Apr-2018
# @Filename: settings.py
# @Last modified by:   edl
# @Last modified time: 18:10:36, 30-Oct-2019


import json
import asyncio
from bot.utils import msgutils, strutils, datautils, userutils, miscutils, cmdutils
from bot.handlers import message_handler, bot_prefix
from discord import Embed, HTTPException, TextChannel
import re
import traceback
import greenlet

async def settings(bot, msg, reg):
    command = reg.group('command');
    perms = msg.channel.permissions_for(msg.author)
    #make sure user is authorized to edit bot preferences
    #and that command exists
    if perms.manage_guild and cmdutils.is_command(command):
        sub = reg.group('sub');
        channels = reg.group('channels')
        if channels == 'all':
            channels = list(n for n in msg.guild.channels if isinstance(n, TextChannel))
        else:
            channels = msg.channel_mentions
        for channel in channels:
            datautils.nested_set(sub == 'disable', 'guilds', msg.guild.id, 'channels', channel.id, 'commands', command)
        await msg.channel.send('Command `{}` has been {}d in {}'.format(command, sub, ', '.join(map(lambda x:x.mention,  channels))))

async def execute(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
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
            out = await aexec('import asyncio\nasync def run_exec():\n\t'+'\t'.join(reg.group("body").strip().splitlines(True))+'\ngawait(run_exec())')
        except Exception:
            await msgutils.send_embed(bot, msg, Embed(title="Output", description=traceback.format_exc(), colour=miscutils.colours['red']))

async def purge(bot, msg, reg):
    perms = msg.channel.permissions_for(msg.author)
    if perms.manage_messages or (await userutils.is_mod(bot, msg.author)):
        await msg.delete()
        num = int(reg.group('num'));
        usr = reg.group('user')
        if usr:
            usr = userutils.get_user(bot, msg.guild, usr)
        def check(message):
            return not usr or usr.id == message.author.id
        await msg.channel.purge(limit=num, check=check)
        await msg.channel.send("**{}** has cleared the last **{}** messages!".format(msg.author.mention,num-1), delete_after=2)
    else:
        em = Embed(title="Insufficient Permissions", description=strutils.format_response("{_mention} does not have sufficient permissions to perform this task.", _msg=msg), colour=miscutils.colour.red)
        await msgutils.send_embed(bot, msg, em, delete_after=2)

async def save(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        await msg.channel.trigger_typing();
        datautils.save_data();
        await msg.channel.send('Data saved!', delete_after=0.5);

async def data(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        await msgutils.send_large_message(bot, msg.channel, json.dumps(datautils.get_data(), indent=2), prefix='```json\n',suffix='```')

async def find(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        path = reg.group('path');
        if not path:
            await msg.channel.send('`' + str(list(datautils.get_data().keys())) + '`')
            return
        await msgutils.send_large_message(bot, msg.channel, json.dumps(datautils.nested_get(*miscutils.list2int(path.split())), indent=2), prefix='```json\n',suffix='```')

async def delete(bot, msg, reg):
    if (await userutils.is_mod(bot, msg.author)):
        keys = miscutils.list2int(reg.group('path').split())
        if isinstance(datautils.nested_get(*keys[:-1]), dict):
            datautils.nested_pop(*keys)
        elif isinstance(datautils.nested_get(*keys[:-1]), list):
            datautils.nested_remove(keys[-1], *keys[:-1])
        await msg.channel.send('deleted `{}`.'.format(reg.group('path')))

async def mod(bot, msg, reg):
    if msg.author == (await userutils.get_owner(bot)):
        if msg.mentions[0] not in datautils.nested_get('moderators', default=[]):
            if reg.group('sub') == 'add':
                datautils.nested_append(msg.mentions[0], 'global', 'moderators')
            else:
                datautils.nested_remove(msg.mentions[0], 'global', 'moderators')

async def ban(bot, msg, reg):
    perms = msg.channel.permissions_for(msg.author)
    usr = userutils.get_user(bot, msg.guild, reg.group('user'))
    if not usr:
        await msg.channel.send('Could not find a user named `{}`. Make sure the name is spelt correctly.'.format(reg.group('user')))
    if perms.ban_members:
        await msg.guild.ban(usr, reason=reg.group('reason'), delete_message_days=reg.group('days') if reg.group('days') else 0)
async def unban(bot, msg, reg):
    perms = msg.channel.permissions_for(msg.author)
    bans = await msg.guild.bans()
    bans = [x.user for x in bans]
    usr = userutils.get_user(bot, msg.guild, reg.group('user'), userlist=bans)
    if not usr:
        await msg.channel.send('Could not find a user named `{}`. Make sure the name is spelt correctly.'.format(reg.group('user')))
    if perms.ban_members:
        await msg.guild.unban(usr, reason=reg.group('reason'))


message_handler.add(execute, r'exec (?P<in>``)?`(?P<body>[^`].*?[^`])(?(in)```|`)')

message_handler.add_public(settings, r'settings (?P<sub>enable|disable) (?P<command>.+?) (?P<channels>all|(?:channel_mention )+)')
message_handler.add_public(purge, r'(?:purge|clear) (?P<num>[0-9]+) (?P<user>.+)?')
message_handler.add_public(ban, r'(?:ban) (?P<user>.+) (?P<reason>.+?)? (?P<days>[0-7])?')
message_handler.add_public(unban, r'(?:unban) (?P<user>.+) (?P<reason>.+)?')

message_handler.add_private(save, r'save')
message_handler.add_private(data, r'data')
message_handler.add_private(delete, r'(?:rm|remove|del(?:ete)?) (?P<path>.*)')
message_handler.add_private(find, r'find (?P<path>.*)')
message_handler.add_private(mod, r'mod (?P<sub> add|del) user_mention')
