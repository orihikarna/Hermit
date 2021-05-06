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
Spline      = kad.Spline
##

# in mm
VIA_Size = [(1.1, 0.6), (1.0, 0.5), (0.8, 0.4), (0.6, 0.3)]

PCB_Width  = 170
PCB_Height = 155

U1_x, U1_y = 82, 95
J1_x, J1_y, J1_angle = 18, 98, 0
J2_x, J2_y, J2_angle = 130, 100, 0
J3_x, J3_y, J3_angle = 85, 118, 10
D1_x, D1_y = 62, 106

keys = {
    '11' : [43.025, -73.079, 17.400, 16.800, 9.6], # N
    '12' : [38.972, -56.727, 17.400, 16.800, 9.6], # H
    '13' : [39.809, -39.544, 17.400, 16.800, 9.6], # Y
    '14' : [41.559, -22.205, 17.400, 16.800, 9.6], # &
    '21' : [60.179, -70.163, 17.400, 16.800, 9.6], # M
    '22' : [56.126, -53.811, 17.400, 16.800, 9.6], # J
    '23' : [56.963, -36.628, 17.400, 16.800, 9.6], # U
    '24' : [58.712, -19.289, 17.400, 16.800, 9.6], # '
    '31' : [79.740, -69.600, 17.400, 16.800, -6.4], # <
    '32' : [78.080, -52.511, 17.400, 16.800, -6.4], # K
    '33' : [76.421, -35.423, 17.400, 16.800, -6.4], # I
    '34' : [78.279, -18.726, 17.400, 16.800, -6.4], # (
    '41' : [97.033, -71.525, 17.400, 16.800, -6.4], # >
    '42' : [96.546, -54.567, 17.400, 16.800, -6.4], # L
    '43' : [96.059, -37.609, 17.400, 16.800, -6.4], # O
    '44' : [95.573, -20.651, 17.400, 16.800, -6.4], # )
    '51' : [117.450, -80.661, 23.490, 16.800, -0.0], # ?
    '52' : [115.159, -62.521, 17.400, 16.800, 9.6], # +
    '53' : [114.672, -45.563, 17.400, 16.800, 9.6], # P
    '54' : [114.185, -28.605, 17.400, 16.800, 9.6], #  
    '62' : [132.809, -62.521, 17.400, 16.800, 9.6], # *
    '63' : [132.322, -45.563, 17.400, 16.800, 9.6], # `
    '64' : [131.835, -28.605, 17.400, 16.800, 9.6], # =
    '71' : [143.289, -80.661, 28.188, 16.800, -0.0], # _
    '72' : [150.458, -62.521, 17.400, 16.800, 9.6], # ]
    '73' : [149.971, -45.563, 17.400, 16.800, 9.6], # [
    '82' : [51.901, -110.752, 20.243, 16.800, -250.4], # S
    '83' : [35.577, -122.015, 20.243, 16.800, -230.4], # S
    '84' : [21.087, -136.423, 17.400, 16.800, -210.4], # R
    '91' : [23.565, -69.264, 17.400, 16.800, 18.1], # E
}

angle_SW82 = 19.6
angle_PB = 9.6
angle_M = 16

holes = [
    ( 16.8, 150, 90 - 16),
    ( 4.4, J1_y - 11, 90),
    ( 4.4, J1_y + 11, 90),
    ( 14, 35, -30),
    ( 66, 5, 90),
    (106, 5, 90),
    (154, 31, 36),
    (163, 84, -40),
    (J2_x - 1.6, J2_y + 10, 90),
    (68, 119.6, -64),
    # (47, 136, -46),
    #
    (65, 84.6, 90),
]

L2R = []
R2L = []

# Board Type
BDL = 0# Left plate
BDR = 1# Right plate
BDT = 2# Top plate
BDB = 3# Bottom plate
BDM = 4# Middle plate
BDS = 5# Second Top thin plate

# Edge.Cuts size
Edge_CX, Edge_CY = 0, 0
Edge_W, Edge_H = 0, 0

def make_corners( key_cnrs ):
    corners = []
    for mod, offset, dangle, cnr_type, prms in key_cnrs:
        if type( mod ) == str:
            x, y, _, _, angle = keys[mod]
            # flip y
            y = -y
            offset = (offset[0], -offset[1])
        else:
            x, y, angle = mod
        # print( x, y, angle, offset )
        pos = vec2.mult( mat2.rotate( angle ), offset, (x, y) )
        corners.append( [(pos, -angle + dangle), cnr_type, prms] )
    return corners

def drawEdgeCuts( board ):
    width = 0.12
    USBC_Width  = 4.675
    USBC_Height = 5.73

    USBT = 0.8
    USBM = 6.3 - USBT * 2
    USBW = 4.0

    U1_mod = (U1_x, U1_y, 0)
    J1_mod = (J1_x, J1_y, J1_angle)
    J2_mod = (J2_x, J2_y, J2_angle)
    J3_mod = (J3_x, J3_y, J3_angle)

    midcnrs_set = []
    if True:# outer
        out_cnrs = []
        mid_cnrs = []
        # LED & J3:
        if True:# bottom right corner
            cnrs = [
                (J3_mod, (-7, 1.27), 180, BezierRound, [14]),
            ]
            for cnr in cnrs:
                out_cnrs.append( cnr )
        if True:# BDM
            cnrs = [
                # J3
                (J3_mod, (+14.8, +1.27), 180, BezierRound, [14]),
                (J3_mod, (+14.2, +1.00), 270, BezierRound, [0.2]),
                (J3_mod, (+13.6, 0),     180, BezierRound, [0.5]),
                (J3_mod, (+13.0, +1.00),  90, BezierRound, [0.5]),
                (J3_mod, (+12.4, +1.27), 180, BezierRound, [0.2]),
                # LED
                (J3_mod, (-1.5,   0), 270, BezierRound, [0.5]),
                (J3_mod, (-4, -2.27), 180, BezierRound, [0.5]),
                (J3_mod, (-5.8,   0),  90, BezierRound, [0.5]),
                (J3_mod, (-7, +1.27), 180, BezierRound, [0.5]),
            ]
            for cnr in cnrs:
                mid_cnrs.append( cnr )
        # bottom left
        cnrs = [
            ('84', (-10.0, 15.0), -30.4, Spline, [70]),
            (J1_mod, (-J1_x,  +10), 270, Round, [20]),
            (J1_mod, (-J1_x/2, +7),   0, Round, [2]),
        ]
        for cnr in cnrs:
            out_cnrs.append( cnr )
            mid_cnrs.append( cnr )
        # J1: Split
        if board in [BDL, BDR]:
            cnrs = [
                (J1_mod, (0, +USBC_Width+1), 270, Round, [0.5]),
                (J1_mod, (3, +USBC_Width  ),   0, Round, [0.5]),
                (J1_mod, (USBC_Height, 0),   270, Round, [0.5]),
                (J1_mod, (3, -USBC_Width),   180, Round, [0.5]),
                (J1_mod, (0, -USBC_Width-1), 270, Round, [0.5]),
            ]
        else:
            cnrs = [
                (J1_mod, (0, 0), 270, Round, [0.5]),
            ]
        for cnr in cnrs:
            out_cnrs.append( cnr )
        if True:# BDM
            cnrs = [
                (J1_mod, (16.4, 0), 270, Round, [0.5]),
            ]
            for cnr in cnrs:
                mid_cnrs.append( cnr )
        # top side
        cnrs = [
            (J1_mod, (-J1_x/2, -7), 180, Round, [0.5]),
            (J1_mod, (-J1_x,  -10), 270, Round, [2]),
            ('34', (-10.4, 16.8), angle_PB - angle_M, Round, [67]),
            ('71', (+26.6, 11.7), 90, Round, [67]),
            ('71', (0, -12.2), 180, Round, [16]),
        ]
        for cnr in cnrs:
            out_cnrs.append( cnr )
            mid_cnrs.append( cnr )
        # J2: USB PC
        if board in [BDL]:
            cnrs = [
                (J2_mod, (2.62, -USBC_Width-1),  90, Round, [0.5]),
                (J2_mod, (2.62-3, -USBC_Width), 180, Round, [0.5]),
                (J2_mod, (2.62-USBC_Height, 0),  90, Round, [0.5]),
                (J2_mod, (2.62-3, +USBC_Width),   0, Round, [0.5]),
                # (J2_mod, (2.62, +USBC_Width+1),  90, Round, [0.5]),
            ]
            for cnr in cnrs:
                out_cnrs.append( cnr )
        if True:# BDM
            cnrs = [
                (J2_mod, (2.62, -USBM-USBT*2-0.2),  90, Round, [0.5]),
                (J2_mod, (-USBW+2, -USBM-USBT*2),  180, Round, [0.2]),
                (J2_mod, (-USBW,   -USBM-USBT),     90, Round, [0.5]),
                (J2_mod, (-USBW+2, -USBM     ),      0, Round, [0.5]),
                (J2_mod, (2.62,    0         ),     90, Round, [0.5]),
                (J2_mod, (-USBW+2, +USBM     ),    180, Round, [0.5]),
                (J2_mod, (-USBW,   +USBM+USBT),     90, Round, [0.5]),
                (J2_mod, (-USBW+2, +USBM+USBT*2),    0, Round, [0.5]),
            ]
            for cnr in cnrs:
                mid_cnrs.append( cnr )
        # bottom right
        cnrs = [
            (J2_mod, (2.62, 10), +90, Round, [0.5]),
            (J2_mod, (-1, 14), 180, Round, [3]),
        ]
        for cnr in cnrs:
            out_cnrs.append( cnr )
            mid_cnrs.append( cnr )
        # BDM
        midcnrs_set.append( make_corners( mid_cnrs ) )
        # draw
        if board is not BDM:
            corners = make_corners( out_cnrs )
            kad.draw_closed_corners( corners, 'Edge.Cuts', width )
            if True:# PCB Size
                x0, x1 = +1e6, -1e6
                y0, y1 = +1e6, -1e6
                for (pos, _), _, _ in corners:
                    x, y = pos
                    x0 = min( x0, x )
                    x1 = max( x1, x )
                    y0 = min( y0, y )
                    y1 = max( y1, y )
                global Edge_CX, Edge_CY
                global Edge_W, Edge_H
                Edge_CX, Edge_CY = (x0 + x1) / 2, (y0 + y1) / 2
                Edge_W, Edge_H = x1 - x0, y1 - y0
                if True:
                    # print( 'Edge: (CX, CY) = ({:.2f}, {:.2f})'.format( Edge_CX, Edge_CY ) )
                    print( 'Edge: (W, H) = ({:.2f}, {:.2f})'.format( Edge_W, Edge_H ) )

    if board in [BDL, BDR, BDM]:# J3
        off_y = -1
        cnrs = [
            (J3_mod, (+14.2, off_y - 0.70), 270, BezierRound, [0.5]),
            (J3_mod, (+10.0, off_y - 1.27), 180, BezierRound, [0.5]),
            (J3_mod, (-0.50, off_y - 0.70),  90, BezierRound, [0.5]),
            (J3_mod, (+10.0, off_y - 0.00),   0, BezierRound, [0.5]),
        ]
        midcnrs_set.append( make_corners( cnrs ) )
    if board in [BDL, BDR, BDM]:# J2 USB PC hole
        cnrs = [
            (J2_mod, (-USBW-3.2, -USBM - USBT*2),   0, Round, [0.5]),
            (J2_mod, (-USBW-1.6, -USBM - USBT  ),  90, Round, [0.5]),
            (J2_mod, (-USBW-3.2, -USBM         ), 180, Round, [0.5]),
            (J2_mod, (-13.0,     0             ),  90, Round, [0.5]),
            (J2_mod, (-USBW-3.2, +USBM         ),   0, Round, [0.5]),
            (J2_mod, (-USBW-1.6, +USBM + USBT  ),  90, Round, [0.5]),
            (J2_mod, (-USBW-3.2, +USBM + USBT*2), 180, Round, [0.5]),
            (J2_mod, (-14.6,     0             ), 270, Round, [0.5]),
        ]
        midcnrs_set.append( make_corners( cnrs ) )
    if board in [BDL, BDR, BDM]:# U1
        cnrs = [
            (U1_mod, (0,   -8),   0, Round, [1]),
            (U1_mod, (13.6, 0),  90, Round, [1]),
            (U1_mod, (0, 10.4), 180, Round, [1]),
            (U1_mod, (-8,   0), 270, Round, [1]),
        ]
        midcnrs_set.append( make_corners( cnrs ) )
    if board in [BDL, BDR, BDM]:# mid hole (4-fingers)
        cnrs = [
            ('14', (-8, 0), 270, BezierRound, [3]),
            ('24', (0, +8.8), 0, BezierRound, [5]),
            ('34', (0, +8.8), 0, BezierRound, [3]),
            ('54', (-9, +13.6), 90 + angle_PB, BezierRound, [3]),
            ('64', (0, +9),     angle_PB,      BezierRound, [3]),
            ('64', (+7, 0),  90, BezierRound, [3]),
            ('73', (0, +8.8), 0, BezierRound, [3]),
            ('73', (+7, 0),  90, BezierRound, [3]),
            ('72', (+6.2, -7.6), 180, BezierRound, [3]),
            ('71', (+11.4, 0), 90, BezierRound, [3]),
            ('71', (0, -7.4), 180, BezierRound, [3]),
            ('51', (-12, -4), 270, BezierRound, [3]),
            ('41', (0, -7.4), 180, BezierRound, [3]),
            ('21', (0, -7.4), 180, BezierRound, [3]),
            ('11', (-16, -5.4), 180 + angle_PB, BezierRound, [3]),
            ('91', (-7, 0),  270, BezierRound, [3]),
            ('91', (0, +8.8),  0, BezierRound, [3]),
            ('12', (-7, 4),  270, BezierRound, [3]),
            ('13', (-7, +7.0), 0, BezierRound, [3]),
        ]
        midcnrs_set.append( make_corners( cnrs ) )
    if board in [BDL, BDR, BDM]:# mid hole (thumb)
        cnrs = [
            ('84', (0, +8.6),   0, BezierRound, [4]),
            ('84', (+7.0, 0),  90, BezierRound, [4]),
            ('83', (+7.0, 0),  90, BezierRound, [4]),
            ('82', (+10, 4),    0, BezierRound, [1]),
            ('82', (+11.6, 0), 90, BezierRound, [1]),
            ('82', (0, -7.6), 180, BezierRound, [4]),
            ('82', (-7.0, 0), 270, BezierRound, [4]),
            ('83', (-7.0, 0), 270, BezierRound, [3]),
            ('84', (-7.0, 0), 270, BezierRound, [3]),
        ]
        midcnrs_set.append( make_corners( cnrs ) )
    if board in [BDL, BDR, BDM]:# draw BDM
        layer = 'Edge.Cuts' if board == BDM else 'F.Fab'
        w = width if board == BDM else width * 2
        for midcnrs in midcnrs_set:
            kad.draw_closed_corners( midcnrs, layer, w )

