import json
import math
import numpy as np
import os
import sys
import collections
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import red, black, white
from reportlab.lib.units import mm

rad2deg = 180 / math.pi
deg2rad = math.pi / 180

anti_alias_scaling = 4

fontpath = "/System/Library/Fonts/Courier.dfont"
font = ImageFont.truetype( fontpath, size = 28 * anti_alias_scaling )

def vec2( x, y ):
    return np.array( [x, y] )

def vec2_find_intersection( p0, t0, p1, t1, tolerance = 1 ):
    A = vec2( t0, t1 )
    R = np.linalg.inv( A )
    B = p1 - p0
    k0, k1 = B @ R
    q0 =  k0 * t0 + p0
    q1 = -k1 * t1 + p1
    dq = np.linalg.norm( q0 - q1 )
    if dq > 1e-3:
        print( 'ERROR |q0 - q1| = {}'.format( dq ) )
    return (q1, k0, -k1)

def vec2_rotate( vec, angle ):
    th = angle * deg2rad
    co = math.cos( th )
    si = math.sin( th )
    nxvec = co * vec[0] - si * vec[1]
    nyvec = si * vec[0] + co * vec[1]
    return (nxvec, nyvec)

def mat2_rot( deg ):
    th = deg / 180 * np.pi
    c = np.cos( th )
    s = np.sin( th )
    return np.array([[c, s], [-s, c]])

def round_corner( radius, fill ):
    """Draw a round corner"""
    corner = Image.new( 'RGBA', (radius, radius), (0, 0, 0, 0) )
    draw = ImageDraw.Draw( corner )
    draw.pieslice( (0, 0, radius * 2, radius * 2), 180, 270, fill = fill )
    return corner

def get_key_image( size, radius, name, fill ):
    """Draw a rounded rectangle"""
    w, h = size[0], size[1]
    sz = int( max( w, h ) * 1.5 )
    rect = Image.new( 'RGBA', (sz, sz), (255, 255, 255, 0) )
    draw = ImageDraw.Draw( rect )
    mx = int( (sz - w) / 2 )
    my = int( (sz - h) / 2 )
    draw.rectangle( (mx, my + radius, mx + w, my + h - radius), fill = fill )
    draw.rectangle( (mx + radius, my, mx + w - radius, my + h), fill = fill )
    corner = round_corner( radius, fill )
    rect.paste( corner, (mx, my) )
    rect.paste( corner.rotate(  90 ), (mx, my + h - radius) )# Rotate the corner and paste it
    rect.paste( corner.rotate( 180 ), (mx + w - radius, my + h - radius) )
    rect.paste( corner.rotate( 270 ), (mx + w - radius, my) )
    # name
    tw, th = draw.textsize( name, font )
    draw.text( (sz / 2 - tw / 2, sz / 2 - th / 2), name, "DarkSlateGrey", font )
    return rect, sz

class keyboard_key:
    def __init__( self, name, prop ):
        self.name = name
        self.prop = prop
        self.x = self.getProperty( "x", 0 )
        self.y = self.getProperty( "y", 0 )
        self.rx = self.getProperty( "rx", 0 )
        self.ry = self.getProperty( "ry", 0 )
        self.r = self.getProperty( "r", 0 )
        self.w = self.getProperty( "w", 1 )
        self.h = self.getProperty( "h", 1 )

    def getProperty( self, key: str, default_value ):
        return self.prop[key] if key in self.prop else default_value

