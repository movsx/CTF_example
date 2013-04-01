# -*- coding: utf-8 -*-
from PIL import Image
import os

def get_pixels(pixels, y, x): # получить характеристики точки
    red_pix = pixels[x, y][0]
    green_pix = pixels[x, y][1]
    blue_pix = pixels[x, y][2]
    #alpha_pix = pixels[x, y][3] # для jpg не работает
    lsb = bin(red_pix)[-2] or bin(blue_pix)[-2] or bin(green_pix)[-2]  # Get the LSB
    return (red_pix, green_pix, blue_pix)

# Delta между двумя одинаковыми точками
def diff_images(steg_pixels, orig_pixels, y, x):
    return tuple(map(lambda p, t: abs(p-t), get_pixels(steg_pixels, y, x), get_pixels(orig_pixels, y, x)))

### Блок для открытия файла, его загрузки и печати пикселей
# Примеры работы с функциями графической библиотеки PIL
def load_image_file():
    im = Image.open('b.jpg', 'r') # Открыть изображение в режиме для чтени
    pixels = im.load()
    width, height = im.size # получить размер картинки в pixel
    # пройтись по каждому пикселю, просто определить цвета
    for y in xrange(height): # Iterate through each pixel
        for x in xrange(width):
            print get_pixels(pixels, y,x)

### Блок для накладывания первой картинки на вторую
# картинка-задача http://dl.dropbox.com/u/17463542/forensics/b.jpg
# картинка-оригинал http://dl.dropbox.com/u/17463542/forensics/c.jpg
def xor_image_file():
    im = Image.open('b.jpg', 'r') # Открыть изображение в режиме для чтени
    pixels = im.load()
    width, height = im.size # получить размер картинки в pixel
    im2 = Image.open('c.jpg', 'r') # Открыть изображение в режиме для чтени
    pixels2 = im2.load()
    width2, height2 = im2.size # получить размер картинки в pixel
    new=Image.new("RGB",(width,height))
    for y in xrange(height): # Iterate through each pixel
        for x in xrange(width):
            new.putpixel((x,y), diff_images(pixels, pixels2, y,x))
    new.save("end.png")


BPP = 4
### Блок для примера работы с техникой bits-per-pixel
def example_bpp():
    with open('image_diff.png','rb') as f:
        image = f.read()
    bts = []
    [bts.extend([b for b in '00000000'[len(bin(ord(c))[2:]):] + bin(ord(c))[2:]]) for c in image]
    with open('out.raw', 'wb') as f:
        for i in range(len(bts) // BPP):
            chunk = ''.join(bts[i * BPP : (i + 1) * BPP])
            f.write(chr(int(chunk, 2)))

xor_image_file()

#example_bpp()


"""
#### This just converts the binary to ASCII
answer = ''
for i in xrange(len(binary_ans)/8):
    answer += chr(int(binary_ans[i*8:i*8+8], 2))
f=open('answer.txt','w')
f.write(answer)
f.close()
print answer
"""