def load_distance_image( path ):
    with open( path ) as fin:
        data = fin.readlines()
        w = int( data[0] )
        h = int( data[1] )
        # print( dist_w, dist_h )
        dist = []
        for y in range( h ):
            vals = data[y+2].split( ',' )
            del vals[-1]
            if len( vals ) != w:
                print( 'Error: len( vals )({}) != w({})'.format( len( vals ), w ) )
                break
            vals = map( lambda v: float( v ) / 100.0, vals )
            dist.append( vals )
    return (dist, w, h)

def get_distance( dist_image, pnt ):
    dist, w, h = dist_image
    x, y = vec2.scale( 10, vec2.sub( pnt, (Edge_CX, Edge_CY) ) )
    x, y = vec2.add( (x, y), (w / 2.0, h / 2.0) )
    x = min( max( x, 0. ), w - 1.01 )
    y = min( max( y, 0. ), h - 1.01 )
    nx = int( math.floor( x ) )
    ny = int( math.floor( y ) )
    # if nx < 0 or w <= nx + 1 or ny < 0 or h <= ny + 1:
    #     return 0
    dx = x - nx
    dy = y - ny
    d  = dist[ny][nx]     * (1 - dx) * (1 - dy)
    d += dist[ny][nx+1]   * dx       * (1 - dy)
    d += dist[ny+1][nx]   * (1 - dx) * dy
    d += dist[ny+1][nx+1] * dx       * dy
    return d

CIDX, POS, NIDX = range( 3 )

def connect_line_ends( line_ends, other_ends, curv_idx, pos, idx, layer, width ):
    # overwrite new line_end
    line_ends[idx] = (curv_idx, pos, 0)

    # connect with up/down neighbors
    for nidx in [idx-1, idx+1]:
        if nidx < 0 or len( line_ends ) <= nidx:
            continue
        # up / down neighbor
        neib = line_ends[nidx]
        if not neib:# no neibor
            continue
        if (neib[NIDX] & (1 << idx)) != 0:# already connected with this index
            #    L1-----R1      L1----
            #    C  ...---^^^ <-- cannot connect L1(right) and L2,
            #     L2--------R2    because L2 is already connected with L1(left)
            continue

        # The lines are drawn from left to right.
        # For the right line ends, reject the neighbor if there is a left end after the neighbor right end.
        # For the left line ends, reject the neighbor if there is a right end after the neighbor left end.
        if other_ends[nidx] and other_ends[nidx][CIDX] > neib[CIDX]:
            #    L1----------------------------R1
            #    C             .....-----^^^^^    <-- cannot connect R1 and R2(right),
            #     L2---------R2        L2---------R2  becuase L2(right) is on the right of R2(left)
            #          neib[CIDX] left[CIDX]
            continue
            pass
        # connect
        curr = line_ends[idx]
        line_ends[idx]  = (curr[CIDX], curr[POS], curr[NIDX] | (1 << nidx))
        line_ends[nidx] = (neib[CIDX], neib[POS], neib[NIDX] | (1 << idx))
        kad.add_line( curr[POS], neib[POS], layer, width )

def draw_top_bottom( board, sw_pos_angles ):
    if board in [BDT, BDS]:# keysw holes
        length = 13.94 if board == BDT else 14.80
        for sw_pos, angle in sw_pos_angles:
            corners = []
            for i in range( 4 ):
                deg = i * 90 + angle
                pos = vec2.scale( length / 2.0, vec2.rotate( deg ), sw_pos )
                corners.append( [(pos, deg + 90), BezierRound, [1]] )
            kad.draw_closed_corners( corners, 'Edge.Cuts', 0.1 )

    if board == BDS:
        return

    if False:# screw holes
        for prm in holes:
            x, y, angle = prm
            ctr = (x, y)
            kad.add_arc( ctr, vec2.add( ctr, (2.5, 0) ), 360, 'Edge.Cuts', 0.1 )
        return

    ctr_pos_angle_vec = []
    anchors = [
        (28, 125),
        (27, 110),
        (1, -3),
        (5, +3),
        (9, -3),
        (13, +3),
        (17, 24),
        (20, 26),
        (24, 28),
    ]
    for n in range( 1, len( anchors ) ):
        anchor_a = anchors[n-1]
        anchor_b = anchors[n]
        pos_a, angle_a = sw_pos_angles[anchor_a[0]]
        pos_b, angle_b = sw_pos_angles[anchor_b[0]]
        angle_a += anchor_a[1]
        angle_b += anchor_b[1]
        if abs( angle_a - angle_b ) > 1:
            vec_a = vec2.rotate( angle_a + 90 )
            vec_b = vec2.rotate( angle_b + 90 )
            ctr, _, _ = vec2.find_intersection( pos_a, vec_a, pos_b, vec_b )
            if n == 1:
                angle_a += (angle_a - angle_b) * 1.1
            elif n + 1 == len( anchors ):
                angle_b += (angle_b - angle_a) * 1.5
            if False:
                layer = 'F.Fab'
                width = 1.0
                # print( ctr, ka, kb )
                kad.add_line( ctr, pos_a, layer, width )
                kad.add_line( ctr, pos_b, layer, width )
        else:
            ctr = None
        ctr_pos_angle_vec.append( (ctr, pos_a, angle_a, pos_b, angle_b) )
    # return

    # read distance data
    board_type = { BDT : 'T', BDB: 'B' }[board]
    dist_image = load_distance_image( '/Users/akihiro/repos/Hermit/Hermit{}/Edge_Fill.txt'.format( board_type ) )

    # draw lines
    pos_dummy = [None, None]
    pitch = 2.0
    nyrange = range( -559, 888, 16 )
    width0, width1 = 0.3, 1.3
    for ny in nyrange:
        y = ny * 0.1
        uy = float( ny - nyrange[0] ) / float( nyrange[-1] - nyrange[0] )
        if True:
            if uy < 0.5:
                uy = 2 * uy
            else:
                uy = 2 * (1 - uy)
        # base position
        idx_base = 2
        anchor_base = anchors[idx_base]
        pos_base, angle_base = sw_pos_angles[anchor_base[0]]
        angle_base += anchor_base[1]
        pos_base = vec2.mult( mat2.rotate( -angle_base ), (0, y), pos_base )
        # control points for one horizontal line
        pos_angles = [(pos_base, angle_base)]
        for dir in [-1, +1]:
            idx = idx_base
            pos_a, angle_a = pos_base, angle_base
            while 0 < idx and idx < len( ctr_pos_angle_vec ):
                idx2 = idx + dir
                if dir == -1:
                    ctr, _, angle_b, _, angle_a = ctr_pos_angle_vec[idx2]
                else:# dir == +1:
                    ctr, _, angle_a, _, angle_b = ctr_pos_angle_vec[idx]
                idx = idx2
                #
                vec_b = vec2.rotate( angle_b + 90 )
                pos_b = vec2.scale( -vec2.distance( pos_a, ctr ), vec_b, ctr )
                pos_angles.append( (pos_b, angle_b) )
                pos_a = pos_b
            if dir == -1:
                pos_angles.reverse()

        # one horizontal line with nearly constant pitch
        curv = []
        for idx, (pos_b, angle_b) in enumerate( pos_angles ):
            if idx == 0:
                curv.append( pos_b )
                continue
            if False:
                curv.append( pos_b )
            else:
                pos_a, angle_a = pos_angles[idx-1]
                # pnts = kad.calc_bezier_round_points( pos_a, vec2.rotate( angle_a ), pos_b, vec2.rotate( angle_b + 180 ), 8 )
                pnts = kad.calc_bezier_corner_points( pos_a, vec2.rotate( angle_a ), pos_b, vec2.rotate( angle_b + 180 ), pitch, ratio = 0.8 )
                for idx in range( 1, len( pnts ) ):
                    curv.append( pnts[idx] )

        gap = 0.5
        if True:# divide if close to the edge
            div = 10
            thick = width1 / 2.0 + gap
            curv2 = []
            for idx, pnt in enumerate( curv ):
                dist = get_distance( dist_image, pnt )
                if idx == 0:
                    prev_pnt = pnt
                    prev_dist = dist
                    curv2.append( pnt )
                    continue
                if max( dist, prev_dist ) > -pitch and min( dist, prev_dist ) < thick:
                    vec = vec2.sub( pnt, prev_pnt )
                    for i in range( 1, div ):
                        curv2.append( vec2.scale( i / float( div ), vec, prev_pnt ) )
                curv2.append( pnt )
                prev_pnt = pnt
                prev_dist = dist
            curv = curv2

        # draw horizontal line avoiding key / screw holes
        w_thin = 0.25
        thick_thin = w_thin / 2.0 + gap
        for lidx, layer in enumerate( ['F.Cu', 'B.Cu'] ):
            if lidx == 0:
                w = width0 + (width1 - width0) * uy
            else:
                w = width1 + (width0 - width1) * uy
            thick = w / 2.0 + gap
            num_lines = int( math.ceil( w / (w_thin * 0.96) ) )
            line_sep = (w - w_thin) / (num_lines - 1)
            line_lefts = [None for _ in range( num_lines )]
            line_rights = [None for _ in range( num_lines )]
            last_pnt = [None for _ in range( num_lines )]
            for cidx in range( 1, len( curv ) ):
                pnt_a = curv[cidx-1]
                pnt_b = curv[cidx]
                if False:
                    kad.add_line( pnt_a, pnt_b, layer, w )
                    # kad.add_arc( pnt_a, vec2.add( pnt_a, (w / 2, 0) ), 360, layer, 0.1 )
                    continue
                vec_ba = vec2.sub( pnt_b, pnt_a )
                unit_ba = vec2.normalize( vec_ba )[0]
                norm_ba = (unit_ba[1], -unit_ba[0])
                # multiple horizontal lines
                single = True
                lines = []
                for m in range( num_lines ):
                    delta = line_sep * m + w_thin / 2.0 - w / 2.0
                    q0 = vec2.scale( delta, norm_ba, pnt_a )
                    q1 = vec2.scale( delta, norm_ba, pnt_b )
                    d0 = get_distance( dist_image, q0 )
                    d1 = get_distance( dist_image, q1 )
                    if min( d0, d1 ) < thick:
                        single = False
                    if d0 >= thick_thin and d1 >= thick_thin:# single line
                        pass
                    elif d0 >= thick_thin:
                        while d1 < thick_thin - 0.01:
                            diff = thick_thin - d1
                            q1 = vec2.scale( -diff * 0.94, unit_ba, q1 )
                            d1 = get_distance( dist_image, q1 )
                        connect_line_ends( line_lefts, line_rights, cidx, q1, m, layer, w_thin )
                    elif d1 >= thick_thin:
                        while d0 < thick_thin - 0.01:
                            diff = thick_thin - d0
                            q0 = vec2.scale( +diff * 0.94, unit_ba, q0 )
                            d0 = get_distance( dist_image, q0 )
                        connect_line_ends( line_rights, line_lefts, cidx, q0, m, layer, w_thin )
                    else:# no line
                        q0 = None
                        q1 = None
                    if q0 and q1:
                        lines.append( (q0, q1) )
                        if last_pnt[m]:
                            d = vec2.distance( last_pnt[m], q0 )
                            if 0.01 < d and d < 0.8:# close tiny gap
                                kad.add_line( last_pnt[m], q0, layer, w_thin )
                        last_pnt[m] = q1

                if single:
                    kad.add_line( pnt_a, pnt_b, layer, w )
                    if not pos_dummy[lidx] and w > 1.1:
                        pos_dummy[lidx] = pnt_a
                else:
                    for (q0, q1) in lines:
                        kad.add_line( q0, q1, layer, w_thin )
                # clear line_ends when single or no line
                if single or len( lines ) == 0:
                    for m in range( num_lines ):
                        line_lefts[m] = None
                        line_rights[m] = None
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
    FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    return map( lambda pt: vec2.add( (size[0] * pt[0], size[1] * pt[1]), offset ), FourCorners )

