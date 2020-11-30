import json
import math
import numpy as np
import os
import collections
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import red, black, white
from reportlab.lib.units import mm

rad2deg = 180 / math.pi
deg2rad = math.pi / 180

anti_alias_scaling = 3

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
            if name in ['M', '<,,', '>,.', '?,/']:
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
                key_image, rsz = get_key_image( (int( dim[0] ), int( dim[1] )), int( L/4 ), key.name, "DarkTurquoise" )
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
                prop["y"] += 1
        return kbd

def print_for_kicad( idx, prop ):
    angle = prop["r"]
    th = angle * deg2rad
    co = math.cos( th )
    si = math.sin( th )
    w = prop["w"]
    h = prop["h"]
    dx = prop["x"] + w / 2.0
    dy = prop["y"] + h / 2.0
    cx = prop["rx"] + co * dx - si * dy
    cy = prop["ry"] + si * dx + co * dy
    print( "['TP{}', {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}],".format( idx, cx, cy, angle, co, si ) )

def add_col( data, angle, org, dxs, names1, names2, xctr, ydir = -1, keyw = 1, keyh = 1 ):
    for idx, names in enumerate( [names1, names2 ]):
        xsign = [+1, -1][idx]
        prop = collections.OrderedDict()
        prop["r"] = xsign * angle
        prop["rx"] = xsign * org[0] + xctr
        prop["ry"] = org[1]
        prop["y"] = -keyh / 2.0
        prop["x"] = -keyw / 2.0
        prop["w"] = keyw
        row = [prop]
        x, y = 0, 0
        for idx, name in enumerate( names ):
            row.append( { "x" : x, "y" : y, "w" : keyw, "h"  : keyh } )
            row.append( name )
            x = -keyw + dxs[min( idx, len( dxs ) - 1 )] * xsign
            y = keyh * ydir
        data.append( row )

