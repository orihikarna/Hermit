import cairosvg
import cv2
import numpy as np
from PIL import Image

board = 'ZoeaT'
board = 'ZoeaB'
root = '/Users/akihiro/repos/Hermit/{}/'.format( board )
path_svg = root + 'layer/{}-Edge_Cuts.svg'.format( board )
path_png = root + 'svg.png'
path_txt = root + 'Edge_Fill.txt'
path_test = root + 'test.png'
cairosvg.svg2png( url = path_svg, write_to = path_png, dpi = 254 )

png = Image.open( path_png )

# voi: x width
y = int( png.size[1] / 2 )
x0 = png.size[0]
x1 = 0
prev_a = 0
for x in range( png.size[0] ):
    r, g, b, a = png.getpixel( (x, y) )
    a = 255 if a >= 128 else 0
    if prev_a != a:
        prev_a = a
        #print( x, a )
    if a == 255:
        x0 = min( x0, x )
        x1 = max( x1, x )
x0 = max( x0 - 1, 0 )
x1 = min( x1 + 1, png.size[0] - 1 )
w = x1 - x0
print( "x = ({}, {}), width = {}".format( x0, x1, w ) )

# voi: y height
x = int( round( x0 + (x1 - x0) / 6 ) )
y0 = png.size[1]
y1 = 0
prev_a = 0
for y in range( png.size[1] ):
    r, g, b, a = png.getpixel( (x, y) )
    a = 255 if a >= 128 else 0
    if prev_a != a:
        prev_a = a
        #print( y, a )
    if a == 255:
        y0 = min( y0, y )
        y1 = max( y1, y )
y0 = max( y0 - 1, 0 )
y1 = min( y1 + 1, png.size[1] - 1 )
h = y1 - y0
print( "y = ({}, {}), height = {}".format( y0, y1, h ) )

mask = np.zeros( (h, w), np.uint8 )
for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        r, g, b, a = png.getpixel( (x, y) )
        v = 0 if a >= 64 else 255
        mask[y - y0, x - x0] = v

retval, labels = cv2.connectedComponents( mask )
label = labels[h >> 1, w >> 1]
#fill_mask = np.zeros( (h + 2, w + 2), np.uint8 )
#cv2.floodFill( mask, fill_mask, (h >> 1, w >> 1), 255, 0, 128, 4 | cv2.FLOODFILL_FIXED_RANGE )

for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        mask[y - y0, x - x0] = 255 if labels[y - y0, x - x0] == label else 0

dist = cv2.distanceTransform( mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE )

test = Image.new( 'RGB', (w, h) )
for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        r = 0 if mask[y - y0, x - x0] == 0 else 255
        g = min( int( round( dist[y - y0, x - x0] * 2 ) ), 255 )
        b = 0
        test.putpixel( (x - x0, y - y0), (r, g, b))
test.save( path_test )

# dump to text file
with open( path_txt, 'w' ) as fout:
    fout.write( '{}\n'.format( w ) )
    fout.write( '{}\n'.format( h ) )
    for y in range( y0, y1 ):
        line = ''
        for x in range( x0, x1 ):
            # r, g, b, a = png.getpixel( (x, y) )
            # a = 255 if a >= 128 and max( r, g, b ) < 128 else 0
            v = dist[y - y0, x - x0]
            line += '{:.0f},'.format( v )
        fout.write( line + '\n' )