### Set mod positios
def place_mods( board ):
    if board == BDL:
        kad.move_mods( (0, 0), 0, [
            # mcu
            (None, (U1_x, U1_y), 0, [
                ('U1', (0, 0), 0),
                # pass caps
                (None, (0, 0), 0, [
                    ('C4', (+5.8, +4.4), 180),
                    ('C3', (-4.4, -5.8), 90),
                    ('C5', (-6.4, -5.8), 90),
                ] ),
                # regulators
                (None, (9.5, 8.0), -90, [
                    ('C1', (0, -2.7), 0),
                    ('U2', (-0.2, 0), 0),
                    ('C2', (0, +2.7), 0),
                ] ),
                # NRST C6 
                ('C6', (3.4, 8.0), -90),
                # LED R1
                ('R1', (-6.4, 4.0), -90),
            ] ),
            # USB (PC) connector
            (None, (J2_x, J2_y), J2_angle, [
                ('J2', (0, 0), 90),
                ('R8', (-7.5, +5.2), 0),
                ('R9', (-7.5, -5.2), 0),
                ('R5', (-12.4, -1.0), 180),# USB DM/DP
                ('R4', (-12.4, +1.0), 180),# USB DM/DP
                ('F1', (-12.4, +3.0), 180),
                ('L1', (-12.4, +5.0), 180),
            ] ),
            # Pin headers
            (None, (J3_x, J3_y), J3_angle, [
                ('J3', (0, 0), 90),
                ('D1', (-3.6, 0), 180),# LED
            ] ),
        ] )
    elif board == BDR:
        kad.move_mods( (0, 0), 0, [
            (None, (U1_x, U1_y), 0, [
                # expander
                ('U1', (0, 0), +90),
                ('C1', (-1.27, 6.4), 180),
                # LED R1
                ('R1', (3.2, 6.4), 180),
            ] ),
            # Pin headers
            (None, (J3_x, J3_y), J3_angle, [
                ('D1', (-3.6, 0), 0),# LED
            ] ),
        ] )

    # J1: Split (USB) connector
    if board in [BDL, BDR]:
        sign = [+1, -1][board]
        kad.move_mods( (J1_x, J1_y), J1_angle, [
            (None, (2.62, 0), 0, [
                ('J1', (0, 0), -90 * sign),
                ('R6', (7.5, -5.2 * sign), 180),
                ('R7', (7.5, +5.2 * sign), 180),
            ] ),
        ] )
        # I2C pull-ups
        if board in [BDL]:
            kad.move_mods( (J1_x, J1_y), J1_angle, [
                (None, (3, 0), 0, [
                    ('R2', (12, -1.9), +90),
                    ('R3', (12, +1.9), -90),
                ] ),
            ] )

    # Debounce RRCs
    if board in [BDL, BDR]:
        for col in map( str, range( 1, [10, 9][board] ) ):
            mod_sw = 'SW' + col + '1'
            if col == '6':
                if board == BDL:
                    mod_sw = 'SW71'
                    dx, dy = 8.0, -2.0
                else:# BDR
                    mod_sw = 'SW51'
                    dx, dy = 8.0, -2.0
            elif col == '8':
                mod_sw = 'SW82'
                dx, dy = -9.4, 0.4
            elif col == '9':
                dx, dy = -9, -10
            else:
                dx, dy = -9.2, -2.0
            if board == BDR and col not in ['8']:
                dx *= -1
            pos, angle = kad.get_mod_pos_angle( mod_sw )
            kad.move_mods( pos, angle + [180, 0][board], [
                (None, (dx, dy), 0, [
                    ('C' + col + '1', (0, -2), [0, 180][board]),
                    ('R' + col + '1', (0,  0), [0, 180][board]),
                    ('R' + col + '2', (0, +2), [0, 180][board]),
                ] ),
            ] )

    # draw USB connector rectangle
    if board in [BDL, BDR]:
        w, h = 14, 5.2
        for name in ('J1', 'J2'):
            if kad.get_mod( name ) == None:
                continue
            pos, angle = kad.get_mod_pos_angle( name )
            corners = []
            for pnt in make_rect( (w, h), (-w/2, -h/2) ):
                pt = vec2.mult( mat2.rotate( angle ), pnt, pos )
                corners.append( [(pt, 0), Line, [0]] )
            kad.draw_closed_corners( corners, 'F.Fab', 0.1 )

    # dummy pads
    if board in [BDM, BDS]:
        for i in range( 2 ):
            dmy = 'P{}'.format( i + 1 )
            if kad.get_mod( dmy ):
                kad.set_mod_pos_angle( dmy, (J1_x + 20, J1_y), 0 )

    # draw mouting holes
    if True:
        for idx, prm in enumerate( holes ):
            x, y, angle = prm
            ctr = (x, y)
            hole = 'H{}'.format( idx + 1 )
            if kad.get_mod( hole ):
                kad.set_mod_pos_angle( hole, (x, y), 0 )
            else:
                corners = []
                if True:
                    hsize = [4.2, 4.86] if board in [BDL, BDR] else [4.4, 5.0]
                    for i in range( 4 ):
                        deg = i * 90 - angle
                        pos = vec2.scale( hsize[i % 2] / 2.0, vec2.rotate( deg ), ctr )
                        corners.append( [(pos, deg + 90), BezierRound, [1.2]] )
                else:
                    for i in range( 6 ):
                        deg = i * 60 - 90
                        pos = vec2.scale( 2.1, vec2.rotate( deg ), ctr )
                        corners.append( [(pos, deg + 90), BezierRound, [0.5]] )
                kad.draw_closed_corners( corners, 'Edge.Cuts', 0.2 )
                if False:
                    corners = []
                    for i in range( 6 ):
                        deg = i * 60 - 90
                        pos = vec2.scale( 2.0, vec2.rotate( deg ), ctr )
                        corners.append( [(pos, deg + 90), Linear, [0]] )
                    kad.draw_closed_corners( corners, 'F.Fab', 0.1 )