def make_kbd_hermit( path: str, unit, paper_size, ratio = 1.0 ):

    data = []
    data.append( { "name" : "Hermit56", "author" : "orihikarna" } ) # meta

    # Left hand
    thumbs2 = ["Alt", "Ctrl", "Lower"]
    col_Gui = ["Win", "Fn"]
    col_Tab = ["|\n¥", "Shift", "Tab", "ESC"]
    col_Z = ["Z", "A", "Q", "!\n1"]
    col_X = ["X", "S", "W", "\n2"]
    col_C = ["C", "D", "E", "#\n3"]
    col_V = ["V", "F", "R", "$\n4"]
    col_B = ["B", "G", "T", "%\n5"]
    col_I2 = ["Del"]

    # Right hand
    col_I1 = ["Entr"]
    col_N = ["N", "H", "Y", "^\n6"]
    col_M = ["M", "J", "U", "'\n7"]
    col_Comm = ["<\n,", "K", "I", "(\n8"]
    col_Dot  = [">\n.", "L", "O", ")\n9"]
    col_Scln = ["?\n/", "+\n;", "P", " \n0"]
    col_Cln  = ["|\n¥", "_\n\\", "*\n:", "=\n-"]
    col_Brac  = ["]\n}", "[\n{"]
    thumbs1 = ["Space", "Shift", "Raise"]

    xctr = (paper_size[0] / 2.0) / unit

    # Comma: the origin
    angle_Comm = -12
    #angle_Comm = 0# For Zoea!
    org_Comm = vec2( 3.8, 4.3 )
    #org_Comm[1] += 30 / unit# yoffset for A4 paper

    # parameters
    dx_Dot_L = -0.12 * ratio
    dx_Comm_K = dx_Dot_L * 3 / 2
    dy_Scln = 0.4 * ratio
    dy_Cln = 0.08 * ratio
    dy_Entr = 0.3 * ratio

    angle_Index_Thmb = 90
    dangle_Thmb = -6 - 12 * ratio
    delta_M_Thmb = vec2( -0.8, 2.1 )
    dy_Thmb = -0.045 - 0.08 * ratio

    # Index columns: M, N, I
    dx_K_I = dx_Comm_K
    dx_I_8 = 0
    dx_Comm_8 = dx_Comm_K + dx_K_I + dx_I_8
    #angle_Comm = -angle_M_Comm# For Zoea!
    angle_M_Comm = 2 * math.atan2( dx_Comm_8, 3 ) * rad2deg
    print( f'angle_M_Comm = {angle_M_Comm:.3f}' )
    dx_M_7 = -dx_Comm_8
    dx_U_7 = -math.sin( angle_M_Comm * deg2rad )
    dx_J_U = dx_U_7
    #dx_J_U = (dx_M_7 - dx_U_7) * (1 + 1 / 2)
    dx_M_J = dx_M_7 - (dx_J_U + dx_U_7)

    angle_Index = angle_M_Comm + angle_Comm
    angle_Inner = angle_Index + math.atan2( dx_M_J, 1 - dy_Entr ) * rad2deg
    delta_Index = vec2( -1, 0 ) @ mat2_rot( angle_Index )
    org_M = org_Comm + vec2( -0.5, +0.5 ) @ mat2_rot( angle_Comm ) + vec2( -0.5, -0.5 ) @ mat2_rot( angle_Index )
    org_N = org_M + delta_Index
    keyh_Inner = 1.25
    org_I = org_N + vec2( -0.5, +0.5 - dy_Entr ) @ mat2_rot( angle_Index ) + vec2( -0.5, -keyh_Inner/2 ) @ mat2_rot( angle_Inner )

    # Dot
    angle_Dot = angle_Comm
    org_Dot = org_Comm + vec2( +1, 0 ) @ mat2_rot( angle_Dot )

    ## Pinky top
    # Scln(;)
    angle_Dot_Scln = math.asin( -dx_Dot_L / (1 - dy_Scln) ) * rad2deg
    angle_PinkyTop = angle_Dot - angle_Dot_Scln
    tr_Dot = org_Dot + vec2( +0.5, -0.5 ) @ mat2_rot( angle_Dot )
    org_Scln = tr_Dot + vec2( +0.5, dy_Scln - 0.5) @ mat2_rot( angle_PinkyTop )
    dx_Scln_P = dy_Scln * math.tan( angle_Dot_Scln * deg2rad )
    # Cln(:), LBrc([)
    org_Cln = org_Scln + vec2( +1, dy_Cln ) @ mat2_rot( angle_PinkyTop )
    org_LBrc = org_Cln + vec2( +1, dy_Cln ) @ mat2_rot( angle_PinkyTop )

    ## Pinky bottom
    tx = 2
    # Bsls(\)
    br_Dot = org_Dot + vec2( +0.5, +0.5 ) @ mat2_rot( angle_Dot )
    lb_key = org_Scln + vec2( tx - 0.5, +0.5 + dy_Cln * tx ) @ mat2_rot( angle_PinkyTop )
    Lt = np.linalg.norm( tr_Dot - lb_key )
    Lb = np.linalg.norm( br_Dot - lb_key )
    angle_1 = math.acos( (1 + Lb * Lb - Lt * Lt ) / (2 * Lb)) * rad2deg
    angle_2 = math.asin( tx / Lb ) * rad2deg
    angle_Dot_Btm = angle_1 - angle_2
    angle_PinkyBtm = angle_Dot + angle_Dot_Btm
    angle_Btm_Top = angle_PinkyBtm - angle_PinkyTop
    # Slsh(/)
    bl_Scln = org_Scln + vec2( -0.5, +0.5 ) @ mat2_rot( angle_PinkyTop )
    x, _, _ = vec2_find_intersection( br_Dot, vec2( 0, 1 ) @ mat2_rot( angle_Dot ), bl_Scln, vec2( -1, 0 ) @ mat2_rot( angle_PinkyBtm ) )
    tl_Slsh = x + (vec2( 1, 0 ) @ mat2_rot( angle_PinkyBtm )) * math.sin( angle_Dot_Btm * deg2rad ) * np.linalg.norm( x - br_Dot )
    org_Slsh = tl_Slsh + vec2( +0.5, +0.5 ) @ mat2_rot( angle_PinkyBtm )
    if tx == 2:
        # RBrc(]), Bsls(\)
        org_RBrc = lb_key + vec2( +0.5, +0.5 ) @ mat2_rot( angle_PinkyBtm )
        org_Bsls = org_RBrc + vec2( -1, math.tan( angle_Btm_Top * deg2rad ) - dy_Cln / math.cos( angle_Btm_Top * deg2rad ) ) @ mat2_rot( angle_PinkyBtm )
        #org_Bsls = (org_RBrc + org_Slsh) * 0.5
    elif tx == 1:
        # RBrc(]), Bsls(\)
        org_Bsls = lb_key + vec2( +0.5, +0.5 ) @ mat2_rot( angle_PinkyBtm )
        org_RBrc = org_Bsls + vec2( +1, -math.tan( angle_Btm_Top * deg2rad ) + dy_Cln / math.cos( angle_Btm_Top * deg2rad ) ) @ mat2_rot( angle_PinkyBtm )
        #org_RBrc = org_Bsls + (org_Bsls - org_Slsh)

    keyw_Cln = 1.0
    keyw_Mins = 1.0
    org_Mins = org_Cln + vec2( dx_Scln_P + (keyw_Mins - 1) / 2, -1 ) @ mat2_rot( angle_PinkyTop )

    add_col( data, angle_Comm, org_Comm, [dx_Comm_K, dx_K_I, dx_I_8], col_Comm, col_C, xctr )
    add_col( data, angle_Dot,  org_Dot,  [dx_Dot_L, dx_Dot_L, dx_Dot_L], col_Dot, col_X, xctr )

    dxs_Index = [dx_M_J, dx_J_U, dx_U_7, 0]
    add_col( data, angle_Index, org_M, dxs_Index, col_M, col_V, xctr )
    add_col( data, angle_Index, org_N, dxs_Index, col_N, col_B, xctr )
    add_col( data, angle_Inner, org_I, dxs_Index, col_I1, col_I2, xctr, keyh = keyh_Inner )

    add_col( data, angle_PinkyTop, org_Scln, [dx_Scln_P] * 3, col_Scln[1:], col_Z[1:], xctr )
    add_col( data, angle_PinkyTop, org_Cln,  [dx_Scln_P],     col_Cln[2:3], col_Tab[2:3], xctr, keyw = keyw_Cln )
    add_col( data, angle_PinkyTop, org_Mins, [dx_Scln_P],     col_Cln[3:4], col_Tab[3:4], xctr, keyw = keyw_Mins )
    add_col( data, angle_PinkyTop, org_LBrc, [0], col_Brac[1:], col_Gui[1:], xctr, ydir = +1 )

    add_col( data, angle_PinkyBtm, org_Slsh, [dx_Scln_P] * 2, col_Scln[0:1], col_Z[0:1], xctr )
    add_col( data, angle_PinkyBtm, org_Bsls, [0], col_Cln[1:0:-1], col_Tab[1:0:-1], xctr, ydir = +1, keyw = keyw_Cln )
    add_col( data, angle_PinkyBtm, org_RBrc, [0], col_Brac[0::-1], col_Gui[0::-1], xctr, ydir = +1 )

    if False:# left side
        keyw_Cln = 1.25
        org_Cln  += vec2( (keyw_Cln - 1) / 2, 0 ) @ mat2_rot( angle_PinkyTop )
        org_Bsls += vec2( (keyw_Cln - 1) / 2, 0 ) @ mat2_rot( angle_PinkyBtm )
        add_col( data, angle_PinkyTop, org_Cln,  [dx_Scln_P], [], col_Tab[2:3], xctr, keyw = keyw_Cln )
        add_col( data, angle_PinkyBtm, org_Bsls, [0], [],  col_Tab[1:0:-1], xctr, ydir = +1, keyw = keyw_Cln )

    #angle_Thmb = angle_Comm_Thmb + angle_Comm
    angle_Thmb = angle_Index_Thmb + angle_Index
    #org_Thmb = org_Comm + delta_Comm_Thmb @ mat2_rot( angle_Comm )
    org_Thmb = org_M + delta_M_Thmb @ mat2_rot( angle_Index )

    angle = angle_Thmb
    org = org_Thmb
    keyw = 1.25
    for idx, name in enumerate( thumbs1 ):
        add_col( data, angle, org, [0], [name], [thumbs2[idx]], xctr, ydir = -1, keyw = keyw )
        org += vec2( +keyw / 2, +0.5 ) @ mat2_rot( angle )
        angle += dangle_Thmb
        org += vec2( -keyw / 2 - dy_Thmb, +0.5 ) @ mat2_rot( angle )

    return data

if __name__=='__main__':

    home_dir = os.path.expanduser( '~' )
    work_dir = os.path.join( home_dir, 'Downloads' )
    dst_path = os.path.join( work_dir, 'hermit-layout.json' )
    dst_png_fmt  = os.path.join( work_dir, 'hermit-layout-{:02d}.png' )
    dst_pdf  = os.path.join( work_dir, 'hermit-layout.pdf' )

    # Hermit
    unit = 17.8
    paper_size = vec2( 297, 210 )
    thickness = 0.3#mm

    N = 16
    #for i in [N]:
    #for i in [0, N]:
    for i in range( 2 * N ):
        ratio = (N - abs( i - N )) / float( N )
        ratio = (1 - math.cos( math.pi * ratio )) / 2
        data = make_kbd_hermit( dst_path, unit, paper_size, ratio )
        # write to json for keyboard layout editor
        with open( dst_path, 'w' ) as fout:
            json.dump( data, fout, indent = 4 )

        kbd = keyboard_layout.load( dst_path )
        kbd.print()
        kbd.write_png( dst_png_fmt.format( i ), unit, thickness, vec2( 297, 170 ) )
        if i == 10 and ratio == 1:
            kbd.write_pdf( dst_pdf, unit, thickness, paper_size )
        #break
