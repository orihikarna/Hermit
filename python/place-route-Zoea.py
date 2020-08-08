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

Line = kad.Line
Linear = kad.Linear
Round = kad.Round
BezierRound = kad.BezierRound
##

# in mm
VIA_Size = [(1.1, 0.6), (1.0, 0.5), (0.8, 0.4), (0.6, 0.3)]

FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
FourCorners2 = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
PCB_Width  = 100
PCB_Height = 57.74# platinum ratio

keys = [
    ['/', 0.000, 0.520, 3.5],
    ['.', -1.000, 0.000, 0.0],
    [',', -2.000, 0.000, 0.0],
    ['M', -3.074, 0.073, -9.1],
]
keys.insert( 0, [' ', 0.8, 0.75, -20] )

KeyUnit = 19.05

def get_key_postfix( idx ):
    if idx == 0:
        return 'B1'
    else:
        return '1{}'.format( idx )

def drawEdgeCuts():
    layer = 'Edge.Cuts'
    width = 0.1
    W = PCB_Width
    H = PCB_Height

    corners = []
    ### top
    corners.append( [((W/2, 0), 0), Round, [2]] )
    ### right
    corners.append( [((W, 10), 90), Round, [2]] )
    # USB
    pos, _ = kad.get_mod_pos_angle( 'J2' )
    if True:
        corners.append( [((W-3, pos[1] - 4.675), 180), Round, [0.5]] )
        corners.append( [((W-5.73, pos[1]     ),  90), Round, [0.5]] )
        corners.append( [((W-3, pos[1] + 4.675),   0), Round, [0.5]] )
        corners.append( [((W, H-5),               90), Round, [0.5]] )
    ### bottom
    corners.append( [((W-5, H), 180), Round, [3]] )
    if True:
        corners.append( [((W*2/3, H-5), -90), Round, [2]] )
        corners.append( [((W/2, H*2/3), 180), Round, [2]] )
        corners.append( [((W/3,   H-5),  90), Round, [2]] )
        corners.append( [((5, H),       180), Round, [2]] )
    ### left
    corners.append( [((0, H - 5), -90), Round, [3]] )
    # split
    pos, _ = kad.get_mod_pos_angle( 'J1' )
    if True:
        corners.append( [((3, pos[1] + 4.675),   0), Round, [0.5]] )
        corners.append( [((5.73, pos[1]     ), -90), Round, [0.5]] )
        corners.append( [((3, pos[1] - 4.675), 180), Round, [0.5]] )
        corners.append( [((0, 5),              -90), Round, [0.5]] )
    # draw
    kad.draw_closed_corners( corners, layer, width )