### Wire mods
def wire_mods( board ):
    layer1 = ['F.Cu', 'B.Cu'][board]
    layer2 = ['B.Cu', 'F.Cu'][board]
    GND = pcb.FindNet( 'GND' )

    w_mcu, r_mcu = 0.5, -0.6
    w_exp, r_exp = 0.44, -0.4
    w_pwr, r_pwr = 0.75, -1
    w_dbn, r_dbn = 0.6, -1
    w_row, r_row = 0.6, -1
    w_col, r_col = 0.6, -1
    w_dat, r_dat = 0.5, -0.75# LED
    w_jtag, r_jtag = 0.4, -0.6

    # J1: Split (USB) connector
    if board in [BDL, BDR]:# connector vias & wires
        via_splt_vba = kad.add_via_relative( 'J1', 'A4', (-0.4,  -5.8), VIA_Size[0] )
        via_splt_vbb = kad.add_via_relative( 'J1', 'B4', (+0.4,  -5.8), VIA_Size[0] )
        via_splt_cc1 = kad.add_via_relative( 'J1', 'A5', (-0.15, -2.4), VIA_Size[3] )
        via_splt_cc2 = kad.add_via_relative( 'J1', 'B5', (+0.15, -3.2), VIA_Size[3] )
        via_splt_dpa = kad.add_via_relative( 'J1', 'A6', (-0.4,  -4.8), VIA_Size[3] )
        via_splt_dpb = kad.add_via_relative( 'J1', 'B6', (+0.15, -4.8), VIA_Size[3] )
        via_splt_dma = kad.add_via_relative( 'J1', 'A7', (+0.15, -4.0), VIA_Size[3] )
        via_splt_dmb = kad.add_via_relative( 'J1', 'B7', (-0.15, -4.1), VIA_Size[3] )
        via_splt_sb1 = kad.add_via_relative( 'J1', 'A8', (+0.15, -2.4), VIA_Size[3] )
        via_splt_sb2 = kad.add_via_relative( 'J1', 'B8', (-0.15, -3.2), VIA_Size[3] )
        via_r6_cc1   = kad.add_via_relative( 'R6', '1',  (0,    -1.24), VIA_Size[3] )
        via_r7_cc2   = kad.add_via_relative( 'R7', '1',  (0,    +1.24), VIA_Size[3] )
        kad.wire_mods( [
            # gnd
            ('J1', 'S1', 'J1', 'S2', w_pwr, (Dird, ([(0.8, 45)], 0), -45), 'Opp'),
            ('J1', 'S2', 'J1', 'S3', w_pwr, (Strt)),
            ('J1', 'S2', 'J1', 'S3', w_pwr, (Strt), 'Opp'),
            ('J1', 'S1', 'J1', 'S4', w_pwr, (Strt)),
            ('J1', 'S1', 'J1', 'S4', w_pwr, (Strt), 'Opp'),
            # vbus
            ('J1', via_splt_vba, 'J1', 'A4', w_pwr, (Dird, +60, ([(1.5, 90), (1.0, 120)], 90))),
            ('J1', via_splt_vbb, 'J1', 'B4', w_pwr, (Dird, -60, ([(1.5, 90), (1.0,  60)], 90))),
            ('J1', via_splt_vba, 'J1', via_splt_vbb, w_pwr, (Strt), 'Opp'),
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
            ('R6', '2', 'J1', 'A1', w_pwr, (Dird, 90, ([(1.1, 90)], -45))),
            ('R7', '2', 'J1', 'B1', w_pwr, (Dird, 90, ([(1.1, 90)], +45))),
            ('R6', '2', 'J1', 'S1', w_pwr, (Dird, 90, 90)),
            ('R7', '2', 'J1', 'S2', w_pwr, (Dird, 90, 90)),
            # sbu = LED
            ('J1', via_splt_sb1, 'J1', 'A8', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_sb2, 'J1', 'B8', 0.3, (Dird, 0, 90)),
            ('J1', via_splt_sb1, 'J1', via_splt_sb2, 0.4, (Dird, 0, -45, -0.6), 'Opp'),
        ] )

    # mcu & expander
    if board == BDL:# mcu
        via_vcc_mcu = kad.add_via_relative( 'U1', '1', (+5.6, +1.1), VIA_Size[0] )
        via_vcca1  = kad.add_via_relative( 'C5', '1', (-1.4, 0), VIA_Size[1] )
        via_vcca5  = kad.add_via_relative( 'C5', '1', (-4.8, 0), VIA_Size[1] )
        via_vcc_c4 = kad.add_via_relative( 'C4', '1', (-1.6, 0), VIA_Size[0] )
        via_gnd_c5 = kad.add_via_relative( 'C5', '2', (0, -2.0), VIA_Size[0] )
        pos, angle = kad.get_mod_pos_angle( 'J1' )
        via_sda_j1 = kad.add_via( vec2.mult( mat2.rotate( angle ), (-3.0, -26), pos ), kad.get_pad_pos_net( 'J1', 'B7' )[1], VIA_Size[1] )
        via_scl_j1 = kad.add_via( vec2.mult( mat2.rotate( angle ), (-2.0, -26), pos ), kad.get_pad_pos_net( 'J1', 'B6' )[1], VIA_Size[1] )
        via_rdi_j1 = kad.add_via( vec2.mult( mat2.rotate( angle ), (-0.4, -26), pos ), kad.get_pad_pos_net( 'J1', 'A8' )[1], VIA_Size[1] )
        kad.wire_mods( [
            # pass caps
            ('C4', '1', 'C4', via_vcc_c4, w_pwr, (Dird, 0, 90, -0)),
            ('U1', '17', 'C4', '1', w_mcu, (Dird,  0, 90, r_mcu)),
            ('C4', '2', 'U1', '16', w_mcu, (Dird,  0, 90, r_mcu)),
            ('C3', '1', 'U1',  '1', w_mcu, (Dird, 90, 90, r_mcu)),
            ('C3', '2', 'U1', '32', w_mcu, (Dird, 90, 90, r_mcu)),
            ('C3', '2', 'C5', '2',  w_pwr, (Dird, 90,  0, r_pwr)),
            # VCCA
            ('U1', '5', 'C5', via_vcca5, w_mcu, (Dird, 0, 0, r_mcu)),
            ('C5', '1', 'C5', via_vcca1, w_pwr, (Strt)),
            ('C5', via_vcca1, 'C5', via_vcca5, w_pwr, (Strt), 'B.Cu'),
            ('U1', via_vcc_mcu, 'U1', '5', w_mcu, (Dird, ([(0.4, 0)], 90), 0, r_mcu), 'F.Cu'),
            # VCC
            ('U1', '1', 'U1', via_vcc_mcu, w_mcu, (Dird, ([(0.8, 0), (0.0, -45)], -45), 0, -0)),
            ('U1', via_vcc_mcu, 'U1', via_vcc_c4, w_pwr, (Dird, ([(1.2, 0)], 90), 0, r_pwr), 'B.Cu'),
            # GND
            ('U1', '16', 'U1', '32', w_mcu, (Dird, 90, ([(0.8, -90), (0.8, -45)], 0), -0)),
            ('C5', '2', 'C5', via_gnd_c5, w_pwr, (Strt)),
            # USB DP/DM
            ('U1', '21', 'R4', '2', w_mcu, (Dird, ([(5.4, 0)], -30), ([(0.4, -90), (0, 0)], 0), r_mcu)),
            ('U1', '22', 'R5', '2', w_mcu, (Dird, ([(6.0, 0)], -30), ([(0.4, +90), (0, 0)], 0), r_mcu)),
            # I2C
            ('U1', '2', 'U1', via_sda_j1, w_mcu, (Dird, 0, angle_SW82, r_mcu)),
            ('U1', '3', 'U1', via_scl_j1, w_mcu, (Dird, 0, angle_SW82, r_mcu)),
            ('U1', via_sda_j1, 'R2', '1', w_mcu, (Dird, angle_SW82, ([(0.6, 135)], -90), r_mcu)),
            ('U1', via_scl_j1, 'R3', '1', w_mcu, (Dird, angle_SW82, ([(0.6, 135)], -90), r_mcu)),
        ] )
        pcb.Delete( via_sda_j1 )
        pcb.Delete( via_scl_j1 )
    if board == BDL:# Regulator
        via_vcc_c1_1 = kad.add_via_relative( 'C1', '1', (5.4, -2.0), VIA_Size[0] )
        via_vcc_c1_2 = kad.add_via_relative( 'C1', '1', (5.4, +2.0), VIA_Size[0] )
        kad.wire_mods( [
            # regulator
            ('U2', '1', 'C1', '1', w_pwr, (ZgZg, 90, 30)),# 5V
            ('U2', '3', 'C1', '2', w_pwr, (ZgZg, 90, 30, r_pwr)),# Gnd
            ('U2', '3', 'C2', '2', w_pwr, (ZgZg, 90, 30, r_pwr)),# Gnd
            ('U2', '2', 'C2', '1', w_pwr, (ZgZg, 90, 30)),# Vcc
            # C4 <--> C2
            ('C4', '1', 'C2', '1', w_pwr, (Dird, 90, 90, r_pwr)),# Vcc
            ('C4', '2', 'C2', '2', w_pwr, (Dird, 90, 90, 0)),# Gnd
            # C1 5V
            ('C1', via_vcc_c1_1, 'L1', '1', w_pwr, (Dird, 90, 90, r_pwr)),
            ('C1', '1', 'C1', via_vcc_c1_1, w_pwr, (Dird, 90,  0, r_pwr)),
            ('C1', via_vcc_c1_1, 'C1', via_vcc_c1_2, w_pwr, (Strt), 'B.Cu'),
            # C1 GND
            ('C1', '2', 'R8', '2', w_pwr, (Dird, 0, ([(4.2, -90)], 0), -0)),
        ] )
    if board == BDL:# J3
        via_nrst_mcu = kad.add_via_relative( 'U1', '4', (5.0, -0.2), VIA_Size[2] )
        via_nrst_c6  = kad.add_via_relative( 'C6', '1', (-1.4, 0.0), VIA_Size[2] )
        via_swclk = kad.add_via_relative( 'U1', '24', (10.8, 1.8), VIA_Size[2] )
        via_swdio = kad.add_via_relative( 'U1', '23', (10.0, 1.8), VIA_Size[2] )
        pos, angle = kad.get_mod_pos_angle( 'U1' )
        via_rx     = kad.add_via( vec2.mult( mat2.rotate( angle ), (-0.2, 5.8), pos ), kad.get_pad_pos_net( 'U1', '9' )[1], VIA_Size[2] )
        via_tx     = kad.add_via( vec2.mult( mat2.rotate( angle ), (-1.2, 6.7), pos ), kad.get_pad_pos_net( 'U1', '8' )[1], VIA_Size[2] )
        via_led_r1 = kad.add_via( vec2.mult( mat2.rotate( angle ), (-2.2, 7.6), pos ), kad.get_pad_pos_net( 'U1', '7' )[1], VIA_Size[2] )
        via_led_d1  = kad.add_via_relative( 'D1', '2', (0, +1.6), VIA_Size[2] )
        kad.wire_mods( [
            # NRST
            ('U1', '4', 'U1', via_nrst_mcu, w_jtag, (Dird, 0, 90)),
            ('C6', '1', 'C6', via_nrst_c6, w_jtag, (Strt)),
            ('C6', '2', 'C2', '2', w_jtag, (Dird, 0, 90, 0)),
            ('U1', via_nrst_mcu, 'U1', via_nrst_c6, w_jtag, (Dird, 90, 0, r_jtag), 'B.Cu'),
            ('U1', via_nrst_mcu, 'U1', via_nrst_c6, w_jtag, (Dird, ([(8, -90)], 90), 0, r_jtag), 'B.Cu'),
            # NRST J3
            ('J3', '4', 'U1', via_nrst_mcu, w_jtag, (Dird, 45, 90, r_jtag), 'B.Cu'),
            # SWCLK/DIO
            ('U1', '24', None, via_swclk, w_jtag, (Dird, 0, -30, r_jtag)),
            ('U1', '23', None, via_swdio, w_jtag, (Dird, 0, -30, r_jtag)),
            # SWCLK/DIO J3
            ('J3', '6', 'U1', via_swclk, w_jtag, (Dird, ([(4.8, -45)], -J3_angle), -30, r_jtag), 'B.Cu'),
            ('J3', '5', 'U1', via_swdio, w_jtag, (Dird, ([(7.2, -45)], -J3_angle), -30, r_jtag), 'B.Cu'),
            # TX/RX
            ('U1', '9', None, via_rx, w_mcu, (Dird, 90, 0, r_mcu)),
            ('U1', '8', None, via_tx, w_mcu, (Dird, 90, 0, r_mcu)),
            # TX/RX J3
            ('J3', '3', 'U1', via_rx, w_jtag, (Dird, 45, 90, r_jtag), 'B.Cu'),
            ('J3', '2', 'U1', via_tx, w_jtag, (Dird, 45, 90, r_jtag), 'B.Cu'),
            # LED D1
            ('U1', '7', 'R1', '1', w_mcu, (Dird, 0, 0, r_mcu)),
            ('R1', '2', 'R1', via_led_r1, w_mcu, (Dird, 0, 90, r_mcu)),
            ('D1', '2', 'D1', via_led_d1, w_mcu, (Strt)),
            ('R1', via_led_r1, 'D1', via_led_d1, w_mcu, (Dird, 0, -90, r_mcu), 'B.Cu'),
            # LED D1 J3
            ('J3', '1', 'D1', '1', w_mcu, (Dird, 0, 0, r_mcu)),
            # GND J3
            ('C1', '2', 'J3', '1', w_pwr, (ZgZg, 0, 70, -0)),
        ] )
    if board == BDR:# mcp23017
        kad.wire_mods( [
            # pass cap
            ('U1',  '9', 'C1', '1', w_exp, (Dird, ([(1.4, 180)], -60), 90, r_exp)),
            ('U1', '10', 'C1', '2', w_exp, (Dird, ([(1.4, 180)], +60), 90, r_exp)),
            # Gnd (Address)
            ('U1', '15', 'U1', '17', w_exp, (Strt)),
            # NRST
            ('U1', '9', 'U1', '18', w_exp, (Dird, ([(4.0, 0)], 90), 0, r_exp)),
        ] )

    # wire between J1 and mcu/expander
    if board == BDL:# wire to mcu
        kad.wire_mods( [
            # I2C pull-ups
            ('J1', via_splt_vba, 'R2', '2', w_pwr, (Dird, -45, 90)),
            ('J1', via_splt_vbb, 'R3', '2', w_pwr, (Dird, +45, 90)),
            ('J1', via_splt_dmb, 'R2', '1', 0.4, (Dird, 90, ([(1.2, +90)], -45), -0.6)),
            ('J1', via_splt_dpb, 'R3', '1', 0.4, (Dird, 90, ([(1.2, -90)], +45), -0.6)),
        ] )
    elif board == BDR:# wire to expander
        via_exp_angle = 90 - angle_SW82
        pos, angle = kad.get_mod_pos_angle( 'U1' )
        via_exp_5v  = kad.add_via( vec2.mult( mat2.rotate( angle ), ( 0.0, -32.4), pos ), kad.get_pad_pos_net( 'U1', '9'  )[1], VIA_Size[2] )
        via_exp_scl = kad.add_via( vec2.mult( mat2.rotate( angle ), (-1.1, -32.8), pos ), kad.get_pad_pos_net( 'U1', '12' )[1], VIA_Size[2] )
        via_exp_sda = kad.add_via( vec2.mult( mat2.rotate( angle ), (-2.2, -33.2), pos ), kad.get_pad_pos_net( 'U1', '13' )[1], VIA_Size[2] )
        via_exp_rdi = kad.add_via( vec2.mult( mat2.rotate( angle ), (-3.3, -33.4), pos ), kad.get_pad_pos_net( 'J1', 'B8' )[1], VIA_Size[2] )
        via_exp_gnd = kad.add_via_relative( 'U1', '15', (0, 2), VIA_Size[1] )
        kad.wire_mods( [
            # Vcc = 5v
            ('J1', via_splt_vbb, 'U1', via_exp_5v, w_exp, (Dird, 90, via_exp_angle, r_exp)),
            ('U1', via_exp_5v, 'U1', '9', w_exp, (Dird, via_exp_angle, ([(4.0, 0)], -90), r_exp)),
            # GND
            ('J1', 'S2', 'U1', via_exp_gnd, w_exp, (Dird, ([(1.4, 0)], 90), 0, r_exp)),
            ('U1', '15', 'U1', via_exp_gnd, w_exp, (Strt)),
            # dm/dp = I2C SDA, SCL
            ('J1', via_splt_dpb, 'U1', via_exp_scl, w_exp, (Dird, 90, via_exp_angle, r_exp)),
            ('J1', via_splt_dmb, 'U1', via_exp_sda, w_exp, (Dird, 90, via_exp_angle, r_exp)),
            ('U1', via_exp_scl, 'U1', '12', w_exp, (Dird, via_exp_angle, ([(3.2, 0)], -90), r_exp)),
            ('U1', via_exp_sda, 'U1', '13', w_exp, (Dird, via_exp_angle, ([(2.4, 0)], -90), r_exp)),
            # RDI SBU1 / SBU2
            ('U1', via_exp_rdi, 'J1', via_splt_sb2, 0.4, (Dird, via_exp_angle, ([(0.8, 135), (1.6, 90), (0.8, 45)], 90), r_exp), 'B.Cu'),
        ] )
        pcb.Delete( via_exp_5v )
        pcb.Delete( via_exp_scl )
        pcb.Delete( via_exp_sda )

    # Debounce
    via_dbn_vccs = {}
    via_dbn_gnds = {}
    if board in [BDL, BDR]:# vias and wires within
        for cidx in range( 1, [10, 9][board] ):
            col = str( cidx )
            # wire islands
            mod_cap = 'C' + col + '1'
            mod_r1 = 'R' + col + '1'
            mod_r2 = 'R' + col + '2'
            kad.wire_mods( [
                (mod_r1, '2', mod_r2,  '2', w_dbn, (Strt)),
                (mod_r1, '1', mod_cap, '1', w_dbn, (Strt)),
            ] )
            if board == BDR and cidx == 8:
                continue
            # Vcc vias
            if cidx in [8]:
                pos_vcc = (0, -1.6)
            else:
                pos_vcc = (0, -3.2)
            # GND vias
            if board == BDL and cidx == 4:
                pos_gnd = (-1.6, -2.0)
            elif board == BDR and cidx == 5:
                pos_gnd = (-1.6, +4.0)
            elif cidx in [8]:
                pos_gnd = (0, +1.6)
            else:
                pos_gnd = (0, +2.0)
            # Gnd, Vcc via and wire
            via_dbn_gnds[col] = kad.add_via_relative( mod_r2,  '1', pos_gnd, VIA_Size[1] )
            via_dbn_vccs[col] = kad.add_via_relative( mod_cap, '2', pos_vcc, VIA_Size[1] )
            kad.wire_mods( [
                (mod_r2,  '1', mod_r2,  via_dbn_gnds[col], w_pwr, (Dird, 0, 90, r_pwr)),
                (mod_cap, '2', mod_cap, via_dbn_vccs[col], w_pwr, (Dird, 90, 0, r_pwr)),
            ] )
    if board in [BDL, BDR]:# row wires for Vcc/Gnd
        sign_LR = [+1, -1][board]
        prm_gnd_right = ([(4, 90), (0, 90), (6.8, 0), (2.8, 40)], 0)
        prm_vcc_offset = (0.4, 90)
        for cidx in range( 0, 7 ):
            if board == BDR and cidx == 0:
                continue
            ccurr = '9' if cidx == 0 else str( cidx )
            cnext = str( cidx + 1 )
            # Vcc
            if cidx in [0]:# '9'
                prm_vcc = (Dird, 90, ([prm_vcc_offset], 0), r_pwr)
            elif cidx in [1, 5]:
                prm_vcc = (Dird, ([prm_vcc_offset, ([1, 0][board], 0)], 0), 90, r_pwr)
            elif cidx in [3, 6]:
                prm_vcc = (Dird, ([prm_vcc_offset, (sign_LR * 0.6, 0)], 0), 90, r_pwr)
            elif cidx in [2]:
                prm_vcc = (Dird, ([prm_vcc_offset, (sign_LR * 0.6, 0)], 0), ([prm_vcc_offset], 0), r_pwr)
            elif cidx in [4]:
                if board == BDL:
                    prm_vcc = (Dird, ([prm_vcc_offset, (1, 0), (3.5, 180)], -45 + angle_M - angle_PB), ([prm_vcc_offset], 0), r_pwr)
                else:# BDR
                    prm_vcc = (Dird, ([prm_vcc_offset, (1, 180)], 0), ([prm_vcc_offset, (1, 180)], 45), r_pwr)
            # GND
            if board == BDL:
                if cidx in [0, 1, 2]:
                    prm_gnd = (Dird, 90, prm_gnd_right, r_pwr)
                elif cidx in [3]:
                    prm_gnd = (Dird, 90, ([(8.4, 0), (2.8, 40)], 0), r_pwr)
                elif cidx in [4]:
                    prm_gnd = (Dird, ([(2.6, 90)], -45 + angle_M - angle_PB), prm_gnd_right, r_pwr)
                elif cidx in [5]:
                    prm_gnd = (Dird, ([(4, 90)], 0), 90, -0)
                elif cidx in [6]:
                    prm_gnd = (Dird, 90, ([(4, 90), (6.8, 0), (2.8, 40)], 0), r_pwr)
            else:# BDR
                if cidx in [1, 2, 3]:
                    prm_gnd = (Dird, prm_gnd_right, 90, r_pwr)
                elif cidx in [4]:
                    prm_gnd = (Dird, ([(4, 90), (0, 90), (6.8, 0)], 40), angle_M - angle_PB, r_pwr)
                elif cidx in [5]:
                    prm_gnd = (Dird, ([(4.0, angle_M - angle_PB), (9.4, 40 + angle_PB)], 0), 90, r_pwr)
                elif cidx in [6]:
                    prm_gnd = (Strt)
            kad.wire_mods( [
                ('C' + ccurr + '1', via_dbn_vccs[ccurr], 'C' + cnext + '1', via_dbn_vccs[cnext], w_pwr, prm_vcc, layer2),
                ('R' + ccurr + '2', via_dbn_gnds[ccurr], 'R' + cnext + '2', via_dbn_gnds[cnext], w_pwr, prm_gnd, layer2),
            ] )
    if board in [BDL, BDR]:# wires for column diodes
        for cidx in range( 1, 9 ):
            if cidx == 8 and board == BDR:
                continue
            col = str( cidx )
            mod_r2 = 'R' + col + '2'
            mod_dio = 'D' + col + ('2' if cidx in [6, 8] else '1')
            prm = None
            if cidx == 6:
                if board == BDL:
                    prm = (Dird, 90, ([(1.6, 90), (11, 0)], 90), r_dbn)
                else:# BDR:
                    prm = (Dird, 90, ([(1.6, 90)], 0), r_dbn)
            else:
                prm = (Dird, 90, 90, r_dbn)
            if prm:
                kad.wire_mods( [
                    (mod_r2, '2', mod_dio, '1', w_dbn, prm),
                ] )
    if board == BDL:# Col8, Col9, mcu, J1
        kad.wire_mods( [
            # Vcc from mcu
            ('U1', via_vcca5, 'C81', via_dbn_vccs['8'], w_pwr, (Dird, 0, -angle_SW82, r_pwr), 'B.Cu'),
            ('U1', via_vcca1, 'C21', via_dbn_vccs['2'], w_pwr, (Dird, 90, ([(3, 90)], -60), r_pwr), 'B.Cu'),
            # Gnd from mcu, J1
            ('J1', 'S2', 'R82', '1', w_pwr, (Dird, ([(1.6, 0)], 90), 90, r_pwr), ('F.Cu')),
            ('C5', via_gnd_c5, 'R82', via_dbn_gnds['8'], w_pwr, (Dird, 90, -angle_SW82, r_pwr), ('B.Cu')),
            ('C5', via_gnd_c5, 'R92', via_dbn_gnds['9'], w_pwr, (Dird, 90, ([(4, 0)], 90), r_pwr), ('B.Cu')),
        ] )
    if board == BDR:# Col8, Col1, expander, J1
        # Col8
        via_c1_vcc_1 = kad.add_via_relative( 'C1', '1', (0, +2), VIA_Size[0] )
        via_c1_vcc_2 = kad.add_via_relative( 'C1', '1', (4, +2), VIA_Size[0] )
        kad.wire_mods( [
            # Vcc
            ('C1', '1', 'C1', via_c1_vcc_1, w_pwr, (Strt)),
            ('C1', via_c1_vcc_1, 'C1', via_c1_vcc_2, w_pwr, (Strt), 'F.Cu'),
            ('C1', via_c1_vcc_2, 'C81', '2', w_pwr, (Dird, ([(8, 45)], 0), 90, r_pwr), 'B.Cu'),
            ('J1', via_splt_vba, 'C81', '2', w_pwr, (Dird, 90, ([(1.4, 0)], 90), r_pwr)),
            # GND
            ('R82', '1', 'C1', '2', w_pwr, (Dird, ([(1.6, 180)], 90), ([(3.4, -90), (4, 0), (6, 45)], 0), -0)),
            ('R82', '1', 'J1', 'S1', w_pwr, (Dird, 90, ([(5.8, 180)], 90), -0)),
        ] )
        # Col1
        via_dbn_vcc_j1 = kad.add_via_relative( 'J1', 'B4', (+0.4, -9.8), VIA_Size[0] )
        kad.wire_mods( [
            # Vcc
            ('J1', via_splt_vbb, 'J1', via_dbn_vcc_j1, w_pwr, (Strt), 'B.Cu'),
            ('J1', via_dbn_vcc_j1, 'C11', via_dbn_vccs['1'], w_pwr, (Dird, 0, ([(prm_vcc_offset)], 0), r_pwr), 'F.Cu'),
            # GND
            ('J1', 'S2', 'R12', via_dbn_gnds['1'], w_pwr, (Dird, ([(1.4, 0)], 90), ([(1.4, 180)], 90), r_pwr), 'B.Cu'),
        ] )
    if board == BDR:# Col9, Col8
        via_col8_r82  = kad.add_via_relative( 'R82', '2', ( 0, 1.6),   VIA_Size[2] )
        via_col8_col9 = kad.add_via_relative( 'D91', '1', (12.0, 6.0), VIA_Size[2] )
        via_col8_sw82 = kad.add_via_relative( 'R82', '2', (-4, 1.6),   VIA_Size[2] )
        kad.wire_mods( [
            ('R82', '2', 'R82', via_col8_r82, w_dbn, (Strt)),
            ('R82', via_col8_r82, 'R82', via_col8_sw82, w_dbn, (Strt), 'F.Cu'),
            ('D91', '1', 'D91', via_col8_col9, w_dbn, (Dird, ([(1.6, -90), (2.0, 0), (3.2, -30)], 0), -45, r_dbn)),
            ('D91', via_col8_col9, 'R82', via_col8_r82, w_dbn, (Dird, -45, ([(11.4, -90 + angle_SW82)], angle_SW82), r_dbn), 'F.Cu'),
            ('R82', via_col8_sw82, 'D82', '1', w_dbn, (Dird, ([(1.0, 180), (6.0, 90), (2.4, 135), (5.0, 180)], 45), ([(2.0, -90)], 0), r_dbn)),
        ] )

    # COL lines
    if board in [BDL, BDR]:# vertical wires
        sign_LR = [+1, -1][board]
        col_dio_offset = (1.6, 90)
        for cidx in range( 1, 9 ):
            col = str( cidx )
            mod_dio = 'D' + col
            for ridx in range( 1, 4 ):
                row = str( ridx )
                prm_col = None
                if cidx == 8:# thumb's row
                    if ridx == 2:
                        if board == BDL:
                            prm_col = (Dird, 0, ([col_dio_offset, (0, 0)], 0), r_col)
                        else:# BDR
                            prm_col = (Dird, ([col_dio_offset], 0), ([col_dio_offset, (0, 0)], 0), r_col)
                    elif ridx == 3:
                        prm_col = (Dird, ([col_dio_offset, (0, 0)], 0), ([col_dio_offset], 0), r_col)
                else:
                    # default
                    idx_curr = col + str( ridx )
                    idx_next = col + str( ridx + 1 )
                    if idx_curr not in keys.keys() or idx_next not in keys.keys():
                        continue
                    pos_curr, angle_curr = kad.get_mod_pos_angle( 'SW' + idx_curr )
                    pos_next, _          = kad.get_mod_pos_angle( 'SW' + idx_next )
                    sign_col = +1 if vec2.dot( vec2.sub( pos_curr, pos_next ), vec2.rotate( -angle_curr ) ) > 1.6 else -1
                    prm_col = (Dird, 180, ([col_dio_offset, (7.4, 0)], [None, 30, 45, 45][ridx] * sign_col), r_col)
                    # overwrite
                    if cidx == 5 and ridx == 1:
                        prm_col = (Dird, [180, 90][board], ([col_dio_offset], 0), r_col)
                    elif cidx == 7 and ridx == 1:
                        prm_col = (Dird, 180, ([col_dio_offset, ([7.4, 6.0][board], 0), (4, - sign_LR * 45)], -90), r_col)
                if prm_col:
                    kad.wire_mods( [(mod_dio + row, '1', mod_dio + str( ridx + 1 ), '1', w_col, prm_col)] )
    if board == BDL:# SW91
        kad.wire_mods( [
            ('R92', '2', 'SW91', '2', w_col, (Dird, 90, 0, r_col)),# 91
            ('C91', '2', 'SW91', '1', w_col, (Dird, ([(1.6, 0)], 90), 0, r_col)),# 91
        ] )
    if board == BDL:# horizontal wires to mcu
        # right col vias
        via_col6_1 = kad.add_via_relative( 'U1', '20', (2.0, 0.2), VIA_Size[2] )
        via_col7_1 = kad.add_via_relative( 'U1', '19', (3.0, 0.4), VIA_Size[2] )
        via_col6_2 = kad.add_via_relative( 'U1', '20', (1.8 + 6.4, 0.2 - 6.4), VIA_Size[2] )
        via_col7_2 = kad.add_via_relative( 'U1', '19', (2.6 + 6.4, 0.4 - 6.4), VIA_Size[2] )
        # Thumb vias
        via_col8_1 = kad.add_via_relative( 'U1',  '6', (-3, 0),   VIA_Size[2] )
        via_col8_2 = kad.add_via_relative( 'C81', '1', (0, -3.8), VIA_Size[2] )
        # wire to mcu
        kad.wire_mods( [
            ('C91', '1', 'U1', '31', w_mcu, (Dird, 90, ([(4.2, 90), (7.8, 180), (6.2, -150)], 0), r_col)),# BOOT0
            ('C11', '1', 'U1', '30', w_mcu, (Dird, 90, ([(5.0, 90), (9.0, 180), (6.0, -150)], 0), r_col)),
            ('C21', '1', 'U1', '29', w_mcu, (Dird, 90, ([(5.8, 90)], 0), r_col)),
            ('C31', '1', 'U1', '27', w_mcu, (Dird, 90, ([(5.8, 90)], 0), r_col)),
            ('C41', '1', 'U1', '26', w_mcu, (Dird, 90, ([(5.0, 90)], 0), r_col)),
            ('C51', '1', 'U1', '25', w_mcu, (Dird, ([(4.4, 90), (12.2, 0)], -45), ([(4.2, 90)], 0), r_col)),
            # right cols
            ('U1', '20', 'U1', via_col6_1, w_mcu, (Dird, 0, -45, r_col)),
            ('U1', '19', 'U1', via_col7_1, w_mcu, (Dird, ([(1.1, 0)], -45), 0, r_col)),
            ('U1', via_col6_1, 'U1', via_col6_2, w_mcu, (Strt), 'B.Cu'),
            ('U1', via_col7_1, 'U1', via_col7_2, w_mcu, (Strt), 'B.Cu'),
            ('C61', '1', 'U1', via_col6_2, w_mcu, (Dird, ([(4.4, 90), (8, 0), (1.2, 45), (12.6, 0), (3.2, -45)], 0), 45, r_col)),
            ('C71', '1', 'U1', via_col7_2, w_mcu, (Dird, ([(4.4, 90), (16.6, 0), (1.2, 45), (7.4, 0), (1.2, 45), (13.6, 0), (3.2, -45)], 0), 45, r_col)),
            # Thumb
            ('C81', '1', 'U1', via_col8_2, w_col, (Dird, 90, 90)),
            ('U1', via_col8_1, 'U1', via_col8_2, w_col, (Dird, 0, 90, r_col), 'B.Cu'),
            ('U1', '6', 'U1', via_col8_1, w_mcu, (Strt)),
        ] )
    elif board == BDR:# horizontal wires to expander
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'SW41', '1' )
        via_col5_tmp = kad.add_via( vec2.mult( mat2.rotate( angle ), (0, -2.8), pos ), kad.get_pad_pos_net( 'U1', '26' )[1], VIA_Size[2] )
        via_col6_tmp = kad.add_via( vec2.mult( mat2.rotate( angle ), (0, -3.6), pos ), kad.get_pad_pos_net( 'U1', '27' )[1], VIA_Size[2] )
        via_col7_tmp = kad.add_via( vec2.mult( mat2.rotate( angle ), (0, -4.4), pos ), kad.get_pad_pos_net( 'U1', '28' )[1], VIA_Size[2] )
        # Thumb vias
        via_col8_1 = kad.add_via_relative( 'U1', '21', (+2, 0.2), VIA_Size[2] )
        via_col8_2 = kad.add_via_relative( 'C81', '1', (0, -6.0), VIA_Size[2] )
        # wire to expander
        kad.wire_mods( [
            ('C11', '1', 'U1', '22', w_exp, (Dird, 90, ([(3.2, 0), (11, -90), (4, -120)], 90), r_col)),
            ('C21', '1', 'U1', '23', w_exp, (Dird, 90, ([(4.0, 0), (12, -90), (4, -120)], 90), r_col)),
            ('C31', '1', 'U1', '24', w_exp, (Dird, ([(4.4, 90)],   0), 0, r_col)),
            ('C41', '1', 'U1', '25', w_exp, (Dird, ([(4.6, 90)], 100), 0, r_col)),
            ('C41', via_col5_tmp, 'U1', '26', w_exp, (Dird, 0, ([(6.8, 0)], 45), r_col)),
            ('C41', via_col6_tmp, 'U1', '27', w_exp, (Dird, 0, ([(6.2, 0)], 45), r_col)),
            ('C41', via_col7_tmp, 'U1', '28', w_exp, (Dird, 0, ([(5.6, 0)], 45), r_col)),
            ('C51', '1', 'C41', via_col5_tmp, w_exp, (Dird, ([(2.2, 180)], 45), 0, r_col)),
            ('C61', '1', 'C41', via_col6_tmp, w_exp, (Dird, ([(4.6, 90), (16.0, 180)], 45), 0, r_col)),
            ('C71', '1', 'C41', via_col7_tmp, w_exp, (Dird, ([(5.4, 90), (25.0, 180)], 45), 0, r_col)),
            # Thumb
            ('U1', '21', 'U1', via_col8_1, w_exp, (Dird, 0, 90, r_exp)),
            ('C81', '1', 'U1', via_col8_2, w_col, (Dird, 90, 90)),
            ('U1', via_col8_1, 'C81', via_col8_2, w_col, (Dird, ([(0.2, -90), (6.6, 180)], 60), ([(2, 90)], 90 + angle_SW82), r_col), 'F.Cu'),
        ] )
        pcb.Delete( via_col5_tmp )
        pcb.Delete( via_col6_tmp )
        pcb.Delete( via_col7_tmp )

    # ROW lines
    if board in [BDL, BDR]:# horizontal wires
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
                    if board == BDL:
                        dx = [None, 2.4, 3.6, 6.4, 6.4][ridx]
                        angle = [None, 45, 60, 60, 60][ridx]
                        prm_row = (Dird, 0, ([(dx, 180)], angle), r_row)
                    else:# BDR
                        if ridx == 1:
                            prm_row = (Dird, 0, ([(8.4, 0)], 135), r_row)
                        else:
                            prm_row = (Dird, 0, -50, r_row)
                elif cidx in [5, 6]:
                    if ridx == 1:
                        prm_row = (Dird, 90, 0, r_row)
                    else:
                        if board == BDL:
                            prm_row = (Dird, ([(3, 0)], 30), 0, r_row)
                        else:# BDR
                            prm_row = (Dird, ([(4.2, 180)], 150), 0, r_row)
                kad.wire_mods( [
                    ('SW'+idx, '1', 'SW'+nidx, '1', w_row, prm_row, layer2),
                ] )
    if board == BDR:# SW91
        kad.wire_mods( [
            ('SW91', '1', 'SW11', '1', w_row, (Dird, -45, 0, r_row), layer2),
        ] )
    if board == BDL:# Row to mcu
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'SW21', '1' )
        via_row4_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (11.6, +5.0), pos ), kad.get_pad_pos_net( 'U1', '12' )[1], VIA_Size[2] )
        via_row3_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (12.8, +7.0), pos ), kad.get_pad_pos_net( 'U1', '11' )[1], VIA_Size[2] )
        via_row2_top = kad.add_via( vec2.mult( mat2.rotate( angle ), (14.0, +9.0), pos ), kad.get_pad_pos_net( 'U1', '10' )[1], VIA_Size[2] )
        kad.wire_mods( [
            ('SW34', '1', 'SW21', via_row4_top, w_row, (Dird, ([(5.0, 180), (3.6, 135)], 90), 90, r_row), 'F.Cu'),# Row4
            ('SW33', '1', 'SW21', via_row3_top, w_row, (Dird, ([(3.8, 180), (3.2, 135)], 90), 90, r_row), 'F.Cu'),# Row3
            ('SW32', '1', 'SW21', via_row2_top, w_row, (Dird, ([(2.0, 180), (2.6, 135)], 90), 90, r_row), 'F.Cu'),# Row2
            ('SW31', '1', 'U1', '28', w_mcu, (Dird, 0, 90, r_mcu), 'F.Cu'),# Row1
        ])
        # Thumb Rows to mcu
        via_row2_btm = kad.add_via_relative( 'U1', '10', (-0.6, -2.8), VIA_Size[2] )
        via_row3_btm = kad.add_via_relative( 'U1', '11', (-0.2, -2.2), VIA_Size[2] )
        via_row4_btm = kad.add_via_relative( 'U1', '12', (+0.2, -1.6), VIA_Size[2] )
        kad.wire_mods( [
            ('SW31', via_row2_top, 'U1', via_row2_btm, w_row, (Dird, 10, 90, r_row), layer2),# Row2
            ('SW31', via_row3_top, 'U1', via_row3_btm, w_row, (Dird, 10, 90, r_row), layer2),# Row3
            ('SW31', via_row4_top, 'U1', via_row4_btm, w_row, (Dird, 10, 90, r_row), layer2),# Row4
            ('U1', '10', 'U1', via_row2_btm, w_mcu, (ZgZg, 90, 45, r_row)),# Row2
            ('U1', '11', 'U1', via_row3_btm, w_mcu, (Dird, 90,  0, r_row)),# Row3
            ('U1', '12', 'U1', via_row4_btm, w_mcu, (Dird, 90,  0, r_row)),# Row4
            ('SW82', '1', 'U1', via_row2_btm, w_row, (Dird, ([(6.4, 180)],  90), 50, r_row), layer2),# Row2
            ('SW83', '1', 'U1', via_row3_btm, w_row, (Dird, ([(4.6, 180)], 110), 50, r_row), layer2),# Row3
            ('SW84', '1', 'U1', via_row4_btm, w_row, (Dird, ([(8.0, 180), (22.4, 110)], 130), 50, r_row), layer2),# Row4
        ])
    elif board == BDR:# Row to expander
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'SW21', '1' )
        via_row2_mid = kad.add_via( vec2.mult( mat2.rotate( angle ), (-7.2, 14), pos ), kad.get_pad_pos_net( 'U1', '4' )[1], VIA_Size[2] )
        via_row3_mid = kad.add_via( vec2.mult( mat2.rotate( angle ), (-8.2, 14), pos ), kad.get_pad_pos_net( 'U1', '3' )[1], VIA_Size[2] )
        via_row4_mid = kad.add_via( vec2.mult( mat2.rotate( angle ), (-9.2, 14), pos ), kad.get_pad_pos_net( 'U1', '2' )[1], VIA_Size[2] )
        # Thumb Rows to mcu
        via_row1_top = kad.add_via_relative( 'U1', '5', (+3.8 + 13 + 0.0, +10.8), VIA_Size[2] )
        via_row2_top = kad.add_via_relative( 'U1', '4', (+3.2 + 13 + 1.6, +10.2), VIA_Size[2] )
        via_row3_top = kad.add_via_relative( 'U1', '3', (+2.6 + 13 + 3.2, +9.6), VIA_Size[2] )
        via_row4_top = kad.add_via_relative( 'U1', '2', (+2.0 + 13 + 4.8, +9.0), VIA_Size[2] )
        via_row1_btm = kad.add_via_relative( 'U1', '5', (+3.2, +0.9), VIA_Size[2] )
        via_row2_btm = kad.add_via_relative( 'U1', '4', (+2.8, +0.3), VIA_Size[2] )
        via_row3_btm = kad.add_via_relative( 'U1', '3', (+2.4, -0.3), VIA_Size[2] )
        via_row4_btm = kad.add_via_relative( 'U1', '2', (+2.0, -0.9), VIA_Size[2] )
        # wires
        kad.wire_mods( [
            ('SW24', '1', 'SW21', via_row4_mid, w_row, (Dird, ([(3.0, 180), (16, 90)], 60), 90, r_row), 'B.Cu'),# Row4
            ('SW23', '1', 'SW21', via_row3_mid, w_row, (Dird,  0, 90, r_row), 'B.Cu'),# Row3
            ('SW22', '1', 'SW21', via_row2_mid, w_row, (Dird,  0, 90, r_row), 'B.Cu'),# Row2
            ('SW21', '1', 'SW31', via_row1_top, w_row, (Dird, 115, 0, r_row), 'B.Cu'),# Row1
            #
            ('SW31', via_row2_mid, 'SW31', via_row2_top, w_row, (Dird, ([(3.0, 106)], 90), 0, r_row), 'B.Cu'),# Row2
            ('SW31', via_row3_mid, 'SW31', via_row3_top, w_row, (Dird, ([(3.0, 106)], 90), 0, r_row), 'B.Cu'),# Row3
            ('SW31', via_row4_mid, 'SW31', via_row4_top, w_row, (Dird, ([(3.0, 106)], 90), 0, r_row), 'B.Cu'),# Row4
            #
            ('U1', via_row1_top, 'U1', via_row1_btm, w_row, (Dird, 96.4, 0, r_row), layer2),# Row1
            ('U1', via_row2_top, 'U1', via_row2_btm, w_row, (Dird, 96.4, 0, r_row), layer2),# Row2
            ('U1', via_row3_top, 'U1', via_row3_btm, w_row, (Dird, 96.4, 0, r_row), layer2),# Row3
            ('U1', via_row4_top, 'U1', via_row4_btm, w_row, (Dird, 96.4, 0, r_row), layer2),# Row4
            ('U1', '5', 'U1', via_row1_btm, w_exp, (Dird, 0, ([(0.5, 180)], -45), r_row)),# Row1
            ('U1', '4', 'U1', via_row2_btm, w_exp, (Dird, 0, -60, r_row)),# Row2
            ('U1', '3', 'U1', via_row3_btm, w_exp, (Dird, 0, +60, r_row)),# Row3
            ('U1', '2', 'U1', via_row4_btm, w_exp, (Dird, 0, +90, r_row)),# Row4
            ('SW82', '1', 'U1', via_row2_btm, w_row, (Dird, 90, -120, r_row), layer2),# Row2
            ('SW83', '1', 'U1', via_row3_btm, w_row, (Dird, ([(4.6, 0)], 70), ([(16, -120)], 45), r_row), layer2),# Row3
            ('SW84', '1', 'U1', via_row4_btm, w_row, (Dird, ([(8.0, 0), (22.6, 70)], 50), ([(16, -120)], 45), r_row), layer2),# Row4
        ])
        pcb.Delete( via_row2_mid )
        pcb.Delete( via_row3_mid )
        pcb.Delete( via_row4_mid )

    # J2: USB (PC) connector
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
            # gnd
            ('J2', 'S1', 'J2', 'S2', w_pwr, (Dird, ([(0.8, 45)], 0), -45), 'Opp'),
            ('J2', 'S2', 'J2', 'S3', w_pwr, (Strt)),
            ('J2', 'S2', 'J2', 'S3', w_pwr, (Strt), 'Opp'),
            ('J2', 'S1', 'J2', 'S4', w_pwr, (Strt)),
            ('J2', 'S1', 'J2', 'S4', w_pwr, (Strt), 'Opp'),
            # vbus
            ('J2', via_usb_vba, 'J2', 'A4', w_pwr, (Dird, +60, ([(1.6, 90), (0.5, 135)], 90))),
            ('J2', via_usb_vbb, 'J2', 'B4', w_pwr, (Dird, -60, ([(1.6, 90), (0.5,  45)], 90))),
            ('J2', via_usb_vba, 'J2', via_usb_vbb, w_pwr, (Strt), 'Opp'),
            # dm/dp
            ('J2', via_usb_dpa, 'J2', 'A6', 0.3, (Dird, 90, ([(2.4, 90)], -45), -0.2)),
            ('J2', via_usb_dpb, 'J2', 'B6', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dpa, 'J2', via_usb_dpb, 0.4, (Strt), 'Opp'),
            ('J2', via_usb_dma, 'J2', 'A7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dmb, 'J2', 'B7', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_dma, 'J2', via_usb_dmb, 0.4, (Dird, 90, 0), 'Opp'),
            # cc1/2
            ('J2', via_usb_cc1, 'J2', 'A5', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_cc2, 'J2', 'B5', 0.3, (Dird, 0, 90)),
            ('J2', via_usb_cc1, 'J2', via_r8_cc1, 0.4, (Dird, -45, 0, -0.6), 'Opp'),
            ('J2', via_usb_cc2, 'J2', via_r9_cc2, 0.4, (Dird, +45, 0, -0.6), 'Opp'),
            ('J2', via_r8_cc1, 'R8', '1', 0.4, (Dird, 45, 90)),
            ('J2', via_r9_cc2, 'R9', '1', 0.4, (Dird, 45, 90)),
            ('R8', '2', 'J2', 'A1', w_pwr, (Dird, 90, ([(1.1, 90)], -45))),
            ('R9', '2', 'J2', 'B1', w_pwr, (Dird, 90, ([(1.1, 90)], +45))),
            ('R8', '2', 'J2', 'S1', w_pwr, (Dird, 90, 90)),
            ('R9', '2', 'J2', 'S2', w_pwr, (Dird, 90, 90)),
        ] )
        kad.wire_mods( [
            # VBUS
            ('J2', via_usb_vba, 'F1', '1', w_pwr, (Dird, -60, 0)),
            ('F1', '2', 'L1', '2', w_pwr, (Dird, 0, 90)),
            # USV DM/DP
            ('J2', via_usb_dpb, 'R5', '1', w_mcu, (Dird, 90, -45, r_mcu)),
            ('J2', via_usb_dmb, 'R4', '1', w_mcu, (Dird, 90, +45, r_mcu)),
        ] )

    # LED D1
    if board == BDR:
        via_led_d1  = kad.add_via_relative( 'D1', '2', (+1.6, 0), VIA_Size[1] )
        via_led_r1  = kad.add_via_relative( 'R1', '2', (0, +1.6), VIA_Size[1] )
        kad.wire_mods( [
            # LED D1
            ('D1', '1', 'C1', '2', w_dat, (Dird, 90 + J3_angle, ([(5, -90)], 0), -0)),
            ('U1', '1', 'R1', '1', w_exp, (Dird, 0, 0)),
            ('D1', '2', 'D1', via_led_d1, w_dat, (Strt)),
            ('R1', '2', 'R1', via_led_r1, w_dat, (Strt)),
            ('D1', via_led_d1, 'R1', via_led_r1, w_dat, (Dird, -45, 90, r_dat), 'F.Cu'),
        ] )

    # RGB LED
    w_pwr = 0.7
    via_led_pwrSs = {}# SW 3 side
    via_led_pwrTs = {}# the other side
    via_led_datSs = {}# SW 3 side
    via_led_datTs = {}# the other side
    if board in [BDL, BDR]:# vias
        for idx in keys.keys():
            sign_led = +1 if idx in [L2R, R2L][board] else -1
            col = idx[0]
            mod_led = 'L' + idx
            mod_cap = 'CL' + idx
            if idx in [L2R, R2L][board]:
                sign = +1
                cap_pwrS, cap_pwrT = '2', '1'
                led_pwrS, led_pwrT = '3', '1'
                led_datS, led_datT = '4', '2'
            else:# R2L
                sign = -1
                cap_pwrS, cap_pwrT = '1', '2'
                led_pwrS, led_pwrT = '1', '3'
                led_datS, led_datT = '2', '4'
            # thumb column (Col8)
            if col == '8':
                # datT via
                via_led_datTs[idx] = kad.add_via_relative( mod_led, led_datT, (0, +sign * 1.5), VIA_Size[1] )
                # pwrT: cap <--> led
                r_tmp = r_dat
                if board == BDL and idx in ['83', '84']:
                    r_tmp = 0
                kad.wire_mods( [
                    (mod_cap, cap_pwrT, mod_led, led_pwrT, w_pwr, (Dird, 0, 90, r_tmp), layer1),
                ] )
            else:# other fingers
                # pwrS/T via
                via_led_pwrTs[idx] = kad.add_via_relative( mod_led, led_pwrT, (0, -sign * 1.8), VIA_Size[0] )
                dx = 0
                if board == BDL:
                    if idx in ['11', '21', '33', '42']:
                        dx = +2.4
                    elif idx in ['41', '43']:
                        dx = -1.6
                else:# BDR
                    if idx in ['53', '63']:
                        dx = +1.6
                    elif idx in ['33', '52', '54', '62', '64', '72']:
                        dx = -1.6
                via_led_pwrSs[idx] = kad.add_via_relative( mod_cap, cap_pwrS, (dx, +sign * 1.85), VIA_Size[0] )
                # datT via
                if (board == BDL and idx not in ['64', '71', '72', '73']) or (board == BDR and idx not in ['14']):
                    via_led_datTs[idx] = kad.add_via_relative( mod_led, led_datT, (-sign * 1.5, 0), VIA_Size[1] )
                kad.wire_mods( [
                    # pwrS: via <--> cap
                    (mod_cap, cap_pwrS, mod_led, via_led_pwrSs[idx], w_pwr, (Dird, 90, ([(-sign_led * 0.2, 90)], 0), r_pwr), layer1),
                    # pwrT: via <--> cap & led
                    (mod_cap, cap_pwrT, mod_cap, via_led_pwrTs[idx], w_pwr, (Dird, 0, 90), layer1),
                    (mod_led, led_pwrT, mod_led, via_led_pwrTs[idx], w_pwr, (Strt), layer1),
                ] )
            # datS via
            if board != BDL or idx not in ['14']:
                via_led_datSs[idx] = kad.add_via_relative( mod_led, led_datS, (0, -sign * 1.1), VIA_Size[1] )
            # pwrS: SW '3' <--> cap & led
            r_tmp = r_dat
            if (board == BDL and idx in ['83']):
                r_tmp = 0
            kad.wire_mods( [
                (mod_cap, cap_pwrS, 'SW' + idx, '3', w_pwr, (Dird, 90, ([(2.3, -90)], 0), r_tmp)),
                (mod_led, led_pwrS, 'SW' + idx, '3', w_pwr, (Dird, 0, 90, r_tmp), layer1),
            ] )
            # datT: led <--> via
            if idx in via_led_datTs:
                kad.wire_mods( [
                    (mod_led, led_datT, mod_led, via_led_datTs[idx], w_dat, (Strt), layer1),
                ] )
            # datS: led <--> via
            if idx in via_led_datSs:
                kad.wire_mods( [
                    (mod_led, led_datS, mod_led, via_led_datSs[idx], w_dat, (Strt), layer1),
                ] )
    if board in [BDL, BDR]:# wires for each row
        # pwrL, pwrR, data lines
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
            if nidx not in keys.keys():
                continue
            sign_led = +1 if idx in [L2R, R2L][board] else -1
            one_row1 = 1 if ridx == 1 else 0
            pwrS_offset = (sign_led * 0.20, 90)
            pwrT_offset = (sign_led * 0.55, 90)
            data_offset_via = (sign_led * 0.25, 90)
            data_offset_vert = (sign_led * 2.8, 90)
            if cidx in [1, 3] or (cidx in [5] and ridx == 1):
                prm_pwrS = (Dird, 90, ([pwrS_offset], 0), r_pwr)
                prm_pwrT = (Dird, ([pwrT_offset, (0, 0)], 90), ([pwrT_offset, (0, 0)], 0), r_pwr)
                prm_data = (Dird, 90, ([data_offset_via], 0), r_dat)
            elif cidx in [2]:
                prm_pwrS = (Dird, ([pwrS_offset], 0), ([pwrS_offset], 0), r_pwr)
                prm_pwrT = (Dird, ([pwrT_offset, (0, 0)], 0), ([pwrT_offset, (0, 0)], 0), r_pwr)
                prm_data = (Dird, ([data_offset_vert], 0), ([data_offset_via], 0), r_dat)
            elif cidx in [4]:
                dangle = angle_PB if ridx == 1 else 0
                if board == BDL:
                    prm_pwrS = (Dird, ([pwrS_offset], 0), ([pwrS_offset, (sign_led * 3.8, 0)], 120 + dangle), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset, (0, 0)], 0), ([pwrT_offset, (0, 0), (sign_led * 8.2, 0)], -120 - dangle), r_pwr)
                    prm_data = (Dird, 0, ([data_offset_via, (sign_led * 3.8, 0)], -120 - dangle), r_dat)
                else:# BDR
                    prm_pwrS = (Dird, ([pwrS_offset], 0), ([pwrS_offset, (-sign_led * (3.4 + 4.6 * one_row1), 0)], -110 - dangle), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset, (0, 0)], 0), ([pwrT_offset, (0, 0), (-sign_led * (2.2 + 2.8 * one_row1), 0)], 110 + dangle), r_pwr)
                    prm_data = (Dird, ([data_offset_vert], 0), ([data_offset_via, (sign_led * 4.0, 0)], 110 + angle_M), r_dat)
            elif cidx in [9]:
                if board == BDL:
                    prm_pwrS = (Dird, 0, ([pwrS_offset, (+sign_led * 1.5, 0)], -45), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset], 0), ([pwrT_offset, (0, 0), (+sign_led * 8.2, 0)], 45), r_pwr)
                    prm_data = (Dird, 0, ([data_offset_via, (sign_led * 3.8, 0)], 45), r_dat)
                else:# BDR
                    prm_pwrS = (Dird, 0, ([pwrS_offset, (-sign_led * 7.4, 0)], -125), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset], 0), ([pwrT_offset, (0, 0), (-sign_led * 4.4, 0)], 125), r_pwr)
                    prm_data = (Dird, ([data_offset_vert], 0), ([data_offset_via, (sign_led * 4.0, 0)], 125 - 8.5), r_dat)
            elif cidx in [5, 6]:
                if board == BDL:
                    prm_pwrS = (Dird, ([pwrS_offset, (sign_led * 7.0, 180)], 150), ([pwrS_offset], 0), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset, (0, 0), (+sign_led * 3.0, 180)], +30), ([pwrT_offset, (0, 0)], 0), r_pwr)
                    prm_data = (Dird, 90, ([data_offset_via], 0), r_dat)
                else:# BDR
                    prm_pwrS = (Dird, ([pwrS_offset, (-sign_led * 7.8, 180)], -150), ([pwrS_offset], 0), r_pwr)
                    prm_pwrT = (Dird, ([pwrT_offset, (0, 0), (-sign_led * 9.2, 180)], -30), ([pwrT_offset, (0, 0)], 0), r_pwr)
                    prm_data = (Dird, ([data_offset_vert], 0), ([data_offset_via, (sign_led * 3.6, 0)], -30), r_dat)
            kad.wire_mods( [
                # pwrT
                ('L' + idx, via_led_pwrTs[idx], 'L' + nidx, via_led_pwrTs[nidx], w_pwr, prm_pwrT),
                # pwrS
                ('CL' + idx, via_led_pwrSs[idx], 'CL' + nidx, via_led_pwrSs[nidx], w_pwr, prm_pwrS, layer2),
            ] )
            # data
            if board == BDL:
                kad.wire_mods( [
                    ('L' + idx, via_led_datTs[idx], 'L' + nidx, via_led_datSs[nidx], w_dat, prm_data),
                ] )
            else:# BDR
                kad.wire_mods( [
                    ('L' + nidx, via_led_datTs[nidx], 'L' + idx, via_led_datSs[idx], w_dat, prm_data),
                ] )
    if board in [BDL, BDR]:# wires between rows
        # Row1 --> Row2
        if board == BDL:
            prm_pwrS = (Dird, ([(1.6, 0)], 90), ([(5, -90), (2, -45), (2.4, -90), (3.4, -135)], 0), r_pwr)
            prm_pwrT = (Dird, 90, ([(6.4, 90), (4.0, 45), (3.6, 0)], 45), r_pwr)
            prm_data = (Dird, ([(1.6, 180)], 90), ([(1.6, 0), (5.2, 90), (4.0, 135)], 0), r_dat)
            kad.wire_mods( [
                ('L71', '2', 'L72', '4', w_dat, prm_data, 'F.Cu'),# data
            ] )
        else:# BDR
            prm_pwrS = (Dird, ([(-0.20, 90)], 0), ([(5, +90), (2, 135), (2.2, +90), (2, 45)], +90), r_pwr)
            prm_pwrT = (Dird, ([(2.4, +45)], 90), ([(6.4, 90), (4.0, 45), (3.6, 0)], 45), r_pwr)
            prm_data = (Dird, 90, ([(2.4, -90), (2.0, -45), (11.0, -90)], 0), r_dat)
            kad.wire_mods( [
                ('CL71', via_led_datSs['71'], 'L72', via_led_datSs['72'], w_dat, prm_data, 'F.Cu'),# data
            ] )
        kad.wire_mods( [
            ('CL11', via_led_pwrSs['11'], 'CL12', via_led_pwrTs['12'], w_pwr, prm_pwrS, layer2),
            ('CL11', via_led_pwrTs['11'], 'SW12', '3', w_pwr, prm_pwrT, layer1),
        ] )
        # Row2 --> Row3
        if board == BDL:
            prm_pwrS = (Dird, 90, ([(5, +90), (2, 135), (2.4, +90), (3.4, 45)], 0), r_pwr)
            prm_pwrT = (Dird, ([(1.5, +90)], -45), 90, r_pwr)
            prm_data = (Dird, 90, ([(4, 90)], 60), r_dat)
            kad.wire_mods( [
                ('CL12', via_led_datSs['12'], 'CL13', via_led_datSs['13'], w_dat, prm_data, layer2),# data
            ] )
        else:# BDR
            prm_pwrS = (Dird, 90, ([(5, -90), (2, -45), (2.2, -90)], -135), r_pwr)
            prm_pwrT = (Dird, 90, ([(6.4, 90), (4.0, 45), (2.6, 0)], 30), r_pwr)
            prm_data = (Dird, 90, 0, r_dat)
            kad.wire_mods( [
                ('CL12', via_led_datTs['12'], 'CL13', via_led_datTs['13'], w_dat, prm_data, layer2),# data
            ] )
        kad.wire_mods( [
            ('CL12', via_led_pwrSs['12'], 'CL13', via_led_pwrTs['13'], w_pwr, prm_pwrS, layer2),
            ('CL12', via_led_pwrTs['12'], 'SW13', '3', w_pwr, prm_pwrT, layer1),
        ] )
        # Row3 --> Row4
        if board == BDL:
            prm_pwrS = (Dird, 90, ([(5, -90), (2, -45), (2.4, -90), (3.4, -135)], 0), r_pwr)
            prm_pwrT = (Dird, ([(2.4, -90)], -60), 90, r_pwr)
            prm_data = (Dird, ([(1.6, 180), (4.0, 90), (3.6, 45)], 0), ([(5.8, 0)], 90), r_dat)
            kad.wire_mods( [
                ('L73', '2', 'L64', '4', w_dat, prm_data, 'F.Cu'),# data
            ] )
        else:# BDR
            prm_pwrS = (Dird, 90, ([(5, +90), (2, 135), (2.2, +90), (2, 45), (2.2, +90)], 135), r_pwr)
            prm_pwrT = (Dird, 90, ([(6.4, 90), (4.0, 45), (2.6, 0)], 30), r_pwr)
            prm_data = (Dird, ([(3.8, -90)], 0), ([(2.4, -90), (6.0, -45), (7.2, -90)], -30), r_dat)
            kad.wire_mods( [
                ('L73', via_led_datSs['73'], 'L64', via_led_datSs['64'], w_dat, prm_data, 'F.Cu'),# data
            ] )
        kad.wire_mods( [
            ('CL13', via_led_pwrSs['13'], 'CL14', via_led_pwrTs['14'], w_pwr, prm_pwrS, layer2),
            ('CL13', via_led_pwrTs['13'], 'SW14', '3', w_pwr, prm_pwrT, layer1),
        ] )
    if board in [BDL, BDR]:# wires for Col9 <-- J1, Col8
        pos_via = [(6.4, 11), (-8.4, -6)][board]
        net_via = kad.get_pad_pos_net( 'L84', '2' )[1]
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL83', '2' )
        via_led_83 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), net_via, VIA_Size[0])
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL84', '2' )
        via_led_84 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), net_via, VIA_Size[0])
        if board == BDL:
            via_led_91 = kad.add_via_relative( 'CL91', '1', (2.0, -11.2), VIA_Size[0])
            kad.wire_mods( [
                ('SW91', '3', 'SW91', via_led_pwrSs['91'], w_pwr, (Dird, 90, 0, r_pwr), 'B.Cu'),# GNDD
                ('J1', 'S4', 'SW91', '3', w_pwr, (Dird, 0, 90, r_pwr), 'B.Cu'),
                ('CL91', via_led_pwrTs['91'], 'CL91', via_led_91, w_pwr, (Dird, ([(5, +90), (2, 135), (2.4, +90)], 45), 0, r_pwr), 'B.Cu'),
                ('J1', via_splt_vba, 'CL91', via_led_91, w_pwr, (Dird, 0, ([(2.6, 0), (4, 90)], 120), r_pwr), 'F.Cu'),
                # data
                ('L84', via_led_datSs['84'], 'L84', via_led_84, w_dat, (Dird, ([(0.8, -90), (5, 0)], 45), 90, r_dat), layer2),
                ('L84', via_led_84, 'L83', via_led_83, w_dat, (Dird, 90, 90, r_dat), layer2),
                ('L83', via_led_83, 'L91', via_led_datSs['91'], w_dat,
                    (Dird, ([(2, 90)], 20 + angle_SW82), ([(4, -90), (1.8, -60), (9, -90)], 60), r_dat), layer2),
            ] )
        else:# BDR
            pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL91', '2' )
            kad.wire_mods( [
                # GND
                ('J1', 'S3', 'CL91', via_led_pwrTs['91'], w_pwr, (Dird, 0, ([(5.0, 0)], 90), -0), 'B.Cu'),
                # 5VD
                ('J1', via_splt_vbb, 'CL91', via_led_pwrSs['91'], w_pwr, (Dird, 0, ([(8.6, 0), (14, -90)], 45), r_pwr), 'F.Cu'),
                # data
                ('L84', via_led_datSs['84'], 'L84', via_led_84, w_dat, (Dird, ([(3.0, +90)], 180), 90, r_dat), layer2),
                ('L84', via_led_84, 'L83', via_led_83, w_dat, (Dird, 90, 90, r_dat), layer2),
                ('L83', via_led_83, 'L91', via_led_datTs['91'], w_dat,
                    (Dird, 90, ([(4, +90), (3.0, 120), (5.8, +90), (9.4, 135)], +90 - 18.1), r_dat), layer2),
            ] )
        pcb.Delete( via_led_83 )
        pcb.Delete( via_led_84 )
    if board in [BDL, BDR]:# wires for Col8 5VD
        net_via = kad.get_pad_pos_net( 'J1', 'A4')[1]
        pos_via = [(9.6, 6), (-7.6, -6)][board]
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL84', '1' )
        via_5v_84 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), net_via, VIA_Size[0])
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL83', '1' )
        via_5v_83 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), net_via, VIA_Size[0])
        if board == BDL:
            kad.wire_mods( [
                ('C1', via_vcc_c1_2, 'D0', '2', w_pwr, (Dird, 90, 0, r_pwr)),
                ('D0', '2', 'SW83', '3', w_pwr, (Dird, ([(1.6, -90)], 0), 90, r_pwr)),# 4.3V
                ('SW83', '3', 'SW84', '3', w_pwr, (Dird, 90, 90, r_pwr), layer1),
                ('SW84', '3', 'SW84', via_5v_84, w_pwr, (Dird, ([(3.0, -90), (7.8, 0)], 45), 90, r_pwr), layer2),
                ('SW84', via_5v_84, 'SW83', via_5v_83, w_pwr, (Dird, 90, 90, r_pwr), layer2),
                ('SW83', via_5v_83, 'J1', via_splt_vbb, w_pwr, (Dird, 90, 0, r_pwr), layer2),
            ] )
        else:# BDR
            kad.wire_mods( [
                ('CL82', '1', 'SW83', '3', w_pwr, (Dird, 90, 90, r_pwr), layer1),
                ('SW83', '3', 'SW84', '3', w_pwr, (Dird, 90, 90, r_pwr), layer1),
                ('SW84', via_5v_84, 'SW84', '3', w_pwr, (Dird, 90, 0, r_pwr), layer2),
                ('SW84', via_5v_84, 'SW83', via_5v_83, w_pwr, (Dird, 90, 90, r_pwr), layer2),
                ('SW83', via_5v_83, 'J1', via_splt_vba, w_pwr, (Dird, 90, 0, r_pwr), layer2),
            ] )
        pcb.Delete( via_5v_84 )
        pcb.Delete( via_5v_83 )
    if board in [BDL, BDR]:# wires for Col8 GNDD
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL84', '2' )
        pos_via = [(7.6, 10), (-9.6, -10)][board]
        via_gnd_84 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), GND, VIA_Size[0])
        pos, angle, _, _ = kad.get_pad_pos_angle_layer_net( 'CL83', '2' )
        pos_via = [(7.6, -6), (-9.6, +6)][board]
        via_gnd_83 = kad.add_via( vec2.mult( mat2.rotate( angle ), pos_via, pos ), GND, VIA_Size[0])
        prm_gnd_led_pad3 = ([(1.6, 0), (5.6, 90), (3.4, 120)], 90)
        if board == BDL:
            kad.wire_mods( [
                ('C1',   '2', 'L82', '3', w_pwr, (Dird, ([(1.6, 0)], 90), prm_gnd_led_pad3, -0), layer1),
                ('CL82', '2', 'L83', '3', w_pwr, (Dird, 90, prm_gnd_led_pad3, r_pwr), layer1),
                ('L83',  '3', 'L84', '3', w_pwr, (Dird, 90, prm_gnd_led_pad3, r_pwr), layer1),
                ('CL84', via_gnd_84, 'CL84', '2', w_pwr, (Dird, 90, ([(1.3, 90), (2.8, 0)], -45), -0)),
                ('CL84', via_gnd_84, 'CL83', via_gnd_83, w_pwr, (Dird, 90, 90, r_pwr)),
                ('J1', 'S3', 'CL83', via_gnd_83, w_pwr, (Dird, 0, 90, r_pwr), layer1),
            ] )
        else:# BDR
            kad.wire_mods( [
                ('CL82', '2', 'L83', '3', w_pwr, (Dird,  0, prm_gnd_led_pad3, r_pwr), layer1),
                ('L83',  '3', 'L84', '3', w_pwr, (Dird, 90, prm_gnd_led_pad3, r_pwr), layer1),
                ('CL84', via_gnd_84, 'CL84', '2', w_pwr, (Dird, 90, ([(1.6, 90)], 0), -0)),
                ('CL84', via_gnd_84, 'CL83', via_gnd_83, w_pwr, (Dird, 90, 90, -0)),
                ('J1', 'S4', 'CL83', via_gnd_83, w_pwr, (Dird, 0, 90, -0), layer1),
            ] )
        pcb.Delete( via_gnd_84 )
        pcb.Delete( via_gnd_83 )
    if board in [BDL, BDR]:# wires for Col8 data
        if board == BDL:
            prm_led_din_83 = ([(1.6, 90)], 60)
            prm_led_din_84 = ([(1.6, 90)], 45)
            prm_led_dout = ([(1, -45), (3.8, -90), (1, -135)], 90)
        else:# BDR
            prm_led_din_83 = ([(1.6, 90)], 20)
            prm_led_din_84 = ([(6.6, 90)], 120)
            prm_led_dout = ([(1, -45), (3.8, -90), (2.8, -135), (3.0, 180), (1.4, -135)], 90)
        kad.wire_mods( [
            ('CL82', via_led_datSs['82'], 'CL83', via_led_datTs['83'], w_dat, (Dird, prm_led_din_83, prm_led_dout, r_dat), layer2),
            ('CL83', via_led_datSs['83'], 'CL84', via_led_datTs['84'], w_dat, (Dird, prm_led_din_84, prm_led_dout, r_dat), layer2),
        ] )
    if board in [BDL, BDR]:# wires for LDI / RDI
        if board == BDL:
            via_ldi_u1 = kad.add_via_relative( 'U1', '15', (-15.0, 5.2), VIA_Size[1] )
            kad.wire_mods( [
                # LDI
                ('U1', '15', 'U1', via_ldi_u1, w_mcu, (Dird, -90, 0, r_mcu)),
                ('U1', via_ldi_u1, 'L82', via_led_datTs['82'], w_mcu, (Dird, 0, ([(1, 45), (3.8, 90), (1, 135)], 90), r_mcu), 'B.Cu'),
                # RDI
                ('U1', '14', 'U1', via_rdi_j1, w_mcu, (Dird, ([(4.4, -90), (9.4, 180)], 90), ([(6.8, angle_SW82)], 0), r_mcu), 'F.Cu'),
                ('U1', via_rdi_j1, 'J1', via_splt_sb1, 0.4, (Dird, angle_SW82, ([(0.3, 45), (2.0, 90), (0.3, 135)], 90), r_mcu), 'F.Cu'),
            ] )
            pcb.Delete( via_rdi_j1 )
        else:# BDR
            kad.wire_mods( [
                # RDI
                ('U1', via_exp_rdi, 'J1', via_splt_sb2, 0.4, (Dird, via_exp_angle, ([(0.8, 135), (1.6, 90), (0.8, 45)], 90), r_exp), 'B.Cu'),
                ('U1', via_exp_rdi, 'CL82', via_led_datTs['82'], w_dat, (Dird, via_exp_angle, ([(1, -45), (3.8, -90), (2.6, -135)], 0), r_dat), layer2),
            ] )

