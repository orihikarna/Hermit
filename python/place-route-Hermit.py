import pcbnew
import math
import sys
import os
import re

##
sys.dont_write_bytecode = True
root_dir = os.path.join( os.path.expanduser( '~' ), 'repos/Hermit/python' )
if not root_dir in sys.path:
    sys.path.append( root_dir )
##
from kadpy import kad
from kadpy import pnt
from kadpy import vec2
from kadpy import mat2

reload( kad )
kad.UnitMM = True
kad.PointDigits = 3

pcb = pcbnew.GetBoard()

# alias
Strt  = kad.Straight # Straight
Strt2 = kad.OffsetStraight
Dird  = kad.OffsetDirected # Directed + Offsets
ZgZg  = kad.ZigZag # ZigZag

Line        = kad.Line
Linear      = kad.Linear
Round       = kad.Round
BezierRound = kad.BezierRound
##

# in mm
VIA_Size = [(1.1, 0.6), (1.0, 0.5), (0.8, 0.4), (0.6, 0.3)]

FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
FourCorners2 = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
PCB_Width  = 170
PCB_Height = 140

J1_x, J1_y = 20, 84
J2_x, J2_y = 96, 99
J3_x, J3_y = 66, 108
D1_x, D1_y = 62, 106

keys = {
    '11' : [46.222, -63.397, 17.400, 16.800, -0.0], # N
    '12' : [44.967, -46.597, 17.400, 16.800, -0.0], # H
    '13' : [48.671, -29.797, 17.400, 16.800, -0.0], # Y
    '14' : [53.302, -12.997, 17.400, 16.800, -0.0], # ^
    '21' : [63.622, -63.397, 17.400, 16.800, -0.0], # M
    '22' : [62.367, -46.597, 17.400, 16.800, -0.0], # J
    '23' : [66.071, -29.797, 17.400, 16.800, -0.0], # U
    '24' : [70.702, -12.997, 17.400, 16.800, -0.0], # '
    '31' : [83.000, -66.120, 17.400, 16.800, -16.0], # <
    '32' : [84.228, -48.995, 17.400, 16.800, -16.0], # K
    '33' : [85.456, -31.870, 17.400, 16.800, -16.0], # I
    '34' : [90.086, -15.721, 17.400, 16.800, -16.0], # (
    '41' : [99.726, -70.916, 17.400, 16.800, -16.0], # >
    '42' : [102.088, -54.116, 17.400, 16.800, -16.0], # L
    '43' : [104.450, -37.317, 17.400, 16.800, -16.0], # O
    '44' : [106.812, -20.517, 17.400, 16.800, -16.0], # )
    '51' : [118.323, -83.344, 23.490, 16.800, -9.6], # ?
    '52' : [119.104, -65.077, 17.400, 16.800, -0.0], # +
    '53' : [121.466, -48.277, 17.400, 16.800, -0.0], # P
    '54' : [123.829, -31.477, 17.400, 16.800, -0.0], #  
    '62' : [136.504, -68.035, 17.400, 16.800, -0.0], # *
    '63' : [138.866, -51.235, 17.400, 16.800, -0.0], # @
    '64' : [141.229, -34.435, 17.400, 16.800, -0.0], # =
    '71' : [143.797, -87.675, 28.188, 16.800, -9.6], # _
    '72' : [153.904, -70.993, 17.400, 16.800, -0.0], # ]
    '73' : [156.266, -54.193, 17.400, 16.800, -0.0], # [
    '82' : [48.658, -102.025, 20.243, 16.800, -260.0], # S
    '83' : [30.678, -110.392, 20.243, 16.800, -240.0], # S
    '84' : [13.978, -122.168, 17.400, 16.800, -220.0], # R
    '91' : [27.676, -56.375, 17.400, 16.800, 8.5], # E
}

L2R = []
R2L = []
for name in keys.keys():
    col = int( name[0] )
    row = int( name[1] )
    if col == 8:
        R2L.append( name )
    else:
        if row in [1, 3]:
            L2R.append( name )
        else:
            R2L.append( name )

# Board Type
BDL = 0# Left plate
BDR = 1# Right plate
BDT = 2# Top plate
BDB = 3# Bottom plate
BDM = 4# Middle plate

def drawEdgeCuts( board ):
    layer = 'Edge.Cuts'
    width = 0.1
    W = PCB_Width
    H = PCB_Height
    mgn = 0.1# margin
    R = 2# corner radius
    USBC_Width  = 4.675
    USBC_Height = 5.73

    corners = []
    if True:
        corners.append( [((W/2, 0),   0), Round, [R]] )
        corners.append( [((W, H/2),  90), Round, [R]] )
        corners.append( [((W/2, H), 180), Round, [R]] )
        corners.append( [((0, H/2), 270), Round, [R]] )
        kad.draw_closed_corners( corners, layer, width )
        return

    midcnrs = []
    midcnrs_set = []
    ## top
    corners.append( [((W/2, 0), 0), Round, [R]] )
    midcnrs.append( corners[-1] )
    ## right
    corners.append( [((W, R+1), 90), Round, [R]] )
    midcnrs.append( corners[-1] )
    USBM = 4.4
    USBT = 1.0
    USBW = 12.5
    ## USB (PC)
    if board == BDL:
        corners.append( [((W - 3,           J2_y - USBC_Width), 180), Round, [0.5]] )
        corners.append( [((W - USBC_Height, J2_y             ),  90), Round, [0.5]] )
        corners.append( [((W - 3,           J2_y + USBC_Width),   0), Round, [0.5]] )
        corners.append( [((W,               H - R - 1        ),  90), Round, [0.5]] )
    if board in [BDL, BDR, BDM]:
        midcnrs.append( [((W-USBW+2, J2_y - USBM - USBT*2), 180), Round, [0.5]] )
        midcnrs.append( [((W-USBW,   J2_y - USBM - USBT  ),  90), Round, [0.8]] )
        midcnrs.append( [((W-USBW+2, J2_y - USBM         ),   0), Round, [0.8]] )
        midcnrs.append( [((W,        J2_y                ),  90), Round, [0.5]] )
        midcnrs.append( [((W-USBW+2, J2_y + USBM         ), 180), Round, [0.5]] )
        midcnrs.append( [((W-USBW,   J2_y + USBM + USBT  ),  90), Round, [0.8]] )
        midcnrs.append( [((W-USBW+2, J2_y + USBM + USBT*2),   0), Round, [0.8]] )
        midcnrs.append( [((W,        H - R - 1),             90), Round, [0.5]] )
    ## bottom
    corners.append( [((W*5/6, H), 180), Round, [R]] )
    midcnrs.append( corners[-1] )
    if True:
        corners.append( [((W*2/3 + mgn,   H - R - 1  ), -90), Round, [R]] )
        midcnrs.append( corners[-1] )
        corners.append( [((W*2/3 - R - 1, H*2/3 - mgn), 180), Round, [R]] )
        midcnrs.append( corners[-1] )
        if board in [BDL, BDR, BDM]:
            # J3 & D1 LED
            midcnrs.append( [((J3_x + 1.27*11, H*2/3 - 1.27), -90), Round, [0.5]] )
            midcnrs.append( [((W/2,            H*2/3 - 2.54), 180), Round, [0.5]] )
            midcnrs.append( [((D1_x - 2.0,     H*2/3 - 1.27),  90), Round, [0.5]] )
            midcnrs.append( [((D1_x - 3.2,     H*2/3 - mgn ), 180), Round, [0.5]] )
        corners.append( [((W/3 - mgn, H - R - 1),  90), Round, [R]] )
        midcnrs.append( corners[-1] )
        corners.append( [((W/6,       H        ), 180), Round, [R]] )
        midcnrs.append( corners[-1] )
    ## left
    corners.append( [((0, H - R - 1), -90), Round, [R]] )
    midcnrs.append( corners[-1] )
    # Split (USB)
    if board in [BDL, BDR]:
        corners.append( [((3,           J1_y + USBC_Width),   0), Round, [0.5]] )
        corners.append( [((USBC_Height, J1_y             ), -90), Round, [0.5]] )
        corners.append( [((3,           J1_y - USBC_Width), 180), Round, [0.5]] )
        corners.append( [((0,           R + 1            ), -90), Round, [0.5]] )
    if board in [BDL, BDR, BDM]:# mid plate
        Jw = 6.3
        midcnrs.append( [((2,           J1_y + Jw    ),   0), BezierRound, [1]] )# J1 bottom
        T = 7.4# thickness for left
        midcnrs.append( [((T,           J1_y + Jw + 2),  90), BezierRound, [1]] )# left
        D = 8.5# diagonal left
        midcnrs.append( [((D,           H - D        ),  45), BezierRound, [1]] )# left bottom corner
        T = 5.5# thickness for bottom
        midcnrs.append( [((W/6,         H - T        ),   0), BezierRound, [1]] )# bottom
        D = 10# diagonal right
        midcnrs.append( [((W/3 - D,     H - D        ), -45), BezierRound, [1]] )# right bottom corner
        T = 6# thickness for right
        midcnrs.append( [((W/3 - T,     H*2/3        ), -90), BezierRound, [1]] )# right
        midcnrs.append( [((W/6 + R + 1, J1_y - 2     ),-135), BezierRound, [1]] )# diagonal
        midcnrs.append( [((2,           J1_y - Jw    ), 180), BezierRound, [1]] )# J1 top
        midcnrs.append( [((0,           R + 1        ), -90), BezierRound, [1]] )# left
        midcnrs_set.append( midcnrs )

    # mid plate USB hole
    if board in [BDL, BDR, BDM]:
        midcnrs = []
        midcnrs.append( [((W-USBW-2.6, J2_y - USBM - USBT*2),   0), Round, [0.5]] )
        midcnrs.append( [((W-USBW-2.0, J2_y - USBM - USBT  ),  90), Round, [0.5]] )
        midcnrs.append( [((W-USBW-2.6, J2_y - USBM         ), 180), Round, [0.5]] )
        midcnrs.append( [((W-16,       J2_y                ),  90), Round, [0.5]] )
        midcnrs.append( [((W-USBW-2.6, J2_y + USBM         ),   0), Round, [0.5]] )
        midcnrs.append( [((W-USBW-2.0, J2_y + USBM + USBT  ),  90), Round, [0.5]] )
        midcnrs.append( [((W-USBW-2.6, J2_y + USBM + USBT*2), 180), Round, [0.5]] )
        midcnrs.append( [((W-18,       J2_y                ), -90), Round, [0.5]] )
        midcnrs_set.append( midcnrs )

    # mid plate main hole
    if board in [BDL, BDR, BDM]:
        midcnrs = []
        T = 4.8# thickness top
        midcnrs.append( [((W/2,     T        ),   0), BezierRound, [1]] )# top
        D = 10# diagonal top right
        midcnrs.append( [((W - D,   D        ),  45), BezierRound, [1]] )# top right diagonal
        T = 5# thickness right
        midcnrs.append( [((W-T,     H/3      ),  90), BezierRound, [1]] )# right
        midcnrs.append( [((W*5/6,   30.6     ), 180), BezierRound, [1]] )# mid horizontal
        T = 5# thickness mid
        midcnrs.append( [((W*2/3-1, H*2/3-T-1.2), 90), BezierRound, [1]] )# mid right
        midcnrs.append( [((W/2,     H*2/3-T  ), 180), BezierRound, [1]] )# mid bottom
        midcnrs.append( [((W/3+6,   H*2/3-T-2), -90), BezierRound, [1]] )# mid left
        midcnrs.append( [((W/3,     22.4     ), 180), BezierRound, [1]] )# mid left horizontal
        midcnrs.append( [((20,      18       ),-135), BezierRound, [1]] )# left bottom
        midcnrs.append( [((16,      H/6      ), -90), BezierRound, [1]] )# top left
        midcnrs_set.append( midcnrs )
    # draw
    if board in [BDL, BDR, BDT, BDB]:
        kad.draw_closed_corners( corners, layer, width )
    for midcnrs in midcnrs_set:
        l = 'Edge.Cuts' if board == BDM else 'F.Fab'
        w = width if board == BDM else width * 3
        kad.draw_closed_corners( midcnrs, l, w )

    # screw holes
    r = 4.5
    for idx, ctr in enumerate( [(r, r), (W-r, r), (W-r, H-r), (r, H-r), (W/3-r-mgn, H-r), (W*2/3+r+mgn, H-r)] ):
        sign = +1 if idx % 2 == 0 else -1
        #if board in [BDT, BDB, BDM]:# move hole mods
        if board in [BDT, BDB]:# move hole mods
            kad.set_mod_pos_angle( 'H{}'.format( idx + 1 ), ctr, 0 )
        if board in [BDL, BDR]:
            corners = []
            for i in range( 6 ):
                deg = i * 60 + 15 * sign
                pos = vec2.scale( 2.74, vec2.rotate( deg ), ctr )
                corners.append( [(pos, deg + 90), BezierRound, [0.7]] )
            kad.draw_closed_corners( corners, layer, width )
        if False:# draw holes in Edge.Cuts
            for brd, rad in [(BDT, 1.6), (BDB, 1.7)]:
                if board == brd:
                    kad.add_arc( ctr, vec2.add( ctr, (rad, 0) ), 360, layer, width )
        layer = 'F.Fab' if board != BDM else 'Edge.Cuts'# holes by edge.cuts
        kad.add_arc( ctr, vec2.add( ctr, (5.96/2, 0) ), 360, layer, width )

