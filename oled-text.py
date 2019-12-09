# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import select
import math
import time
import os
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as this python script!
# Some nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 18)

# Create drawing object.
draw = ImageDraw.Draw(image)
# Define text and get total width.
firstLine = ''
secondLine = ''
thirdLine = ''

lineHeight = 18
interline = 4
# Animate text moving in sine wave.
firstPos = 0
secondPos = 0
thirdPos = 0
firstScroll = 'A'
secondScroll = 'A'
thirdScroll = 'A'
print('READY')
while True:
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line:
            print('FREE')
            sys.stdout.flush()
            if line[0] == '1':
                firstScroll = line[1]
                firstPos=0
                firstLine = line[2:len(line)]
            if line[0] == '2':
                secondScroll = line[1]
                secondPos=0
                secondLine = line[2:len(line)]
            if line[0] == '3':
                thirdScroll = line[1]
                thirdPos=0
                thirdLine = line[2:len(line)]
        else: # an empty line means stdin has been closed
            print('closed from python')
            exit(0)
    else:
        sys.stdout.flush()
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Enumerate characters and draw them offset vertically based on a sine wave.
        maxwidth, unused = draw.textsize(firstLine, font=font)
        x = firstPos
        for i, c in enumerate(firstLine):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            # Draw text.
            draw.text((x, 0), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        if firstPos < -maxwidth:
            firstPos = width
        maxwidth, unused = draw.textsize(secondLine, font=font)
        x = secondPos
        for i, c in enumerate(secondLine):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            # Draw text.
            draw.text((x, lineHeight+interline), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        if secondPos < -maxwidth:
            secondPos = width
        maxwidth, unused = draw.textsize(thirdLine, font=font)
        x = thirdPos
        for i, c in enumerate(thirdLine):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            # Draw text.
            draw.text((x, lineHeight*2+interline*2), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            if thirdPos < -maxwidth:
                thirdPos = width
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        if len(firstLine)>0 or len(secondLine)>0 or len(thirdLine)>0:
            disp.image(image)
            disp.display()
        # Move position for next frame.
        # print(width)
        if firstScroll == '1' or (firstScroll == 'A' and draw.textsize(firstLine, font=font)[0] > width):
            firstPos += -2
        if secondScroll == '1' or (secondScroll == 'A' and draw.textsize(secondLine, font=font)[0] > width):
            secondPos += -2
        if thirdScroll == '1' or (thirdScroll == 'A' and draw.textsize(thirdLine, font=font)[0] > width):
            thirdPos += -2

        # Pause briefly before drawing next frame.
        time.sleep(0.001)
