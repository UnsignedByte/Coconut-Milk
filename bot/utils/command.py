# @Author: Edmund Lam <edl>
# @Date:   11:17:55, 08-Oct-2019
# @Filename: utils.py
# @Last modified by:   edl
# @Last modified time: 16:58:23, 08-Oct-2019
from bot.handlers import message_handlers

def is_command(cmd):
    return cmd in message_handlers

def allowed_command(cmd, channel):
    if cmd not in bot_data['settings']:
        return True
    else:
        return channel not in bot_data['settings'][cmd]