class keyboard_layout:
    def __init__( self ):
        self.meta = {}
        self.keys = []

    def print( self ):
        for k, v in self.meta.items():
            print( "meta: {} -> {}".format( k, v ) )
        keys = []
        for key in self.keys:
            ps = ""
            for k, v in key.prop.items():
                if v != 0:
                    ps += ", {}={}".format( k, v )
            name = key.name.replace( '\n', ',' )
            #print( "key '{}' {}".format( name, ps[2:] ) )
            # if name in ['M', '<,,', '>,.', '?,/']:# for Zoea
            if True:
                (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
                px = x - rx + w / 2
                py = y - ry + h / 2
                q = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
                keys.append( (name, q, r) )
        max_x = max( map( lambda vals: vals[1][0], keys ) )
        min_y = min( map( lambda vals: vals[1][1], keys ) )
        keys.sort( key = lambda vals: -vals[1][0] )
        for name, q, r in keys:
            print( "    ['{}', {:.3f}, {:.3f}, {:.1f}],".format( name[-1], (q[0] - max_x), (q[1] - min_y), r ) )

    def write_png( self, path: str, unit, thickness, paper_size ):
        # 2560 x 1600, 286mm x 179mm, MacBook size
        scale = 2560.0 / 286.0 / 2 * anti_alias_scaling
        size = scale * paper_size
        L = scale * unit
        Th = thickness / unit

        image = Image.new( 'RGBA', (math.ceil( size[0] ), math.ceil( size[1] )), ( 255, 255, 255, 255 ) )
        draw = ImageDraw.Draw( image )
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)

            if False:
                pnts = []
                th = Th
                th = 0
                for dx, dy in [vec2( 0, 0 ), vec2( 1, 0 ), vec2( 1, 1 ), vec2( 0, 1 )]:
                    px = x - rx + th + (w - 2 * th) * dx
                    py = y - ry + th + (h - 2 * th) * dy
                    q = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
                    t = L * q
                    pnts.append( (t[0], t[1]) )
                draw.polygon( pnts, outline = ( 0, 0, 0 ) )

            px = x - rx + w / 2
            py = y - ry + h / 2
            q = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
            t = L * q

            if True:
                dim = vec2( w - 2 * Th, h - 2 * Th ) * L
                key_image, rsz = get_key_image( (int( dim[0] ), int( dim[1] )), int( L/12 ), key.name, "DarkTurquoise" )
                key_image = key_image.rotate( -r )
                pos = t - vec2( rsz, rsz ) / 2
                image.paste( key_image, (int( pos[0] ), int( pos[1] )), key_image )

            if False:
                tx, ty = t[0], t[1]
                tw, th = draw.textsize( key.name, font )
                draw.text( (tx - tw / 2, ty - th / 2), key.name, ( 0, 0, 0 ), font )
        xsize = round( size[0] / anti_alias_scaling )
        ysize = round( size[1] / anti_alias_scaling )
        image = image.resize( (xsize, ysize), Image.ANTIALIAS )
        image.save( path )

    def write_pdf( self, path: str, unit, thickness, paper_size ):
        L = unit * mm
        Th = thickness * mm# cap thickness

        font = "HeiseiKakuGo-W5"
        pdfmetrics.registerFont( UnicodeCIDFont( font ) )
        c = canvas.Canvas( path )
        size = paper_size * mm
        c.setPageSize( size )
        c.drawString( size[0] / 2, size[1] - 20 * mm, '150 x 150 mm' )
        c.rect( size[0] / 2, size[1] - 162 * mm, 150 * mm, 150 * mm, stroke = 1, fill = 0 )
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
            px = x - rx + w / 2
            py = y - ry + h / 2
            q = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
            t = L * q
            #
            c.saveState()
            c.translate( t[0], size[1] - t[1] )
            c.rotate( -r )
            c.setLineWidth( 1 )
            c.setStrokeColor( black )
            c.roundRect( -L * w / 2 + Th, -L * h / 2 + Th, L * w - 2 * Th, L * h - 2 * Th, unit / 5 * mm, stroke = 1, fill = 1 )
            c.setLineWidth( 0.2 )
            c.setStrokeColor( red )
            c.rect( -L * w / 2, -L * h / 2, L * w, L * h, stroke = 1, fill = 0 )
            lines = key.name.split( '\n' )
            y = -len( lines ) / 2.0 * c._leading
            y = c._leading * (len( lines ) / 4.0 - 1 / 4.0)
            c.setFillColor( white ) 
            for line in lines:
                c.drawCentredString( 0, y, line )
                y -= c._leading
            c.restoreState()
        c.showPage()
        c.save()

    def write_scad( self, path: str, unit_w: float ):
        with open( path, 'w' ) as fout:
            fout.write( f'key_w = {unit_w};\n' )
            fout.write( f'key_h = {unit_h};\n' )
            fout.write( 'key_pos_angles = [\n' )
            idx = 0
            for key in self.keys:
                (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
                px = x - rx + w / 2
                py = y - ry + h / 2
                t = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
                t *= unit_w
                w *= unit_w
                h *= unit_w
                fout.write( '    [{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {}, "{}"],\n'.format( t[0], -t[1], -r, w, h, idx, key.name ) )
                idx += 1
            fout.write( '];\n' )

    def write_kicad( self, fout, unit_w: float ):
        fout.write( 'keys = {\n' )
        col = 1
        row = 1
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
            px = x - rx + w / 2
            py = y - ry + h / 2
            t = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
            keyidx = f'{col}{row}'
            row += 1
            if row == 4:
                if col == 7:
                    col += 1
                    row = 2
            elif row == 5:
                if col == 5:
                    row = 2
                elif col == 8:
                    row = 1
                else:
                    row = 1
                col += 1
            t *= unit_w
            w *= unit_w
            h *= unit_w
            fout.write( '    \'{}\' : [{:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.1f}], # {}\n'.format( keyidx, t[0], -t[1], w, h, -r, key.name[0] ) )
        fout.write( '}\n' )

    def save( self, path: str ):
        data = []
        data.append( self.meta )
        for key in self.keys:
            prop = collections.OrderedDict()
            prop['w'] = key.w
            prop['h'] = key.h
            prop['r'] = key.r
            prop['rx'] = key.rx
            prop['ry'] = key.ry
            prop['x'] = key.x - key.rx
            prop['y'] = key.y - key.ry
            row = [prop, key.name]
            data.append( row )
        with open( path, 'w' ) as fout:
            json.dump( data, fout, indent = 4)

    @staticmethod
    def load( path: str ):
        kbd = keyboard_layout()
        with open( path ) as fin:
            cfg = json.load( fin )
            #print( "{}".format( json.dumps( cfg, indent=4 ) ) )
            kbd.meta = cfg[0]

            prop = {}
            prop["y"] = 0
            prop["rx"] = 0
            for row in cfg[1:]:
                prop["x"] = prop["rx"]
                for item in row:
                    if type( item ) is str:
                        key = keyboard_key( item, prop.copy() )
                        kbd.keys.append( key )
                        prop["x"] += key.w
                    else:
                        for key, val in item.items():
                            if key in ("x", "y"):
                                prop[key] += val
                            else:
                                prop[key] = val
                                if key == "rx":
                                    prop["x"] = val
                                elif key == "ry":
                                    prop["y"] = val
                prop["y"] += key.h
        return kbd

class key_layout_maker:
    def __init__( self, xctr, keyh ):
        self.data = []
        self.xctr = xctr
        self.keyh = keyh

    def add_col( self, angle, org, dxs, names1, names2, ydir = -1, keyw = 1, keyh = -1 ):
        if keyh < 0:
            keyh = self.keyh
        for idx, names in enumerate( [names1, names2]):
            if idx in [1]:
                continue
            xsign = [+1, -1][idx]
            prop = collections.OrderedDict()
            prop["r"] = xsign * angle
            prop["rx"] = xsign * org[0] + self.xctr
            prop["ry"] = org[1]
            prop["x"] = -keyw / 2.0
            prop["y"] = -keyh / 2.0
            prop["w"] = keyw
            prop["h"] = keyh
            row = [prop]
            x, y = 0, 0
            for idx, name in enumerate( names ):
                if name == '':
                    continue
                row.append( { "x" : x, "y" : y, "w" : keyw, "h" : keyh } )
                row.append( name )
                x = -keyw + dxs[min( idx, len( dxs ) - 1 )] * xsign
                y = keyh * ydir
            self.data.append( row )

def make_kbd_hermit( unit_w, unit_h, paper_size, ratio = 1.0 ):

    # Left hand
    thumbs2 = ["Alt", "Ctrl", "Lower"]
    col_Gui = ["Shift", "Tab", "Win"]
    col_Tab = ["", "~\n^", "|\n¥", "ESC"]
    col_Z = ["Z", "A", "Q", "!\n1"]
    col_X = ["X", "S", "W", "\"\n2"]
    col_C = ["C", "D", "E", "#\n3"]
    col_V = ["V", "F", "R", "$\n4"]
    col_B = ["B", "G", "T", "%\n5"]
    col_I2 = ["Del"]

    # Right hand
    col_I1 = ["Entr"]
    col_N = ["N", "H", "Y", "&\n6"]
    col_M = ["M", "J", "U", "'\n7"]
    col_Comm = ["<\n,", "K", "I", "(\n8"]
    col_Dot  = [">\n.", "L", "O", ")\n9"]
    col_Scln = ["?\n/", "+\n;", "P", " \n0"]
    col_Cln  = ["", "*\n:", "`\n@", "=\n-"]
    col_Brac = ["_\nBsls", "]\n}", "[\n{"]
    thumbs1  = ["Space", "Shift", "Raise"]

    xctr = (paper_size[0] / 2.0) / unit_w
    keyh = unit_h / unit_w

    maker = key_layout_maker( xctr, keyh )
    maker.data.append( { "name" : "Hermit60", "author" : "orihikarna" } ) # meta
    print( f'ratio = {ratio}')

    # Comma: the origin
    output_type = 'kicad'
    if output_type in ['png', 'pdf']:
        angle_Comm = 0
        org_Comm = vec2( 4.5, 4.3 )
    elif output_type in ['scad']:
        angle_Comm = 45
        org_Comm = vec2( 5.6, 4.3 )
    elif output_type in ['kicad']:
        # angle_Comm = 0
        # angle_Comm = 16
        angle_Comm = 6.351954683901843
        org_Comm = vec2( -4.9, 4.0 )
    else:
        return

    # org_Comm[1] += 30 / unit_w# yoffset for A4 paper

    # parameters
    angle_M_Comm = -16 * ratio
    # print( f'angle_M_Comm = {angle_M_Comm:.6f}' )
    dy_Cln = 0.17 * ratio
    dy_Entr = 0.5 * ratio

    angle_Index_Thmb = 80
    dangles_Thmb = [-20 * ratio, -20 * ratio, 0]
    delta_M_Thmb = vec2( -0.86, 2.22 )
    dys_Thmb = [-0.1 * ratio, 0.1 * ratio, 0]

    ## Middle finger: Comm(,)
    dx_Comm_8 = 3 * math.tan( angle_M_Comm / 2 * deg2rad * keyh )
    dx_I_8 = 0
    dx_Comm_K = dx_K_I = (dx_Comm_8 - dx_I_8) / 2

    ## Index finger: M, N
    angle_Index = angle_M_Comm + angle_Comm
    org_M = org_Comm \
        + vec2( -0.5, +0.5 * keyh ) @ mat2_rot( angle_Comm ) \
        + vec2( -0.5, -0.5 * keyh ) @ mat2_rot( angle_Index )
    org_N = org_M + vec2( -1, 0 ) @ mat2_rot( angle_Index )

    dx_M_7 = -dx_Comm_8
    dx_U_7 = -math.sin( angle_M_Comm * deg2rad ) * keyh
    dx_J_U = dx_U_7 * 0.8
    dx_M_J = dx_M_7 - (dx_J_U + dx_U_7)
    # print( f'dx_M_J={dx_M_J:.3f}, dx_J_U={dx_J_U:.3f}, dx_U_7={dx_U_7:.3f}')

    ## Inner most
    keyh_Inner = keyh
    angle_Inner = angle_Index + math.atan2( dx_M_J, (1 - dy_Entr) * keyh ) * rad2deg
    org_Inner = org_N \
        + vec2( -0.5, (+0.5 - dy_Entr) * keyh ) @ mat2_rot( angle_Index ) \
        + vec2( -0.5, -keyh_Inner/2 ) @ mat2_rot( angle_Inner )

    ## Ring finger: Dot
    angle_Dot = angle_Comm
    org_Dot = org_Comm + vec2( +1, 0 ) @ mat2_rot( angle_Dot )
    dx_Dot_L = dx_Comm_8 / 3

    ## Pinky finger: top
    angle_Dot_Scln = -angle_M_Comm
    if angle_Dot_Scln == 0:
        dy_Scln = 0.5 * keyh
    else:
        dy_Scln = keyh + dx_Dot_L / math.sin( angle_Dot_Scln * deg2rad )
    if False:
        dy_Scln *= ratio
        angle_Dot_Scln = math.asin( dx_Dot_L / (dy_Scln - keyh) ) * rad2deg
    print( f'angle_Dot_Scln={angle_Dot_Scln}, dx_Dot_L={dx_Dot_L}, dy_Scln={dy_Scln}')
    # Scln(;)
    angle_PinkyTop = angle_Dot - angle_Dot_Scln
    tr_Dot = org_Dot + vec2( +0.5, -0.5 * keyh ) @ mat2_rot( angle_Dot )
    org_Scln = tr_Dot + vec2( +0.5, dy_Scln - 0.5 * keyh) @ mat2_rot( angle_PinkyTop )
    dx_Scln_P = dy_Scln * math.tan( angle_Dot_Scln * deg2rad )
    # Cln(:), RBrc(])
    org_Cln = org_Scln + vec2( +1, dy_Cln ) @ mat2_rot( angle_PinkyTop )
    org_RBrc = org_Cln + vec2( +1, dy_Cln ) @ mat2_rot( angle_PinkyTop )

    ## Pinky finger: bottom
    angle_Pinky_Btm_Top = math.atan2( dy_Cln, 1 ) * rad2deg# 1 == keyw
    angle_PinkyBtm = angle_PinkyTop + angle_Pinky_Btm_Top
    print( f'angle_PinkyBtm = {angle_PinkyBtm}' )
    keyw_Slsh = 1.25 + 0.1
    keyw_Bsls = 1.5 + 0.12
    # Slsh(/)
    br_Dot = org_Dot + vec2( +0.5, +0.5 * keyh ) @ mat2_rot( angle_Dot )
    bl_Scln = org_Scln + vec2( -0.5, +0.5 * keyh ) @ mat2_rot( angle_PinkyTop )
    tl_Slsh = vec2_find_intersection( bl_Scln, vec2( 1, 0 ) @ mat2_rot( angle_PinkyBtm ),
                                      br_Dot,  vec2( 1, 0 ) @ mat2_rot( angle_Dot + 90 ) )[0]
    org_Slsh = tl_Slsh + vec2( keyw_Slsh / 2, +0.5 * keyh ) @ mat2_rot( angle_PinkyBtm )
    # Bsls(\)
    org_Bsls = org_Slsh + vec2( (keyw_Slsh + keyw_Bsls) / 2, 0 ) @ mat2_rot( angle_PinkyBtm )

    ### add columns
    dxs_Index = [dx_M_J, dx_J_U, dx_U_7]
    maker.add_col( angle_Index, org_N, dxs_Index, col_N, col_B )
    maker.add_col( angle_Index, org_M, dxs_Index, col_M, col_V )
    maker.add_col( angle_Comm,  org_Comm, [dx_Comm_K, dx_K_I, dx_I_8], col_Comm, col_C )
    maker.add_col( angle_Dot,   org_Dot,  [dx_Dot_L, dx_Dot_L, dx_Dot_L], col_Dot, col_X )
    #
    maker.add_col( angle_PinkyBtm, org_Slsh, [0], col_Scln[0:1], col_Z[0:1], keyw = keyw_Slsh )
    maker.add_col( angle_PinkyTop, org_Scln, [dx_Scln_P], col_Scln[1:], col_Z[1:] )
    #
    maker.add_col( angle_PinkyTop, org_Cln,  [dx_Scln_P], col_Cln[1:], col_Tab[1:] )
    #
    maker.add_col( angle_PinkyBtm, org_Bsls, [0], col_Brac[0:1], col_Gui[0:1], keyw = keyw_Bsls )
    maker.add_col( angle_PinkyTop, org_RBrc, [dx_Scln_P], col_Brac[1:], col_Gui[1:] )

    # add the thumb row
    keyw12 = (1.25 * 19.05 - (19.05 - unit_w)) / 19.05
    keyws = [keyw12, keyw12, 1]
    # keyw12 = 1.25
    keyw = keyw12

    angle_Thmb = angle_Index_Thmb + angle_Index
    org_Thmb = org_M + delta_M_Thmb @ mat2_rot( angle_Index )
    for idx, name in enumerate( thumbs1 ):
        maker.add_col( angle_Thmb + 180, org_Thmb, [0], [name], [thumbs2[idx]], keyw = keyws[idx] )
        org_Thmb += vec2( +keyw / 2, +0.5 * keyh ) @ mat2_rot( angle_Thmb )
        angle_Thmb += dangles_Thmb[idx]
        org_Thmb += vec2( -keyw / 2 - dys_Thmb[idx], +0.5 * keyh ) @ mat2_rot( angle_Thmb )

    # the inner most key (Enter, Del)
    maker.add_col( angle_Inner, org_Inner, [0], col_I1, col_I2, keyh = keyh_Inner )

    return maker.data

if __name__=='__main__':

    home_dir = os.path.expanduser( '~' )
    work_dir = os.path.join( home_dir, 'Downloads' )
    dst_path = os.path.join( work_dir, 'hermit-layout.json' )
    dst_png_fmt  = os.path.join( work_dir, 'hermit-layout-{:02d}.png' )
    dst_pdf  = os.path.join( work_dir, 'hermit-layout.pdf' )
    dst_scad = os.path.join( work_dir, home_dir + '/repos/mywork/hermit-layout.scad' )

    ## Hermit
    unit_w = 17.4
    unit_h = 16.8
    # paper_size = vec2( 297, 210 )# A4
    # paper_size = vec2( 364, 257 )# B4
    paper_size = vec2( 330, 165 )
    thickness = 0.3# mm

    N = 32
    for i in [N]:
    # for i in [0, N]:
    # for i in [0, 1, int(N/2)]:
    # for i in range( N + 1 ):
    # for i in range( 2 * N ):
        ratio = (N - abs( i - N )) / float( N )
        ratio = (1 - math.cos( math.pi * ratio )) / 2
        data = make_kbd_hermit( unit_w, unit_h, paper_size, ratio )
        # write to json for keyboard layout editor
        with open( dst_path, 'w' ) as fout:
            json.dump( data, fout, indent = 4 )

        kbd = keyboard_layout.load( dst_path )
        # kbd.print()
        kbd.write_png( dst_png_fmt.format( i ), unit_w, thickness, paper_size )
        if i == N and ratio == 1:
            kbd.write_pdf( dst_pdf, unit_w, thickness, paper_size )
            kbd.write_scad( dst_scad, unit_w )
            kbd.write_kicad( sys.stdout, unit_w )
        # break
