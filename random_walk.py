#!/usr/bin/env python

import io
import random
import numpy as np
from PIL import Image

def makeImage(arr, filepath):
    image = Image.fromarray(arr)
    if image.mode != 'RGB':
        image.convert('HSV')
    image.save(filepath, format='BMP')
    '''
    with io.BytesIO() as f:
        image.save(f, format='BMP')
        send_to_device(f);
    '''

def nextColor(color, step):
    #ret = np.zeros((3,), dtype=np.uint8)
    ret = np.copy(color)
    which = np.uint8(random.random() * 3)
    f = float(color[which]) + random.random() * step[0]
    if f > 255 or f < 0:
        step[0] = -step[0]
        f = float(color[which]) + random.random() * step[0]
    ret[which] = f
    #ret[which] = np.uint8((float(color[which]) + random.random() * step) % 255)
    return ret

'''
def nextColor(color, step):
    i = (np.uint32(color[2]) << 16) + (np.uint32(color[1]) << 8) + (np.uint32(color[0]))
    i = i + np.uint32(step)
    ret = np.zeros((3,), dtype=np.uint8)
    ret[0] = np.uint8(i & 255)
    ret[1] = np.uint8((i >> 8) & 255)
    ret[2] = np.uint8((i >> 16) & 255)
    return ret
'''


'''
def nextColor(color, step):
    ret = np.zeros((3,), dtype=np.uint8)
    if color[0] > 255 - step:
        if color[1] > 255 - step:
            if color[2] > 255 - step:
                ret[2] = color[2] - (255 - step)
                ret[1] = color[1] - (255 - step)
                ret[0] = color[0] - (255 - step)
            else:
                ret[2] = color[2] + step
                ret[1] = color[1]
                ret[0] = color[0]
        else:
            ret[2] = color[2]
            ret[1] = color[1] + step
            ret[0] = color[0]
    else:
        ret[2] = color[2]
        ret[1] = color[1]
        ret[0] = color[0] + step
    return ret
'''

'''
def nextColor(color, step):
    cmax = max(color)
    cmin = min(color)
    diff = float(cmax-cmin)
    h = 0
    r = float(color[0])
    g = float(color[1])
    b = float(color[2])
    if cmax == 0 and cmin == 0:
        h = step
    elif cmax == r:
        h = (60 * ((g-b)/diff)+360 + step) % 360
    elif cmax == g:
        h = (60 * ((b-r)/diff)+120 + step) % 360
    elif cmax == b:
        h = (60 * ((r-g)/diff)+240 + step) % 360
    x = 1-abs(((h/60)%2-1))
    ret = np.zeros((3,), dtype=np.float)
    if h < 60:
        ret[0], ret[1], ret[2] = 1, x, 0
    elif h < 120:
        ret[0], ret[1], ret[2] = x, 1, 0
    elif h < 180:
        ret[0], ret[1], ret[2] = 0, 1, x
    elif h < 240:
        ret[0], ret[1], ret[2] = 0, x, 1
    elif h < 300:
        ret[0], ret[1], ret[2] = x, 0, 1
    elif h < 360:
        ret[0], ret[1], ret[2] = 1, 0, x
    ret = ret * 255
    ret = ret.astype(np.uint8)
    return ret
'''

def neighbor_coord(coord, which, xmax, ymax, visited):
    x = coord[0]
    y = coord[1]
    neighbor_coords = [
            (x % xmax, (y - 1) % ymax),
            ((x - 1) % xmax, y % ymax),
            ((x + 1) % xmax, y % ymax),
            (x % xmax, (y + 1) % ymax)
    ]
    uv_neighbor_coords = []
    for nc in neighbor_coords:
        if not visited[nc[0]][nc[1]]:
            uv_neighbor_coords.append(nc)
    if uv_neighbor_coords:
        return uv_neighbor_coords[int(which * len(uv_neighbor_coords))]
    else:
        return None

def visit(coord, xmax, ymax, visited, img, color):
    x = coord[0]
    y = coord[1]
    visited[x][y] = True
    img[x][y] = color
    '''
    to_visit = neighbor_coord(coord, random.random(), xmax, ymax, visited)
    while to_visit is not None:
        visit(to_visit, xmax, ymax, visited, img, nextColor(color, 5))
        to_visit = neighbor_coord(coord, random.random(), xmax, ymax, visited)
    return
    '''

def random_walk(xmax, ymax, step, r, g, b):
    step = [step]
    img = np.zeros((xmax, ymax, 3,), dtype=np.uint8)
    visited = np.zeros((xmax, ymax), dtype=np.bool_)
    color = np.copy(img[0][0])
    color = (r, g, b)
    coord = (int(xmax * random.random()), int(ymax * random.random()))
    visit(coord, xmax, ymax, visited, img, color)
    to_visit = [coord]
    while to_visit:
        coord = to_visit[-1]
        if not visited[coord[0]][coord[1]]: # Remove this if you want to trace over old stuff
            visit(coord, xmax, ymax, visited, img, color)
        #visit(coord, xmax, ymax, visited, img, color)
        next_coord = neighbor_coord(coord, random.random(), xmax, ymax, visited)
        if next_coord is None:
            to_visit.pop()
        else:
            to_visit.append(next_coord)
        color = nextColor(color, step)

    return img


def main():
    makeImage(random_walk(2160, 1080, 2, 0, 0, 255), 'phone_wallpaper.bmp')

main()
