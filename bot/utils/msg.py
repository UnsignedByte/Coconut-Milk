# @Author: Edmund Lam <edl>
# @Date:   10:01:53, 03-Nov-2018
# @Filename: msgutils.py
# @Last modified by:   edl
# @Last modified time: 16:55:45, 08-Oct-2019

import asyncio
from discord import VoiceRegion, Forbidden
from bot.utils import str, user

## Usable

async def send_embed(Bot, msg, embed, usr=None):
    if not usr:
        usr = Bot.user
    txt = "Created by {}.".format(user.nickname(usr, msg.server))
    embed.set_footer(text=txt, icon_url=(usr.avatar_url if usr.avatar_url else usr.default_avatar_url))
    try:
        m = await Bot.send_message(msg.channel, embed=embed)
        return m
    except Forbidden:
        await Bot.send_message(msg.channel, "**Missing Permissions**\nDiscow is missing permissions to send embeds.")
        return None

async def edit_embed(Bot, msg, embed, usr=None):
    if not usr:
        usr = Bot.user
    txt = "Edited by {}.".format(user.nickname(usr, msg.server))
    embed.set_footer(text=txt, icon_url=(usr.avatar_url if usr.avatar_url else usr.default_avatar_url))
    m = await Bot.edit_message(msg, embed=embed)
    return m

async def send_large_message(Bot, channel, content, prefix='', suffix=''):
    clist = strutils.split_str_chunks(content, 2000, prefix=prefix, suffix=suffix)
    for l in clist:
        await Bot.send_message(channel, l)
