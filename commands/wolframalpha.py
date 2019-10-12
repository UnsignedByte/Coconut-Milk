# @Author: Edmund Lam <edl>
# @Date:   15:55:15, 12-Aug-2018
# @Filename: wolframalpha.py
# @Last modified by:   edl
# @Last modified time: 20:02:27, 11-Oct-2019

import asyncio
import os
import pyimgur
from bot.utils import imgutils, msgutils, strutils, miscutils
from bot.handlers import message_handler
from bot.client.getkey import readKey
from discord import Embed
import wolframalpha
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import itertools
import textwrap

print("\tInitializing Wolfram Alpha Command")

wa_client = wolframalpha.Client(readKey(2))
imgur_client = pyimgur.Imgur(readKey(1))

async def wolfram(bot, msg, reg):
    query = reg.group('query')
    em = Embed(title=query, description="Requesting data", colour=0xe4671b)
    oldem = await msgutils.send_embed(bot, msg, em)

    res = wa_client.query(query)

    if not res.success: # if query fails
        em = Embed(title=query, description="No results", colour=0xe4671b)
        await msgutils.edit_embed(bot, oldem, em)
        return

    titles = []
    images = []

    item_padding = 20
    font_size = 15
    font_padding = 3
    font = ImageFont.truetype("data/Roboto-Regular.ttf", font_size)

    podn = 0
    for pod in res.pod:
        podn+=1
        t = textwrap.wrap(pod.title, width=50)
        # titles.append(t)
        subimgs = []
        for sub in pod.subpod:
            subimgs.append(Image.open(BytesIO(requests.get(sub['img']['@src']).content)))
        # images.append(subimgs)

        widths, heights = zip(*(i.size for i in subimgs))
        total_height = sum(heights)+item_padding*(len(subimgs)+len(t))+(font_padding+font_size)*len(t)
        max_width = max(widths)
        pod_img = Image.new('RGBA', (max_width, total_height), (0,0,0,0))
        draw = ImageDraw.Draw(pod_img)
        max_width = max(max_width+item_padding, draw.textsize('\n'.join(t), font=font)[0]+item_padding)
        pod_img = Image.new('RGBA', (max_width, total_height), (0,0,0,0))
        draw = ImageDraw.Draw(pod_img)

        y_offset = 0
        for line in t:
            draw.text((item_padding, y_offset), line, fill=(119, 165, 182), font=font)
            y_offset+=font_size+font_padding

        y_offset+=item_padding
        for im in subimgs:
            pod_img.paste(im, (item_padding,y_offset))
            y_offset += im.size[1]+item_padding
            if podn < len(res['pod'])-1:
                draw.line((0,y_offset-item_padding/2,max_width,y_offset-item_padding/2),fill=(233,233,233),width=1)
        images.append(pod_img);

    # chained_imgs = list(itertools.chain.from_iterable(images))
    #
    widths, heights = zip(*(i.size for i in images))
    #
    max_width = max(widths)
    total_height = sum(heights)+item_padding*2

    # miscutils.partition_list(heights, )

    new_im = imgutils.round_rectangle((max_width, total_height), item_padding, "white")
    draw = ImageDraw.Draw(new_im)


    y_offset = item_padding
    for im in images:
        new_im.paste(im, (0,y_offset), im)
        y_offset+=im.size[1]
    new_im.save("data/wa_save.png")

    res_img = imgur_client.upload_image("data/wa_save.png", title=query)

    em = Embed(title=query, url=res_img.link, colour = 0xe4671b)
    em.set_image(url=res_img.link)
    await msgutils.edit_embed(bot, oldem, em)

message_handler.add(wolfram, r'(?:wolfram(?:alpha)?|wa) (?P<query>.+)')
print("\tWolfram Alpha Command Initialized")
