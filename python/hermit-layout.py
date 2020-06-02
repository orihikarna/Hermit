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
    th = angle / 180 * math.pi
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

fontpath = "/System/Library/Fonts/Courier.dfont"

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
        for key in self.keys:
            ps = ""
            for k, v in key.prop.items():
                if v != 0:
                    ps += ", {}={}".format( k, v )
            print( "key '{}' {}".format( key.name.replace( '\n', ',' ), ps[2:] ) )

    def write_png( self, path: str, unit, thickness, paper_size ):
        # 2560 x 1600, 286mm x 179mm, MacBook size
        scale = 2560.0 / 286.0 / 2
        size = scale * paper_size
        L = scale * unit
        Th = scale * thickness * 2 / L

        font = ImageFont.truetype( fontpath, size = 24 )
        image = Image.new( 'RGBA', (math.ceil( size[0] ), math.ceil( size[1] )), ( 255, 255, 255 ) )
        draw = ImageDraw.Draw( image )
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
            pnts = []
            for dx, dy in [vec2( 0, 0 ), vec2( 1, 0 ), vec2( 1, 1 ), vec2( 0, 1 ), vec2( 0.5, 0.5 )]:
                px = x - rx + (w - Th) * dx
                py = y - ry + (h - Th) * dy
                q = vec2( rx, ry ) + vec2( px, py ) @ mat2_rot( r )
                t = L * q
                pnts.append( (t[0], t[1]) )
            draw.polygon( pnts[:4], outline = ( 0, 0, 0 ) )
            w, h = draw.textsize( key.name, font )
            tx, ty = pnts[4]
            draw.text( (tx - w / 2, ty - h / 2), key.name, ( 0, 0, 0 ), font )
        image.save( path )

    def write_pdf( self, path: str, unit, thickness, paper_size ):
        L = unit * mm
        Th = thickness * mm# cap thickness

        font = "HeiseiKakuGo-W5"
        pdfmetrics.registerFont( UnicodeCIDFont( font ) )
        c = canvas.Canvas( path )
        size = paper_size * mm
        c.setPageSize( size )
        c.drawString( size[0] / 2, size[1], '140 x 150 mm' )
        c.rect( size[0] / 2, size[1] - 150 * mm, 140 * mm, 150 * mm, stroke = 1, fill = 0 )
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
    th = angle / 180.0 * math.pi
    co = math.cos( th )
    si = math.sin( th )
    w = prop["w"]
    h = prop["h"]
    dx = prop["x"] + w / 2.0
    dy = prop["y"] + h / 2.0
    cx = prop["rx"] + co * dx - si * dy
    cy = prop["ry"] + si * dx + co * dy
    print( "['TP{}', {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}],".format( idx, cx, cy, angle, co, si ) )

def add_col( data, angle, org, dxs, names1, names2, xctr, ydir = -1, keyw = 1 ):
    keyh = 1
    for idx, names in enumerate( [names1, names2 ]):
        xsign = +1 if idx == 0 else -1
        prop = collections.OrderedDict()
        prop["r"] = xsign * angle
        prop["rx"] = xsign * org[0] + xctr
        prop["ry"] = org[1]
        prop["y"] = -keyh / 2
        prop["x"] = -keyw / 2
        prop["w"] = keyw
        row = [prop]
        x, y = 0, 0
        for idx, name in enumerate( names ):
            row.append( { "x" : x, "y" : y } )
            row.append( name )
            x = -keyw + dxs[min( idx, len( dxs ) - 1 )] * xsign
            y = keyh * ydir
        data.append( row )

