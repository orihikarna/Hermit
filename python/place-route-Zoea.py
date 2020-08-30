import pcbnew
import math
import sys
import os

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
PCB_Width  = 99.6
PCB_Height = 57.72# platinum ratio

J1_y = PCB_Height / 2
J2_y = 40
J3_x = PCB_Width/2 - 1.27 * 4
D1_x = PCB_Width/3 + 7.5

keys = [
    ['/', 0.000, 0.520, 3.5],
    ['.', -1.000, 0.000, 0.0],
    [',', -2.000, 0.000, 0.0],
    ['M', -3.074, 0.073, -9.1],
]
keys.append( [' ', 0.8, 0.75, -20] )

KeyUnit = 19.05

# Board Type
BZL = 0# Left plate
BZR = 1# Right plate
BZT = 2# Top plate
BZB = 3# Bottom plate
BZM = 4# Middle plate

def get_key_postfix( idx ):
    if idx == 4:
        return 'B1'
    else:
        return '1{}'.format( idx + 1 )

def drawEdgeCuts( board ):
    layer = 'Edge.Cuts'
    width = 0.1
    W = PCB_Width
    H = PCB_Height
    R = 2# corner radius
    USBC_Width  = 4.675
    USBC_Height = 5.73

    corners = []
    midcnrs = []
    midcnrs_set = []
    ## top
    corners.append( [((W/2, 0), 0), Round, [R]] )
    midcnrs.append( corners[-1] )
    ## right
    corners.append( [((W, R+1), 90), Round, [R]] )
    midcnrs.append( corners[-1] )
    USBM = 5
    USBT = 1.1
    USBW = 6
    ## USB (PC)
    if board == BZL:
        corners.append( [((W - 3,           J2_y - USBC_Width), 180), Round, [0.5]] )
        corners.append( [((W - USBC_Height, J2_y             ),  90), Round, [0.5]] )
        corners.append( [((W - 3,           J2_y + USBC_Width),   0), Round, [0.5]] )
        corners.append( [((W,               H - R - 1        ),  90), Round, [0.5]] )
    if board in [BZL, BZR, BZM]:
        midcnrs.append( [((W-USBW+2, J2_y - USBM - USBT*2), 180), Round, [1]] )
        midcnrs.append( [((W-USBW,   J2_y - USBM - USBT  ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW+2, J2_y - USBM         ),   0), Round, [1]] )
        midcnrs.append( [((W,        J2_y                ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW+2, J2_y + USBM         ), 180), Round, [1]] )
        midcnrs.append( [((W-USBW,   J2_y + USBM + USBT  ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW+2, J2_y + USBM + USBT*2),   0), Round, [1]] )
        midcnrs.append( [((W,        H-5),                   90), Round, [1]] )
    ## bottom
    corners.append( [((W*5/6, H), 180), Round, [R]] )
    midcnrs.append( corners[-1] )
    if True:
        mgn = 0.1# margin
        corners.append( [((W*2/3 + mgn,   H - R - 1  ), -90), Round, [R]] )
        midcnrs.append( corners[-1] )
        corners.append( [((W*2/3 - R - 1, H*2/3 - mgn), 180), Round, [R]] )
        midcnrs.append( corners[-1] )
        if board in [BZL, BZR, BZM]:
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
    if board in [BZL, BZR]:
        corners.append( [((3,           J1_y + USBC_Width),   0), Round, [0.5]] )
        corners.append( [((USBC_Height, J1_y             ), -90), Round, [0.5]] )
        corners.append( [((3,           J1_y - USBC_Width), 180), Round, [0.5]] )
        corners.append( [((0,           R + 1            ), -90), Round, [0.5]] )
    if board in [BZL, BZR, BZM]:# mid plate
        Jw = 6.3
        midcnrs.append( [((2,           J1_y + Jw    ),   0), BezierRound, [1]] )# J1 bottom
        T = 7.4# thickness for left
        midcnrs.append( [((T,           J1_y + Jw + 2),  90), BezierRound, [1]] )# left
        D = 8.5# diagonal left
        midcnrs.append( [((D,           H - D        ),  45), BezierRound, [1]] )# left bottom corner
        T = 5.8# thickness for bottom
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
    if board in [BZL, BZR, BZM]:
        midcnrs = []
        midcnrs.append( [((W-USBW-4, J2_y - USBM - USBT*2),   0), Round, [1]] )
        midcnrs.append( [((W-USBW-2, J2_y - USBM - USBT  ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW-4, J2_y - USBM         ), 180), Round, [1]] )
        midcnrs.append( [((W-16,     J2_y                ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW-4, J2_y + USBM         ),   0), Round, [1]] )
        midcnrs.append( [((W-USBW-2, J2_y + USBM + USBT  ),  90), Round, [1]] )
        midcnrs.append( [((W-USBW-4, J2_y + USBM + USBT*2), 180), Round, [1]] )
        midcnrs.append( [((W-18,     J2_y                ), -90), Round, [1]] )
        midcnrs_set.append( midcnrs )

    # mid plate main hole
    if board in [BZL, BZR, BZM]:
        midcnrs = []
        T = 5# thickness top
        midcnrs.append( [((W/2,     T        ),   0), BezierRound, [1]] )# top
        D = 10# diagonal top right
        midcnrs.append( [((W - D,   D        ),  45), BezierRound, [1]] )# top right diagonal
        T = 5# thickness right
        midcnrs.append( [((W-T,     H/3      ),  90), BezierRound, [1]] )# right
        midcnrs.append( [((W*5/6,   29       ), 180), BezierRound, [1]] )# mid horizontal
        T = 5# thickness mid
        midcnrs.append( [((W*2/3-1, H*2/3-T-2),  90), BezierRound, [1]] )# mid right
        midcnrs.append( [((W/2,     H*2/3-T  ), 180), BezierRound, [1]] )# mid bottom
        midcnrs.append( [((W/3+6,   H*2/3-T-2), -90), BezierRound, [1]] )# mid left
        midcnrs.append( [((W/3,     22       ), 180), BezierRound, [1]] )# mid left horizontal
        midcnrs.append( [((20,      18.5     ),-135), BezierRound, [1]] )# left bottom
        midcnrs.append( [((15,      H/6      ), -90), BezierRound, [1]] )# top left
        midcnrs_set.append( midcnrs )
    # draw
    if board in [BZL, BZR, BZT, BZB]:
        kad.draw_closed_corners( corners, layer, width )
    for midcnrs in midcnrs_set:
        l = 'Edge.Cuts' if board == BZM else 'F.Fab'
        w = width if board == BZM else width * 3
        kad.draw_closed_corners( midcnrs, l, w )

    # screw holes
    r = 4.5
    for idx, ctr in enumerate( [(r, r), (W-r, r), (W-r, H-r), (r, H-r), (W/3-r, H-r), (W*2/3+r, H-r)] ):
        sign = +1 if idx % 2 == 0 else -1
        if board in [BZT, BZB, BZM]:# move hole mods
            kad.set_mod_pos_angle( 'H{}'.format( idx + 1 ), ctr, 0 )
        if board in [BZL, BZR]:
            corners = []
            for i in range( 6 ):
                deg = i * 60 + 15 * sign
                pos = vec2.scale( 2.74, vec2.rotate( deg ), ctr )
                corners.append( [(pos, deg + 90), BezierRound, [0.7]] )
            kad.draw_closed_corners( corners, layer, width )
        if False:# draw holes in Edge.Cuts
            for brd, rad in [(BZT, 1.6), (BZB, 1.7)]:
                if board == brd:
                    kad.add_arc( ctr, vec2.add( ctr, (rad, 0) ), 360, layer, width )
        kad.add_arc( ctr, vec2.add( ctr, (3.0, 0) ), 360, 'F.Fab', width )

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
    if board == BZT:# keysw holes
        for sw_pos, angle in sw_pos_angles:
            corners = []
            for i in range(4):
                deg = i * 90 + angle
                pos = vec2.scale( 13.90 / 2.0, vec2.rotate( deg ), sw_pos )
                corners.append( [(pos, deg + 90), BezierRound, [1]] )
            kad.draw_closed_corners( corners, 'Edge.Cuts', 0.1 )

    # read distance data
    board_type = 'T' if board == BZT else 'B'
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
                    w = widths[lidx if board == BZT else 1 - lidx]
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
    boardname = filename[filename.find( 'Zoea' ) + 4]
    # print( filename, boardname )
    for bname, btype in [('L', BZL), ('R', BZR), ('T', BZT), ('B', BZB), ('M', BZM)]:
        if boardname == bname:
            board = btype
            if board in [BZL, BZR, BZM]:
                kad.add_text( (PCB_Width/2, 1.5), 0, 'Zoea{} by orihikarna 20/08/31'.format( bname ), 'F.SilkS', (1, 1), 0.15,
                    pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER )
            break

    drawEdgeCuts( board )

    ### zones
    zones = []
    if board in [BZL, BZR, BZM]:
        add_zone( 'GND', 'F.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )
        add_zone( 'GND', 'B.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )

    ###
    ### Set key positios
    ###
    sw_pos_angles = []
    for idx, key in enumerate( keys ):
        _, x, y, angle = key
        name = get_key_postfix( idx )
        if idx == 4:# SWB1
            px = x * KeyUnit
            py = PCB_Height - y * KeyUnit
        else:
            px = (x - 0.5) * KeyUnit - 2.5 + PCB_Width
            py = (y + 0.5) * KeyUnit + 2.5
        if board == BZR:
            angle += 180# back side
        sw_pos = (px, py)
        sw_pos_angles.append( (sw_pos, angle) )

        # SW & LED & Diode
        if board in [BZL, BZR]:
            sign = [+1, -1][board]
            ## SW
            kad.set_mod_pos_angle( 'SW' + name, sw_pos, 180 - angle )
            ## LED
            pos = vec2.scale( 4.93, vec2.rotate( 90 * sign + angle ), sw_pos )
            kad.set_mod_pos_angle( 'L' + name, pos, -angle )
            # wire LED GND to SW's fixed pin
            kad.wire_mods([('L' + name, '6', 'SW' + name, '3', 0.6, (Dird, 0, 90))])
            ## Diode
            if idx < 4:
                pos = vec2.mult( mat2.rotate( -angle ), (-8, 1 * sign), sw_pos )
                kad.set_mod_pos_angle( 'D' + name, pos, - 90 * sign - angle )
                # wire to SW
                kad.wire_mods([('D' + name, '1', 'SW' + name, '2', 0.5, (Dird, 0, 0, -1))])

    if board in [BZT, BZB]:
        draw_top_bottom( board, sw_pos_angles )

    ###
    ### Set mod positios
    ###
    if board == BZL:
        kad.move_mods( (0, 0), 0, [
            # mcu
            (None, (PCB_Width/2, 28), 0, [
                ('U1', (0, 0), 0),
                # pass caps
                (None, (-4.8, -5.2), 0, [
                    ('C3', (0, 0), 90),
                    ('C5', (-2, 0), 90),
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
            ('J3', (J3_x, PCB_Height*2/3 - 1.27), 90),
            # D0
            ('D0', (73, 25.4), 180),
        ] )
    elif board == BZR:
        # expander
        kad.move_mods( (PCB_Width/2, 28.5), 0, [
            ('U1', (0, 0), -90),
            ('C1', (+1.3, -5.8), 0),
            # R1
            ('R1', (-7.5, 3.2), 0),
        ] )
    if board in [BZL, BZR]:
        # Debounce
        pos, angle = kad.get_mod_pos_angle( 'SW14' )
        kad.move_mods( pos, angle + [0, 180][board], [
            (None, (+11, 3.9), 0, [
                ('C11', (0, -2), 0),
                ('R11', (0,  0), 0),
                ('R12', (0, +2), 0),
            ] ),
        ] )
        pos, angle = kad.get_mod_pos_angle( 'SWB1' )
        kad.move_mods( pos, angle + [0, 180][board], [
            (None, (-11, 3.9), 0, [
                ('CB1', (0, -2), 180),
                ('RB1', (0,  0), 180),
                ('RB2', (0, +2), 180),
            ] ),
        ] )
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

    ###
    ### Wire mods
    ###
    # COL lines
    if board in [BZL, BZR]:
        kad.wire_mods( [
            ('SW14', '1', 'SW13', '1', 0.5, (Dird, 0,  0, -5)),
            ('SW13', '1', 'SW12', '1', 0.5, (Dird, 0, 90, -1)),
            ('SW12', '1', 'SW11', '1', 0.5, (Dird, 0, 90, -9)),
        ] )
    # ROW lines
    if board == BZL:
        kad.wire_mods( [
            ('D11', '2', 'U1', '26', 0.5, (Dird, ([(2, -90)], 45), ([(2.4, 90)], 0), -1.0)),
            ('D12', '2', 'U1', '27', 0.5, (Dird,  0, ([(3.2, 90)], 0), -1.6)),
            ('D13', '2', 'U1', '28', 0.5, (Dird,  0, ([(4.8, 90)], 0), -2.2)),
            ('D14', '2', 'U1', '29', 0.5, (Dird,  0, ([(4.0, 90)], 0), -1.6)),
            ('C11', '2', 'U1', '30', 0.5, (Dird, 90, ([(3.2, 90)], 0), -1.0)),
        ] )
    elif board == BZR:
        kad.wire_mods( [
            ('D11', '2', 'U1', '5', 0.45, (Dird, ([(5, 0), (14, 90)], -45), ([(3.6, 180)], -90), -1)),
            ('D12', '2', 'U1', '4', 0.45, (Dird, 0, ([(4.4, 180)], 90), -1.4)),
            ('D13', '2', 'U1', '3', 0.45, (Dird, 0, ([(5.2, 180)], 90), -2.0)),
            ('D14', '2', 'U1', '2', 0.45, (Dird, 0, ([(4.4, 180)], 90), -1.4)),
            ('RB1', '2', 'U1', '22',0.45, (Dird, 0, ([(2.0, 180)], 90), -0.8)),
        ] )
    # Split (USB) connector
    if board in [BZL, BZR]:
        via_splt_vba = kad.add_via_relative( 'J1', 'A4', (-0.4,  -5.8), VIA_Size[1] )
        via_splt_vbb = kad.add_via_relative( 'J1', 'B4', (-0.8,  -5.8), VIA_Size[1] )
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
            ('J1', via_splt_vba, 'J1', 'A4', 0.8, (Dird, 90, ([(1.6, 90)], -45))),
            ('J1', via_splt_vbb, 'J1', 'B4', 0.8, (Dird, -60, ([(1.6, 90), (0.5,  45)], 90))),
            ('J1', via_splt_vba, 'J1', via_splt_vbb, 0.8, (Strt), 'Opp'),
            # dm/dp = I2C
            ('J1', via_splt_dpa, 'J1', 'A6', 0.3, (Dird, 90, ([(3.52, 90)], -45), -0.1)),
            ('J1', via_splt_dpb, 'J1', 'B6', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dpa, 'J1', via_splt_dpb, 0.4, (Strt), 'Opp'),
            ('J1', via_splt_dma, 'J1', 'A7', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dmb, 'J1', 'B7', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_dma, 'J1', via_splt_dmb, 0.4, (ZgZg, 0, 45, -0.8), 'Opp'),
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
        ] )
    if board == BZL:
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
    if board == BZL:
        kad.wire_mods( [
            # I2C pull-ups
            ('J1', via_splt_vba, 'R2', '2', 0.8, (Dird, 90, 0)),
            ('J1', via_splt_vbb, 'R3', '2', 0.8, (Dird, 90, 0)),
            ('J1', via_splt_dmb, 'R2', '1', 0.4, (Dird, 90, ([(1.2, +90)], -45), -0.6)),
            ('J1', via_splt_dpb, 'R3', '1', 0.4, (Dird, 90, ([(1.2, -90)], +45), -0.6)),
            # VBUS
            ('F1', '1', 'J2', via_usb_vbb, 0.6, (Dird, 0, 90)),
            ('F1', '2', 'L1', '2', 0.6, (Dird, 0, 90)),
        ] )
    elif board == BZR:
        kad.wire_mods( [
            # 5v
            ('J1', via_splt_vbb, 'C11', '1', 0.5, (Dird, ([(7, 90)], 0), 90, -0.8)),
            ('J1', via_splt_vbb, 'C11', '1', 0.5, (Dird, ([(9, 90), (-2, 90)], 0), 90, -0.8)),
            # dm/dp = I2C
            ('J1', via_splt_dmb, 'U1', '13', 0.45, (Dird, ([(6, 90), (0.6, 45), (17, 90)], 45), ([(3.6, 0)], 90), -1)),
            ('J1', via_splt_dpb, 'U1', '12', 0.45, (Dird, ([(5, 90), (0.6, 45), (17, 90)], 45), ([(2.8, 0)], 90), -1)),
        ] )
    if board == BZL:
        # mcu
        via_vcca1 = kad.add_via_relative( 'U1', '1',  (-2.6, -0.1), VIA_Size[2] )
        via_vcca5 = kad.add_via_relative( 'U1', '5',  (-2.6, +0.0), VIA_Size[2] )
        via_nrst  = kad.add_via_relative( 'U1', '4',  (-1.6,  0  ), VIA_Size[3] )
        via_swdio = kad.add_via_relative( 'U1', '23', (-4.0,  0.8), VIA_Size[3] )
        via_swclk = kad.add_via_relative( 'U1', '24', (-4.8,  0.8), VIA_Size[3] )
        via_gnd = kad.add_via_relative( 'J3', '1', (0, -4), VIA_Size[3] )
        VCC = pcb.FindNet( 'VCC' )
        via_u1_ctr = kad.add_via( kad.get_mod_pos_angle( 'U1' )[0], VCC, VIA_Size[1] )
        kad.wire_mods( [
            # pass caps
            ('C4', '1', 'U1', '17', 0.5, (ZgZg, 90, 45)),
            ('C4', '2', 'U1', '16', 0.5, (Dird, 90, 90, -1)),
            ('C3', '1', 'U1',  '1', 0.5, (Dird, 0, 0)),
            ('C3', '2', 'U1', '32', 0.5, (Dird, 90, 90, -1)),
            ('C3', '2', 'C5', '2',  0.5, (Dird, 0, 90)),
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
            ('C5', '1', None, via_vcca1, 0.5, (Dird, 90, 0, -1)),
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
            ('J3', '3', 'U1', via_swclk, 0.4, (Dird, ([(2.2, 0)], 90), ([(3, -135)], 90), -1), 'B.Cu'),
            ('J3', '4', 'U1', via_swdio, 0.4, (Dird, ([(3.0, 0)], 90), ([(3, -135)], 90), -1), 'B.Cu'),
            # TX/RX
            ('J3', '5', 'U1', '8', 0.4, (Dird, ([(2.2, 0)], 90), 90, -1)),
            ('J3', '6', 'U1', '9', 0.4, (Dird, ([(3.0, 0)], 90), 90, -1)),
            # D1
            ('U1', '7', 'R1', '1', 0.5, (Dird, 0, 90, -1)),
            ('R1', '2', 'D1', '2', 0.5, (Dird, 0, 90, -1)),
            ('J3', '1', 'D1', '1', 0.5, (Dird, 0, 0, -1)),
            # J3 GND
            ('J3', '1', 'J3', via_gnd, 0.5, (Strt), 'B.Cu'),
        ] )
        pcb.Delete( via_u1_ctr )
        pcb.Delete( via_gnd )
    elif board == BZR:
        # mcp23017
        via_u1_vcc  = kad.add_via_relative( 'U1', '9',  (+1.8, 0), VIA_Size[2] )
        via_u1_nrst = kad.add_via_relative( 'U1', '18', (-1.8, 0), VIA_Size[2] )
        via_led_u1 = kad.add_via_relative( 'U1', '1', (0, -2), VIA_Size[2] )
        via_led_d1 = kad.add_via_relative( 'D1', '2', (0, -2), VIA_Size[2] )
        kad.wire_mods( [
            # Gnd
            ('U1', '15', 'U1', '17', 0.45, (Strt)),
            # pass caps
            ('U1',  '9', 'C1', '1', 0.45, (Dird, 0, +45, -0.6)),
            ('U1', '10', 'C1', '2', 0.45, (Dird, 0, -45, -0.6)),
            # NRST
            ('U1', via_u1_nrst, 'U1', '18', 0.4, (Dird, 90, 0)),
            ('U1', via_u1_vcc, 'U1', '9', 0.45, (Dird, -45, 0, -0.2)),
            ('U1', via_u1_vcc, 'U1', via_u1_nrst, 0.4, (ZgZg, 0, 45, -0.6), 'Opp'),
            # Vcc
            ('U1', via_u1_vcc, 'J1', via_splt_vbb, 0.5, (Dird, ([(0.2, 0)], 90), ([(21, 90)], 45), -1)),
            # D1
            ('R1', '1', 'D1', '1', 0.5, (ZgZg, 90, 45, -0.8)),
            ('U1', '1', 'U1', via_led_u1, 0.45, (Dird, 90, 0)),
            ('D1', '2', 'D1', via_led_d1, 0.45, (Dird, 90, 0)),
            ('U1', via_led_u1, 'D1', via_led_d1, 0.5, (Dird, 90, 90, -0.8), 'Opp'),
        ] )
    # Debounce (common, internal)
    if board in [BZL, BZR]:
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
            ('RB2', '1', 'SWB1', '1', 0.5, (Dird, 0, 90)),
            ('CB1', '1', 'SWB1', '2', 0.6, (Dird, ([(1.4, 180)], 90), 0, -1)),
        ] )
    # Debounce
    if board == BZL:
        via_vcc_col1 = kad.add_via_relative( 'C11', '1', (0, -2), VIA_Size[1] )
        kad.wire_mods( [
            # Vcc
            ('C11', '1', None, via_vcc_col1, 0.5, (Strt)),
            ('SWB1', '2', 'J1', via_vcc_col1, 0.5, (Dird, 0, 0, -1)),
        ] )
        via_bt01 = kad.add_via_relative( 'U1', '31', ( 0, -2), VIA_Size[3] )
        via_bt02 = kad.add_via_relative( 'RB1', '2', (15, -2.4), VIA_Size[2] )
        kad.wire_mods( [
            # Vcc
            ('U1', via_bt01, 'RB1', via_bt02, 0.5, (Dird, ([(8, 180)], 90), 0, -1), 'B.Cu'),
            ('CB1', '1', 'U1', '5', 0.5, (Dird, ([(1.5, -90), (4.4, 0), (4.8, 90)], 0), 0, -1)),
            # boot0
            ('U1', '31', 'U1', via_bt01, 0.5, (Dird, 90, 0, -1)),
            ('RB1', '2', 'RB1', via_bt02, 0.5, (Dird, ([(1.4, 0)], 90), 0, -1)),
        ] )
    elif board == BZR:
        pos_u1, net = kad.get_pad_pos_net( 'U1', '21' )
        pos_c11 = kad.get_pad_pos( 'C11', '2' )
        via_col1_u1 = kad.add_via( (pos_c11[0] + 1, pos_u1[1] - 2.0), net, VIA_Size[2] )
        via_col1_c11 = kad.add_via_relative( 'C11', '2', (0, 4), VIA_Size[2] )
        kad.wire_mods( [
            ('U1', '21', 'U1', via_col1_u1, 0.45, (Dird, ([(2.8, 180), (15, 90)], 45), 90, -1)),
            ('C11', '2', 'C11', via_col1_c11, 0.45, (Dird, 90, 0)),
            ('U1', via_col1_u1, 'C11', via_col1_c11, 0.45, (Dird, 0, 90, -1), 'Opp'),
        ] )
    # LED
    if board == BZL:
        via_lci = kad.add_via_relative( 'U1', '11', (1.8, -2.2), VIA_Size[3] )
        via_ldi = kad.add_via_relative( 'U1', '13', (1.0, -1.4), VIA_Size[3] )
        via_lb1_5v = kad.add_via_relative( 'R2', '2', (0, 11.9 + 0.2), VIA_Size[1] )
        via_lb1_ci = kad.add_via_relative( 'R2', '2', (0, 11.0), VIA_Size[2] )
        via_lb1_di = kad.add_via_relative( 'R2', '2', (0, 10.1), VIA_Size[2] )
        kad.wire_mods( [
            # LB1
            ('LB1', '3', 'J1', via_splt_sb1, 0.4, (Dird, ([(3.3, -180), (5.2, -135), (5.2, -90)], -30), 0, -1)),
            ('LB1', '2', 'J1', via_splt_sb2, 0.4, (Dird, ([(3.8, -180), (6.0, -135), (6.1, -90)], -30), ([(2.2, -45)], 0), -1)),
            # L <-2.4-> R
            # R <-3.8-> 3:GND
            # LDI
            #   3.8 - 3.2/2 - 1.0x0.707 = 1.493
            ('LB1', '4', 'J1', via_lb1_di, 0.4, (Dird, ([(1.5, 0), (1.0, -45)], 0), 0, -0.6)),
            ('J1', via_lb1_di, 'L14', '3', 0.4, (Dird, 0, 180, -2.2)),
            ('L14', '4', 'L13', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0)], +45), 0, -0.6)),
            ('L13', '4', 'L12', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0)], +45), 0, -0.6)),
            ('L12', '4', 'L11', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0)], +45), ([(2.4, -180)], -120), -0.6)),
            ('L11', '4','U1',via_ldi,0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0), (1.9, +45)], +90), ([(10, 0), (4, -45), (13, 0), (4, +45)], 0), -0.6)),
            ('U1', '13','U1',via_ldi,0.4, (Dird, 90, 0, -1)),
            # LCI
            #   3.8 - 2.4/2 - 1.2x0.707 = 1.752
            ('LB1', '5', 'J1', via_lb1_ci, 0.4, (Dird, ([(1.75, 0), (1.2, -45)], 0), 0, -0.6)),
            ('J1', via_lb1_ci, 'L14', '2', 0.4, (Dird, 0, 180, -1.6)),
            ('L14', '5', 'L13', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0)], +45), 0, -0.6)),
            ('L13', '5', 'L12', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0)], +45), 0, -0.6)),
            ('L12', '5', 'L11', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0)], +45), ([(2.8, -180)], -120), -0.6)),
            ('L11', '5','U1',via_lci,0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0), (1.2, +45)], +90), ([(11.2, 0), (4, -45), (12, 0), (4, 45)], 0), -0.6)),
            ('U1', '11','U1',via_lci,0.4, (Dird, 90, 0, -1)),
            # Vcc
            #   3.8 + 2.4 - 2.6/2 - 1.0x0.707 = 4.9 - 0.707 = 4.193
            ('LB1', '1', 'J1', via_lb1_5v, 0.6, (Dird, ([(1.2, +90), (7.8, 0), (3.0, -45)], 0), 0, -1)),
            ('J1', via_lb1_5v, 'L14', '1', 0.6, (Dird, 0, 180, -1)),
            ('L14', '1', 'L13', '1', 0.6, (Dird, ([(1.2, +90), (7.8, 0)], -45), 0, -1)),
            ('L13', '1', 'L12', '1', 0.6, (Dird, ([(1.2, +90), (7.8, 0)], -45), 0, -1)),
            ('R2', '2', None, via_lb1_5v, 0.6, (Dird, 90, 0)),
        ] )
        pcb.Delete( via_lb1_ci )
        pcb.Delete( via_lb1_di )
        # D0
        pos_l12_1 = kad.get_pad_pos( 'L12', '1' )
        pos_d0_2 = kad.get_pad_pos( 'D0', '2' )
        via_vcc_l11 = kad.add_via_relative( 'L11', '1', (-6, 0.5), VIA_Size[0] )
        via_vcc_l12 = kad.add_via_relative( 'L12', '1', (0, pos_l12_1[1] - pos_d0_2[1]), VIA_Size[0] )
        via_vcc_c1  = kad.add_via_relative( 'L12', '1', (0, -12.5), VIA_Size[0] )
        kad.wire_mods( [
            ('C1',  '1', None, via_vcc_c1,  0.6, (Dird, 90, 0, -1)),
            ('L11', '1', None, via_vcc_l11, 0.6, (Dird, 0, -30, -1)),
            ('L12', '1', None, via_vcc_l12, 0.6, (Dird, 0, 90)),
            ('L12', via_vcc_l12, 'L12', via_vcc_c1, 0.6, (ZgZg, 90, 60), 'B.Cu'),
            ('D0', '1', 'L11', via_vcc_l11, 0.6, (Dird, 0, 30, -1)),
            ('D0', '2', 'L12', via_vcc_l12, 0.6, (Dird, 0, 90)),
            ('D0', '2', 'L1', '1', 0.6, (Dird, 90, ([(1.4, 90)], 45), -0.4)),
        ] )
    elif board == BZR:
        via_vcc_l14 = kad.add_via_relative( 'L14', '1', (0, -4), VIA_Size[0] )
        via_vcc_lb1 = kad.add_via_relative( 'CB1', '1', (0, -2), VIA_Size[0] )
        kad.wire_mods( [
            # LB1
            ('LB1', '4', 'J1', via_splt_sb2, 0.4, (Dird, ([(1.5, 0), (2.0, -45)], -90), ([(0.2, 0), (1.7, -90)], 0), -1)),
            ('LB1', '5', 'J1', via_splt_sb1, 0.4, (Dird, ([(1.75, 0), (2.8, -45)], -90), ([(2.2, -135)], 0), -1)),
            # LDI
            ('L11', '4', 'L12', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0)], -45), 0, -0.6)),
            ('L12', '4', 'L13', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0)], +45), 0, -0.6)),
            ('L13', '4', 'L14', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45)], 0), 0, -0.6)),
            ('L14', '4', 'LB1', '3', 0.4, (Dird, ([(1.5, 0), (1.0, -45), (3.2, 0), (3, +45)], +45), ([(3.3, -180), (4.2, -135), (10, -90)], -110), -0.6)),
            # LCI
            ('L11', '5', 'L12', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (3.2, 0)], -45), 0, -0.6)),
            ('L12', '5', 'L13', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0)], +45), 0, -0.6)),
            ('L13', '5', 'L14', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45)], 0), 0, -0.6)),
            ('L14', '5', 'LB1', '2', 0.4, (Dird, ([(1.75, 0), (1.2, -45), (2.4, 0)], +45), ([(3.8, -180), (5.0, -135), (10, -90)], -110), -0.6)),
            # 5V
            ('L11', '1', 'L12', '1', 0.6, (Dird, ([(1.2, +90), (7.8, 0), (1, -45), (1, -90)], -45), 0, -1)),
            ('L12', '1', 'L13', '1', 0.6, (Dird, ([(1.2, +90), (7.8, 0)], -45), 0, -1)),
            ('L13', '1', 'L14', '1', 0.6, (Dird, ([(1.2, +90), (7.8, 0)], -45), 0, -1)),
            ('L14', '1', 'L14', via_vcc_l14, 0.6, (Dird, 90, 0)),
            ('J1', via_splt_vbb, 'J1', via_vcc_l14, 0.5, (Dird, 90, 0)),
            # SWB1
            ('J1', via_splt_vba, 'SWB1', '2', 0.6, (Dird, 90, 90, -1)),
            # LB1 5V
            ('LB1', '1', 'LB1', via_vcc_lb1, 0.6, (Dird, ([(4.4, -180)], -135), 90, -1)),
            ('CB1', '1', 'CB1', via_vcc_lb1, 0.6, (Dird, 90, 0)),
        ] )

    ###
    ### Ref
    ###
    if board == BZL:
        refs = [
            (3,   135,   0, ['U1']),
            (2.8,   0,  90, ['U2']),
            (2.5,   0,  90, ['C1', 'C2', 'C4']),
            (3,     0, 180, ['C3', 'C5', 'C6', 'R1', 'D1']),
            (3.3,   0, 180, ['C11', 'R11', 'R12']),
            (3.3, 180,   0, ['CB1', 'RB1', 'RB2']),
            (1.8, -90,   0, ['R2']),
            (1.8, +90, 180, ['R3']),
            (3,   180, 180, ['R4', 'R5', 'R6', 'R7']),
            (3,   180,   0, ['R8', 'R9', 'L1', 'F1']),
            (1.8, -90, 180, ['D0', 'D11', 'D12', 'D13', 'D14']),
            (7,     0, +90, ['J1']),
            (7,   180, -90, ['J2']),
            (15,  -90,  -90, ['J3']),
        ]
    elif board == BZR:
        refs = [
            (3,   135,   0, ['U1']),
            (3,     0,   0, ['C1']),
            (3.3, 180,   0, ['R1']),
            (3.3,   0, 180, ['D1']),
            (3.3, 180, 180, ['C11', 'R11', 'R12']),
            (3.3,   0,   0, ['CB1', 'RB1', 'RB2']),
            (3,   180, 180, ['R6', 'R7']),
            (1.8, -90, 180, ['D11', 'D12', 'D13', 'D14']),
            (7,     0, -90, ['J1']),
        ]
    else:
        refs = [ (0, 0, None, ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']) ]
    for offset_length, offset_angle, text_angle, mod_names in refs:
        for mod_name in mod_names:
            mod = kad.get_mod( mod_name )
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
    if board == BZL:
        pads = [
            ('1', 'GND'),
            ('2', 'nRST'),
            ('3', 'CLK'),
            ('4', 'DIO'),
            ('5', 'TX'),
            ('6', 'RX'),
        ]
        for pad, text in pads:
            pos = kad.get_pad_pos( 'J3', pad )
            pos = vec2.scale( 2, vec2.rotate( -90 ), pos )
            kad.add_text( pos, 0, text, 'F.SilkS', (0.9, 0.9), 0.15,
                pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )

    pcbnew.Refresh()

if __name__=='__main__':
    main()
