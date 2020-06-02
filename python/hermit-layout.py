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
from reportlab.lib.pagesizes import A4, landscape

rad2deg = 180 / math.pi
deg2rad = math.pi / 180

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

    def write_png( self, path: str, unit, board_size ):
        # 2560 x 1600, 286mm x 179mm
        w = board_size[0]#mm
        h = board_size[1]#mm
        scale = 2560.0 / 286.0 / 2
        size = ( w * scale, h * scale )
        L = scale * unit

        font = ImageFont.truetype( fontpath, size = 24 )
        image = Image.new( 'RGBA', (math.ceil( size[0] ), math.ceil( size[1] )), ( 255, 255, 255 ) )
        draw = ImageDraw.Draw( image )
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
            pnts = []
            for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]:
                px = x - rx + w * dx
                py = y - ry + h * dy
                rad = r / 180.0 * math.pi
                co = math.cos( rad )
                si = math.sin( rad )
                qx = co * px - si * py + rx
                qy = si * px + co * py + ry
                pnts.append( (L * qx, L * qy) )
            draw.polygon( pnts[:4], outline = ( 0, 0, 0 ) )
            w, h = draw.textsize( key.name, font )
            tx, ty = pnts[4]
            draw.text( (tx - w / 2, ty - h / 2), key.name, ( 0, 0, 0 ), font )
        image.save( path )

    def write_pdf( self, path: str, unit, thickness ):
        L = unit * mm
        Th = thickness * mm# cap thickness

        font = "HeiseiKakuGo-W5"
        pdfmetrics.registerFont( UnicodeCIDFont( font ) )
        c = canvas.Canvas( path )
        size = landscape( A4 )
        c.setPageSize( size )
        xoffset = size[0] / 2 - 30 * mm
        yoffset = size[1] - 20 * mm
        c.drawString( xoffset, yoffset, '150 x 150 mm' )
        c.rect( xoffset, yoffset - 150 * mm, 150 * mm, 150 * mm, stroke = 1, fill = 0 )
        for key in self.keys:
            (x, y, r, rx, ry, w, h) = (key.x, key.y, key.r, key.rx, key.ry, key.w, key.h)
            px = x - rx + w / 2
            py = y - ry + h / 2
            rad = r * deg2rad
            co = math.cos( rad )
            si = math.sin( rad )
            qx = co * px - si * py + rx
            qy = si * px + co * py + ry
            tx, ty = L * qx, L * qy
            #
            c.saveState()
            c.translate( xoffset + tx, yoffset - ty )
            c.rotate( -key.r )
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
            #prop['w'] = key.w
            #prop['h'] = key.h
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
    dx = prop["x"] + 0.5
    dy = prop["y"] + 0.5
    cx = prop["rx"] + co * dx - si * dy
    cy = prop["ry"] + si * dx + co * dy
    print( "['TP{}', {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}],".format( idx, cx, cy, angle, co, si ) )

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

def create_col_data( angle, org, dxs, names, ydir = -1, keyw = 1 ):
    prop = collections.OrderedDict()
    prop["r"] = angle
    prop["rx"] = org[0]
    prop["ry"] = org[1]
    prop["y"] = -0.5
    prop["x"] = -0.5
    prop["w"] = keyw
    row = [prop]
    x, y = 0, 0
    for idx, name in enumerate( names ):
        row.append( { "x" : x, "y" : y } )
        row.append( name )
        x = -1 + dxs[min( idx, len( dxs ) - 1 )]
        y = ydir
    return row

