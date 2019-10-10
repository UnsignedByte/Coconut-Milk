# @Author: Edmund Lam <edl>
# @Date:   10:01:28, 03-Nov-2018
# @Filename: strutils.py
# @Last modified by:   edl
# @Last modified time: 21:43:42, 09-Oct-2019

from bot.handlers import bot_prefix
import re

def format_response(string, **kwargs):
    if "_msg" in kwargs:
        message = kwargs["_msg"]
        kwargs["_msgcontent"] = message.content
        kwargs["_author"] = message.author
    if "_author" in kwargs:
        author = kwargs["_author"]
        kwargs["_name"] = author.display_name
        kwargs["_username"] = author.name
        kwargs["_mention"] = author.mention

    return string.format(**kwargs)

def format_regex(keyword):
    formatreg = {
        'channel_mention': r'<#[0-9]+>',
        'user_mention': r'<@!?[0-9]+>',
        'role_mention': r'<@&[0-9]+>',
    }
    for i in formatreg:
        keyword = keyword.replace(i, formatreg[i])

    keyword = keyword.replace(' ', '\s*') # allow all whitespace
    keyword = re.escape(bot_prefix)+keyword+r'\Z' #Make sure command ends at end of match
    return keyword

def escape_markdown(s):
    return re.sub(r'(?:`|\(|\\|\[|\]|\)|\*|~|_)', r'\\\g<0>', s)
