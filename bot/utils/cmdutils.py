# @Author: Edmund Lam <edl>
# @Date:   11:17:55, 08-Oct-2019
# @Filename: utils.py
# @Last modified by:   edl
# @Last modified time: 11:26:47, 11-Oct-2019
from bot.handlers import public_message_handlers
from bot.utils import datautils

def is_command(cmd):
    return cmd in map(lambda x: x.__name__, public_message_handlers.values());

def allowed_command(cmd, channel):
    return not datautils.nested_get('guilds', channel.guild.id, 'channels', channel.id, 'commands', cmd)
