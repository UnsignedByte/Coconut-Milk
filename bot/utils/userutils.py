# @Author: Edmund Lam <edl>
# @Date:   20:17:56, 04-Nov-2018
# @Filename: memberutils.py
# @Last modified by:   edl
# @Last modified time: 16:14:15, 09-Oct-2019

import asyncio
from bot.utils import datautils
import discord

async def get_owner(Bot):
    return (await Bot.application_info()).owner

async def is_mod(Bot, user):
    return user == (await get_owner(Bot)) or user in datautils.nested_get('global_data', 'moderators', default=[])

def get_user_color(user):
    if isinstance(user, discord.Member):
        return user.colour
    else:
        return 0x3a71c1

def nickname(usr, srv):
    if not srv:
        return usr.name
    n = srv.get_member(usr.id).nick
    if not n:
        return usr.name
    return n
