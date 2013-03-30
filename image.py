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
    return tuple(map(lambda x, y: x^y, get_pixels(steg_pixels, y, x), get_pixels(orig_pixels, y, x)))

### Блок для открытия файла, его загрузки и печати пикселей
# Примеры работы с функциями графической библиотеки PIL
im = Image.open('b.jpg', 'r') # Открыть изображение в режиме для чтени
pixels = im.load()
width, height = im.size # получить размер картинки в pixel

# пройтись по каждому пикселю, просто определить цвета
#for y in xrange(height): # Iterate through each pixel
#    for x in xrange(width):
#        print get_pixels(pixels, y,x)

### Блок для накладывания первой картинки на вторую
im2 = Image.open('c.jpg', 'r') # Открыть изображение в режиме для чтени
pixels2 = im2.load()
width2, height2 = im2.size # получить размер картинки в pixel
new=Image.new("RGB",(width,height))
for y in xrange(height): # Iterate through each pixel
    for x in xrange(width):
        new.putpixel((x,y), diff_images(pixels, pixels2, y,x))
new.save("end.png")



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