def make_kbd_hermit( path: str, unit, paper_size ):

    data = []
    data.append( { "name" : "Hermit56", "author" : "orihikarna" } ) # meta

    # Left hand
    thumbs2 = ["Alt", "Ctrl", "Lower"]
    col_Tab = ["|\n¥", "Shift", "Tab", "ESC"]
    col_Z = ["Z", "A", "Q", "!\n1"]
    col_X = ["X", "S", "W", "\n2"]
    col_C = ["C", "D", "E", "#\n3"]
    col_V = ["V", "F", "R", "$\n4"]
    col_B = ["B", "G", "T", "%\n5"]
    col_I2 = ["["]

    # Right hand
    col_I1 = ["]"]
    col_N = ["N", "H", "Y", "^\n6"]
    col_M = ["M", "J", "U", "'\n7"]
    col_Comm = ["<\n,", "K", "I", "(\n8"]
    col_Dot  = [">\n.", "L", "O", ")\n9"]
    col_Scln = ["?\n/", "+\n;", "P", " \n0"]
    col_Cln  = ["|\n¥", "_\n\\", "*\n:", "=\n-"]
    thumbs1 = ["Space", "Shift", "Raise"]

    xctr = paper_size[0] / 2.0 / unit

    # Comma: the origin
    angle_Comm = -6
    org_Comm = vec2( 4.0, 3.6 )
    org_Comm[1] += 30 / unit# yoffset

    # parameters
    dx_Dot_L = -0.1
    dx_Comm_K = dx_Dot_L * 2.0
    dy_Scln = 0.4

    dangles_Thmb = (-16, -6)
    angle_Comm_Thmb = 68
    delta_Comm_Thmb = vec2( -1.3, 2.4 )
    dy_Thmb = -0.125

    # Index columns: M, N, I
    dx_I_8 = dx_Dot_L * 3 - dx_Comm_K * 2
    angle_M_Comm = math.atan2( dx_Comm_K, 1 ) * rad2deg
    dx_M_7 = -math.sin( angle_M_Comm * deg2rad ) + dx_I_8 / math.cos( angle_M_Comm * deg2rad )
    dx_M_J = -dx_M_7
    angle_Index = angle_M_Comm + angle_Comm
    delta_Index = vec2( -1, 0 ) @ mat2_rot( angle_Index )
    org_M = org_Comm + vec2( -0.5 + dx_Comm_K, -0.5 ) @ mat2_rot( angle_Comm ) + vec2( -0.5, +0.5 ) @ mat2_rot( angle_Index )
    org_N = org_M + delta_Index
    org_I = org_N + delta_Index

    # Dot
    angle_Dot = angle_Comm
    org_Dot = org_Comm + vec2( +1, 0 ) @ mat2_rot( angle_Dot )

    ## Pinky top
    # Scln(;)
    angle_Dot_Scln = math.asin( -dx_Dot_L / (1 - dy_Scln) ) / math.pi * 180
    angle_PinkyTop = angle_Dot - angle_Dot_Scln
    tr_Dot = org_Dot + vec2( +0.5, -0.5 ) @ mat2_rot( angle_Dot )
    org_Scln = tr_Dot + vec2( +0.5, dy_Scln - 0.5) @ mat2_rot( angle_PinkyTop )
    dx_Scln_P = dy_Scln * math.tan( angle_Dot_Scln / 180 * math.pi )
    # Cln(:)
    org_Cln = org_Scln + vec2( +1, 0 ) @ mat2_rot( angle_PinkyTop )

    ## Pinky bottom
    # Bsls(\)
    tr_Dot = org_Dot + vec2( +0.5, -0.5 ) @ mat2_rot( angle_Dot )
    br_Dot = org_Dot + vec2( +0.5, +0.5 ) @ mat2_rot( angle_Dot )
    lb_Cln = org_Cln - vec2( +0.5, -0.5 ) @ mat2_rot( angle_PinkyTop )
    Lt = np.linalg.norm( tr_Dot - lb_Cln )
    Lb = np.linalg.norm( br_Dot - lb_Cln )
    angle_1 = math.acos( (1 + Lb * Lb - Lt * Lt ) / (2 * Lb)) / math.pi * 180
    angle_2 = math.asin( 1 / Lb ) / math.pi * 180
    angle_Dot_Bsls = angle_1 - angle_2
    angle_PinkyBtm = angle_Dot + angle_Dot_Bsls
    org_Bsls = lb_Cln + vec2( +0.5, +0.5 ) @ mat2_rot( angle_PinkyBtm )
    # Slsh(/)
    bl_Scln = org_Scln + vec2( -0.5, +0.5 ) @ mat2_rot( angle_PinkyTop )
    x, _, _ = vec2_find_intersection( br_Dot, vec2( 0, 1 ) @ mat2_rot( angle_Dot ), bl_Scln, vec2( -1, 0 ) @ mat2_rot( angle_PinkyBtm ) )
    tl_Slsh = x + (vec2( 1, 0 ) @ mat2_rot( angle_PinkyBtm )) * math.sin( angle_Dot_Bsls / 180 * math.pi ) * np.linalg.norm( x - br_Dot )
    org_Slsh = tl_Slsh + vec2( +0.5, +0.5 ) @ mat2_rot( angle_PinkyBtm )

    add_col( data, angle_Comm,  org_Comm, [dx_Comm_K, dx_Comm_K, dx_I_8], col_Comm, col_C, xctr )
    add_col( data, angle_Dot,   org_Dot,  [dx_Dot_L, dx_Dot_L, dx_Dot_L], col_Dot, col_X, xctr )

    dxs_Index = [dx_M_J, -dx_M_J, dx_M_7, 0]
    add_col( data, angle_Index, org_M, dxs_Index, col_M, col_V, xctr )
    add_col( data, angle_Index, org_N, dxs_Index, col_N, col_B, xctr )
    add_col( data, angle_Index, org_I, dxs_Index, col_I1, col_I2, xctr )

    add_col( data, angle_PinkyTop, org_Scln, [dx_Scln_P] * 3, col_Scln[1:], col_Z[1:], xctr )
    add_col( data,  angle_PinkyTop, org_Cln,  [dx_Scln_P] * 2, col_Cln[2:], col_Tab[2:], xctr )
    add_col( data, angle_PinkyBtm, org_Slsh, [dx_Scln_P] * 2, col_Scln[0:1], col_Z[0:1], xctr )
    add_col( data, angle_PinkyBtm, org_Bsls, [0] * 2, col_Cln[1::-1], col_Tab[1::-1], xctr, ydir = +1 )

    angle_Thmb = angle_Comm_Thmb + angle_Comm
    org_Thmb = org_Comm + delta_Comm_Thmb @ mat2_rot( angle_Comm )

    angle = angle_Thmb
    org = org_Thmb
    keyw = 1.25
    for idx, name in enumerate( thumbs1 ):
        add_col( data, angle, org, [0], [name], [thumbs2[idx]], xctr, ydir = -1, keyw = keyw )
        org += vec2( +keyw / 2 - dy_Thmb, +0.5 ) @ mat2_rot( angle )
        angle += dangles_Thmb[min( idx, len( dangles_Thmb ) - 1 )]
        org += vec2( -keyw / 2, +0.5 ) @ mat2_rot( angle )

    return data

if __name__=='__main__':

    home_dir = os.path.expanduser( '~' )
    work_dir = os.path.join( home_dir, 'Downloads' )
    dst_path = os.path.join( work_dir + 'hermit-layout.json' )
    dst_png  = os.path.join( work_dir + 'hermit-layout.png' )
    dst_pdf  = os.path.join( work_dir + 'hermit-layout.pdf' )

    # Hermit
    unit = 17.8
    paper_size = vec2( 294, 210 )
    data = make_kbd_hermit( dst_path, unit, paper_size )

    # write to json for keyboard layout editor
    with open( dst_path, 'w' ) as fout:
        json.dump( data, fout, indent = 4)

    kbd = keyboard_layout.load( dst_path )
    # kbd.print()
    thickness = 0.3#mm
    kbd.write_png( dst_png, unit, thickness, paper_size )
    kbd.write_pdf( dst_pdf, unit, thickness, paper_size )
