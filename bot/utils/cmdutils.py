# @Author: Edmund Lam <edl>
# @Date:   11:17:55, 08-Oct-2019
# @Filename: utils.py
# @Last modified by:   edl
# @Last modified time: 22:08:36, 09-Oct-2019
from bot.handlers import message_handlers, nested_get

def is_command(cmd):
    return cmd in map(lambda x: x.__name__, message_handlers.values());

def allowed_command(cmd, channel):
    return not nested_get('guilds', channel.guild.id, 'channels', channel.id, 'commands', cmd)
