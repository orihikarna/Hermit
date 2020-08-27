import cairosvg
from PIL import Image

root = '/Users/akihiro/repos/Hermit/ZoeaT/'
path_svg = root + 'layer/ZoeaT-B_Cu.svg'
path_png = root + 'svg.png'
path_txt = root + 'B_Cu_fill.txt'
cairosvg.svg2png( url = path_svg, write_to = path_png, dpi = 254 )

image = Image.open( path_png )
size = image.size

# voi: x width
y = int( size[1] / 2 )
x0 = size[0]
x1 = 0
prev_a = 0
for x in range( size[0] ):
    r, g, b, a = image.getpixel( (x, y) )
    a = 255 if a >= 128 else 0
    if prev_a != a:
        prev_a = a
        #print( x, a )
    if a == 255:
        x0 = min( x0, x )
        x1 = max( x1, x )
w = x1 - x0
print( "x = ({}, {}), width = {}".format( x0, x1, w ) )

# voi: y height
x = int( round( x0 + (x1 - x0) / 6 ) )
y0 = size[1]
y1 = 0
prev_a = 0
for y in range( size[1] ):
    r, g, b, a = image.getpixel( (x, y) )
    a = 255 if a >= 128 else 0
    if prev_a != a:
        prev_a = a
        #print( y, a )
    if a == 255:
        y0 = min( y0, y )
        y1 = max( y1, y )
h = y1 - y0
print( "y = ({}, {}), height = {}".format( y0, y1, h ) )

#
with open( path_txt, 'w' ) as fout:
    fout.write( '{}\n'.format( w ) )
    fout.write( '{}\n'.format( h ) )
    for y in range( y0, y1 ):
        line = ''
        for x in range( x0, x1 ):
            r, g, b, a = image.getpixel( (x, y) )
            a = 255 if a >= 128 and max( r, g, b ) < 128 else 0
            line += '0' if a == 0 else '1'
        fout.write( line + '\n' )
