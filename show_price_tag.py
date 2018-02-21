# coding=utf-8

import sys
import numpy
import colorsys
import epd2in13b
from os import path
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageEnhance

E_PAPER_WIDTH = 104
E_PAPER_HEIGHT = 212

FONT_PATH = path.dirname(path.abspath(__file__)) + '/mplus-2p-regular.ttf'


def create_blank_image():
    image = Image.new("RGB", (E_PAPER_HEIGHT, E_PAPER_WIDTH), (255, 255, 255))
    return image


def add_header(image, text):
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, E_PAPER_HEIGHT, 24), fill=(0, 0, 0))

    draw.font = ImageFont.truetype(FONT_PATH, 22, encoding='unic')

    img_size = numpy.array((E_PAPER_HEIGHT, 24))
    txt_size = numpy.array(draw.font.getsize(text))
    pos = (img_size - txt_size) / 2
    draw.text(pos, text, (255, 255, 255))

    # make it bold
    pos = pos + (1, 0)
    draw.text(pos, text, (255, 255, 255))

    return image


def add_title(image, text):
    draw = ImageDraw.Draw(image)

    draw.font = ImageFont.truetype(FONT_PATH, 30, encoding='unic')

    draw.text((0, 24 + (35 - draw.font.getsize(text)
                        [1]) / 2), text, (0, 0, 0))

    # make it bold
    draw.text((1, 24 + (35 - draw.font.getsize(text)
                        [1]) / 2), text, (0, 0, 0))

    return image


def add_subtitle(image, text):
    draw = ImageDraw.Draw(image)

    draw.font = ImageFont.truetype(FONT_PATH, 16, encoding='unic')

    draw.text((0, 24 + 35 + (10 - draw.font.getsize(text)
                             [1]) / 2), text, (0, 0, 0))

    # make it bold
    draw.text((1, 24 + 35 + (10 - draw.font.getsize(text)
                             [1]) / 2), text, (0, 0, 0))

    return image


def add_price(image, text):
    draw = ImageDraw.Draw(image)

    draw.font = ImageFont.truetype(FONT_PATH, 30, encoding='unic')

    draw.text((E_PAPER_HEIGHT - draw.font.getsize(text)
               [0], 24 + 35 + 10 + (35 - draw.font.getsize(text)[1]) / 2), text, (0, 0, 0))

    # make it bold
    draw.text((E_PAPER_HEIGHT - draw.font.getsize(text)
               [0] - 1, 24 + 35 + 10 + (35 - draw.font.getsize(text)[1]) / 2), text, (0, 0, 0))

    return image


def show_image(black_image, red_image):
    epd = epd2in13b.EPD()
    epd.init()

    frame_black = epd.get_frame_buffer(black_image)
    frame_red = epd.get_frame_buffer(red_image)
    epd.display_frame(frame_black, frame_red)


if __name__ == '__main__':
    black_image = create_blank_image()
    red_image = create_blank_image()

    red_image = add_header(red_image, sys.argv[1].decode('utf-8'))
    black_image = add_title(black_image, sys.argv[2].decode('utf-8'))
    black_image = add_subtitle(black_image, sys.argv[3].decode('utf-8'))
    red_image = add_price(red_image, sys.argv[4].decode('utf-8'))

    black_image = black_image.rotate(270, expand=True)
    red_image = red_image.rotate(270, expand=True)

    show_image(black_image, red_image)
