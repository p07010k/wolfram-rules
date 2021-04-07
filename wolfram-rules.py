# -*- coding: utf-8 -*-
"""
Creating a picture of Wolfram rule

Author:  @pnqke

2020-07-28
"""
from PIL import Image, ImageDraw
from random import random
from itertools import product
from datetime import datetime


DEFAULT_RULE = 30
WIDTH = 256
HEIGHT = 256
RC = 5  # resize coefficient
COLOR_0 = (255, 255, 255)
COLOR_1 = (0, 0, 0)
INIT_DENS = 0.8


def main(rule):
    # A bool list out of int rule
    ruleTF = [(rule//(2**i) % 2) == 1 for i in range(8)]
    
    # An empty bool 2D list as a canvas  
    canvas = [[False] * WIDTH] * HEIGHT
    h, w = len(canvas), len(canvas[0])
    
    # Fill initial row with random dots
    canvas[0] = [random() < INIT_DENS for i in range(w)]
    
    # Calculating following rows
    for j in range(1, h):
        # neighbors upstairs
        neibs = [canvas[j-1][k] for k in (w-1, 0, 1)]
        row = []
        
        for i in range(w):
            # applying the rule
            rule_digit = 4*neibs[0] + 2*neibs[1] + neibs[2]
            row.append(ruleTF[rule_digit])
            
            # shift neibours
            neibs.pop(0)
            neibs.append(canvas[j-1][(i+1) % w])
        
        canvas[j] = row
        
    # Drawing an image out of canvas
    img = Image.new("RGB", (w*RC, h*RC), COLOR_0)
    img_drw = ImageDraw.Draw(img)
    for i, j in product(range(w), range(h)):
        if canvas[j][i]:
            shape = [(i*RC, j*RC), ((i+1)*RC-1, (j+1)*RC-1)]
            img_drw.rectangle(shape, COLOR_1)  # shape, fill, outline
            #img.putpixel((i, j), COLOR_1)
    
    # Saving image
    cur_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "rule_{}_{}.png".format(rule, cur_time)
    img.save(filename, "PNG")
    print("The picture is saved as '{}'".format(filename))


if __name__ == '__main__':
    # Input rule number
    #  IDEA: input canvas size, init_dens, colors, resize coeff
    try:
        rule = int(input())
    except:
        rule = DEFAULT_RULE
    
    main(rule)