# @Author: Edmund Lam <edl>
# @Date:   15:55:15, 12-Aug-2018
# @Filename: wolframalpha.py
# @Last modified by:   edl
# @Last modified time: 14:31:51, 12-Oct-2019

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
    em = Embed(title=query, description="Requesting data", colour=miscutils.colours['orange'])
    oldem = await msgutils.send_embed(bot, msg, em)

    res = wa_client.query(query)

    if res.success.lower() == 'false': # if query fails
        em = Embed(title=query, description="No results", colour=miscutils.colours['orange'])
        await msgutils.edit_embed(bot, oldem, em)
        return

    em = Embed(title=query, description="Loading Images", colour=miscutils.colours['orange'])
    await msgutils.edit_embed(bot, oldem, em)

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
        pod_img = Image.new('RGBA', (max_width, total_height), (255,255,255,0))
        draw = ImageDraw.Draw(pod_img)

        y_offset = 0
        for line in t:
            draw.text((item_padding, y_offset), line, fill=(119, 165, 182), font=font)
            y_offset+=font_size+font_padding

        y_offset+=item_padding
        for im in subimgs:
            pod_img.paste(im, (item_padding,y_offset))
            y_offset += im.size[1]+item_padding
        images.append(pod_img);

    em = Embed(title=query, description="Combining Images", colour=miscutils.colours['orange'])
    await msgutils.edit_embed(bot, oldem, em)

    # chained_imgs = list(itertools.chain.from_iterable(images))
    #
    widths, heights = zip(*(i.size for i in images))
    #
    max_width = max(widths)+item_padding
    total_height = sum(heights)+item_padding*2

    partitioned_heights = miscutils.partition_list(heights, int((total_height*max_width)**0.5//max_width+1))
    partitions = [len(i) for i in partitioned_heights]
    sum_partitions = [sum(partitions[0:i]) for i in range(len(partitions)+1)]
    partitioned_widths = [max(widths[sum_partitions[i]:sum_partitions[i+1]]) for i in range(len(sum_partitions)-1)]

    max_height = max(sum(i) for i in partitioned_heights)+item_padding*2
    total_width = sum(partitioned_widths)+item_padding*2

    # miscutils.partition_list(heights, )

    new_im = imgutils.round_rectangle((total_width, max_height), item_padding, "white")
    draw = ImageDraw.Draw(new_im)

    x_offset = 0
    # for i in range(len(partitioned_widths))
    for i in range(len(partitioned_widths)):
        y_offset = item_padding
        for j in range(sum_partitions[i], sum_partitions[i+1]):
            im = images[j]
            new_im.paste(im, (x_offset,y_offset), im)
            y_offset+=im.size[1]
            if j < sum_partitions[i+1]-1: #draw horizontal line
                x1 = x_offset+item_padding/2
                x2 = x_offset+partitioned_widths[i]+item_padding/2
                y = y_offset-item_padding/2
                if i == 0:
                    x1 = 0
                elif i == len(partitioned_widths)-1:
                    x2 = total_width
                draw.line((x1,y,x2,y),fill=(233,233,233),width=1)
        if i < len(partitioned_widths)-1: #Draw vertical line
            x = x_offset+partitioned_widths[i]+item_padding/2
            draw.line((x,0,x,max_height),fill=(233,233,233),width=1)
        x_offset += partitioned_widths[i]
    new_im.save("data/wa_save.png")

    res_img = imgur_client.upload_image("data/wa_save.png", title=query)

    em = Embed(title=query, url=res_img.link, colour = miscutils.colours['orange'])
    em.set_image(url=res_img.link)
    await msgutils.edit_embed(bot, oldem, em)

message_handler.add(wolfram, r'(?:wolfram(?:alpha)?|wa) (?P<query>.+)')
print("\tWolfram Alpha Command Initialized")