def make_kbd_hermit( path: str ):

    data = []
    data.append( { "name" : "Hermit56", "author" : "orihikarna" } ) # meta

    # finger columns
    # col_n = []
    # col_e = ["ESC", "Tab", "~\n^", "|\n¥"]
    # col_1 = ["!\n1", "Q", "A", "Z"]
    # col_2 = ['"\n2', "W", "S", "X"]
    # col_3 = ["#\n3", "E", "D", "C"]
    # col_4 = ["$\n4", "R", "F", "V"]
    # col_5 = ["%\n5", "T", "G", "B"]
    # col_l = ["{\n[", "BS\nDel"]

    col_I = ["["]
    col_N = ["N", "H", "Y", "^\n6"]
    col_M = ["M", "J", "U", "'\n7"]
    col_Comm = ["<\n,", "K", "I", "(\n8"]
    col_Dot  = [">\n.", "L", "O", ")\n9"]
    col_Scln = ["?\n/", "+\n;", "P", " \n0"]
    col_Cln  = ["|\n¥", "_\n\\", "*\n:", "=\n-"]
    thumbs = ["Space", "Shift", "Raise"]

    XYOffset = vec2( 0, 0 )

    # Comma: the origin
    angle_Comm = 0
    org_Comm = vec2( 4.2, 3.6 )

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

    data.append( create_col_data( angle_Comm,  org_Comm + XYOffset, [dx_Comm_K, dx_Comm_K, dx_I_8], col_Comm ) )
    data.append( create_col_data( angle_Dot,   org_Dot  + XYOffset, [dx_Dot_L, dx_Dot_L, dx_Dot_L], col_Dot ) )
    data.append( create_col_data( angle_Index, org_M    + XYOffset, [dx_M_J, -dx_M_J, dx_M_7], col_M ) )

    dxs_Index = [dx_M_J, -dx_M_J, dx_M_7, 0]
    data.append( create_col_data( angle_Index, org_M + XYOffset, dxs_Index, col_M ) )
    data.append( create_col_data( angle_Index, org_N + XYOffset, dxs_Index, col_N ) )
    data.append( create_col_data( angle_Index, org_I + XYOffset, dxs_Index, col_I ) )

    data.append( create_col_data( angle_PinkyTop, org_Scln + XYOffset, [dx_Scln_P] * 3, col_Scln[1:] ) )
    data.append( create_col_data( angle_PinkyTop, org_Cln  + XYOffset, [dx_Scln_P] * 2, col_Cln[2:] ) )
    data.append( create_col_data( angle_PinkyBtm, org_Slsh + XYOffset, [dx_Scln_P] * 2, col_Scln[0:1] ) )
    data.append( create_col_data( angle_PinkyBtm, org_Bsls + XYOffset, [0] * 2, col_Cln[1::-1], ydir = +1 ) )

    angle_Thmb = angle_Comm_Thmb + angle_Comm
    org_Thmb = org_Comm + delta_Comm_Thmb @ mat2_rot( angle_Comm )

    angle = angle_Thmb
    org = org_Thmb
    keyw = 1.25
    for idx, name in enumerate( thumbs ):
        data.append( create_col_data( angle, org + XYOffset, [0], [name], ydir = -1, keyw = keyw ) )
        org += vec2( +keyw / 2 - dy_Thmb, +0.5 ) @ mat2_rot( angle )
        angle += dangles_Thmb[min( idx, len( dangles_Thmb ) - 1 )]
        org += vec2( -keyw / 2, +0.5 ) @ mat2_rot( angle )

    return data

if __name__=='__main__':

    home_dir = os.path.expanduser( '~/' )
    work_dir = os.path.join( home_dir, 'Downloads/' )
    dst_path = work_dir + 'hermit-layout.json'
    dst_png  = work_dir + 'hermit-layout.png'
    dst_pdf  = work_dir + 'hermit-layout.pdf'

    # Hermit
    unit = 17.8
    board_size = (315, 155)
    data = make_kbd_hermit( dst_path )

    # write to json for keyboard layout editor
    with open( dst_path, 'w' ) as fout:
        json.dump( data, fout, indent = 4)

    kbd = keyboard_layout.load( dst_path )
    # kbd.print()
    kbd.write_png( dst_png, unit, board_size )
    kbd.write_pdf( dst_pdf, unit, 0.3 )
