# @Author: Edmund Lam <edl>
# @Date:   11:04:49, 05-Apr-2018
# @Filename: settings.py
# @Last modified by:   edl
# @Last modified time: 21:46:34, 09-Oct-2019


import asyncio
from bot.utils import msgutils, strutils, cmdutils
from bot.handlers import add_message_handler, nested_set
from discord import Embed, ChannelType

async def settings(bot, msg, reg):
    command = reg.group('command');
    perms = msg.channel.permissions_for(msg.author)
    #make sure user is authorized to edit bot preferences
    #and that command exists
    if perms.manage_guild and commandutils.is_command(command):
        sub = reg.group('sub');
        channels = reg.group('channels')
        if channels == 'all':
            list(n for n in msg.guild.channels if isinstance(channel, discord.Textchannel))
        else:
            channels = msg.channel_mentions
        for channel in channels:
            nested_set(sub == 'enable', 'guilds', msg.guild.id, 'channels', msg.channel.id, 'commands', command)

add_message_handler(settings, r'settings (?P<sub>enable|disable) (?P<command>.+?) (?P<channels>all|(?:channel_mention )+)')
