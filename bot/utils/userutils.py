# @Author: Edmund Lam <edl>
# @Date:   20:17:56, 04-Nov-2018
# @Filename: memberutils.py
# @Last modified by:   edl
# @Last modified time: 13:00:18, 27-Oct-2019

import asyncio
from bot.utils import datautils
import discord
import re
import difflib

async def get_owner(bot):
    return (await bot.application_info()).owner

async def is_mod(bot, user):
    return (user.id == await get_owner(bot).id) or user.id in datautils.nested_get('global', 'moderators', default=[])

def get_user_color(user):
    if isinstance(user, discord.Member):
        return user.colour
    else:
        return 0x3a71c1

def nickname(usr, srv):
    if srv:
        n = srv.get_member(usr.id)
        if n and n.nick:
            return n.nick
    return usr.name

def get_user(bot, guild, selector, userlist=None):
    reg = re.compile(r'(?:<@!?(?P<id>[0-9]+)>)').match(selector)
    if reg:
        return bot.get_user(int(reg.group('id')))
    else:
        if not userlist:
            userlist = guild.members
        namelist = list(map(lambda x:nickname(x, guild).lower(), userlist))
        selector = selector.lower()
        closest = difflib.get_close_matches(selector, namelist, n=1)
        closest.extend([x for x in namelist if selector in x])
        if closest:
            return userlist[namelist.index(closest[0])]
        else:
            return None
