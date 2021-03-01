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
PCB_Width  = 160
PCB_Height = 160

J1_y = 90
J2_y = 40
J3_x = PCB_Width/2
D1_x = PCB_Width/3 + 7.5

keys = {
    '11' : [36.456, -73.640, 17.400, 16.800, 16.0], # N
    '12' : [30.618, -57.836, 17.400, 16.800, 16.0], # H
    '13' : [29.549, -40.666, 17.400, 16.800, 16.0], # Y
    '14' : [29.369, -23.240, 17.400, 16.800, 16.0], # ^
    '21' : [53.182, -68.843, 17.400, 16.800, 16.0], # M
    '22' : [47.344, -53.040, 17.400, 16.800, 16.0], # J
    '23' : [46.275, -35.870, 17.400, 16.800, 16.0], # U
    '24' : [46.095, -18.444, 17.400, 16.800, 16.0], # '
    '31' : [72.560, -66.120, 17.400, 16.800, 0.0], # <
    '32' : [69.020, -49.320, 17.400, 16.800, 0.0], # K
    '33' : [65.480, -32.520, 17.400, 16.800, 0.0], # I
    '34' : [65.480, -15.720, 17.400, 16.800, 0.0], # (
    '41' : [89.960, -66.120, 17.400, 16.800, 0.0], # >
    '42' : [87.600, -49.320, 17.400, 16.800, 0.0], # L
    '43' : [85.240, -32.520, 17.400, 16.800, 0.0], # O
    '44' : [82.880, -15.720, 17.400, 16.800, 0.0], # )
    '51' : [111.262, -72.941, 23.490, 16.800, 6.4], # ?
    '52' : [106.978, -55.166, 17.400, 16.800, 16.0], # +
    '53' : [104.618, -38.366, 17.400, 16.800, 16.0], # P
    '54' : [102.258, -21.566, 17.400, 16.800, 16.0], #  
    '61' : [136.943, -70.082, 28.188, 16.800, 6.4], # _
    '62' : [124.520, -53.213, 17.400, 16.800, 16.0], # *
    '63' : [122.160, -36.413, 17.400, 16.800, 16.0], # @
    '64' : [119.800, -19.613, 17.400, 16.800, 16.0], # =
    '72' : [142.061, -51.261, 17.400, 16.800, 16.0], # ]
    '73' : [139.701, -34.460, 17.400, 16.800, 16.0], # [
    '81' : [49.445, -110.100, 20.243, 16.800, -64.0], # S
    '82' : [34.468, -123.099, 20.243, 16.800, -44.0], # S
    '83' : [21.661, -139.022, 17.400, 16.800, -24.0], # R
    '91' : [16.693, -72.001, 17.400, 16.800, 24.5], # E
}

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
    kad.removeDrawings()
    kad.removeTracksAndVias()

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
        angle = -angle
        if board == BDR:
            angle += 180# back side
        sw_pos = (px, -py)
        sw_pos_angles.append( (sw_pos, angle) )

        # SW & LED & Diode
        if board in [BDL, BDR]:
            sign = [+1, -1][board]
            ## SW
            kad.set_mod_pos_angle( 'SW' + name, sw_pos, - angle )
            ## LED
            pos = vec2.scale( 4.93, vec2.rotate( - 90 * sign + angle ), sw_pos )
            kad.set_mod_pos_angle( 'L' + name, pos, 180 - angle )
            if True:# LED holes
                corners = []
                for i in range( 4 ):
                    deg = i * 90 + angle
                    pt = vec2.scale( [3.6, 3.2][i % 2] / 2.0, vec2.rotate( deg ), pos )
                    corners.append( [(pt, deg + 90), BezierRound, [0.2]] )
                kad.draw_closed_corners( corners, 'Edge.Cuts', 0.1 )
            # wire LED GND to SW's fixed pin
            kad.wire_mods([('L' + name, '3', 'SW' + name, '3', 0.6, (Dird, 0, 90, -1), ['F.Cu', 'B.Cu'][board])])
            # LED pass caps
            pos = vec2.mult( mat2.rotate( -angle ), (0, -7.5 * sign), sw_pos )
            kad.set_mod_pos_angle( 'CL' + name, pos, 180 - angle )
            kad.wire_mods( [
                ('CL' + name, '1', 'L'  + name, '1', 0.6, (Dird, 0, 90, -0.6)),
                ('CL' + name, '2', 'SW' + name, '3', 0.6, (Dird, ([(0.5, -45)], 0), 90, -1)),
            ] )
            ## Diode
            Dx = 8.6 * sign
            Dy = 0.6 * sign
            if name != '91':#(board == BDL and idx < 2) or (board == BDR and idx < 3):
                pos = vec2.mult( mat2.rotate( -angle ), (+Dx, Dy), sw_pos )
                kad.set_mod_pos_angle( 'D' + name, pos, - 90 * sign - angle )
                # wire to SW
                kad.wire_mods( [('D' + name, '2', 'SW' + name, '2', 0.5, (Dird, 0, 0, -1))])
            elif False:#idx < 4:
                pos = vec2.mult( mat2.rotate( -angle ), (-Dx, Dy), sw_pos )
                kad.set_mod_pos_angle( 'D' + name, pos, - 90 * sign - angle )
                # wire to SW
                kad.wire_mods( [('D' + name, '1', 'SW' + name, '2', 0.5, (Dird, 0, 0, -1))])

    # if board in [BDT, BDB]:
    #     draw_top_bottom( board, sw_pos_angles )

    ###
    ### Set mod positios
    ###
    if board == BDL:
        kad.move_mods( (-10, 60), 0, [
            # mcu
            (None, (PCB_Width/2, 28), 0, [
                ('U1', (0, 0), 0),
                # pass caps
                (None, (-5.8, -4.2), 0, [
                    ('C3', (0, -0.2), 0),
                    ('C5', (-2.9, 0), 90),
                ] ),
                # C4 & regulators
                (None, (6.8, 3.3), -90, [
                    ('C4', (0, 0), 0),
                    (None, (0, -4.7), 0, [
                        ('C1', (0, -2.7), 0),
                        ('U2', (-0.25, 0), 0),
                        ('C2', (0, +2.7), 0),
                    ] ),
                ] ),
                # NRST
                ('C6', (-7.5, 4.2), 180),
                # R1
                ('R1', (-7.5, 2.2), 180),
                # USB DM/DP
                ('R4', (8.5, +0.2), 180),
                ('R5', (8.5, -1.8), 180),
            ] ),
            # I2C pull-ups
            (None, (2.62, PCB_Height/2), 0, [
                ('R2', (12, -1.9), +90),
                ('R3', (12, +1.9), -90),
            ] ),
            # USB (PC) connector
            (None, (PCB_Width - 2.62, J2_y), 0, [
                ('J2', (0, 0), 90),
                ('R8', (-7.5, +5.2), 0),
                ('R9', (-7.5, -5.2), 0),
                ('F1', (-12, -3), 90),
                ('L1', (-14, -3), 90),
            ] ),
            # Pin headers
            ('J3', (J3_x, 40), 90),
            # D0
            ('D0', (73, 25.4), 180),
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
    if board in [BDL, BDR]:
        # Split (USB) connector
        sign = [+1, -1][board]
        kad.move_mods( (0, J1_y), 0, [
            (None, (2.62, 0), 0, [
                ('J1', (0, 0), -90 * sign),
                ('R6', (7.5, -5.2 * sign), 180),
                ('R7', (7.5, +5.2 * sign), 180),
            ] ),
        ] )
        # D1
        kad.move_mods( (0, 0), 0, [
            ('D1', (D1_x, PCB_Height*2/3 - 1.2), 180),
        ] )
    if board in []:#[BDL, BDR]:
        # Debounce
        pos, angle = kad.get_mod_pos_angle( 'SW14' )
        kad.move_mods( pos, angle + [0, 180][board], [
            (None, (+9.6, 3.9), 0, [
                ('C11', (0, -2), 0),
                ('R11', (0,  0), 0),
                ('R12', (0, +2), 0),
            ] ),
        ] )
        pos, angle = kad.get_mod_pos_angle( 'SWB1' )
        kad.move_mods( pos, angle + [0, 180][board], [
            (None, (-9.6, 5.9), 0, [
                ('CB1', (0, -2), 180),
                ('RB1', (0,  0), 180),
                ('RB2', (0, +2), 180),
            ] ),
        ] )

    ###
    ### Wire mods
    ###
    # ROW lines
    if board == BDL:
        for row in ['4', '3', '2', '1']:
            kad.wire_mods( [
                ('SW1'+row, '1', 'SW2'+row, '1', 0.5, (Strt)),
                ('SW2'+row, '1', 'SW3'+row, '1', 0.5, (Dird, 0, 0, -5)),
                ('SW3'+row, '1', 'SW4'+row, '1', 0.5, (Strt)),
                ('SW4'+row, '1', 'SW5'+row, '1', 0.5, (ZgZg, 0, 60, -5)),
                ('SW5'+row, '1', 'SW6'+row, '1', 0.5, (ZgZg, 0, 45, -5)),
            ] )
            if '7'+row in keys.keys():
                kad.wire_mods( [
                    ('SW6'+row, '1', 'SW7'+row, '1', 0.5, (Dird, 0, 45, -5)),
                ] )
       
    return



    # COL lines
    if board in [BDL, BDR]:
        kad.wire_mods( [
            ('SW14', '1', 'SW13', '1', 0.5, (Dird, 0,  0, -5)),
            ('SW13', '1', 'SW12', '1', 0.5, (Dird, 0, 90, -1)),
            ('SW12', '1', 'SW11', '1', 0.5, (Dird, 0, 90, -9)),
        ] )
    # ROW lines
    if board == BDL:
        kad.wire_mods( [
            ('D11', '2', 'U1', '26', 0.5, (Dird, ([(2, -90)], 45), ([(1.4, 90)], 0), -0.8)),
            ('D12', '2', 'U1', '27', 0.5, (Dird,  0, ([(2.2, 90)], 0), -1.4)),
            ('D13', '2', 'U1', '28', 0.5, (Dird,  0, ([(3.0, 90)], 0), -1.4)),
            ('D14', '2', 'U1', '29', 0.5, (Dird,  0, ([(3.1, 90)], 0), -1.4)),
            ('C11', '2', 'U1', '30', 0.5, (Dird, 90, ([(2.3, 90), (12.0, 180), (3, -135)], 0), -0.8)),
        ] )
    elif board == BDR:
        kad.wire_mods( [
            ('D11', '2', 'U1', '5', 0.45, (Dird, ([(6, 0), (14, 90)], -45), ([(2.2, 180)], -90), -1)),
            ('D12', '2', 'U1', '4', 0.45, (Dird, 0, ([(3.0, 180)], 90), -1.6)),
            ('D13', '2', 'U1', '3', 0.45, (Dird, 0, ([(3.0, 180)], 90), -1.6)),
            ('D14', '2', 'U1', '2', 0.45, (Dird, 0, ([(2.2, 180)], 90), -1.0)),
            ('RB1', '2', 'U1', '22',0.45, (Dird, 0, ([(2.0, 180)], 90), -0.8)),
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
    if board == BDL:
        # USB (PC) connector
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
            # dm/dp
            ('J2', via_usb_dpa, 'J2', 'A6', 0.3, (Dird, 90, ([(2.4, 90)], -45), -0.2)),
            ('J2', via_usb_dpb, 'J2', 'B6', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dpa, 'J2', via_usb_dpb, 0.4, (Strt), 'Opp'),
            ('J2', via_usb_dma, 'J2', 'A7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dmb, 'J2', 'B7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dma, 'J2', via_usb_dmb, 0.4, (Dird, 90, 0), 'Opp'),
            ('J2', via_usb_dpb, 'R5', '1', 0.5, (Dird, ([(7.0, 90)], 45), ([(-1, 0), (-0.8, -45)], 0), -0.3)),
            ('J2', via_usb_dmb, 'R4', '1', 0.5, (Dird, ([(8.2, 90)], 45), ([(-1, 0), (-0.8, +45)], 0), -0.3)),
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
        kad.wire_mods( [
            # I2C pull-ups
            ('J1', via_splt_vba, 'R2', '2', 0.8, (Dird, -45, 90)),
            ('J1', via_splt_vbb, 'R3', '2', 0.8, (Dird, +45, 90)),
            ('J1', via_splt_dmb, 'R2', '1', 0.4, (Dird, 90, ([(1.2, +90)], -45), -0.6)),
            ('J1', via_splt_dpb, 'R3', '1', 0.4, (Dird, 90, ([(1.2, -90)], +45), -0.6)),
            # VBUS
            ('F1', '1', 'J2', via_usb_vbb, 0.6, (Dird, 0, 90)),
            ('F1', '2', 'L1', '2', 0.6, (Dird, 0, 90)),
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
    # J3 Gnd
    if board in [BDL, BDR]:
        via_gnd = kad.add_via_relative( 'J3', '1', (0, -4), VIA_Size[3] )
        kad.wire_mods( [
            # J3 GND
            ('J3', '1', 'J3', via_gnd, 0.5, (Strt), ['B.Cu', 'F.Cu'][board]),
        ] )
        pcb.Delete( via_gnd )
    if board == BDL:
        # mcu
        via_vcca1 = kad.add_via_relative( 'U1', '1',  (-3.0, -0.15), VIA_Size[2] )
        via_vcca5 = kad.add_via_relative( 'U1', '5',  (-3.0, +0.0), VIA_Size[2] )
        via_nrst  = kad.add_via_relative( 'U1', '4',  (-1.6,  0  ), VIA_Size[3] )
        via_swdio = kad.add_via_relative( 'U1', '23', (-4.0,  0.8), VIA_Size[3] )
        via_swclk = kad.add_via_relative( 'U1', '24', (-4.8,  0.8), VIA_Size[3] )
        VCC = pcb.FindNet( 'VCC' )
        via_u1_ctr = kad.add_via( kad.get_mod_pos_angle( 'U1' )[0], VCC, VIA_Size[1] )
        kad.wire_mods( [
            # pass caps
            ('C4', '1', 'U1', '17', 0.5, (ZgZg, 90, 45)),
            ('C4', '2', 'U1', '16', 0.5, (Dird, 90, 90, -1)),
            ('C3', '1', 'U1',  '1', 0.5, (Dird, -45, 0, -0.6)),
            ('C3', '2', 'U1', '32', 0.5, (Dird, 0, 90, -1)),
            ('C3', '2', 'C5', '2',  0.5, (Dird, ([(1.25, 90)], 0), -45, -1)),
            # regulator
            ('U2', '1', 'C1', '1', 0.6, (ZgZg, 90, 30)),# 5V
            ('U2', '3', 'C1', '2', 0.6, (ZgZg, 90, 30, -1)),# Gnd
            ('U2', '3', 'C2', '2', 0.6, (ZgZg, 90, 30, -1)),# Gnd
            ('U2', '2', 'C2', '1', 0.6, (ZgZg, 90, 30)),# Vcc
            #
            ('C4', '1', 'C2', '1', 0.6, (Dird, 0, 90)),# Vcc
            ('C4', '2', 'C2', '2', 0.6, (Dird, 0, 90)),# Gnd
            # VCC
            ('U1',  '1', None, via_u1_ctr, 0.5, (Dird, 0, -45, -0.4)),
            ('U1', '17', None, via_u1_ctr, 0.5, (Dird, 0, -45, -0.4)),
            ('U1',  '5', None, via_u1_ctr, 0.5, (Dird, 0, -45)),
            # VCCA
            ('U1', '5', None, via_vcca5, 0.5, (Strt)),
            ('C5', '1', None, via_vcca1, 0.5, (Dird, 45, 90)),
            ('U1', via_vcca1, None, via_vcca5, 0.6, (Strt), 'B.Cu'),
            # USB
            ('U1', '21', 'R4', '2', 0.5, (Dird, 0, ([(1, 0)], -45), -0.3)),
            ('U1', '22', 'R5', '2', 0.5, (Dird, 0, ([(1, 0)], +45), -0.3)),
            # I2C pull-up's
            ('U1', '2', 'R2', '1', 0.5, (Dird, 180, ([(-2, 90), (1.4, -45), (-12.5, 90)], -45), -0.8)),
            ('U1', '3', 'R3', '1', 0.5, (Dird, 180, ([(+2, 90), (2.4, 135), (+12, 90)], -45), -0.8)),
            # NRST
            ('U1', '4', None, via_nrst, 0.4, (Strt)),
            ('J3', '2', None, via_nrst, 0.4, (Dird, ([(1.4, 0)], 90), 0, -1), 'B.Cu'),
            ('J3', '2', 'C6', '1', 0.4, (Dird, ([(1.4, 0)], 90), 90, -1)),
            # SWCLK/DIO
            ('U1', '23', None, via_swdio, 0.4, (Dird, 0, 45, -0.4)),
            ('U1', '24', None, via_swclk, 0.4, (Dird, 0, 45, -0.4)),
            ('J3', '3', 'U1', via_swclk, 0.4, (Dird, ([(2.2, 0)], 90), ([(2.0, -135)], 90), -1), 'B.Cu'),
            ('J3', '4', 'U1', via_swdio, 0.4, (Dird, ([(3.0, 0)], 90), ([(1.6, -135)], 90), -1), 'B.Cu'),
            # TX/RX
            ('J3', '5', 'U1', '8', 0.4, (Dird, ([(2.2, 0)], 90), 90, -1)),
            ('J3', '6', 'U1', '9', 0.4, (Dird, ([(3.0, 0)], 90), 90, -1)),
            # D1
            ('U1', '7', 'R1', '1', 0.5, (Dird, 0, 90, -1)),
            ('R1', '2', 'D1', '2', 0.5, (Dird, 0, 90, -1)),
            ('J3', '1', 'D1', '1', 0.5, (Dird, 0, 0, -1)),
        ] )
        pcb.Delete( via_u1_ctr )
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
    # Debounce (common, internal)
    if board in [BDL, BDR]:
        kad.wire_mods( [
            # COL1
            ('R11', '1', 'R12', '1', 0.5, (Strt)),
            ('R11', '2', 'C11', '2', 0.5, (Strt)),
            # BOOT0
            ('RB1', '1', 'RB2', '1', 0.5, (Strt)),
            ('RB1', '2', 'CB1', '2', 0.5, (Strt)),
            # SW14
            ('R12', '1', 'SW14', '1', 0.5, (Dird, 0, 90)),
            # SWB1
            ('RB1', '1', 'SWB1', '1', 0.5, (Dird, 0, 90)),
            ('CB1', '1', 'SWB1', '2', 0.6, (Dird, 90, 0, -1)),
        ] )
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
    # LED
    via_led_dos = {}
    via_led_dis = {}
    via_led_5vs = {}
    if board == BDL:
        # LED vias
        for idx in range( 5 ):
            mod_led = 'L' + get_key_postfix( idx )
            via_led_dos[mod_led] = kad.add_via_relative( mod_led, '2', (-1.6, 0), VIA_Size[2] )
            via_led_dis[mod_led] = kad.add_via_relative( mod_led, '4', (+0.6, -1.2), VIA_Size[2] )
            kad.wire_mods( [(mod_led, '2', mod_led, via_led_dos[mod_led], 0.5, (Strt), 'F.Cu')] )
            kad.wire_mods( [(mod_led, '4', mod_led, via_led_dis[mod_led], 0.5, (Dird, 90, 0, -0.8), 'F.Cu')] )
            if mod_led != 'L11':
                via_led_5vs[mod_led] = kad.add_via_relative( mod_led, '1', (-1.6, 0), VIA_Size[1] )
                kad.wire_mods( [(mod_led, '1', mod_led, via_led_5vs[mod_led], 0.6, (Strt), 'F.Cu')] )

        via_ldi = kad.add_via_relative( 'U1', '12', (1.6, -1.4), VIA_Size[3] )
        via_lb1_5v = kad.add_via_relative( 'R2', '2', (0, 11.6), VIA_Size[1] )
        via_lb1_di = kad.add_via_relative( 'R2', '2', (0, 10.3), VIA_Size[2] )
        kad.wire_mods( [
            # 5V
            ('LB1', via_led_5vs['LB1'], 'J1', via_lb1_5v, 0.6, (Dird, ([(2.4, 90), (11.2, 0)], -45), 0, -1)),
            ('J1', via_lb1_5v, 'L14', via_led_5vs['L14'], 0.6, (Dird, 0, 90, -1), 'B.Cu'),
            ('L14', via_led_5vs['L14'], 'L13', via_led_5vs['L13'], 0.6, (Dird, ([(2.4, 90), (11.2, 0)], -45), 0, -1)),
            ('L13', via_led_5vs['L13'], 'L12', via_led_5vs['L12'], 0.6, (Dird, ([(2.4, 90), (11.2, 0)], -45), 0, -1)),
            # DI <-- DO
            ('J1', via_splt_sb1, 'LB1', via_led_dos['LB1'],  0.5, (Dird, 0, ([(5, -135), (5, -90)], -45), -1), 'B.Cu'),
            ('LB1', via_led_dis['LB1'], 'J1', via_lb1_di, 0.5, (Dird, ([(0.3, 90), (3.3, 0)], -45), 0, -1)),
            ('J1', via_lb1_di, 'L14', via_led_dos['L14'], 0.5, (Dird, 0, ([(1.4, 180)], 90), -1), 'B.Cu'),
            ('L14', via_led_dis['L14'], 'L13', via_led_dos['L13'], 0.5, (Dird, ([(0.3, 90), (3.3, 0)], -45), 0, -1)),
            ('L13', via_led_dis['L13'], 'L12', via_led_dos['L12'], 0.5, (Dird, ([(0.3, 90), (3.3, 0)], -45), 0, -1)),
            ('L12', via_led_dis['L12'], 'L11', via_led_dos['L11'], 0.5, (Dird, ([(0.3, 90)], 0), 45, -1)),
            ('L11', via_led_dis['L11'], 'U1', via_ldi, 0.4, (Dird, 90, ([(10, 0), (3, -45), (13, 0), (3, +45)], 0), -0.6)),
            ('U1', '12', 'U1', via_ldi, 0.4, (Dird, 90, 0, -0.6)),
            #
            ('R2', '2', 'J1', via_lb1_5v, 0.6, (Dird, 90, 0)),
        ] )
        pcb.Delete( via_lb1_di )

        # D0
        pos_c1_1 = kad.get_pad_pos( 'C1', '1' )
        pos_d0_2 = kad.get_pad_pos( 'D0', '2' )
        via_vcc_l12 = kad.add_via_relative( 'C1', '1', (pos_d0_2[1] - pos_c1_1[1], 0), VIA_Size[0] )
        via_vcc_c1  = kad.add_via_relative( 'C1', '1', (-1.5, 0), VIA_Size[0] )
        kad.wire_mods( [
            ('C1',  '1', None, via_vcc_c1,  0.6, (Dird, 90, 0, -1)),
            ('L12', via_led_5vs['L12'], None, via_vcc_l12, 0.6, (ZgZg, 90, 45, -1)),
            ('L12', via_vcc_l12, 'L12', via_vcc_c1, 0.6, (ZgZg, 90, 60), 'B.Cu'),
            ('D0', '1', 'L11', '1', 0.6, (Dird, ([(3, 180)], -30), 0, -1)),
            ('D0', '2', 'L12', via_vcc_l12, 0.6, (Dird, 0, 90)),
            ('D0', '2', 'L1', '1', 0.6, (Dird, 90, ([(1.4, 90)], 45), -0.4)),
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
            via_led_5vs[mod_led] = kad.add_via_relative( mod_led, '1', (-1.6, 0), VIA_Size[1] )
            kad.wire_mods( [(mod_led, '1', mod_led, via_led_5vs[mod_led], 0.6, (Strt), 'B.Cu')] )
        via_l14_5v = kad.add_via_relative( 'J1', 'B4', (0, -18), VIA_Size[0] )
        via_l14_di = kad.add_via_relative( 'J1', 'B4', (0, -17), VIA_Size[0] )
        kad.wire_mods( [
            # 5V
            ('SWB1', '2', mod_led, via_led_5vs[mod_led], 0.6, (Dird, ([(0.5, 0)], 90), 0, -1), 'B.Cu'),
            ('LB1', via_led_5vs['LB1'], 'J1', via_l14_5v, 0.6, (Dird, 0, 0, -1)),
            ('J1', via_l14_5v, 'L14', via_led_5vs['L14'], 0.6, (Dird, 0, ([(2.4, 90)], 0), -1), 'F.Cu'),
            ('L14', via_led_5vs['L14'], 'L13', via_led_5vs['L13'], 0.6, (Dird, 0, ([(2.4, 90), (11.3, 0)], -45), -1)),
            ('L13', via_led_5vs['L13'], 'L12', via_led_5vs['L12'], 0.6, (Dird, 0, ([(2.4, 90), (11.3, 0)], -45), -1)),
            ('L12', via_led_5vs['L12'], 'L11', via_led_5vs['L11'], 0.6, (Dird, 90, ([(2.4, 90), (11.3, 0)], -45), -1)),
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
    main()
    pcbnew.Refresh()