def divide_line( a, b, pitch ):
    v = vec2.sub( b, a )
    l = vec2.length( v )
    n = int( round( l / pitch ) )
    dv = vec2.scale( 1.0 / n, v )
    pnts = []
    for i in range( n ):
        pnts.append( vec2.scale( i, dv, a ) )
    pnts.append( b )
    return pnts

def get_distance( dist, dist_size, pnt ):
    x, y = vec2.scale( 10, vec2.sub( pnt, (PCB_Width/2.0, PCB_Height/2.0) ) )
    x = int( round( x + dist_size[0] / 2.0 ) )
    y = int( round( y + dist_size[1] / 2.0 ) )
    if 0 <= x and x < dist_size[0] and 0 <= y and y < dist_size[1]:
        return dist[y][x] / 10.0
    return 0

def draw_top_bottom( board, sw_pos_angles ):
    if board == BDT:# keysw holes
        for sw_pos, angle in sw_pos_angles:
            corners = []
            for i in range(4):
                deg = i * 90 + angle
                pos = vec2.scale( 13.90 / 2.0, vec2.rotate( deg ), sw_pos )
                corners.append( [(pos, deg + 90), BezierRound, [1]] )
            kad.draw_closed_corners( corners, 'Edge.Cuts', 0.1 )

    # read distance data
    board_type = 'T' if board == BDT else 'B'
    with open( '/Users/akihiro/repos/Hermit/Zoea{}/Edge_Fill.txt'.format( board_type ) ) as fin:
        dist_data = fin.readlines()
        dist_w = int( dist_data[0] )
        dist_h = int( dist_data[1] )
        # print( dist_w, dist_h )
        dist = []
        for y in range( dist_h ):
            vals = dist_data[y+2].split( ',' )
            del vals[-1]
            if len( vals ) != dist_w:
                print( 'Error: len( vals )({}) != dist_w({})'.format( len( vals ), dist_w ) )
                break
            vals = map( lambda v: float( v ), vals )
            dist.append( vals )

    layer = 'F.Cu'
    width = 1.0
    ctr_angles = []
    for idx, sw_pos_angle in enumerate( sw_pos_angles ):
        # print( idx, sw_pos_angle )
        if idx == 0:
            continue
        pos_a, angle_a = sw_pos_angles[idx-1]
        pos_b, angle_b = sw_pos_angle
        if abs( angle_a - angle_b ) > 1:
            vec_a = vec2.rotate( angle_a + 90 )
            vec_b = vec2.rotate( angle_b + 90 )
            ctr, ka, kb = vec2.find_intersection( pos_a, vec_a, pos_b, vec_b )
            if idx == 1:
                angle_a += (angle_a - angle_b) * 1.0
            elif idx + 1 == len( sw_pos_angles ):
                angle_b += (angle_b - angle_a) * 1.0
            ctr_angles.append( (ctr, angle_a, angle_b) )
            if False:
                print( ctr, ka, kb )
                kad.add_line( ctr, pos_a, layer, width )
                kad.add_line( ctr, pos_b, layer, width )
        else:
            ctr_angles.append( (None, pos_a, pos_b) )

    pos_dummy = [None, None]
    pitch = 2.0
    nyrange = range( -186, 450, 16 )
    width0, width1 = 0.3, 1.3
    for ny in nyrange:
        y = ny * 0.1
        uy = float( ny - nyrange[0] ) / float( nyrange[-1] - nyrange[0] )
        widths = [
            width0 + (width1 - width0) * uy,
            width1 + (width0 - width1) * uy,
        ]
        curvs = []
        for dir in [-1, +1]:
            idx = 1# base index
            pos, _ = sw_pos_angles[idx]
            pos = vec2.add( pos, (0, y) )
            while True:#0 <= idx and idx < len( sw_pos_angles ):
                idx2 = idx + dir
                if dir == -1:
                    if idx2 < 0:
                        break
                    ctr, angle_b, angle_a = ctr_angles[idx2]
                    vec_b = vec2.rotate( angle_b + 90 )
                    pos_b = vec2.scale( -vec2.distance( pos, ctr ), vec_b, ctr )
                    #kad.add_line( pos_a, pos_b, layer, width )
                    #curv = kad.calc_bezier_round_points( pos, vec2.rotate( angle_a ), pos_b, vec2.rotate( 180 + angle_b ), 8 )
                    curv = kad.calc_bezier_corner_points( pos, vec2.rotate( angle_a ), pos_b, vec2.rotate( 180 + angle_b ), pitch )
                    curvs.append( curv )
                    pos = pos_b
                elif dir == +1:
                    if idx2 >= len( sw_pos_angles ):
                        break
                    ctr, angle_a, angle_b = ctr_angles[idx]
                    if ctr == None:# parallel lines
                        pos_b = angle_b
                        pos_b = vec2.add( pos_b, (0, y) )
                        #kad.add_line( pos, pos_b, layer, width )
                        curv = divide_line( pos, pos_b, pitch )
                        curvs.append( curv )
                        pos = pos_b
                    else:
                        vec_b = vec2.rotate( angle_b + 90 )
                        pos_b = vec2.scale( -vec2.distance( pos, ctr ), vec_b, ctr )
                        #kad.add_line( pos_a, pos_b, layer, width )
                        #curv = kad.calc_bezier_round_points( pos, vec2.rotate( 180 + angle_a ), pos_b, vec2.rotate( angle_b ), 6 )
                        curv = kad.calc_bezier_corner_points( pos, vec2.rotate( 180 + angle_a ), pos_b, vec2.rotate( angle_b ), pitch )
                        curvs.append( curv )
                        pos = pos_b
                idx = idx2

        for curv in curvs:
            # kad.add_lines( curv, layer, width )
            for idx, pnt in enumerate( curv ):
                if idx == 0:
                    continue
                for lidx, layer in enumerate( ['F.Cu', 'B.Cu'] ):
                    w = widths[lidx if board == BDT else 1 - lidx]
                    thr = w / 2.0 + 0.5
                    pnt_a = curv[idx-1]
                    pnt_b = pnt
                    dpt_a = None
                    dpt_b = None
                    div = 20
                    for n in range( 0, div + 1 ):
                        t = n / float( div )
                        p = vec2.scale( t, vec2.sub( pnt_b, pnt_a ), pnt_a )
                        d = get_distance( dist, (dist_w, dist_h), p )
                        if d >= thr:
                            if dpt_a == None:
                                dpt_a = p
                            dpt_b = p
                    if dpt_a != None and vec2.distance( dpt_a, dpt_b ) > 0.1:
                        kad.add_line( dpt_a, dpt_b, layer, w )
                        if pos_dummy[lidx] == None and w > 1.1:
                            pos_dummy[lidx] = pnt
    kad.set_mod_pos_angle( 'P1', pos_dummy[0], 0 )
    kad.set_mod_pos_angle( 'P2', pos_dummy[1], 0 )