### Ref
def set_refs( board ):
    if board == BDL:
        refs = [
            (6.4, 90, 0, ['J1']),
            (6.4, 90, 0, ['J2']),
            (15,  -90, -90, ['J3']),
            (3,   135,   0, ['U1']),
            (2.8,   0,  90, ['U2']),
            (2.5,   0, +90, ['C1', 'C2', 'C6', 'C3', 'C5', 'R1']),
            (2.5, 180, -90, ['C4', 'R4', 'R5', 'L1', 'F1']),
            (1.8, +90,   0, ['R2', 'R6', 'R8', 'D0']),
            (1.8, -90, 180, ['R3', 'R7', 'R9', 'D1']),
        ]
    elif board == BDR:
        refs = [
            (6.4, -90, 180, ['J1']),
            (4,  -110,  90, ['U1']),
            (1.8, -90, 180, ['R6']),
            (1.8, +90,   0, ['R7', 'R1', 'C1', 'D1']),
        ]
    else:# key holes
        refs = [ (0, 0, None, ['H{}'.format( idx ) for idx in range( 1, 13 )]) ]
    # sw
    if board in [BDL, BDR]:
        for name in keys:
            refs.append( (1.6, [-90, +90][board], [180, 0][board], ['D' + name]) )
            if name in R2L:
                refs.append( (4.0, [180, 0][board], 0, ['CL' + name]) )
                refs.append( (4.3, [0, 180][board], [-90, +90][board], ['L' + name]) )
            else:
                refs.append( (4.0, [0, 180][board], 180, ['CL' + name]) )
                refs.append( (4.3, [180, 0][board], [+90, -90][board], ['L' + name]) )
    # debounce
    if board in [BDL, BDR]:
        tangle = [180, 0][board]
        for idx in range( 1, 10 ):
            name = str( idx )
            refs.append( (3.3, 180, tangle, ['C' + name + '1']) )
            refs.append( (3.3, 180, tangle, ['R{}1'.format( idx )]) )
            refs.append( (3.3, 180, tangle, ['R{}2'.format( idx )]) )
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
    else:
        pads = []
    for idx, text in enumerate( pads ):
        pos = kad.get_pad_pos( 'J3', '{}'.format( idx + 1 ) )
        pos = vec2.scale( 1.6, vec2.rotate( -90 - J3_angle ), pos )
        kad.add_text( pos, J3_angle, text, ['F.SilkS', 'B.SilkS'][board], (0.8, 0.8), 0.15,
            pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )

