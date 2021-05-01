import cairosvg
import cv2
import numpy as np
from PIL import Image

board = 'ZoeaT'
board = 'ZoeaB'
board = 'HermitT'
# board = 'HermitB'
root = '/Users/akihiro/repos/Hermit/{}/'.format( board )
path_svg = root + 'layer/{}-Edge_Cuts.svg'.format( board )
path_png = root + 'svg.png'
path_txt = root + 'Edge_Fill.txt'
path_test = root + 'test.png'
cairosvg.svg2png( url = path_svg, write_to = path_png, dpi = 254 )

png = Image.open( path_png )
print( f'png size = {png.size}' )
# voi: x width
x0 = png.size[0]
x1 = 0
for x in range( png.size[0] ):
    for y in range( 0, png.size[1], 5 ):
        _, _, _, a = png.getpixel( (x, y) )
        a = 255 if a >= 128 else 0
        if a == 255:
            x0 = min( x0, x )
            x1 = max( x1, x )
            break
x0 -= 1
x1 += 1
# x0 = max( x0, 0 )
# x1 = min( x1, png.size[0] - 1 )
w = x1 - x0
print( "x = ({}, {}), width = {}".format( x0, x1, w ) )

# voi: y height
y0 = png.size[1]
y1 = 0
for y in range( png.size[1] ):
    for x in range( 0, png.size[0], 5 ):
        _, _, _, a = png.getpixel( (x, y) )
        a = 255 if a >= 128 else 0
        if a == 255:
            y0 = min( y0, y )
            y1 = max( y1, y )
            break
y0 -= 1
y1 += 1
# y0 = max( y0, 0 )
# y1 = min( y1, png.size[1] - 1 )
h = y1 - y0
print( "y = ({}, {}), height = {}".format( y0, y1, h ) )

mask = np.zeros( (h, w), np.uint8 )
for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        if 0 <= x and x < png.size[0] and 0 <= y and y < png.size[1]:
            _, _, _, a = png.getpixel( (x, y) )
        else:
            a = 0
        v = 0 if a >= 64 else 255
        mask[y - y0, x - x0] = v

if False:
    retval, labels = cv2.connectedComponents( mask )
    label = labels[h >> 1, w >> 1]
    print( f'#labels = {retval}, label = {label}' )
else:
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats( mask )
    total_area = w * h
    max_area = -1
    for idx, (x, y, _, _, area) in enumerate( stats ):
        if area > total_area / 8:
            print( f'idx = {idx}, area = {area} total = {total_area}' )
        if max_area < area:
            max_area = area
            label = idx
    print( f'#labels = {retval}, label = {label}, max_area = {max_area}' )
#fill_mask = np.zeros( (h + 2, w + 2), np.uint8 )
#cv2.floodFill( mask, fill_mask, (h >> 1, w >> 1), 255, 0, 128, 4 | cv2.FLOODFILL_FIXED_RANGE )

mask1 = np.zeros( (h, w), np.uint8 )
mask2 = np.zeros( (h, w), np.uint8 )
for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        inside = (labels[y - y0, x - x0] == label)
        mask1[y - y0, x - x0] = 255 if inside else 0
        mask2[y - y0, x - x0] = 0 if inside else 255
print( 'done largest label mask' )

dist1 = cv2.distanceTransform( mask1, cv2.DIST_L2, cv2.DIST_MASK_PRECISE )
dist2 = cv2.distanceTransform( mask2, cv2.DIST_L2, cv2.DIST_MASK_PRECISE )
dist1 = cv2.GaussianBlur( dist1, ksize = (7, 7), sigmaX = 0.7 )
dist2 = cv2.GaussianBlur( dist2, ksize = (7, 7), sigmaX = 0.7 )
print( 'done distance transform' )

# test = Image.new( 'RGB', (w, h) )
test = np.empty((h, w, 3), np.uint8)
for y in range( y0, y1 ):
    for x in range( x0, x1 ):
        inside = True if mask1[y - y0, x - x0] != 0 else False
        val = dist1[y - y0, x - x0] if inside else dist2[y - y0, x - x0]
        val = int( round( val * 3 ) )
        val = min( max( val, 0), 255 )
        r = 255 if inside else 0
        b = 0 if inside else 255
        g = val
        # test.putpixel( (x - x0, y - y0), (r, g, b))
        test[y - y0, x - x0, 0] = r
        test[y - y0, x - x0, 1] = g
        test[y - y0, x - x0, 2] = b
test = Image.fromarray( test )
test.save( path_test )
print( f'saved {path_test}' )

# dump to text file
with open( path_txt, 'w' ) as fout:
    fout.write( '{}\n'.format( w ) )
    fout.write( '{}\n'.format( h ) )
    for y in range( y0, y1 ):
        line = ''
        for x in range( x0, x1 ):
            inside = True if mask1[y - y0, x - x0] != 0 else False
            val = dist1[y - y0, x - x0] if inside else -dist2[y - y0, x - x0]
            line += '{:.0f},'.format( val * 10 )
        fout.write( line + '\n' )
print( f'saved {path_txt}' )
