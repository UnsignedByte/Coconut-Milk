# @Author: Edmund Lam <edl>
# @Date:   19:01:44, 02-Apr-2018
# @Filename: help.py
# @Last modified by:   edl
# @Last modified time: 11:20:43, 11-Oct-2019


import asyncio
from discord import Embed
from bot.handlers import message_handler, bot_prefix
from collections import OrderedDict

print("\tInitializing Help Command")
print("\t\tParsing Help Command")
helpvals = OrderedDict()
helppages = []

with open("README.md", "r") as f:
    lastheader = ""
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        if l:
            if l.startswith("#"):
                lastheader = l.lstrip("#").strip()
                helpvals.update({lastheader : []})
            elif l in ["| **Name** | **Usage** | **Description** | **Aliases** |", "|:-:|:-:|:-:|:-:|"]:
                pass
            elif l.startswith("|") and l.endswith("|"):
                cmd = list(map(lambda x:x.replace('`', ""), l.strip("|").split("|")))
                helpvals[lastheader].append("< "+cmd[1]+" >\n[ AKA "+cmd[3].ljust(15)+" ]( "+cmd[2]+" )")
            else:
                helpvals[lastheader].append('> '+l.replace('`', ''))

helpembed = Embed(colour=0x9542f4)

desc = "```markdown"

first = True
for key, value in helpvals.items():
    if first:
        helpembed.title = key
        helpembed.description = '\n'.join(map(lambda x:x.lstrip(">").strip(), value))+'\n\nTo display another page, do `{}help {{page number}}`. For more help, take a look at [the Readme](https://github.com/UnsignedByte/Persimmon/blob/master/README.md) on our [github repository](https://github.com/UnsignedByte/Persimmon)!'.format(bot_prefix)
        first = False
    else:
        stoadd = "\n\n# "+key+'\n\n'+'\n'.join(value)
        if len(desc)+len(stoadd) >= 1000:
            helpembed.add_field(name='\a', value=desc+'```')
            desc = "```markdown"+stoadd
        else:
            desc+=stoadd
print("\t\tFinished Parsing")
helpembed.add_field(name='\a', value=desc+'```')

async def help(Bot, msg, reg):
    await msg.channel.send("Sent you command information!")
    await msg.author.send(embed=helpembed)


message_handler.add(help, r'(?:help|commands)')
print("\tHelp Command Initialized")
