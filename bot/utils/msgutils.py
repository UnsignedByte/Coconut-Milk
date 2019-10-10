# @Author: Edmund Lam <edl>
# @Date:   10:01:53, 03-Nov-2018
# @Filename: msgutils.py
# @Last modified by:   edl
# @Last modified time: 16:19:38, 09-Oct-2019

import asyncio
from discord import VoiceRegion, Forbidden
from bot.utils import strutils, userutils

## Usable

async def send_embed(bot, msg, embed, usr=None):
    if not usr:
        usr = bot.user
    txt = "Created by {}.".format(userutils.nickname(usr, msg.guild))
    embed.set_footer(text=txt, icon_url=(usr.avatar_url if usr.avatar_url else usr.default_avatar_url))
    try:
        m = await msg.channel.send(embed=embed)
        return m
    except Forbidden:
        await msg.channel.send("**Missing Permissions**\nDiscow is missing permissions to send embeds.")
        return None

async def edit_embed(bot, msg, embed, usr=None):
    if not usr:
        usr = bot.user
    txt = "Edited by {}.".format(userutils.nickname(usr, msg.guild))
    embed.set_footer(text=txt, icon_url=(usr.avatar_url if usr.avatar_url else usr.default_avatar_url))
    m = await msg.edit(embed=embed)
    return m

async def send_large_message(bot, channel, content, prefix='', suffix=''):
    clist = strutils.split_str_chunks(content, 2000, prefix=prefix, suffix=suffix)
    for l in clist:
        await channel.send(l)