def main():
    # board type
    filename = pcb.GetFileName()
    m = re.search( r'/Hermit([^/])/', filename )
    if not m:
        return
    boardname = m.group( 1 )
    # print( filename, boardname )
    for bname, btype in [('L', BDL), ('R', BDR), ('T', BDT), ('B', BDB), ('M', BDM), ('S', BDS)]:
        if boardname == bname:
            board = btype
            if board in [BDL, BDR, BDM, BDS]:
                kad.add_text( (86, 2.6), 0, '  Hermit{} by orihikarna 21/05/05  '.format( bname ),
                    'F.Cu' if board != BDR else 'B.Cu', (1.2, 1.2), 0.2,
                    pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER )
            break

    for name in keys.keys():
        col = int( name[0] )
        row = int( name[1] )
        if col == 8:
            if board == BDL:
                R2L.append( name )
            elif board == BDR:
                L2R.append( name )
        else:
            if row in [1, 3]:
                L2R.append( name )
            else:
                R2L.append( name )

    drawEdgeCuts( board )

    ### zones
    zones = []
    if board in [BDL, BDR, BDM, BDS]:
        add_zone( 'GND', 'F.Cu', make_rect( (PCB_Width, PCB_Height) ), zones )
        add_zone( 'GND', 'B.Cu', make_rect( (PCB_Width, PCB_Height) ), zones )

    ###
    ### Set key positios
    ###
    GND = pcb.FindNet( 'GND' )
    sw_pos_angles = []
    for name in sorted( keys.keys() ):
        key = keys[name]
        px, py, w, h, angle = key
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
            # print( name )
            if True:# SW rectangle
                corners = []
                for pnt in make_rect( (w, h), (-w/2, -h/2) ):
                    pt = vec2.mult( mat2.rotate( angle ), pnt, sw_pos )
                    corners.append( [(pt, 0), Line, [0]] )
                kad.draw_closed_corners( corners, 'F.Fab', 0.1 )
            ## LED
            sign = [+1, -1][board]
            led_base_angle = 180 if name in [L2R, R2L][board] else 0
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
            Dx = +5.8
            Dy = -0.6 * sign
            if not (board == BDL and name == '91'):
                pos = vec2.mult( mat2.rotate( angle ), (+Dx, +Dy), sw_pos )
                kad.set_mod_pos_angle( 'D' + name, pos, angle - 90 * sign )
                # wire to SW
                kad.wire_mods( [('D' + name, '2', 'SW' + name, '2', 0.5, (Dird, 0, 0))])
            ## D0
            if board == BDL and name == '82':
                pos = vec2.mult( mat2.rotate( angle ), (-Dx, -Dy), sw_pos )
                kad.set_mod_pos_angle( 'D0', pos, angle - 90 )
                # wire to SW
                kad.wire_mods( [('D0', '1', 'SW' + name, '3', 0.5, (Dird, 0, 0))])
            ## GND Vias
            if name[0] not in ['1', '8', '9'] and name[1] not in ['1']:
                if board != BDR or name[0] != '7':
                    pos = vec2.mult( mat2.rotate( angle ), (-5, 0), sw_pos )
                    kad.add_via( pos, GND, VIA_Size[1] )

    # draw top & bottom patterns
    if board in [BDT, BDB, BDS]:
        draw_top_bottom( board, sw_pos_angles )

    set_refs( board )
    # return

    # place & route
    place_mods( board )
    if board in [BDL, BDR]:
        wire_mods( board )


if __name__=='__main__':
    kad.removeDrawings()
    kad.removeTracksAndVias()
    main()
    pcbnew.Refresh()
