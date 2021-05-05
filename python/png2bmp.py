import cairosvg
import cv2
import numpy as np
import sys
from PIL import Image

board = 'stm32tiny'
layer = 'F_Paste'
# layer = 'B_Paste'
root = '/Users/akihiro/repos/Hermit/{}/'.format( board )
path_png = root + 'layer/{}-{}.png'.format( board, layer )
path_bmp = root + 'layer/{}-{}.bmp'.format( board, layer )

if __name__ == '__main__':
    png = Image.open( path_png )
    w, h = png.size
    print( f'png size = {w} x {h}' )
    w2 = int( (w + 7) / 8 ) * 8
    h2 = int( (h + 7) / 8 ) * 8
    print( f'png size2 = {w2} x {h2}' )

    r, g, b, a = png.split()
    print( type( a ) )
    # img = Image.merge("RGB", (r, g, b))
    v = np.array( a )
    v = 255 - v
    a = Image.fromarray( v )
    img = Image.merge("RGB", (a, a, a))
    bmp = Image.new("RGB", (w2, h2), (255, 255, 255))
    bmp.paste( img, ((w2 - w) >> 1, (h2 - h) >> 1) )
    bmp.save( path_bmp )
