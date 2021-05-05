import cairosvg
import cv2
import numpy as np
from PIL import Image

board = 'ZoeaT'
board = 'ZoeaB'
board = 'HermitT'
board = 'HermitB'
layer = 'Edge_Cuts'
root = '/Users/akihiro/repos/Hermit/{}/'.format( board )
path_svg = root + 'layer/{}-{}.svg'.format( board, layer )
path_png = root + 'svg.png'
path_txt = root + 'Edge_Fill.txt'
path_dist = root + 'dist.png'
cairosvg.svg2png( url = path_svg, write_to = path_png, dpi = 254 )
if True:
    png = Image.open( path_png )
    cairosvg.svg2png( url = path_svg, write_to = path_png, dpi = 254,
        output_width = png.size[0] + 2, output_height = png.size[1] + 2 )

png = Image.open( path_png )
print( f'png size = {png.size}' )
# voi: x width
ix0 = png.size[0]
ix1 = 0
for ix in range( png.size[0] ):
    for iy in range( 0, png.size[1], 5 ):
        _, _, _, a = png.getpixel( (ix, iy) )
        a = 255 if a >= 128 else 0
        if a == 255:
            ix0 = min( ix0, ix )
            ix1 = max( ix1, ix )
            break
ix0 -= 1
ix1 += 1
w = ix1 - ix0 + 1
print( "ix = ({}, {}), width = {}".format( ix0, ix1, w ) )

# voi: y height
iy0 = png.size[1]
iy1 = 0
for iy in range( png.size[1] ):
    for ix in range( 0, png.size[0], 5 ):
        _, _, _, a = png.getpixel( (ix, iy) )
        a = 255 if a >= 128 else 0
        if a == 255:
            iy0 = min( iy0, iy )
            iy1 = max( iy1, iy )
            break
iy0 -= 1
iy1 += 1
h = iy1 - iy0 + 1
print( "iy = ({}, {}), height = {}".format( iy0, iy1, h ) )

mask = np.zeros( (h, w), np.uint8 )
for y in range( h ):
    iy = y + iy0
    for x in range( w ):
        ix = x + ix0
        if 0 <= ix and ix < png.size[0] and 0 <= iy and iy < png.size[1]:
            _, _, _, a = png.getpixel( (ix, iy) )
        else:
            a = 0
        v = 0 if a >= 64 else 255
        mask[y, x] = v

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
for y in range( h ):
    for x in range( w ):
        inside = (labels[y, x] == label)
        mask1[y, x] = 255 if inside else 0
        mask2[y, x] = 0 if inside else 255
print( 'done largest label mask' )

dist1 = cv2.distanceTransform( mask1, cv2.DIST_L2, cv2.DIST_MASK_PRECISE )
dist2 = cv2.distanceTransform( mask2, cv2.DIST_L2, cv2.DIST_MASK_PRECISE )
dist1 = cv2.GaussianBlur( dist1, ksize = (7, 7), sigmaX = 0.7 )
dist2 = cv2.GaussianBlur( dist2, ksize = (7, 7), sigmaX = 0.7 )
print( 'done distance transform' )

# dist = Image.new( 'RGB', (w, h) )
dist = np.empty((h, w, 3), np.uint8)
for y in range( h ):
    for x in range( w ):
        inside = True if mask1[y, x] != 0 else False
        val = dist1[y, x] if inside else dist2[y, x]
        val = int( round( val * 3 ) )
        val = min( max( val, 0), 255 )
        r = 255 if inside else 0
        b = 0 if inside else 255
        g = val
        # dist.putpixel( (x, y), (r, g, b))
        dist[y, x, 0] = r
        dist[y, x, 1] = g
        dist[y, x, 2] = b
dist = Image.fromarray( dist )
dist.save( path_dist )
print( f'saved {path_dist}' )

# dump to text file
with open( path_txt, 'w' ) as fout:
    fout.write( '{}\n'.format( w ) )
    fout.write( '{}\n'.format( h ) )
    for y in range( h ):
        line = ''
        for x in range( w ):
            inside = True if mask1[y, x] != 0 else False
            val = dist1[y, x] if inside else -dist2[y, x]
            line += '{:.0f},'.format( val * 10 )
        fout.write( line + '\n' )
print( f'saved {path_txt}' )