def add_zone( net_name, layer_name, rect, zones ):
    layer = pcb.GetLayerID( layer_name )
    zone, poly = kad.add_zone( rect, layer, len( zones ), net_name )
    zone.SetZoneClearance( pcbnew.FromMils( 20 ) )
    zone.SetMinThickness( pcbnew.FromMils( 16 ) )
    #zone.SetThermalReliefGap( pcbnew.FromMils( 12 ) )
    #zone.SetThermalReliefCopperBridge( pcbnew.FromMils( 24 ) )
    zone.Hatch()
    #
    zones.append( zone )
    #polys.append( poly )

def make_rect( size, offset = (0, 0) ):
    return map( lambda pt: vec2.add( (size[0] * pt[0], size[1] * pt[1]), offset ), FourCorners )


def main():
    # board type
    filename = pcb.GetFileName()
    m = re.search( r'/Hermit([^/])/', filename )
    if not m:
        return
    boardname = m.group( 1 )
    # print( filename, boardname )
    for bname, btype in [('L', BDL), ('R', BDR), ('T', BDT), ('B', BDB), ('M', BDM)]:
        if boardname == bname:
            board = btype
            if board in [BDL, BDR, BDM]:
                kad.add_text( (PCB_Width/2, 1.5), 0, 'Hermit{} by orihikarna 21/04/01'.format( bname ),
                    'F.SilkS' if board != BDR else 'B.SilkS', (1, 1), 0.15,
                    pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER )
            break

    drawEdgeCuts( board )

    ### zones
    zones = []
    if board in [BDL, BDR, BDM]:
        add_zone( 'GND', 'F.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )
        add_zone( 'GND', 'B.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )

    ###
    ### Set key positios
    ###
    sw_pos_angles = []
    for name, key in keys.items():
        px, py, _, _, angle = key
        if board == BDR:
            angle += 180# back side
        sw_pos = (px, -py)
        sw_pos_angles.append( (sw_pos, -angle) )
        # col = int( name[0] )
        row = int( name[1] )
        # SW & LED & Diode
        if board in [BDL, BDR]:
            ## SW
            kad.set_mod_pos_angle( 'SW' + name, sw_pos, angle )
            ## LED
            sign = [+1, -1][board]
            led_base_angle = 180 if name in L2R else 0
            pos = vec2.scale( 4.93, vec2.rotate( - angle - 90 * sign ), sw_pos )
            kad.set_mod_pos_angle( 'L' + name, pos, led_base_angle + angle )
            if True:# LED holes
                corners = []
                for i in range( 4 ):
                    deg = i * 90 - angle
                    pt = vec2.scale( [3.6, 3.2][i % 2] / 2.0, vec2.rotate( deg ), pos )
                    corners.append( [(pt, deg + 90), BezierRound, [0.2]] )
                kad.draw_closed_corners( corners, 'Edge.Cuts', 0.1 )
            # LED pass caps
            pos = vec2.mult( mat2.rotate( angle ), (0, -7.5 * sign), sw_pos )
            kad.set_mod_pos_angle( 'CL' + name, pos, led_base_angle + angle )
            ## Diode
            Dx = +5.8 * sign
            Dy = -0.6 * sign
            if name != '91':
                pos = vec2.mult( mat2.rotate( angle ), (+Dx, +Dy), sw_pos )
                kad.set_mod_pos_angle( 'D' + name, pos, angle - 90 * sign )
                # wire to SW
                kad.wire_mods( [('D' + name, '2', 'SW' + name, '2', 0.5, (Dird, 0, 0))])
            ## D0
            if name == '82':
                pos = vec2.mult( mat2.rotate( angle ), (-Dx, -Dy), sw_pos )
                kad.set_mod_pos_angle( 'D0', pos, angle - 90 )
                # wire to SW
                kad.wire_mods( [('D0', '1', 'SW' + name, '3', 0.5, (Dird, 0, 0))])

    # if board in [BDT, BDB]:
    #     draw_top_bottom( board, sw_pos_angles )

    ###
    ### Set mod positios
    ###
    if board == BDL:
        kad.move_mods( (0, 0), 0, [
            # mcu
            (None, (63, 85), 0, [
                ('U1', (0, 0), 0),
                # pass caps
                (None, (0, 0), 0, [
                    ('C4', (+5.8, +4.4), 180),
                    ('C3', (-5.8, -4.4), 0),
                    ('C5', (-8.7, -4.2), 90),
                ] ),
            ] ),
            # regulators
            (None, (72, 100), -90 - 9.6, [
                ('C1', (0, -2.7), 0),
                ('U2', (-0.2, 0), 0),
                ('C2', (0, +2.7), 0),
            ] ),
            # USB (PC) connector
            (None, (J2_x, J2_y), -9.6, [
                ('J2', (0, 0), 90),
                ('R8', (-7.5, +5.2), 0),
                ('R9', (-7.5, -5.2), 0),
                ('R5', (-12.4, -2), 180),# USB DM/DP
                ('R4', (-12.4,  0), 180),# USB DM/DP
                ('F1', (-12.4, +2), 180),
                ('L1', (-12.4, +4), 180),
            ] ),
            # Pin headers
            (None, (J3_x, J3_y), 0, [
                ('J3', (0, 0), 90),
                ('C6', (3.81, -2.4), 180),# NRST
                ('D1', (-3.6, 0), 180),# LED
                ('R1', (-3.6, -2.0), 180),
            ] ),
        ] )
    elif board == BDR:
        kad.move_mods( (PCB_Width/2, 28.5), 0, [
            # expander
            ('U1', (0, 0), -90),
            ('C1', (6.5, -2.8), 90),
            # R1
            ('R1', (-7.5, 3.2), 0),
        ] )
        kad.move_mods( (0, 0), 0, [
            # Pin headers
            ('J3', (J3_x + 1.27, PCB_Height*2/3 - 1.27), 90),
        ] )
    # Split (USB) connector
    if board in [BDL, BDR]:
        # Split (USB) connector
        sign = [+1, -1][board]
        kad.move_mods( (J1_x, J1_y), 0, [
            (None, (2.62, 0), 0, [
                ('J1', (0, 0), -90 * sign),
                ('R6', (7.5, -5.2 * sign), 180),
                ('R7', (7.5, +5.2 * sign), 180),
            ] ),
            # I2C pull-ups
            (None, (3, 0), 0, [
                ('R2', (12, -1.9), +90),
                ('R3', (12, +1.9), -90),
            ] ),
        ] )
    # Debounce RRCs
    if board in [BDL]:#[BDL, BDR]:
        for col in map( str, range( 1, 10 ) ):
            mod_sw = 'SW' + col + '1'
            if col == '6':
                mod_sw = 'SW71'
                dx, dy = 8.0, -3.8
            elif col == '8':
                mod_sw = 'SW82'
                dx, dy = -9.4, 0
            elif col == '9':
                dx, dy = -9, -10
            else:
                dx, dy = -9.2, -3.8
            pos, angle = kad.get_mod_pos_angle( mod_sw )
            kad.move_mods( pos, angle + [180, 0][board], [
                (None, (dx, dy), 0, [
                    ('C' + col + '1', (0, -2), 0),
                    ('R' + col + '1', (0,  0), 0),
                    ('R' + col + '2', (0, +2), 0),
                ] ),
            ] )

    ###
    ### Wire mods
    ###
    # mcu
    if board == BDL:
        # mcu
        via_vcca1 = kad.add_via_relative( 'U1',  '1', (-3.0, -0.15), VIA_Size[2] )
        via_vcca5 = kad.add_via_relative( 'U1',  '5', (-3.0, +0.0), VIA_Size[2] )
        via_nrst  = kad.add_via_relative( 'U1',  '4', (6.0, 0), VIA_Size[3] )
        via_swclk = kad.add_via_relative( 'U1', '24', (5.0, 0), VIA_Size[3] )
        via_swdio = kad.add_via_relative( 'U1', '23', (4.0, 0), VIA_Size[3] )
        via_rx    = kad.add_via_relative( 'U1',  '9', (1.2, 2.0), VIA_Size[3] )
        via_tx    = kad.add_via_relative( 'U1',  '8', (3.0, 4.2), VIA_Size[3] )
        via_led1  = kad.add_via_relative( 'U1', '13', (0, 4.0), VIA_Size[3] )
        via_led2  = kad.add_via_relative( 'R1',  '1', (0, 2.0), VIA_Size[3] )
        via_gnd_c5 = kad.add_via_relative( 'C5', '2', (0, -2.0), VIA_Size[1] )
        via_5v_c1_1 = kad.add_via_relative( 'C1', '1', (-2.0, 0), VIA_Size[1] )
        via_5v_c1_2 = kad.add_via_relative( 'C1', '1', (+4.0, 0), VIA_Size[1] )
        # VCC = pcb.FindNet( 'VCC' )
        kad.wire_mods( [
            # pass caps
            ('C4', '1', 'U1', '17', 0.5, (Dird, -45, 0, -0.6)),
            ('C4', '2', 'U1', '16', 0.5, (Dird, 0, 90, -1)),
            ('C3', '1', 'U1',  '1', 0.5, (Dird, -45, 0, -0.6)),
            ('C3', '2', 'U1', '32', 0.5, (Dird, 0, 90, -1)),
            ('C3', '2', 'C5', '2',  0.5, (Dird, ([(1.25, 90)], 0), -45, -1)),
            # regulator
            ('U2', '1', 'C1', '1', 0.6, (ZgZg, 90, 30)),# 5V
            ('U2', '3', 'C1', '2', 0.6, (ZgZg, 90, 30, -1)),# Gnd
            ('U2', '3', 'C2', '2', 0.6, (ZgZg, 90, 30, -1)),# Gnd
            ('U2', '2', 'C2', '1', 0.6, (ZgZg, 90, 30)),# Vcc
            # C4 <--> C2
            ('C4', '1', 'C2', '1', 0.6, (Dird, 90, 90)),# Vcc
            ('C4', '2', 'C2', '2', 0.6, (Dird, 90, 90)),# Gnd
            # C1 5V
            ('C1', '1', 'C1', via_5v_c1_1, 0.6, (Strt)),
            ('C1', via_5v_c1_1, 'C1', via_5v_c1_2, 0.6, (Strt), 'B.Cu'),
            # C1 GND
            ('C1', '2', 'R8', '2', 0.6, (Dird, 90, 90)),
            # VCC
            ('U1', '1', 'U1', '17', 0.5, (Dird, 0, ([(1.4, 180)], 90), -0.4)),
            ('U1', '5', 'U1', '17', 0.5, (Dird, 0, ([(1.4, 180)], 90), -0.4)),
            # VCCA
            ('U1', '5', None, via_vcca5, 0.5, (Strt)),
            ('C5', '1', None, via_vcca1, 0.5, (Dird, 45, 90)),
            ('U1', via_vcca1, None, via_vcca5, 0.6, (Strt), 'B.Cu'),
            # GND
            ('C5', '2', 'C5', via_gnd_c5, 0.6, (Strt)),
            # USB
            ('U1', '21', 'R4', '2', 0.5, (Dird, 0, ([(1.0, 0)], -45), -0.3)),
            ('U1', '22', 'R5', '2', 0.5, (Dird, 0, ([(1.6, 0)], -45), -0.3)),
            # I2C pull-up's
            ('U1', '2', 'R2', '1', 0.5, (Dird, 180, -45, -0.8)),
            ('U1', '3', 'R3', '1', 0.5, (Dird, 180, -45, -0.8)),
            # NRST
            ('U1', '4', None, via_nrst, 0.4, (Strt)),
            ('J3', '4', None, via_nrst, 0.4, (Dird, 0, 90, -1), 'B.Cu'),
            ('J3', '4', 'C6', '1', 0.4, (Dird, 0, 0, -1)),
            ('J3', '1', 'C6', '2', 0.4, (Dird, 0, 0, -1)),
            # SWCLK/DIO
            ('U1', '24', None, via_swclk, 0.4, (Strt)),
            ('U1', '23', None, via_swdio, 0.4, (Strt)),
            ('J3', '6', 'U1', via_swclk, 0.4, (Dird, 0, 0, -1), 'B.Cu'),
            ('J3', '5', 'U1', via_swdio, 0.4, (Dird, 0, 0, -1), 'B.Cu'),
            # TX/RX
            ('U1', '9', None, via_rx, 0.4, (Dird, 90, 0)),
            ('U1', '8', None, via_tx, 0.4, (Dird, 90, 0)),
            ('J3', '3', 'U1', via_rx, 0.4, (Dird, 0, 0, -1), 'B.Cu'),
            ('J3', '2', 'U1', via_tx, 0.4, (Dird, 0, 0, -1), 'B.Cu'),
            # D1
            ('U1', '13', None, via_led1, 0.5, (Dird, 0, 90, -1)),
            ('U1', via_led1, None, via_led2, 0.5, (Dird, 0, 90, -1), 'B.Cu'),
            ('U1', via_led2, 'R1', '1', 0.5, (Dird, 0, 90, -1)),
            ('R1', '2', 'D1', '2', 0.5, (Dird, 0, 90, -1)),
            ('J3', '1', 'D1', '1', 0.5, (Dird, 0, 0, -1)),
        ] )
    elif board == BDR:
        # mcp23017
        via_u1_vcc  = kad.add_via_relative( 'U1', '9', (1.8, 0), VIA_Size[2] )
        via_u1_vcc2 = kad.add_via_relative( 'U1', '9', (1.8, 4), VIA_Size[2] )
        via_u1_nrst = kad.add_via_relative( 'U1', '9', (4.5, 0), VIA_Size[3] )
        via_led_u1 = kad.add_via_relative( 'U1', '1', (0, -2), VIA_Size[2] )
        via_led_d1 = kad.add_via_relative( 'D1', '2', (0, -5), VIA_Size[2] )
        kad.wire_mods( [
            # Gnd
            ('U1', '15', 'U1', '17', 0.45, (Strt)),
            # pass caps
            ('U1', via_u1_vcc2, 'C1', '1', 0.45, (Dird, 90, 0)),
            ('U1', '10', 'C1', '2', 0.45, (Dird, ([(1.4, 180)], 90), 0, -0.4)),
            # NRST
            ('U1', via_u1_nrst, 'U1', '18', 0.4, (Dird, -45, 0, -0.4)),
            ('U1', via_u1_vcc, 'U1', '9', 0.45, (Dird, -45, 0, -0.2)),
            ('U1', via_u1_vcc, 'U1', via_u1_vcc2, 0.5, (Strt), 'Opp'),
            ('U1', via_u1_vcc, 'U1', via_u1_nrst, 0.4, (Dird, 0, 90, -0.6), 'Opp'),
            # Vcc
            ('U1', via_u1_vcc, 'J1', via_splt_vbb, 0.5, (Dird, ([(0.2, 0)], 90), ([(21, 90)], -45), -1)),
            # D1
            ('R1', '1', 'D1', '1', 0.5, (ZgZg, 90, 45, -0.8)),
            ('U1', '1', 'U1', via_led_u1, 0.45, (Dird, 90, 0)),
            ('D1', '2', 'D1', via_led_d1, 0.45, (Dird, 90, 0)),
            ('U1', via_led_u1, 'D1', via_led_d1, 0.5, (Dird, 90, 90, -0.8), 'Opp'),
            # J3
            ('J3', '3', 'U1', via_scl, 0.45, (Dird, -45, ([(0.4, 45)], 0), -1)),
            ('J3', '4', 'U1', via_sda, 0.45, (Dird, 45, 0, -1)),
            ('J3', '5', 'U1', via_u1_vcc2, 0.5, (ZgZg, 0, 45, -1)),
        ] )
    # Split (USB) connector
    if board in [BDL, BDR]:
        via_splt_vba = kad.add_via_relative( 'J1', 'A4', (-0.4,  -5.8), VIA_Size[1] )
        via_splt_vbb = kad.add_via_relative( 'J1', 'B4', (+0.4,  -5.8), VIA_Size[1] )
        via_splt_cc1 = kad.add_via_relative( 'J1', 'A5', (-0.15, -2.4), VIA_Size[3] )
        via_splt_cc2 = kad.add_via_relative( 'J1', 'B5', (+0.15, -3.2), VIA_Size[3] )
        via_splt_dpa = kad.add_via_relative( 'J1', 'A6', (-0.5,  -4.8), VIA_Size[3] )
        via_splt_dpb = kad.add_via_relative( 'J1', 'B6', (+0.15, -4.8), VIA_Size[3] )
        via_splt_dma = kad.add_via_relative( 'J1', 'A7', (+0.15, -4.0), VIA_Size[3] )
        via_splt_dmb = kad.add_via_relative( 'J1', 'B7', (-0.15, -4.1), VIA_Size[3] )
        via_splt_sb1 = kad.add_via_relative( 'J1', 'A8', (+0.15, -2.4), VIA_Size[3] )
        via_splt_sb2 = kad.add_via_relative( 'J1', 'B8', (-0.15, -3.2), VIA_Size[3] )
        via_r6_cc1   = kad.add_via_relative( 'R6', '1',  (0,     -1.4), VIA_Size[3] )
        via_r7_cc2   = kad.add_via_relative( 'R7', '1',  (0,     +1.4), VIA_Size[3] )
        kad.wire_mods( [
            # gnd
            ('J1', 'S1', 'J1', 'S2', 0.8, (Dird, ([(0.8, 45)], 0), -45), 'Opp'),
            # vbus
            ('J1', via_splt_vba, 'J1', 'A4', 0.8, (Dird, +60, ([(1.6, 90), (0.5, 135)], 90))),
            ('J1', via_splt_vbb, 'J1', 'B4', 0.8, (Dird, -60, ([(1.6, 90), (0.5,  45)], 90))),
            ('J1', via_splt_vba, 'J1', via_splt_vbb, 0.8, (Strt), 'Opp'),
            # dm/dp = I2C
            ('J1', via_splt_dpa, 'J1', 'A6', 0.3, (Dird, 90, ([(3.52, 90)], -45), -0.1)),
            ('J1', via_splt_dpb, 'J1', 'B6', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dpa, 'J1', via_splt_dpb, 0.4, (Strt), 'Opp'),
            ('J1', via_splt_dma, 'J1', 'A7', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dmb, 'J1', 'B7', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dma, 'J1', via_splt_dmb, 0.4, (Dird, 0, -45, -0.6), 'Opp'),
            # cc1/2
            ('J1', via_splt_cc1, 'J1', 'A5', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_cc2, 'J1', 'B5', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_cc1, 'J1', via_r6_cc1, 0.4, (Dird, -45, 0, -0.6), 'Opp'),
            ('J1', via_splt_cc2, 'J1', via_r7_cc2, 0.4, (Dird, +45, 0, -0.6), 'Opp'),
            ('J1', via_r6_cc1, 'R6', '1', 0.4, (Dird, 45, 90)),
            ('J1', via_r7_cc2, 'R7', '1', 0.4, (Dird, 45, 90)),
            ('R6', '2', 'J1', 'A1', 0.8, (Dird, 90, ([(1.1, 90)], -45))),
            ('R7', '2', 'J1', 'B1', 0.8, (Dird, 90, ([(1.1, 90)], +45))),
            ('R6', '2', 'J1', 'S1', 0.8, (Dird, 90, 90)),
            ('R7', '2', 'J1', 'S2', 0.8, (Dird, 90, 90)),
            # sbu = LED
            ('J1', via_splt_sb1, 'J1', 'A8', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_sb2, 'J1', 'B8', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_sb1, 'J1', via_splt_sb2, 0.4, (Dird, 0, -45, -0.6), 'Opp'),
        ] )
    # Debounce
    via_dbn_vccs = {}
    via_dbn_gnds = {}
    if board in [BDL]:
        w_dbn = 0.5
        r_dbn = -1
        for cidx in range( 1, 10 ):
            col = str( cidx )
            # wire islands
            mod_cap = 'C' + col + '1'
            mod_r1 = 'R' + col + '1'
            mod_r2 = 'R' + col + '2'
            kad.wire_mods( [
                (mod_r1, '2', mod_r2,  '2', w_dbn, (Strt)),
                (mod_r1, '1', mod_cap, '1', w_dbn, (Strt)),
            ])
            # wire to column diodes
            mod_dio = 'D' + col + ('2' if cidx in [6, 8] else '1')
            if cidx == 6:
                kad.wire_mods( [
                    (mod_r2, '2', mod_dio, '1', w_dbn, (Dird, 90, ([(2, 90), (10, 0)], 90, r_dbn))),# 62
                ] )
            if cidx not in [6, 9]:
                kad.wire_mods( [
                    (mod_r2, '2', mod_dio, '1', w_dbn, (Dird, 90, 90, r_dbn)),
                ] )
            # Vcc/Gnd vias
            if cidx in [8]:
                pos = (-1.8, 0)
            else:
                pos = (-1.6, -7.0)
            via_dbn_gnds[col] = kad.add_via_relative( mod_r2,  '1', pos, VIA_Size[1] )
            via_dbn_vccs[col] = kad.add_via_relative( mod_cap, '2', (0, -1.8), VIA_Size[1] )
            kad.wire_mods( [
                (mod_r2,  '1', mod_r2,  via_dbn_gnds[col], w_dbn, (Dird, 0, 90, r_dbn)),
                (mod_cap, '2', mod_cap, via_dbn_vccs[col], w_dbn, (Strt)),
            ] )
        # wire Vcc/Gnd via rows
        for cidx in range( 0, 7 ):
            ccurr = '9' if cidx == 0 else str( cidx )
            cnext = str( cidx + 1 )
            kad.wire_mods( [
                ('C' + ccurr + '1', via_dbn_vccs[ccurr], 'C' + cnext + '1', via_dbn_vccs[cnext], 0.6, (Strt), 'B.Cu'),
                ('R' + ccurr + '2', via_dbn_gnds[ccurr], 'R' + cnext + '2', via_dbn_gnds[cnext], 0.6, (Strt), 'B.Cu'),
            ] )
        # Vcc from mcu
        kad.wire_mods( [
            ('U1', via_vcca5, 'C81', via_dbn_vccs['8'], 0.6, (Dird, 0, 0), 'B.Cu'),
            ('C81', via_dbn_vccs['8'], 'C91', via_dbn_vccs['9'], 0.6, (Dird, 90, 90), 'B.Cu'),
        ] )
    # ROW lines
    if board == BDL:
        w_row = 0.6
        r_row = -1
        for ridx in range( 1, 5 ):
            row = str( ridx )
            for cidx in range( 1, 7 ):
                idx = str( cidx ) + row
                if idx not in keys.keys():
                    continue
                cnext = 7 if cidx == 5 and row == '1' else cidx + 1
                nidx = str( cnext ) + row
                if nidx not in keys.keys():
                    continue
                if cidx in [1, 3]:
                    prm_row = (Strt)
                elif cidx in [2]:
                    prm_row = (Dird, 0, 0, r_row)
                elif cidx in [4]:
                    dx = [None, 2.4, 3.6, 6.4, 6.4][ridx]
                    angle = [None, 45, 45 + 9.6, 60, 60][ridx]
                    prm_row = (Dird, 0, ([(dx, 180)], angle), r_row)
                elif cidx in [5, 6]:
                    prm_row = (Dird, ([(3, 0)], 30), 0, r_row)
                kad.wire_mods( [
                    ('SW'+idx, '1', 'SW'+nidx, '1', w_row, prm_row),
                ] )
        # Row to mcu
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'SW31', '1' )
        via_row4_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (-6.0, +3), pos ), kad.get_pad_pos_net( 'U1', '12' )[1], VIA_Size[2] )
        via_row3_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (-3.5, +5), pos ), kad.get_pad_pos_net( 'U1', '11' )[1], VIA_Size[2] )
        via_row2_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (-2.0, +3), pos ), kad.get_pad_pos_net( 'U1', '10' )[1], VIA_Size[2] )
        kad.wire_mods( [
            ('SW34', '1', 'U1', via_row4_top, w_row, (Dird, ([(4, 180), (6, 135), (20, 90)], 74), 0), 'F.Cu'),# Row4
            ('SW33', '1', 'U1', via_row3_top, w_row, (Dird, ([(4, 180), (4, 135), (4, 90)], 74), 0), 'F.Cu'),# Row3
            ('SW32', '1', 'U1', via_row2_top, w_row, (Dird, ([(2, 180), (3, 135), (3, 90)], 74), 0), 'F.Cu'),# Row2
            ('SW21', '1', 'U1', '28', w_row, (Dird, 0, 90, 0), 'F.Cu'),# Row1
        ])
        # Thumb Rows to mcu
        via_row2_btm = kad.add_via_relative( 'U1', '10', (0, -3.2), VIA_Size[3] )
        via_row3_btm = kad.add_via_relative( 'U1', '11', (0, -2.4), VIA_Size[3] )
        via_row4_btm = kad.add_via_relative( 'U1', '12', (0, -1.6), VIA_Size[3] )
        kad.wire_mods( [
            ('SW31', via_row2_top, 'U1', via_row2_btm, w_row, (Dird, -30, 90), 'B.Cu'),# Row2
            ('SW31', via_row3_top, 'U1', via_row3_btm, w_row, (Dird, -30, 90), 'B.Cu'),# Row3
            ('SW31', via_row4_top, 'U1', via_row4_btm, w_row, (Dird, -30, 90), 'B.Cu'),# Row4
            ('U1', '10', 'U1', via_row2_btm, w_row, (Strt)),# Row2
            ('U1', '11', 'U1', via_row3_btm, w_row, (Strt)),# Row3
            ('U1', '12', 'U1', via_row4_btm, w_row, (Strt)),# Row4
            ('SW82', '1', 'U1', via_row2_btm, w_row, (Dird, 0, ([(2, 180)], 45)), 'B.Cu'),# Row2
            ('SW83', '1', 'U1', via_row3_btm, w_row, (Dird, ([(6, 180), (16, 110), (6, 54)], 20), ([(2, 180)], 45)), 'B.Cu'),# Row3
            ('SW84', '1', 'U1', via_row4_btm, w_row, (Dird, ([(9, 180), (20, 110), (14, 130), (8, 74)], 40), ([(2, 180)], 45)), 'B.Cu'),# Row4
        ])
    # COL lines
    if board == BDL:
        for col in map( str, range( 1, 9 ) ):
            mod_dio = 'D' + col
            if col == '8':
                prm_23 = (Dird, 0, ([(2, 90)], 0), -0.4)
                prm_34 = (Dird, ([(2, 90)], 0), ([(2, 90)], 0), -0.4)
            else:
                prm_12 = (Dird, ([(8, 180)], 90), ([(2, 90)], 0), -0.4)
                prm_23 = (Dird, ([(7, 180)], 90), ([(2, 90)], 0), -0.4)
                prm_34 = (Dird, ([(7, 180)], 90), ([(2, 90)], 0), -0.4)
            if col not in['6', '8']:
                kad.wire_mods( [(mod_dio + '1', '1', mod_dio + '2', '1', 0.5, prm_12)] )
            if True:
                kad.wire_mods( [(mod_dio + '2', '1', mod_dio + '3', '1', 0.5, prm_23)] )
            if col not in ['7']:
                kad.wire_mods( [(mod_dio + '3', '1', mod_dio + '4', '1', 0.5, prm_34)] )
        kad.wire_mods( [
            ('R92', '2', 'SW91', '2', 0.5, (Dird, 90, 0, -0.4)),# 91
            ('C91', '2', 'SW91', '1', 0.5, (Dird, ([(1.6, 0)], 90), 0, -0.4)),# 91
        ] )
        via_col8_1 = kad.add_via_relative( 'U1', '7', (-3, 0), VIA_Size[2] )
        via_col8_2 = kad.add_via_relative( 'U1', '7', (-6, 0), VIA_Size[2] )
        kad.wire_mods( [
            ('C91', '1', 'U1', '31', 0.5, (Dird, 90, ([(8, 90)], 0))),
            ('C11', '1', 'U1', '29', 0.5, (Dird, 90, ([(10, 90)], 0))),
            ('C21', '1', 'U1', '27', 0.5, (Dird, 90, ([(2.8, 90)], 0))),
            ('C31', '1', 'U1', '26', 0.5, (Dird, 90, ([(2.0, 90)], 0))),
            ('C41', '1', 'U1', '25', 0.5, (Dird, 90, 0)),
            ('C81', '1', 'U1', via_col8_2, 0.5, (Dird, 90, 90)),
            ('U1', via_col8_1, 'U1', via_col8_2, 0.5, (Strt), 'B.Cu'),
            ('U1', '7', 'U1', via_col8_1, 0.5, (Strt)),
        ] )
        via_col5_1 = kad.add_via_relative( 'U1', '20', (3, 0), VIA_Size[3] )
        via_col6_1 = kad.add_via_relative( 'U1', '19', (3, 0), VIA_Size[3] )
        via_col7_1 = kad.add_via_relative( 'U1', '18', (3, 0), VIA_Size[3] )
        via_col5_2 = kad.add_via_relative( 'U1', '20', (8, -5), VIA_Size[3] )
        via_col6_2 = kad.add_via_relative( 'U1', '19', (8, -5), VIA_Size[3] )
        via_col7_2 = kad.add_via_relative( 'U1', '18', (8, -5), VIA_Size[3] )
        kad.wire_mods( [
            ('U1', '20', 'U1', via_col5_1, 0.4, (Strt)),
            ('U1', '19', 'U1', via_col6_1, 0.4, (Strt)),
            ('U1', '18', 'U1', via_col7_1, 0.4, (Strt)),
            ('U1', via_col5_1, 'U1', via_col5_2, 0.4, (Strt), 'B.Cu'),
            ('U1', via_col6_1, 'U1', via_col6_2, 0.4, (Strt), 'B.Cu'),
            ('U1', via_col7_1, 'U1', via_col7_2, 0.4, (Strt), 'B.Cu'),
            ('C51', '1', 'U1', via_col5_2, 0.5, (Dird, ([(3.0, 90), (20, 0)], -9.6), 0)),
            ('C61', '1', 'U1', via_col6_2, 0.5, (Dird, ([(3.8, 90), (20, 0)], -9.6), 0)),
            ('C71', '1', 'U1', via_col7_2, 0.5, (Dird, ([(4.6, 90), (20, 0)], -9.6), 0)),
        ] )
    elif board == BDR:
        kad.wire_mods( [
            ('D11', '2', 'U1', '5', 0.45, (Dird, ([(6, 0), (14, 90)], -45), ([(2.2, 180)], -90), -1)),
            ('D12', '2', 'U1', '4', 0.45, (Dird, 0, ([(3.0, 180)], 90), -1.6)),
            ('D13', '2', 'U1', '3', 0.45, (Dird, 0, ([(3.0, 180)], 90), -1.6)),
            ('D14', '2', 'U1', '2', 0.45, (Dird, 0, ([(2.2, 180)], 90), -1.0)),
            ('RB1', '2', 'U1', '22',0.45, (Dird, 0, ([(2.0, 180)], 90), -0.8)),
        ] )
    # LED
    w_pwr = 0.75
    w_pwr2 = 0.6
    w_dat = 0.4
    r_pwr = -1
    r_dat = -0.6
    via_led_pwrLs = {}
    via_led_pwrRs = {}
    via_led_datLs = {}
    via_led_datRs = {}
    if board == BDL:
        # LED vias
        for idx in keys.keys():
            col = idx[0]
            mod_led = 'L' + idx
            mod_cap = 'CL' + idx
            if idx in L2R:
                sign = +1
                cap_pwrL, cap_pwrR = '2', '1'
                led_pwrL, led_pwrR = '3', '1'
                led_datL, led_datR = '4', '2'
            else:# R2L
                sign = -1
                cap_pwrL, cap_pwrR = '1', '2'
                led_pwrL, led_pwrR = '1', '3'
                led_datL, led_datR = '2', '4'
            # thumb column (Col8)
            if col == '8':
                # datR via
                if idx not in ['82']:
                    via_led_datRs[idx] = kad.add_via_relative( mod_led, led_datR, (0, +sign * 1.4), VIA_Size[2] )
                # pwrR: cap <--> led
                r = 0 if idx in ['83', '84'] else r_dat
                kad.wire_mods( [
                    (mod_cap, cap_pwrR, mod_led, led_pwrR, w_pwr2, (Dird, 0, 90, r), 'F.Cu'),
                ] )
            else:# other fingers
                # pwrL/R via
                via_led_pwrRs[idx] = kad.add_via_relative( mod_led, led_pwrR, (0, -sign * 1.8), VIA_Size[1] )
                if idx not in ['14', '91']:
                    via_led_pwrLs[idx] = kad.add_via_relative( mod_cap, cap_pwrL, (0, +sign * 1.7), VIA_Size[1] )
                # datR via
                if idx not in ['64', '71', '72', '73']:
                    via_led_datRs[idx] = kad.add_via_relative( mod_led, led_datR, (-sign * 1.4, 0), VIA_Size[2] )
                # pwrL: via <--> cap
                if idx in via_led_pwrLs:
                    kad.wire_mods( [
                        (mod_cap, cap_pwrL, mod_led, via_led_pwrLs[idx], w_pwr2, (Strt), 'F.Cu'),
                    ] )
                # pwrR: via <--> cap & led
                kad.wire_mods( [
                    (mod_cap, cap_pwrR, mod_cap, via_led_pwrRs[idx], w_pwr2, (Dird, 0, 90), 'F.Cu'),
                    (mod_led, led_pwrR, mod_led, via_led_pwrRs[idx], w_pwr2, (Strt), 'F.Cu'),
                ] )
            # datL via
            if idx not in ['14']:
                via_led_datLs[idx] = kad.add_via_relative( mod_led, led_datL, (0, -sign * 1.1), VIA_Size[2] )
            # pwrL: SW '3' <--> cap & led
            r = 0 if idx in ['83', '84'] else r_dat
            kad.wire_mods( [
                (mod_cap, cap_pwrL, 'SW' + idx, '3', w_pwr2, (Dird, 90, ([(2.3, -90)], 0), r)),
                (mod_led, led_pwrL, 'SW' + idx, '3', w_pwr2, (Dird, 0, 90, r), ['F.Cu', 'B.Cu'][board]),
            ] )
            # datR: led <--> via
            if idx in via_led_datRs:
                kad.wire_mods( [
                    (mod_led, led_datR, mod_led, via_led_datRs[idx], w_dat, (Strt), 'F.Cu'),
                ] )
            # datL: led <--> via
            if idx in via_led_datLs:
                kad.wire_mods( [
                    (mod_led, led_datL, mod_led, via_led_datLs[idx], w_dat, (Strt), 'F.Cu'),
                ] )
        # pwrL, pwrR, data lines
        prm_pwrL_left = ([(3.6, -90), (12.1, 0)], 45 + 8.5)
        for idx in keys.keys():
            ccurr = idx[0]
            rcurr = idx[1]
            cidx = int( ccurr )
            ridx = int( rcurr )
            if cidx in [7, 8]:
                continue
            if cidx == 9:
                cnext = '1'
            else:
                cnext = str( cidx + (2 if cidx == 5 and ridx == 1 else 1) )
            nidx = cnext + rcurr
            sign = +1 if idx in L2R else -1
            if nidx not in keys.keys():
                continue
            pwrR_offset = (sign * 0.5, 90)
            data_offset = (sign * 0.3, 90)
            if cidx in [1, 3] or (cidx == 5 and ridx == 1):
                prm_pwrL = (Dird, 90, 0, r_pwr)
                prm_pwrR = (Dird, 90, ([pwrR_offset], 0), r_pwr)
                prm_data = (Dird, 90, ([data_offset], 0), r_dat)
            elif cidx in [2]:
                prm_pwrL = (Dird, 0, 0, r_pwr)
                prm_pwrR = (Dird, ([pwrR_offset], 0), ([pwrR_offset], 0), r_pwr)
                prm_data = (Dird, ([(sign * 2.9, 90)], 0), ([data_offset], 0), r_dat)
            elif cidx in [4, 9]:
                dangle = 15 if ridx == 1 else 0
                if cidx in [9]:
                    prm_pwrL = (Dird, prm_pwrL_left, 0, r_pwr)
                else:
                    prm_pwrL = (Dird, 0, ([(sign * 3.8, 0)], 120 + dangle), r_pwr)
                prm_pwrR = (Dird, 0, ([pwrR_offset, (sign * 8.2, 0)], 60 - dangle), r_pwr)
                prm_data = (Dird, 0, ([data_offset, (sign * 3.8, 0)], 60 - dangle), r_dat)
            elif cidx in [5, 6]:
                prm_pwrL = (Dird, ([(sign * 6.4, 180)], 150), 0, r_pwr)
                prm_pwrR = (Dird, ([(sign * 3.2, 180)], 30), ([pwrR_offset], 0), r_pwr)
                prm_data = (Dird, 90, ([data_offset], 0), r_dat)
            kad.wire_mods( [
                ('L' + idx, via_led_pwrRs[idx], 'L' + nidx, via_led_pwrRs[nidx], w_pwr, prm_pwrR),
                ('L' + idx, via_led_datRs[idx], 'L' + nidx, via_led_datLs[nidx], w_dat, prm_data),
            ] )
            if idx in via_led_pwrLs:
                kad.wire_mods( [
                    ('CL' + idx, via_led_pwrLs[idx], 'CL' + nidx, via_led_pwrLs[nidx], w_pwr, prm_pwrL, 'B.Cu'),
                ] )
            else:
                kad.wire_mods( [
                    ('SW' + idx, '3', 'CL' + nidx, via_led_pwrLs[nidx], w_pwr, prm_pwrL, 'B.Cu'),
                ] )
        # Row1 --> Row2
        prm_pwrL = (Dird, prm_pwrL_left, ([(5, -90), (2, -45), (2.4, -90), (3.4, -135)], 0), r_pwr)
        prm_pwrR = (Dird, 0, 90, r_pwr)
        kad.wire_mods( [
            ('SW91', '3', 'CL12', via_led_pwrRs['12'], w_pwr, prm_pwrL, 'B.Cu'),# GNDD
            ('CL91', via_led_pwrRs['91'], 'SW12', '3', w_pwr, prm_pwrR, 'F.Cu'),
            ('L71', '2', 'L72', '4', w_dat, (Dird, ([(1.6, 180)], 90), ([(1.6, 0), (5.2, 90), (4.0, 135)], 0), r_dat), 'F.Cu'),# data
        ] )
        # Row2 --> Row3
        prm_pwrL = (Dird, 90, ([(5, +90), (2, 135), (2.4, +90), (3.4, 45)], 0), r_pwr)
        prm_pwrR = (Dird, ([(1.5, +90)], -45), 90, r_pwr)
        kad.wire_mods( [
            ('CL12', via_led_pwrLs['12'], 'CL13', via_led_pwrRs['13'], w_pwr, prm_pwrL, 'B.Cu'),
            ('CL12', via_led_pwrRs['12'], 'SW13', '3', w_pwr, prm_pwrR, 'F.Cu'),
            ('CL12', via_led_datLs['12'], 'CL13', via_led_datLs['13'], w_dat, (Dird, 90, ([(4, 90)], 60), r_dat), 'B.Cu'),# data
        ] )
        # Row3 --> Row4
        prm_pwrL = (Dird, 90, ([(5, -90), (2, -45), (2.4, -90), (3.4, -135)], 0), r_pwr)
        prm_pwrR = (Dird, ([(2.4, -90)], -60), 90, r_pwr)
        kad.wire_mods( [
            ('CL13', via_led_pwrLs['13'], 'CL14', via_led_pwrRs['14'], w_pwr, prm_pwrL, 'B.Cu'),
            ('CL13', via_led_pwrRs['13'], 'SW14', '3', w_pwr, prm_pwrR, 'F.Cu'),
            ('L73', '2', 'L64', '4', w_dat, (Dird, ([(1.6, 180), (6.0, 90)], 0), ([(5.8, 0)], 90), r_dat), 'F.Cu'),# data
        ] )
        # Col8, J1 --> Col9
        kad.wire_mods( [
            ('SW91', '3', 'J1', 'S4', w_pwr, (Dird, 90, 0, r_pwr), 'B.Cu'),
            ('J1', via_splt_vba, 'CL91', via_led_pwrRs['91'], w_pwr, (Dird, 0, ([(1.67, -90), (9.8, 0), (12, 90)], 135), r_pwr)),
            ('CL84', via_led_datLs['84'], 'CL91', via_led_datLs['91'], w_dat,
                (Dird, ([(0.8, 90), (5, 0), (7, -45), (16, -90), (20, -110), (4, -130)], -50), ([(4, 90), (1.8, 60), (9, 90), (10, 180)], 90), r_dat), 'B.Cu'),
        ] )
        # Col8 5V
        kad.wire_mods( [
            ('C1', via_5v_c1_2, 'D0', '2', w_pwr, (Dird, 0, 0, r_pwr)),
            ('D0', '2', 'SW83', '3', w_pwr, (Dird, ([(1.6, -90)], 0), 90, r_pwr)),
            ('SW83', '3', 'SW84', '3', w_pwr, (Dird, 90, 90, r_pwr), 'F.Cu'),
            ('J1', via_splt_vbb, 'SW84', '3', w_pwr, (Dird, 0, ([(3.6, -90), (14, 0), (20, +90)], -70), r_pwr), 'F.Cu'),
        ] )
        # Col8 GNDD
        via_led_pwrRs['84'] = kad.add_via_relative( 'CL84', '2', (4.8, 0), VIA_Size[0] )
        kad.wire_mods( [
            ('CL82', '2', 'L83', '3', w_pwr2, (Dird, 90, ([(1.6, 0), (5.6, 90), (3.4, 120)], 90), r_pwr), 'F.Cu'),
            ('L83',  '3', 'L84', '3', w_pwr2, (Dird, 90, ([(1.6, 0), (5.6, 90), (3.4, 120)], 90), r_pwr), 'F.Cu'),
            ('CL84', '2', 'CL84', via_led_pwrRs['84'], w_pwr, (Dird, 0, 90, r_pwr)),
            ('J1', 'S3',  'CL84', via_led_pwrRs['84'], w_pwr, (Dird, 0, ([(3, 0), (20, -90)], -110), r_pwr), 'B.Cu'),
        ] )
        # Col8 dat
        kad.wire_mods( [
            ('CL82', via_led_datLs['82'], 'CL83', via_led_datRs['83'], w_dat, (Dird, ([(1.6, 90)], 60), ([(1, -45), (3.8, -90), (1, -135)], 90), r_dat), 'B.Cu'),
            ('CL83', via_led_datLs['83'], 'CL84', via_led_datRs['84'], w_dat, (Dird, ([(1.6, 90)], 45), ([(1, -45), (3.8, -90), (1, -135)], 90), r_dat), 'B.Cu'),
        ] )
        # LDI
        kad.wire_mods( [
            ('U1', '15', 'L82', '4', w_dat, (Dird, 90, ([(1.6, 90), (1, 45), (3.8, 90), (1, 135)], 90), r_dat), 'F.Cu'),
        ] )
        # RDI
        kad.wire_mods( [
            ('U1', '14', 'J1', via_splt_sb1, 0.4, (Dird, ([(6, -90), (10, 180)], 90), 90, r_dat), 'F.Cu'),
        ] )
    elif board == BDR:
        # LED vias
        for idx in range( 5 ):
            mod_led = 'L' + get_key_postfix( idx )
            if mod_led != 'L11':
                via_led_dos[mod_led] = kad.add_via_relative( mod_led, '2', (-1.6, 0), VIA_Size[2] )
                kad.wire_mods( [(mod_led, '2', mod_led, via_led_dos[mod_led], 0.5, (Strt), 'B.Cu')] )
            via_led_dis[mod_led] = kad.add_via_relative( mod_led, '4', (+0.6, -1.2), VIA_Size[2] )
            kad.wire_mods( [(mod_led, '4', mod_led, via_led_dis[mod_led], 0.5, (Dird, 90, 0, -0.8), 'B.Cu')] )
            via_led_vccs[mod_led] = kad.add_via_relative( mod_led, '1', (-1.6, 0), VIA_Size[1] )
            kad.wire_mods( [(mod_led, '1', mod_led, via_led_vccs[mod_led], 0.6, (Strt), 'B.Cu')] )
        via_l14_5v = kad.add_via_relative( 'J1', 'B4', (0, -18), VIA_Size[0] )
        via_l14_di = kad.add_via_relative( 'J1', 'B4', (0, -17), VIA_Size[0] )
        kad.wire_mods( [
            # 5V
            ('SWB1', '2', mod_led, via_led_vccs[mod_led], 0.6, (Dird, ([(0.5, 0)], 90), 0, -1), 'B.Cu'),
            ('LB1', via_led_vccs['LB1'], 'J1', via_l14_5v, 0.6, (Dird, 0, 0, -1)),
            ('J1', via_l14_5v, 'L14', via_led_vccs['L14'], 0.6, (Dird, 0, ([(2.4, 90)], 0), -1), 'F.Cu'),
            ('L14', via_led_vccs['L14'], 'L13', via_led_vccs['L13'], 0.6, (Dird, 0, ([(2.4, 90), (11.3, 0)], -45), -1)),
            ('L13', via_led_vccs['L13'], 'L12', via_led_vccs['L12'], 0.6, (Dird, 0, ([(2.4, 90), (11.3, 0)], -45), -1)),
            ('L12', via_led_vccs['L12'], 'L11', via_led_vccs['L11'], 0.6, (Dird, 90, ([(2.4, 90), (11.3, 0)], -45), -1)),
            # DO --> DI
            ('L12', via_led_dos['L12'], 'L11', via_led_dis['L11'], 0.5, (Dird, ([(1.2, 180)], 90), ([(0.3, 90), (3.3, 0)], -45), -1)),
            ('L13', via_led_dos['L13'], 'L12', via_led_dis['L12'], 0.5, (Dird, 0, ([(0.3, 90), (3.3, 0)], -45), -1)),
            ('L14', via_led_dos['L14'], 'L13', via_led_dis['L13'], 0.5, (Dird, 0, ([(0.3, 90), (3.3, 0)], -45), -1)),
            ('J1', via_l14_di, 'L14', via_led_dis['L14'], 0.5, (Dird, 0, ([(0.3, 90)], 0), -1), 'F.Cu'),
            ('LB1', via_led_dos['LB1'], 'J1', via_l14_di, 0.5, (Dird, 0, 0, -1)),
            ('J1', via_splt_sb1, 'LB1', via_led_dis['LB1'], 0.5, (Dird, ([(2, 180), (1.4, -135)], 0), ([(0.3, 90), (3.3, 0)], -45), -1), 'Opp'),
            # J3
            ('J3', '2', 'LB1', via_led_dis['LB1'], 0.45, (Dird, ([(2, 0), (16, 90)], -30), ([(0.3, 90)], 0), -1)),
        ] )
        pcb.Delete( via_l14_5v )
        pcb.Delete( via_l14_di )

    # USB (PC) connector
    if board == BDL:
        via_usb_vba = kad.add_via_relative( 'J2', 'A4', (+0.5,  -5.0), VIA_Size[1] )
        via_usb_vbb = kad.add_via_relative( 'J2', 'B4', (-0.5,  -5.0), VIA_Size[1] )
        via_usb_cc1 = kad.add_via_relative( 'J2', 'A5', (-0.15, -2.4), VIA_Size[3] )
        via_usb_cc2 = kad.add_via_relative( 'J2', 'B5', (+0.15, -2.4), VIA_Size[3] )
        via_usb_dpa = kad.add_via_relative( 'J2', 'A6', (-0.5,  -4.0), VIA_Size[3] )
        via_usb_dpb = kad.add_via_relative( 'J2', 'B6', (+0.15, -4.0), VIA_Size[3] )
        via_usb_dma = kad.add_via_relative( 'J2', 'A7', (+0.15, -3.2), VIA_Size[3] )
        via_usb_dmb = kad.add_via_relative( 'J2', 'B7', (-0.15, -3.2), VIA_Size[3] )
        via_r8_cc1  = kad.add_via_relative( 'R8', '1',  (0,     -1.4), VIA_Size[3] )
        via_r9_cc2  = kad.add_via_relative( 'R9', '1',  (0,     +1.4), VIA_Size[3] )
        kad.wire_mods( [
            # vbus
            ('J2', via_usb_vba, 'J2', 'A4', 0.8, (Dird, +60, ([(1.6, 90), (0.5, 135)], 90))),
            ('J2', via_usb_vbb, 'J2', 'B4', 0.8, (Dird, -60, ([(1.6, 90), (0.5,  45)], 90))),
            ('J2', via_usb_vba, 'J2', via_usb_vbb, 0.8, (Strt), 'Opp'),
            ('J2', via_usb_vba, 'F1', '1', 0.6, (ZgZg, 90, 45)),
            # dm/dp
            ('J2', via_usb_dpa, 'J2', 'A6', 0.3, (Dird, 90, ([(2.4, 90)], -45), -0.2)),
            ('J2', via_usb_dpb, 'J2', 'B6', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dpa, 'J2', via_usb_dpb, 0.4, (Strt), 'Opp'),
            ('J2', via_usb_dma, 'J2', 'A7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dmb, 'J2', 'B7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dma, 'J2', via_usb_dmb, 0.4, (Dird, 90, 0), 'Opp'),
            ('J2', via_usb_dpb, 'R5', '1', 0.5, (Dird, 90, -30, -0.3)),
            ('J2', via_usb_dmb, 'R4', '1', 0.5, (Dird, 90, +30, -0.3)),
            # cc1/2
            ('J2', via_usb_cc1, 'J2', 'A5', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_cc2, 'J2', 'B5', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_cc1, 'J2', via_r8_cc1, 0.4, (Dird, -45, 0, -0.6), 'Opp'),
            ('J2', via_usb_cc2, 'J2', via_r9_cc2, 0.4, (Dird, +45, 0, -0.6), 'Opp'),
            ('J2', via_r8_cc1, 'R8', '1', 0.4, (Dird, 45, 90)),
            ('J2', via_r9_cc2, 'R9', '1', 0.4, (Dird, 45, 90)),
            ('R8', '2', 'J2', 'A1', 0.8, (Dird, 90, ([(1.1, 90)], -45))),
            ('R9', '2', 'J2', 'B1', 0.8, (Dird, 90, ([(1.1, 90)], +45))),
            ('R8', '2', 'J2', 'S1', 0.8, (Dird, 90, 90)),
            ('R9', '2', 'J2', 'S2', 0.8, (Dird, 90, 90)),
        ] )

    # J1/J2
    if board == BDL:
        via_mxrst1 = kad.add_via_relative( 'U1', '30', (0, -3), VIA_Size[3] )
        via_mxrst2 = kad.add_via_relative( 'U1', '30', (-12, 0), VIA_Size[3] )
        kad.wire_mods( [
            # I2C pull-ups
            ('J1', via_splt_vba, 'R2', '2', 0.8, (Dird, -45, 90)),
            ('J1', via_splt_vbb, 'R3', '2', 0.8, (Dird, +45, 90)),
            ('J1', via_splt_dmb, 'R2', '1', 0.4, (Dird, 90, ([(1.2, +90)], -45), -0.6)),
            ('J1', via_splt_dpb, 'R3', '1', 0.4, (Dird, 90, ([(1.2, -90)], +45), -0.6)),
            # VBUS
            ('F1', '2', 'L1', '2', 0.6, (Dird, 0, 90)),
            ('C1', '1', 'L1', '1', 0.6, (Dird, 90, 90)),
            # MX RST
            ('U1', '30', 'U1', via_mxrst1, 0.4, (Strt)),
            ('U1', via_mxrst1, 'U1', via_mxrst2, 0.4, (Dird, 0, 90), 'B.Cu'),
            ('J1', via_splt_sb2, 'U1', via_mxrst2, 0.4, (Dird, ([(0.4, 180)], 90), 90)),
        ] )
    elif board == BDR:
        via_scl = kad.add_via_relative( 'U1', '12', (2.8 - 0.2, -0.2), VIA_Size[3] )
        via_sda = kad.add_via_relative( 'U1', '13', (3.6 - 0.2, -0.2), VIA_Size[3] )
        kad.wire_mods( [
            # 5v
            ('J1', via_splt_vbb, 'C11', '1', 0.5, (Dird, ([(9, 90)], 0), 90, -0.8)),
            ('J1', via_splt_vbb, 'C11', '1', 0.5, (Dird, ([(11, 90), (-2, 90)], 0), 90, -0.8)),
            ('J1', via_splt_vba, 'SWB1', '2', 0.6, (Dird, 90, 90, -1)),
            # dm/dp = I2C
            ('U1', via_sda, 'U1', '13', 0.45, (Dird, 45, 0, -1)),
            ('U1', via_scl, 'U1', '12', 0.45, (Dird, 45, 0, -1)),
            ('J1', via_splt_dmb, 'U1', via_sda, 0.45, (Dird, ([(2, 90)], 45), ([(0.2, 0), (19.4, 90), (1.2, 135)], 90), -1)),
            ('J1', via_splt_dpb, 'U1', via_scl, 0.45, (Dird, ([(1, 90)], 45), ([(0.2, 0), (18.4, 90), (1.2, 135)], 90), -1)),
        ] )

    return

    # J3 Gnd
    if board in []:#[BDL, BDR]:
        via_gnd = kad.add_via_relative( 'J3', '1', (0, -4), VIA_Size[3] )
        kad.wire_mods( [
            # J3 GND
            ('J3', '1', 'J3', via_gnd, 0.5, (Strt), ['B.Cu', 'F.Cu'][board]),
        ] )
        pcb.Delete( via_gnd )
    # Debounce
    if board == BDL:
        via_vcc_col1 = kad.add_via_relative( 'C11', '1', (0, -2), VIA_Size[1] )
        kad.wire_mods( [
            # Vcc
            ('C11', '1', None, via_vcc_col1, 0.5, (Strt)),
            ('SWB1', '2', 'J1', via_vcc_col1, 0.5, (Dird, 0, 0, -1)),
        ] )
        via_bt01 = kad.add_via_relative( 'U1', '31', (-1.6, -1.4), VIA_Size[2] )
        via_bt02 = kad.add_via_relative( 'RB1', '2', (16, 0), VIA_Size[2] )
        kad.wire_mods( [
            # Vcc
            ('U1', via_bt01, 'RB1', via_bt02, 0.5, (Dird, ([(7, 180)], 90), 0, -1), 'B.Cu'),
            ('CB1', '1', 'U1', '5', 0.5, (Dird, ([(1.5, -90), (3.4, 0), (2.6, 90)], 0), 0, -1)),
            # boot0
            ('U1', '31', 'U1', via_bt01, 0.5, (Dird, 90, 0, -0.8)),
            ('RB1', '2', 'RB1', via_bt02, 0.5, (Dird, 0, 90, -1)),
        ] )
    elif board == BDR:
        pos_u1, net = kad.get_pad_pos_net( 'U1', '21' )
        pos_c11 = kad.get_pad_pos( 'C11', '2' )
        via_col1_u1 = kad.add_via( (pos_c11[0] + 1, pos_u1[1] - 3.2), net, VIA_Size[1] )
        via_col1_c11 = kad.add_via_relative( 'C11', '2', (0, 5), VIA_Size[2] )
        kad.wire_mods( [
            ('U1', '21', 'U1', via_col1_u1, 0.45, (Dird, ([(2.8, 180), (16.6, 90), (1.2, 135)], 90), 45, -1)),
            ('C11', '2', 'C11', via_col1_c11, 0.45, (Dird, 90, 0)),
            ('U1', via_col1_u1, 'C11', via_col1_c11, 0.45, (Dird, 0, 90, -1), 'Opp'),
        ] )

    ###
    ### Ref
    ###
    if board == BDL:
        refs = [
            (3,   135,   0, ['U1']),
            (2.8,   0,  90, ['U2']),
            (2.5,   0,  90, ['C1', 'C2', 'C4']),
            (1.8,  90,   0, ['C3', 'C5']),
            (3,     0, 180, ['C6', 'R1', 'D1']),
            (3.3,   0, 180, ['C11', 'R11', 'R12']),
            (3.3, 180,   0, ['CB1', 'RB1', 'RB2']),
            (1.8, -90,   0, ['R2']),
            (1.8, +90, 180, ['R3']),
            (3,   180, 180, ['R4', 'R5', 'R6', 'R7']),
            (3,   180,   0, ['R8', 'R9', 'L1', 'F1']),
            (4.0, 145,   0, ['LB1', 'L11', 'L12', 'L13', 'L14']),
            (4,     0,   0, ['CLB1', 'CL11', 'CL12', 'CL13', 'CL14']),
            (4.5,   0, 180, ['D0']),
            (4.5,   0,   0, ['D11', 'D12', 'D13', 'D14']),
            (7,     0, +90, ['J1']),
            (7,   180, -90, ['J2']),
            (15,  -90, -90, ['J3']),
        ]
    elif board == BDR:
        refs = [
            (4,  -110,  90, ['U1']),
            (1.8, -90,   0, ['C1']),
            (3.3, 180,   0, ['R1']),
            (3.3,   0, 180, ['D1']),
            (3.3, 180, 180, ['C11', 'R11', 'R12']),
            (3.3,   0,   0, ['CB1', 'RB1', 'RB2']),
            (3,   180, 180, ['R6', 'R7']),
            (4.0,-145, 180, ['LB1', 'L11', 'L12', 'L13', 'L14']),
            (4,     0, 180, ['CLB1', 'CL11', 'CL12', 'CL13', 'CL14']),
            (4.5,   0, 180, ['D11', 'D12', 'D13', 'D14']),
            (7,     0, -90, ['J1']),
            (13,  -90, -90, ['J3']),
        ]
    else:
        refs = [ (0, 0, None, ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']) ]
    for offset_length, offset_angle, text_angle, mod_names in refs:
        for mod_name in mod_names:
            mod = kad.get_mod( mod_name )
            if mod == None:
                continue
            pos, angle = kad.get_mod_pos_angle( mod_name )
            ref = mod.Reference()
            if text_angle == None:
                ref.SetVisible( False )
            else:
                ref.SetTextSize( pcbnew.wxSizeMM( 1, 1 ) )
                ref.SetThickness( pcbnew.FromMM( 0.15 ) )
                pos_ref = vec2.scale( offset_length, vec2.rotate( - (offset_angle + angle) ), pos )
                ref.SetPosition( pnt.to_unit( vec2.round( pos_ref, 3 ), True ) )
                ref.SetTextAngle( text_angle * 10 )
                ref.SetKeepUpright( False )
    # J3
    if board == BDL:
        pads = ['GND', 'nRST', 'CLK', 'DIO', 'TX', 'RX']
    elif board == BDR:
        pads = ['GND', 'LDI', 'SCL', 'SDA', '5V']
    else:
        pads = []
    for idx, text in enumerate( pads ):
        pos = kad.get_pad_pos( 'J3', '{}'.format( idx + 1 ) )
        pos = vec2.scale( 2, vec2.rotate( -90 ), pos )
        kad.add_text( pos, 0, text, ['F.SilkS', 'B.SilkS'][board], (0.9, 0.9), 0.15,
            pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )

if __name__=='__main__':
    kad.removeDrawings()
    kad.removeTracksAndVias()
    main()
    pcbnew.Refresh()