def add_zone( net_name, layer_name, rect, zones ):
    layer = pcb.GetLayerID( layer_name )
    zone, poly = kad.add_zone( rect, layer, len( zones ), net_name )
    zone.SetZoneClearance( pcbnew.FromMils( 12 ) )
    #zone.SetMinThickness( pcbnew.FromMils( 10 ) )
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

    drawEdgeCuts()

    zones = []
    add_zone( 'GND', 'F.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )
    add_zone( 'GND', 'B.Cu', make_rect( (PCB_Width, PCB_Height), (0, 0) ), zones )
    # add_zone( 'VCC', 'B.Cu', make_rect( (300, 100), (110, 110)), zones )

    # kad.add_text( (440, 405), 0, '   STM32\n   F042K6\n     tiny\n   orihikarna\n200710', 'F.SilkS', (0.9, 0.9), 6,
    #     pcbnew.GR_TEXT_HJUSTIFY_LEFT, pcbnew.GR_TEXT_VJUSTIFY_CENTER )

    ###
    ### Set key positios
    ###
    for idx, key in enumerate( keys ):
        _, x, y, angle = key
        name = get_key_postfix( idx )
        if idx == 0:
            px = x * KeyUnit
            py = PCB_Height - y * KeyUnit
        else:
            px = PCB_Width + (x - 0.5) * KeyUnit - 2.5
            py = (y + 0.5) * KeyUnit + 2.5
        ## SW
        sw_pos = (px, py)
        kad.set_mod_pos_angle( 'SW' + name, sw_pos, 180 - angle )
        ## LED
        pos = vec2.scale( 4.93, vec2.rotate( 90 + angle ), sw_pos )
        kad.set_mod_pos_angle( 'L' + name, pos, -angle )
        # wire GND to SW
        kad.wire_mods([('L' + name, '6', 'SW' + name, '3', 0.6, (Dird, 0, 90))])
        ## Diode
        if idx > 0:
            pos = vec2.mult( mat2.rotate( -angle ), (-8, -2), sw_pos )
            kad.set_mod_pos_angle( 'D' + name, pos, -90 - angle )
            # wire to SW
            kad.wire_mods([('D' + name, '1', 'SW' + name, '2', 0.5, (Dird, 0, 0))])
        if idx == 1:
            pos = vec2.mult( mat2.rotate( -angle ), (-10.5, 8), sw_pos )
            kad.set_mod_pos_angle( 'D0', pos, -90 - angle )

    ###
    ### Set mod positios
    ###
    kad.move_mods( (0, 0), 0, [
        # mcu
        (None, (52, 29), 0, [
            ('U1', (0, 0), 0),
            # pass caps
            (None, (-4.8, -5.2), 0, [
                ('C3', (0, 0), 90),
                ('C5', (-2, 0), 90),
            ] ),
            # USB DM/DP
            ('R4', (8.5, +0.2), 180),
            ('R5', (8.5, -1.8), 180),
            # C4 & regulators
            (None, (4.8, 5.2), -90, [
                ('C4', (0, 0), 0),
                (None, (0, -4.7), 0, [
                    ('C1', (0, -2.7), 0),
                    ('U2', (-0.15, 0), 0),
                    ('C2', (0, +2.7), 0),
                ] ),
            ] ),
        ] ),
        # Split (USB) connector
        (None, (+2.62, PCB_Height/2), 180, [
            ('J1', (0, 0), +90),
            ('R6', (-7.5, +5.4), 0),
            ('R7', (-7.5, -5.4), 0),
            # I2C pull-up's
            ('R2', (-12, +1.9), -90),
            ('R3', (-12, -1.9), +90),
        ] ),
        # USB connector
        (None, (100-2.62, 40), 0, [
            ('J2', (0, 0), +90),
            ('R8', (-7.5, +5.4), 0),
            ('R9', (-7.5, -5.4), 0),
            # 5V
            ('F1', (-12, -4), 90),
            ('L1', (-14, -4), 90),
        ] ),
        # D1
        (None, (50.5, PCB_Height*2/3 - 1.27), 0, [
            ('D1', (0, 0), 180),
            ('R1', (4, 0), 0),
        ] ),
        # Pin headers & NRST
        (None, (PCB_Width/3 + 1.27, PCB_Height*2/3 - 1.27), 0, [
            ('J3', (0, 0),  90),
            ('C6', (1.27, -2.54), 180),
        ] ),
    ] )
    # Debounce
    pos, angle = kad.get_mod_pos_angle( 'SW14' )
    kad.move_mods( pos, angle, [
        (None, (12, 5.9), 0, [
            ('C11', (0, -2), 0),
            ('R11', (0,  0), 0),
            ('R12', (0, +2), 0),
        ] ),
    ] )
    pos, angle = kad.get_mod_pos_angle( 'SWB1' )
    kad.move_mods( pos, angle, [
        (None, (-12, 5.9), 180, [
            ('CB1', (0, +2), 0),
            ('RB1', (0,  0), 0),
            ('RB2', (0, -2), 0),
        ] ),
    ] )

    ###
    ### Wire mods
    ###

    # COL lines
    kad.wire_mods( [
        ('SW14', '1', 'SW13', '1', 0.5, (Dird, 0,   0, -1)),
        ('SW13', '1', 'SW12', '1', 0.5, (Dird, 0,  90, -1)),
        ('SW12', '1', 'SW11', '1', 0.5, (Dird, 0, 135, -1)),
    ] )
    # ROW lines
    kad.wire_mods( [
        ('D11', '2', 'U1', '26', 0.5, (Dird, 0, ([(1.6, 90)], 0), -1)),
        ('D12', '2', 'U1', '27', 0.5, (Dird, 0, ([(2.4, 90)], 0), -1)),
        ('D13', '2', 'U1', '28', 0.5, (Dird, 0, ([(4.8, 90)], 0), -1)),
        ('D14', '2', 'U1', '29', 0.5, (Dird, 0, ([(4.0, 90)], 0), -1)),
        ('C11', '2', 'U1', '30', 0.5, (Dird, 90, ([(3.2, 90)], 0), -1)),
    ] )
    # Debouce
    via_vcc_col1 = kad.add_via_relative( 'C11', '1', (0, -2), VIA_Size[1] )
    kad.wire_mods( [
        ('R11', '1', 'R12', '1', 0.5, (Strt)),
        ('R11', '2', 'C11', '2', 0.5, (Strt)),
        # SW
        ('R11', '1', 'SW14', '1', 0.5, (Dird, 0, 90)),
        # Vcc
        ('C11', '1', None, via_vcc_col1, 0.5, (Strt)),
        ('SWB1','2', 'J1', via_vcc_col1, 0.5, (Dird, 0, 0)),
    ] )
    via_bt01 = kad.add_via_relative( 'U1', '31', (0, -2), VIA_Size[3] )
    via_bt02 = kad.add_via_relative( 'RB1', '2', (10, 0), VIA_Size[2] )
    kad.wire_mods( [
        ('RB1', '1', 'RB2', '1', 0.5, (Strt)),
        ('RB1', '2', 'CB1', '2', 0.5, (Strt)),
        # SW
        ('RB1', '1', 'SWB1', '1', 0.5, (Dird, 0, 90)),
        ('CB1', '1', 'SWB1', '2', 0.5, (Dird, 0, 90)),
        # Vcc
        ('U1', via_bt01, None, via_bt02, 0.5, (Dird, 0, 45, -1), 'B.Cu'),
        ('CB1', '1', 'U1', '5', 0.5, (Dird, ([(1.5, -90), (3.4, 0), (2.5, 90)], 0), 0, -1)),
        # boot0
        ('U1', '31', None, via_bt01, 0.5, (Dird, 90, 0, -1)),
        ('RB1', '2', None, via_bt02, 0.5, (Dird, 0, 90)),
    ] )
    # LED
    via_lci = kad.add_via_relative( 'U1', '11', (0, -2.5), VIA_Size[2] )
    via_ldi = kad.add_via_relative( 'U1', '13', (0, -1.5), VIA_Size[2] )
    via_lb1_5v = kad.add_via_relative( 'R2', '2', (0, 12.5), VIA_Size[1] )
    via_lb1_ci = kad.add_via_relative( 'R2', '2', (0, 11), VIA_Size[2] )
    via_lb1_di = kad.add_via_relative( 'R2', '2', (0, 10), VIA_Size[2] )
    kad.wire_mods( [
        # L <-2.4-> R
        # R <-3.8-> 3:GND
        #   3.8 - 3.2/2 - 1.0x0.707 = 1.493
        ('LB1', '4', 'J1', via_lb1_di, 0.4, (Dird, ([(1.5, 0), (1.0, +45), (3.2, 0), (1.0, -45)], 0), 0, -0.4)),
        ('J1', via_lb1_di, 'L14', '3', 0.4, (Dird, 0, 180, -0.4)),
        ('L14', '4', 'L13', '3', 0.4, (Dird, ([(1.5, 0), (1.0, +45), (3.2, 0)], -45), 0, -0.4)),
        ('L13', '4', 'L12', '3', 0.4, (Dird, ([(1.5, 0), (1.0, +45), (3.2, 0)], -45), 0, -0.4)),
        ('L12', '4', 'L11', '3', 0.4, (Dird, ([(1.5, 0), (1.0, +45), (3.2, 0), (1.0, -45)], -45), ([(2.4, 180)], 120), -0.4)),
        ('L11', '4','U1',via_ldi,0.4, (Dird, ([(1.5, 0), (1.0, +45), (3.2, 0), (2.0, -45)], -90), 0, -0.4)),
        ('U1', '13','U1',via_ldi,0.4, (Dird, 0, 90)),
        #   3.8 - 2.4/2 - 1.2x0.707 = 1.752
        ('LB1', '5', 'J1', via_lb1_ci, 0.4, (Dird, ([(1.75, 0), (1.2, +45), (2.4, 0), (1.2, -45)], 0), 0, -0.4)),
        ('J1', via_lb1_ci, 'L14', '2', 0.4, (Dird, 0, 180, -0.4)),
        ('L14', '5', 'L13', '2', 0.4, (Dird, ([(1.75, 0), (1.2, +45), (2.4, 0)], -45), 0, -0.4)),
        ('L13', '5', 'L12', '2', 0.4, (Dird, ([(1.75, 0), (1.2, +45), (2.4, 0)], -45), 0, -0.4)),
        ('L12', '5', 'L11', '2', 0.4, (Dird, ([(1.75, 0), (1.2, +45), (2.4, 0), (1.2, -45)], -45), ([(3, 180)], 120), -0.4)),
        ('L11', '5','U1',via_lci,0.4, (Dird, ([(1.75, 0), (1.2, +45), (2.4, 0), (1.2, -45)], -90), 0, -0.4)),
        ('U1', '11','U1',via_lci,0.4, (Dird, 0, 90)),
        #   3.8 + 2.4 - 2.6/2 - 1.0x0.707 = 4.9 - 0.707 = 4.193
        ('LB1', '1', 'J1', via_lb1_5v, 0.8, (Dird, ([(0.5, -90), (0.5, -45), (4.2, 0), (0.5, -45), (2.6, 0), (1.5, +45)], +0), 0, -0.5)),
        ('J1', via_lb1_5v, 'L14', '1', 0.8, (Dird, 0, 180, -0.5)),
        ('L14', '1', 'L13', '1', 0.8, (Dird, ([(0.5, -90), (0.5, -45), (4.2, 0), (0.5, -45), (2.6, 0), (0.5, +45)], +45), 0, -0.5)),
        ('L13', '1', 'L12', '1', 0.8, (Dird, ([(0.5, -90), (0.5, -45), (4.2, 0), (0.5, -45), (2.6, 0), (0.5, +45)], +45), 0, -0.5)),
        #('L12', '1', 'L11', '1', 0.8, (Dird, ([(0.5, -90), (0.5, -45), (4.2, 0), (0.5, -45), (3.8, 0)], -45), ([(4, 180)], 120), -0.5)),
        ('R2', '2', None, via_lb1_5v, 0.8, (Dird, 90, 0)),
    ] )
    pcb.Delete( via_lb1_ci )
    pcb.Delete( via_lb1_di )
    via_vcc_l11 = kad.add_via_relative( 'L11', '1', (-4.5, 0.2), VIA_Size[1] )
    via_vcc_l12 = kad.add_via_relative( 'L12', '1', (0, 8), VIA_Size[1] )
    via_vcc_c1 = kad.add_via_relative( 'C1', '1', (-3.5, 0), VIA_Size[1] )
    kad.wire_mods( [
        ('L11', '1', None, via_vcc_l11, 0.6, (Dird, 0, 45)),
        ('L12', '1', None, via_vcc_l12, 0.6, (Dird, 0, 90)),
        ('C1',  '1', None, via_vcc_c1, 0.6, (Dird, 0, 90)),
        (None, via_vcc_l12, None, via_vcc_c1, 0.6, (ZgZg, 0, 60), 'B.Cu'),
        ('D0', '1', 'L11', via_vcc_l11, 0.6, (Dird, 90, +45, -1.0)),
        ('D0', '2', 'L12', via_vcc_l12, 0.6, (Dird, 45, 0, -1.0)),
        ('D0', '2', 'L1', '1', 0.6, (Dird, 45, 90)),
        ('F1', '2', 'L1', '2', 0.6, (Dird, 0, 90)),
    ] )

    # mcu
    via_vcca1 = kad.add_via_relative( 'U1', '1', (-4.2, -1.27), VIA_Size[1] )
    via_vcca5 = kad.add_via_relative( 'U1', '5', (-4.2, 0), VIA_Size[1] )
    via_nrst  = kad.add_via_relative( 'U1',  '4', (-1.5, 0), VIA_Size[3] )
    via_swdio = kad.add_via_relative( 'U1', '23', (-1.5, 0), VIA_Size[3] )
    via_swclk = kad.add_via_relative( 'U1', '24', (-2.0, 0), VIA_Size[3] )
    kad.wire_mods( [
        # pass caps
        ('C4', '1', 'U1', '17', 0.5, (Dird, 0, 0, -0.5)),
        ('C4', '2', 'U1', '16', 0.5, (Dird, 90, 90)),
        ('C3', '1', 'U1',  '1', 0.5, (Dird, 0, 0, -0.5)),
        ('C3', '2', 'U1', '32', 0.5, (Dird, 90, 90)),
        ('C3', '2', 'C5', '2',  0.6, (Dird, 0, 90, -0.8)),
        # VCC
        ('U1', '17', 'U1', '1', 0.5, (Dird, ([(-1.3, 0)], 135), 0)),
        ('U1', '17', 'U1', '5', 0.5, (Dird, ([(-1.3, 0)], 135), 0)),
        # VCCA
        ('U1', '5', None, via_vcca5, 0.5, (Strt)),
        ('C5', '1', None, via_vcca1, 0.6, (Dird, 90, 0, -1)),
        (None, via_vcca1, None, via_vcca5, 0.6, (Strt), 'B.Cu'),
        # NRST
        ('U1', '4', None, via_nrst, 0.5, (Strt)),
        ('J3', '2', None, via_nrst, 0.5, (ZgZg, 0, 60), 'B.Cu'),
        # SWCLK/DIO
        ('U1', '23', None, via_swdio, 0.5, (Strt)),
        ('U1', '24', None, via_swclk, 0.5, (Strt)),
        ('J3', '5', None, via_swclk, 0.5, (Dird, ([(2, 0)], -45), 90), 'B.Cu'),
        ('J3', '6', None, via_swdio, 0.5, (Dird, ([(3, 0)], -45), 90), 'B.Cu'),
        # TX/RX
        ('J3', '3', 'U1', '8', 0.5, (Dird, 0, 0, -1)),
        ('J3', '4', 'U1', '9', 0.5, (Dird, 0, 0, -1)),
        # USB
        ('U1', '21', 'R4', '2', 0.5, (Dird, 0, ([(1, 0)], -45))),
        ('U1', '22', 'R5', '2', 0.5, (Dird, 0, ([(1, 0)], +45))),
        # I2C pull-up's
        ('U1', '2', 'R2', '1', 0.5, (Dird, 180, ([(-2, 90)], -45), -0.8)),
        ('U1', '3', 'R3', '1', 0.5, (Dird, 180, ([(+2, 90)], -45), -0.8)),
    ] )
    # USB connector
    via_usb_vba = kad.add_via_relative( 'J2', 'A4', (-0.4, -5.2), VIA_Size[1] )
    via_usb_vbb = kad.add_via_relative( 'J2', 'B4', (+0.4, -5.2), VIA_Size[1] )
    via_usb_cc1 = kad.add_via_relative( 'J2', 'A5', (-0.15, -2.5), VIA_Size[3] )
    via_usb_cc2 = kad.add_via_relative( 'J2', 'B5', (+0.15, -2.5), VIA_Size[3] )
    via_usb_dpa = kad.add_via_relative( 'J2', 'A6', (-0.5,  -4.1), VIA_Size[3] )
    via_usb_dpb = kad.add_via_relative( 'J2', 'B6', (+0.15, -4.1), VIA_Size[3] )
    via_usb_dma = kad.add_via_relative( 'J2', 'A7', (+0.15, -3.3), VIA_Size[3] )
    via_usb_dmb = kad.add_via_relative( 'J2', 'B7', (-0.15, -3.3), VIA_Size[3] )
    via_r8_cc1 = kad.add_via_relative( 'R8', '1', (0, -1.4), VIA_Size[3] )
    via_r9_cc2 = kad.add_via_relative( 'R9', '1', (0, +1.4), VIA_Size[3] )
    kad.wire_mods( [
        (None, via_usb_vba, 'J2', 'A4', 0.8, (Dird, 90, ([(1.8, 90)], -45))),
        (None, via_usb_vbb, 'J2', 'B4', 0.8, (Dird, 90, ([(1.8, 90)], +45))),
        (None, via_usb_vba, None, via_usb_vbb, 0.8, (Strt), 'B.Cu'),
        (None, via_usb_cc1, 'J2', 'A5', 0.3, (Dird, -45, 90)),
        (None, via_usb_cc2, 'J2', 'B5', 0.3, (Dird, +45, 90)),
        (None, via_usb_dpa, 'J2', 'A6', 0.3, (Dird, 90, ([(2.5, 90)], -45))),
        (None, via_usb_dpb, 'J2', 'B6', 0.3, (Dird, +45, 90)),
        (None, via_usb_dpa, None, via_usb_dpb, 0.3, (Strt), 'B.Cu'),
        (None, via_usb_dma, 'J2', 'A7', 0.3, (Dird, +45, 90)),
        (None, via_usb_dmb, 'J2', 'B7', 0.3, (Dird, -45, 90)),
        (None, via_usb_dma, None, via_usb_dmb, 0.3, (Strt), 'B.Cu'),
        (None, via_usb_cc1, None, via_r8_cc1, 0.3, (Dird, -45, 0), 'B.Cu'),
        (None, via_usb_cc2, None, via_r9_cc2, 0.3, (Dird, +45, 0), 'B.Cu'),
        ('J2', via_usb_dpb, 'R5', '1', 0.4, (Dird, ([(7, 90)], 45), ([(-1, 0), (-0.9, -45)], 0))),
        ('J2', via_usb_dmb, 'R4', '1', 0.4, (Dird, ([(8, 90)], 45), ([(-1, 0), (-0.9, +45)], 0))),
        (None, via_r8_cc1, 'R8', '1', 0.3, (Dird, 45, 90)),
        (None, via_r9_cc2, 'R9', '1', 0.3, (Dird, 45, 90)),
        ('R8', '2', 'J2', 'A1', 0.8, (Dird, 90, ([(1.2, 90)], -45))),
        ('R9', '2', 'J2', 'B1', 0.8, (Dird, 90, ([(1.2, 90)], +45))),
        ('R8', '2', 'J2', 'S1', 0.8, (Dird, 0, 0)),
        ('R9', '2', 'J2', 'S2', 0.8, (Dird, 0, 0)),
        ('F1', '1', None, via_usb_vbb, 0.6, (Dird, 0, 90)),
    ] )
    # Split USB connector
    via_splt_vba = kad.add_via_relative( 'J1', 'A4', (-0.4, -6), VIA_Size[1] )
    via_splt_vbb = kad.add_via_relative( 'J1', 'B4', (+0.4, -6), VIA_Size[1] )
    via_splt_cc1 = kad.add_via_relative( 'J1', 'A5', (-0.15, -2.5), VIA_Size[3] )
    via_splt_cc2 = kad.add_via_relative( 'J1', 'B5', (+0.15, -3.3), VIA_Size[3] )
    via_splt_dpa = kad.add_via_relative( 'J1', 'A6', (-0.5,  -4.9), VIA_Size[3] )
    via_splt_dpb = kad.add_via_relative( 'J1', 'B6', (+0.15, -4.9), VIA_Size[3] )
    via_splt_dma = kad.add_via_relative( 'J1', 'A7', (+0.15, -4.1), VIA_Size[3] )
    via_splt_dmb = kad.add_via_relative( 'J1', 'B7', (-0.15, -4.1), VIA_Size[3] )
    via_splt_sb1 = kad.add_via_relative( 'J1', 'A8', (+0.15, -2.5), VIA_Size[3] )
    via_splt_sb2 = kad.add_via_relative( 'J1', 'B8', (-0.15, -3.3), VIA_Size[3] )
    via_r6_cc1 = kad.add_via_relative( 'R6', '1', (0, -1.4), VIA_Size[3] )
    via_r7_cc2 = kad.add_via_relative( 'R7', '1', (0, +1.4), VIA_Size[3] )
    kad.wire_mods( [
        ('J1', 'S1', 'J1', 'S2', 0.8, (Dird, ([(0.8, 45)], 0), -45), 'B.Cu'),
        (None, via_splt_vba, 'J1', 'A4', 0.8, (Dird, 90, ([(1.8, 90)], -45))),
        (None, via_splt_vbb, 'J1', 'B4', 0.8, (Dird, 90, ([(1.8, 90)], +45))),
        (None, via_splt_vba, None, via_splt_vbb, 0.8, (Strt), 'B.Cu'),
        (None, via_splt_vba, 'R2', '2', 0.8, (Dird, 90, 0)),
        (None, via_splt_vbb, 'R3', '2', 0.8, (Dird, 90, 0)),
        (None, via_splt_cc1, 'J1', 'A5', 0.3, (Dird, -45, 90)),
        (None, via_splt_cc2, 'J1', 'B5', 0.3, (Dird, +45, 90)),
        (None, via_splt_dpa, 'J1', 'A6', 0.3, (Dird, 90, ([(3.5, 90)], -45))),
        (None, via_splt_dpb, 'J1', 'B6', 0.3, (Dird, +45, 90)),
        (None, via_splt_dpa, None, via_splt_dpb, 0.3, (Strt), 'B.Cu'),
        (None, via_splt_dma, 'J1', 'A7', 0.3, (Dird, +45, 90)),
        (None, via_splt_dmb, 'J1', 'B7', 0.3, (Dird, -45, 90)),
        (None, via_splt_dma, None, via_splt_dmb, 0.3, (Strt), 'B.Cu'),
        (None, via_splt_sb1, 'J1', 'A8', 0.3, (Dird, +45, 90)),
        (None, via_splt_sb2, 'J1', 'B8', 0.3, (Dird, -45, 90)),
        (None, via_splt_cc1, None, via_r6_cc1, 0.3, (Dird, -45, 0), 'B.Cu'),
        (None, via_splt_cc2, None, via_r7_cc2, 0.3, (Dird, +45, 0), 'B.Cu'),
        (None, via_splt_dmb, 'R2', '1', 0.4, (ZgZg, 90, 45)),
        (None, via_splt_dpb, 'R3', '1', 0.4, (ZgZg, 90, 45)),
        (None, via_r6_cc1, 'R6', '1', 0.3, (Dird, 45, 90)),
        (None, via_r7_cc2, 'R7', '1', 0.3, (Dird, 45, 90)),
        ('R6', '2', 'J1', 'A1', 0.8, (Dird, 90, ([(1.2, 90)], -45))),
        ('R7', '2', 'J1', 'B1', 0.8, (Dird, 90, ([(1.2, 90)], +45))),
        ('R6', '2', 'J1', 'S1', 0.8, (Dird, 0, 0)),
        ('R7', '2', 'J1', 'S2', 0.8, (Dird, 0, 0)),
    ] )
    kad.wire_mods( [
        ('LB1', '3', 'J1', via_splt_sb1, 0.4, (Dird, ([(6, 180), (11, 90)], 0), 0, -0.4)),
        ('LB1', '2', 'J1', via_splt_sb2, 0.4, (Dird, ([(7, 180), (13, 90)], 0), ([(4, -30)], 0), -0.4)),
    ] )

    # # regulator
    # via_reggnd1 = kad.add_via_relative( 'U2', '3', (-15, +48), VIA_Size[1] )
    # via_reggnd2 = kad.add_via_relative( 'U2', '3', (-15, -48), VIA_Size[1] )
    kad.wire_mods( [
    #     ('F1', '2', 'L1', '2', 24, (ZgZg, 0, 70, -20)),
    #     ('C1', '1', 'L1', '1', 24, (Strt)),
        ('U2', '1', 'C1', '1', 0.6, (Dird, 0, 90)),# 5V
        ('U2', '3', 'C1', '2', 0.6, (Dird, 0, 90)),# Gnd
        ('U2', '3', 'C2', '2', 0.6, (Dird, 0, 90)),# Gnd
        ('U2', '2', 'C2', '1', 0.6, (Dird, 0, 90)),# Vcc
        #
        ('C4', '1', 'C2', '1', 0.6, (Dird, 0, 90)),# Vcc
        ('C4', '2', 'C2', '2', 0.6, (Dird, 0, 90)),# Gnd
    #     # Gnd
    #     (None, via_reggnd1, 'U2', '3', 24, (Dird, 0, 90)),
    #     (None, via_reggnd2, 'U2', '3', 24, (Dird, 0, 90)),
    #     (None, via_reggnd1, 'U2', '3', 24, (Dird, ([(35, 180)], 90), ([(50, 180)], 0), -32)),
    #     (None, via_reggnd2, 'U2', '3', 24, (Dird, ([(35, 180)], 90), ([(50, 180)], 0), -32)),
    ] )
    kad.wire_mods( [
        # LED
        ('D1', '2', 'U1', '10', 0.5, (ZgZg, 90, 45)),
        ('D1', '1', 'R1', '1', 0.5, (Dird, 0, 90)),
        # NRST
        ('C6', '1', 'J3', '2', 0.4, (Dird, 0, 0)),
        ('C6', '2', 'J3', '1', 0.4, (Dird, 0, 0)),
    ] )


    ###
    ### Ref
    ###
    # refs = [
    #     ('C1', 90, +40, 90),
    #     ('C2', 90, -40, 90),
    #     ('C3', -60, 70, 180),
    #     ('C4',  60,120, 180),
    #     ('C5', -60, 70, 180),
    #     ('C6',  60,-60, 180),
    #     ('C7',  90,  0,  90),
    #     ('C8',  90,  0,  90),
    #     ('C9', -90,  0, -90),
    #     ('R1', -15, 0, 0),
    #     ('R2', -15, 0, 0),
    #     ('R4',  60,120, 180),
    #     ('R5', -60, 60, 180),
    #     ('R6', -100, 0, -90),
    #     ('R7', -100, 0, -90),
    #     ('L1',  100, 0,  90),
    #     ('F1', -100, 0, -90),
    #     ('R3', 100, 0, 90),
    #     ('R8', 100, 0, 90),
    #     ('R9', 100, 0, 90),
    #     ('U1', 120, 135, 0),
    #     ('U2', 0, 0, -90),
    #     ('D1', 15, 0, 0),
    #     ('D2', 15, 0, 0),
    #     ('D3', 50, 90, -90),
    #     ('SW1', 0, 0, -90),
    #     ('J1', 0, 0, None),
    #     ('J2', 0, 0, None),
    #     ('J3', 0, 0, None),
    # ]
    # for mod_name, offset_length, offset_angle, text_angle in refs:
    #     mod = kad.get_mod( mod_name )
    #     pos, angle = kad.get_mod_pos_angle( mod_name )
    #     ref = mod.Reference()
    #     if text_angle == None:
    #         ref.SetVisible( False )
    #     else:
    #         ref.SetTextSize( pcbnew.wxSizeMM( 0.9, 0.9 ) )
    #         ref.SetThickness( pcbnew.FromMils( 7 ) )
    #         pos_ref = vec2.scale( offset_length, vec2.rotate( - (offset_angle + angle) ), pos )
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )
    #         ref.SetTextAngle( text_angle * 10 )
    #         ref.SetKeepUpright( False )

    # refs = [ ('J3', (0, 90), (90, 0), [
    #         ('1', 'A5', 'SCK'),
    #         ('2', 'A6', 'MISO'),
    #         ('3', 'A7', 'MOSI'),
    #     ] ), ('J2', (90, 0), (0, 90), [
    #         ('1', 'A3', 'RX'),
    #         ('2', 'A2', 'TX'),
    #         ('3', 'nRST', 'nRST'),
    #         ('4', 'F1', 'F1'),
    #         ('5', 'F0', 'F0'),
    #         ('6', 'GND', 'GND'),
    #         ('7', '3V3', '3V3'),
    #     ] ), ('J1', (-90, 180), (0, -90), [
    #         ('1', '5V', '5V'),
    #         ('2', 'A9',  'SCL'),
    #         ('3', 'A10', 'SDA'),
    #         ('4', 'A13', 'DIO'),
    #         ('5', 'A14', 'CLK'),
    #         ('6', 'B3', 'SCK'),
    #         ('7', 'B4', 'MISO'),
    #         ('8', 'B5', 'MOSI'),
    #     ] ),
    # ]
    # for mod, angles1, angles2, pads in refs:
    #     for pad, text1, text2 in pads:
    #         pos = kad.get_pad_pos( mod, pad )
    #         angle_pos1, angle_text1 = angles1
    #         angle_pos2, angle_text2 = angles2
    #         for idx, layer in enumerate( ['F.SilkS', 'B.SilkS'] ):
    #             pos1 = vec2.scale( [65, 65][idx], vec2.rotate( angle_pos1 ), pos )
    #             pos2 = vec2.scale( 50, vec2.rotate( angle_pos2 ), pos )
    #             kad.add_text( pos1, angle_text1, text1, layer, (0.7, 0.7), 6,
    #                 pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )
    #             kad.add_text( pos2, angle_text2, text2, layer, (0.7, 0.7), 6,
    #                 pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )

    # pos, angle = kad.get_mod_pos_angle( 'SW1' )
    # kad.add_text( pos, angle + 90, 'BOOT0', 'F.SilkS', (0.85, 0.65), 6,
    #     pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER )
    pcbnew.Refresh()

if __name__=='__main__':
    main()
