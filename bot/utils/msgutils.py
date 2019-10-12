# @Author: Edmund Lam <edl>
# @Date:   10:01:53, 03-Nov-2018
# @Filename: msgutils.py
# @Last modified by:   edl
# @Last modified time: 00:01:54, 12-Oct-2019

import asyncio
from discord import Forbidden
from bot.utils import strutils, userutils

## Usable

async def send_embed(bot, msg, embed, usr=None, delete_after=None):
    if embed.footer.text == embed.Empty:
        if not usr:
            usr = msg.author
        txt = "Requested by {}.".format(userutils.nickname(usr, msg.guild))
        embed.set_footer(text=txt, icon_url=(usr.avatar_url if usr.avatar_url else usr.default_avatar_url))
    try:
        m = await msg.channel.send(embed=embed, delete_after=delete_after)
        return m
    except Forbidden:
        await msg.channel.send("**Missing Permissions**\nPersimmon is missing permissions to send embeds.", delete_after=2)
        return None

async def edit_embed(bot, msg, embed, delete_after=None):
    if embed.footer.text == embed.Empty:
        foot = msg.embeds[0].footer
        embed.set_footer(text=foot.text, icon_url=foot.icon_url)
    await msg.edit(embed=embed, delete_after=delete_after)

async def send_large_message(bot, channel, content, prefix='', suffix=''):
    clist = strutils.split_str_chunks(content, 2000, prefix=prefix, suffix=suffix)
    for l in clist:
        await channel.send(l)
