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
PCB_Width  = 950
PCB_Height = 700


def drawEdgeCuts():
    layer = 'Edge.Cuts'
    width = 2
    W = PCB_Width
    H = PCB_Height

    corners = []
    ### top
    corners.append( [((W/2,  0), 0), Round, [30]] )
    ### right
    corners.append( [((W, 100), 90), Round, [30]] )
    # USB
    pos, _ = kad.get_mod_pos_angle( 'J4' )
    if False:
        corners.append( [((W+12, pos[1] - 180),   0), Round, [10]] )
        corners.append( [((W+24, pos[1]      ),  90), Round, [10]] )
        corners.append( [((W+12, pos[1] + 180), 180), Round, [10]] )
        corners.append( [((W,    H-100),         90), Round, [10]] )
    ### bottom
    corners.append( [((W/2, H), 180), Round, [30]] )
    ### left
    corners.append( [((0, H - 50), -90), Round, [30]] )
    if True:# LED (80mils in 200mils = 60mils each on above and below)
        LED_W = 80#mils = 2.32mm
        # slope
        sl_w = (200 - LED_W) / 2
        sl_h = 30# 0.75mm
        sl_angle = int( math.atan2( sl_h, sl_w ) / math.pi * 180 )
        pos, _ = kad.get_mod_pos_angle( 'D3' )
        corners.append( [((-sl_h/2, pos[1] + (LED_W + sl_w) / 2), -90-sl_angle), BezierRound, [8]] )
        corners.append( [((-sl_h/2, pos[1] + LED_W / 2),                     0), BezierRound, [8]] )
        corners.append( [((      0, pos[1] ),                              -90), Round, [8]] )
        corners.append( [((-sl_h/2, pos[1] - LED_W / 2),                   180), Round, [8]] )
        corners.append( [((-sl_h/2, pos[1] - (LED_W + sl_w) / 2), -90+sl_angle), BezierRound, [8]] )
        corners.append( [((0, 50), -90), BezierRound, [9]] )
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

    #PCB_Rect = map( lambda pt: (PCB_Width * pt[0], PCB_Height * pt[1]), FourCorners )
    #kad.drawRect( PCB_Rect, 'Edge.Cuts', R = 40 )
    drawEdgeCuts()

    zones = []
    add_zone( 'GND', 'F.Cu', make_rect( (PCB_Width - 100, PCB_Height), (100, 0) ), zones )
    add_zone( 'GND', 'B.Cu', make_rect( (PCB_Width - 500, PCB_Height), (500, 0)), zones )
    add_zone( 'VCC', 'B.Cu', make_rect( (300, 100), (110, 110)), zones )

    kad.add_text( (440, 405), 0, '   STM32\n   F042K6\n     tiny\n   orihikarna\n200710', 'F.SilkS', (0.9, 0.9), 6,
        pcbnew.GR_TEXT_HJUSTIFY_LEFT, pcbnew.GR_TEXT_VJUSTIFY_CENTER )

    ###
    ### Set mod positios
    ###
    kad.move_mods( (300, 350), 0, [
        # Pin headers
        ('J1', (-250, +300), 90),
        ('J2', (-250, -300), 90),
        ('J3', (-250, -200),  0),
        # USB connector
        (None, (550, -5), 0, [
            ('J4', (0, 0), -90),
            (None, (-40, -25), 0, [
                ('R3', (0, -75), 0),# BOOT0 pull-down
                ('R8', (0,   0), 0),
                ('R9', (0, +75), 0),
            ] ),
        ] ),
        # BOOT0 (SW1)
        ('SW1', (525, -275), -90),
        # D1/D2
        (None, (575, 230), 0, [
            (None, (0,  0), 180, [ ('D1', (0, 0), 0), ('R1', (0, 0), 0) ] ),
            (None, (0, 75), 180, [ ('D2', (0, 0), 0), ('R2', (0, 0), 0) ] ),
        ] ),
        # mcu
        (None, (15, 0), 0, [
            ('U1', (0, 0), -90),
            # pass caps
            (None, ( 235, -155), -90, [ ('C3', (0, 0), 0), ('C4', (0, 0), 0) ] ),
            (None, (-235,  155), +90, [ ('C5', (0, 0), 0), ('C6', (0, 0), 0) ] ),
            # Vcca pass caps
            (None, (  90, -115), 0, [ ('C7', (0, 0), 0), ('C8', (0, -75), 0) ] ),
        ] ),
        # D3
        ('D3', (-280, 150), 0),
        # NRST
        ('C9', (-100, -125), 180),
        # USB DM/DP
        (None, (164, 112.5), 0, [ ('R6', (0, 0), 180), ('R7', (-10, 75), 180) ] ),
        # I2C pull-up's
        (None, (-80, 155), 0, [ ('R4', (0, 0), 90), ('R5', (75, 0), 90) ] ),
        # regulators
        (None, (-40, 0), 0, [
            ('U2', (   0, 6), 90),
            ('C1', ( 104, 0), 90),
            ('C2', (-104, 0), 90),
            ('L1', ( 215, +37.5),   0),
            ('F1', ( 225, -37.5), 180),
        ] ),
    ] )

    ###
    ### Wire mods
    ###
    # regulator
    via_reggnd1 = kad.add_via_relative( 'U2', '3', (-15, +48), VIA_Size[1] )
    via_reggnd2 = kad.add_via_relative( 'U2', '3', (-15, -48), VIA_Size[1] )
    kad.wire_mods( [
        ('F1', '2', 'L1', '2', 24, (ZgZg, 0, 70, -20)),
        ('C1', '1', 'L1', '1', 24, (Strt)),
        ('U2', '1', 'C1', '1', 24, (Dird, 90, 0)),# 5V
        ('U2', '3', 'C1', '2', 24, (Dird, 90, 0)),# Gnd
        ('U2', '3', 'C2', '2', 24, (Dird, 90, 0)),# Gnd
        ('U2', '2', 'C2', '1', 24, (Dird, 90, 0)),# Vcc
        # Gnd
        (None, via_reggnd1, 'U2', '3', 24, (Dird, 0, 90)),
        (None, via_reggnd2, 'U2', '3', 24, (Dird, 0, 90)),
        (None, via_reggnd1, 'U2', '3', 24, (Dird, ([(35, 180)], 90), ([(50, 180)], 0), -32)),
        (None, via_reggnd2, 'U2', '3', 24, (Dird, ([(35, 180)], 90), ([(50, 180)], 0), -32)),
    ] )
    # mcu
    via_vcca = kad.add_via_relative( 'U1', '5', (-65, 10), VIA_Size[0] )
    kad.wire_mods( [
        # mcu <--> Vcc x 2
        ('U1', '1', 'C3', '1', 24, (ZgZg, 90, 45, -20)),# Vcc
        ('U1','32', 'C3', '2', 24, (Dird, 90, 0)),# Gnd
        ('U1','17', 'C5', '1', 24, (ZgZg, 90, 45, -20)),# Vcc
        ('U1','16', 'C5', '2', 24, (Dird, 90, 0)),# Gnd
        # Vcc <--> Vcc
        ('U1', '1', 'U1', '17', 20, (Dird,
            ([(33,   0), (80, -45), (80, -90)], 135),
            ([(33, 180), (80, 135)], 180), -16)),# Vcc
        # Vcca
        ('U1', '5', None, via_vcca, 24, (Dird, 0, 90)),
        ('C8', '1', None, via_vcca, 24, (Dird, 0, 90)),
        ('C7', '1', 'C8', '1', 24, (Strt)),
        ('C7', '2', 'C8', '2', 24, (Strt)),
        # Gnd
        ('C4', '2', 'C7', '2', 24, (Dird, 0, 0)),
        (None, via_reggnd1, 'U1', '32', 20, (Dird, 90, ([(33, -90)], 135), -16)),
        (None, via_reggnd2, 'U1', '16', 20, (Dird,  0, ([(33, +90)], -45), -16)),
    ] )
    via_pads = [
        ('C3', '1'), ('C3', '2'),
        ('C5', '1'), ('C5', '2'),
    ]
    for mod_name, pad_name in via_pads:
        kad.add_via_on_pad( mod_name, pad_name, VIA_Size[1] )

    ## pin headers [(80, 45), (56, 90)] is a basic shape
    # J1
    kad.wire_mods( [
        # left B.Cu
        ('R4', '1', 'J1', '2', 20, (Dird, 0, -45, -16)),# PA9
        ('R5', '1', 'J1', '3', 20, (Dird, 0, -45, -16)),# PA10
        # left F.Cu
        ('U1','19', 'J1', '2', 20, (Dird, 0, ([(80, -45), (40, -90)], -45), -16)),# PA9
        ('U1','20', 'J1', '3', 20, (Dird, 0, -45, -16)),# PA10
        ('U1','23', 'J1', '4', 20, (Dird, 0, -45, -16)),# PA13
        ('U1','24', 'J1', '5', 20, (Dird, 0, +45, -16)),# PA14
        # right (separation = 30 mils, 30 * sin(22.5) = 11.48, (30 - 11.5) x 1.414 ~ 26.2)
        ('U1','26', 'J1', '6', 20, (Dird, ([(40,      90), (12,      45)], 0), 45, -16)),# PB3
        ('U1','27', 'J1', '7', 20, (Dird, ([(40+11.5, 90), (12+26.2, 45)], 0), 45, -16)),# PB4
        ('U1','28', 'J1', '8', 20, (Dird, ([(40+23.0, 90), (12+52.4, 45)], 0), ([(80, 45), (56, 90)], 45), -16)),# PB5
    ] )
    # J2
    kad.wire_mods( [
        ('U1', '9', 'J2', '1', 20, (Dird, 0, +45, -16)),# PA3
        ('U1', '8', 'J2', '2', 20, (Dird, 0, +45, -16)),# PA2
        (None, via_vcca, 'J2', '3', 24, (Dird, 45, 0), 'F.Cu'),
        (None, via_vcca, 'J2', '3', 24, (Dird, 90, 0), 'B.Cu'),
        ('U1', '4', 'J2', '4', 20, (ZgZg, 0, 25, -16)),# NRST
        ('U1', '3', 'J2', '5', 20, (Dird, 0, -45, -16)),# PF1
        ('U1', '2', 'J2', '6', 20, (Dird, 0, ([(80, 135), (56, 90)], -45), -16)),# PF0
    ] )
    # J3
    kad.wire_mods( [
        ('U1', '13', 'J3', '3', 20, (Dird, -90, -45, -16)),# PA7
        ('U1', '12', 'J3', '2', 20, (Dird, -90, ([(27, -90)], -45), -16)),# PA6
        ('U1', '11', 'J3', '1', 20, (Dird, ([(33, -90)], 45), ([(25, -90), (75, -45)], -90), -16)),# PA5
    ] )
    # J4 (USB)
    via_cc1 = kad.add_via_relative( 'J4', 'A5', (+22, -70), VIA_Size[2] )
    via_cc2 = kad.add_via_relative( 'J4', 'B5', (-22, -70), VIA_Size[2] )
    kad.wire_mods( [
        # VBUS A4 <--> B4
        # ('J4', 'A4', 'J4', 'B4', 12.4, (Strt2,
        #     [(-3.1, 0), (15, 90), (24,  60), (40, 90), (40,  45)],
        #     [(+3.1, 0), (15, 90), (24, 120), (40, 90), (40, 135)], 5)),
        ('J4', 'A4', 'J4', 'B4', 20, (Strt2,
            [(-1.75, 0), (30, 90), (20,  62), (65, 90)],
            [(+1.75, 0), (30, 90), (20, 118), (65, 90)], -32)),
        # Vcc <--> D1
        ('D1', '2', 'J4', 'B4', 20, (Dird,
            ([(100, -45)], 90),
            ([(+1.75, 0), (30, 90), (20, 118)], 90), -32)),
        # Gnd Shield
        ('J4', 'A1', 'J4', 'S1', 23.5, (Dird, 0, -45)),
        ('J4', 'B1', 'J4', 'S2', 23.5, (Dird, 0, +45)),
        ('J4', 'A1', 'J4', 'S1', 23.5, (Dird, ([(55, -90)], 0), 90, 0)),
        ('J4', 'B1', 'J4', 'S2', 23.5, (Dird, ([(55, -90)], 0), 90, 0)),
        ('J4', 'S1', 'J4', 'S4', 24, (Strt), 'B.Cu'),
        ('J4', 'S2', 'J4', 'S3', 24, (Strt), 'F.Cu'),
        ('C3', '2',  'J4', 'S1', 24, (Dird, 90, -45, -20), 'F.Cu'),
        ('J2', '7',  'J4', 'S1', 24, (Dird, 0, 45, -20), 'B.Cu'),
        ('R3', '2',  'J4', 'S4', 24, (Dird, 0, 0), 'F.Cu'),
        ('R9', '2',  'J4', 'S3', 24, (Dird, 0, 0), 'F.Cu'),
        ('R1', '2',  'J4', 'S3', 24, (Dird, 90, 90), 'F.Cu'),
        # DM/DP
        ('J4', 'A7', 'J4', 'B7', 11.72, (Strt2, [(50, -90)], [(50, -90)], -16)),# DM
        ('J4', 'A7', 'J4', 'B7', 11.72, (Strt2, [(50+30, -90), (-30, -90)], [(50, -90)], -16)),# DM
        ('J4', 'A6', 'J4', 'B6', 11.72, (Strt2, [(50, +90)], [(50, +90)], -16)),# DP
        # DM/DP <--> R6, R7
        ('J4', 'A7', 'R6', '1', 11.72, (Dird, -90, ([(26, +90), (40, 180), (45, -90), (28, -135)], -90), -16)),# DM
        ('J4', 'B6', 'R7', '1', 11.72, (Dird, -90, ([(26, -90), (72, 180), (55, -90), (28, -135)], -90), -16)),# DP
        # Gnd: CC1/CC2/BOOT0
        ('R8', '2', 'R9', '2', 20, (Strt)),
        ('R8', '2', 'R3', '2', 20, (Strt)),
        # CC1/CC2
        (None, via_cc1, 'J4', 'A5', 11.72, (Dird, -90, ([(50, 90)], -135), -20)),
        (None, via_cc1, 'R8',  '1', 16, (Dird, 0, 90, 25)),
        (None, via_cc2, 'J4', 'B5', 11.72, (Dird, -90, ([(50, 90)], +135), -20)),
        (None, via_cc2, 'R9',  '1', 16, (Dird, 0, 90, 25)),
    ] )
    # Vcc rounting
    kad.wire_mods( [
        # C4 <--> C8
        ('C4', '1', 'C8', '1', 24, (Dird, ([(46, 180)], 90), 90, -20)),
        # C2 <--> C6
        ('C2', '1', 'C6', '1', 24, (Dird, ([(25, 90)], 0), -90, -20)),
        # C2 <--> C4
        ('C4', '1', 'C2', '1', 24, (Dird, ([(46, 180)], 90), ([(50, 90)], 0), -20)),# Vcc
    ] )
    # 5V routing
    kad.wire_mods( [
        # regulator <--> I2C
        ('R5', '2', 'U2', '1', 24, (Dird, 0, 90)),
        # I2C pull-up's
        ('R4', '2', 'R5', '2', 24, (Strt)),
        # I2C <--> J1
        ('R4', '2', 'J1', '1', 24, (Dird, ([(50, 90)], 180), ([(80, -45), (40, -90)], -45), -20), 'B.Cu'),# 5V
    ] )
    # USB DM/DP <--> mcu
    via_dm = kad.add_via_relative( 'U1', '21', (-55, -26), VIA_Size[2] )
    via_dp = kad.add_via_relative( 'U1', '22', ( 55,   4), VIA_Size[2] )
    kad.wire_mods( [
        (None, via_dm, 'U1', '21', 20, (Dird, 90, 0, -16)),
        (None, via_dp, 'U1', '22', 20, (Dird, 90, 0, -16)),
        (None, via_dm, 'R6',  '2', 20, (Dird, 0, 90, -16)),
        (None, via_dp, 'R7',  '2', 20, (Dird, 90, 0, -16)),
    ] )
    # connections
    kad.wire_mods( [
        # VBUS: J4 <--> Regulator/F1
        ('J4', 'A4', 'F1', '1', 23.5, (Dird, ([(55, -90)], 0), ([(45, 180)], 45), -20)),
        # Gnd: J4/A1 <--> mcu/C4
        ('J4', 'A1', 'C4', '2', 23.5, (Dird, 90, -45, -20)),
        # Gnd: Regulator/C1 <--> Vdda/C7
        ('C1', '2', 'C7', '2', 24, (ZgZg, 90, 55, -20)),
        # BOOT0: mcu/PB8 <--> R3
        ('U1', '31', 'R3', '1', 16, (Dird, ([(36, 90), (14, 45), (50, 90), (24, 135)], 90), 90, -12)),
    ] )
    # NRST
    via_nrst = kad.add_via_relative( 'U1', '4', (55, 30), VIA_Size[2] )
    kad.wire_mods( [
        ('U1', '4', None, via_nrst, 16, (Dird, 0, 90, -12)),
        ('C9', '1', None, via_nrst, 16, (Dird, 90, 0)),
        # Gnd: C9 <--> Regulator/C2
        ('C9', '2', 'C2', '2', 16, (Dird, 0, 0)),
    ] )
    # BOOT0
    via_sw1   = kad.add_via_relative( 'SW1', '1', (50, 40), VIA_Size[2] )
    via_boot0 = kad.add_via_relative( 'SW1', '2', (0, 125), VIA_Size[2] )
    kad.wire_mods( [
        (None, via_boot0, 'SW1', '2', 16, (Dird, 90, 0, -12)),
        (None, via_boot0, 'R3',  '1', 16, (ZgZg, 90, 45, -12)),
        (None, via_sw1, 'SW1', '1', 16, (Dird, 90, 0, -12)),# Vcc
        (None, via_sw1, 'C3',  '1', 16, (ZgZg, 90, 60, -12)),# Vcc
    ] )
    # D1/D2
    via_pads = [ ('R1', '1'), ('R2', '1') ]
    for mod_name, pad_name in via_pads:
        kad.add_via_on_pad( mod_name, pad_name, VIA_Size[1] )
    # D2
    via_d2 = kad.add_via_relative( 'U1', '25', (135, 0), VIA_Size[1] )
    kad.wire_mods( [
        ('R1', '2', 'R2', '2', 20, (Strt)),
        (None, via_d2, 'U1', '25', 20, (Dird, 90, 0)),# PA15
        (None, via_d2, 'D2', '2', 20, (Dird, 0, 135, -16)),
    ] )
    # D3
    via_d3 = kad.add_via_relative( 'D3', '3', (40, -62), VIA_Size[2] )
    kad.wire_mods( [
        ('D3', '4', 'J1', '1', 20, (Dird, ([(10, 0)], 90), 45, -16), 'B.Cu'),# 5V
        ('D3', '2', 'C5', '2', 20, (Dird, ([(10, 0)], 90), 90), 'F.Cu'),# Gnd
        (None, via_d3, 'D3',  '3', 16, (Dird, 0, ([(10, 0)], 90), -16)),
        (None, via_d3, 'U1', '15', 16, (ZgZg, 90, 45, -16)),
    ] )


    ###
    ### Ref
    ###
    refs = [
        ('C1', 90, +40, 90),
        ('C2', 90, -40, 90),
        ('C3', -60, 70, 180),
        ('C4',  60,120, 180),
        ('C5', -60, 70, 180),
        ('C6',  60,-60, 180),
        ('C7',  90,  0,  90),
        ('C8',  90,  0,  90),
        ('C9', -90,  0, -90),
        ('R1', -15, 0, 0),
        ('R2', -15, 0, 0),
        ('R4',  60,120, 180),
        ('R5', -60, 60, 180),
        ('R6', -100, 0, -90),
        ('R7', -100, 0, -90),
        ('L1',  100, 0,  90),
        ('F1', -100, 0, -90),
        ('R3', 100, 0, 90),
        ('R8', 100, 0, 90),
        ('R9', 100, 0, 90),
        ('U1', 120, 135, 0),
        ('U2', 0, 0, -90),
        ('D1', 15, 0, 0),
        ('D2', 15, 0, 0),
        ('D3', 50, 90, -90),
        ('SW1', 0, 0, -90),
        ('J1', 0, 0, None),
        ('J2', 0, 0, None),
        ('J3', 0, 0, None),
    ]
    for mod_name, offset_length, offset_angle, text_angle in refs:
        mod = kad.get_mod( mod_name )
        pos, angle = kad.get_mod_pos_angle( mod_name )
        ref = mod.Reference()
        if text_angle == None:
            ref.SetVisible( False )
        else:
            ref.SetTextSize( pcbnew.wxSizeMM( 0.9, 0.9 ) )
            ref.SetThickness( pcbnew.FromMils( 7 ) )
            pos_ref = vec2.scale( offset_length, vec2.rotate( - (offset_angle + angle) ), pos )
            ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )
            ref.SetTextAngle( text_angle * 10 )
            ref.SetKeepUpright( False )

    refs = [ ('J3', (0, 90), (90, 0), [
            ('1', 'A5', 'SCK'),
            ('2', 'A6', 'MISO'),
            ('3', 'A7', 'MOSI'),
        ] ), ('J2', (90, 0), (0, 90), [
            ('1', 'A3', 'RX'),
            ('2', 'A2', 'TX'),
            ('3', 'nRST', 'nRST'),
            ('4', 'F1', 'F1'),
            ('5', 'F0', 'F0'),
            ('6', 'GND', 'GND'),
            ('7', '3V3', '3V3'),
        ] ), ('J1', (-90, 180), (0, -90), [
            ('1', '5V', '5V'),
            ('2', 'A9',  'SCL'),
            ('3', 'A10', 'SDA'),
            ('4', 'A13', 'DIO'),
            ('5', 'A14', 'CLK'),
            ('6', 'B3', 'SCK'),
            ('7', 'B4', 'MISO'),
            ('8', 'B5', 'MOSI'),
        ] ),
    ]
    for mod, angles1, angles2, pads in refs:
        for pad, text1, text2 in pads:
            pos = kad.get_pad_pos( mod, pad )
            angle_pos1, angle_text1 = angles1
            angle_pos2, angle_text2 = angles2
            for idx, layer in enumerate( ['F.SilkS', 'B.SilkS'] ):
                pos1 = vec2.scale( [65, 65][idx], vec2.rotate( angle_pos1 ), pos )
                pos2 = vec2.scale( 50, vec2.rotate( angle_pos2 ), pos )
                kad.add_text( pos1, angle_text1, text1, layer, (0.7, 0.7), 6,
                    pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )
                kad.add_text( pos2, angle_text2, text2, layer, (0.7, 0.7), 6,
                    pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER  )

    pos, angle = kad.get_mod_pos_angle( 'SW1' )
    kad.add_text( pos, angle + 90, 'BOOT0', 'F.SilkS', (0.85, 0.65), 6,
        pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER )

    pcbnew.Refresh()

if __name__=='__main__':
    main()
