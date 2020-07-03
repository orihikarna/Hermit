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

pcb = pcbnew.GetBoard()

# alias
Strt  = kad.Straight # Straight
Strt2 = kad.OffsetStraight
Dird  = kad.OffsetDirected # Directed + Offsets
ZgZg  = kad.ZigZag # ZigZag

Round = kad.Round
BezierRound = kad.BezierRound
##

# in mm
VIA_Size = [(1.1, 0.6), (0.9, 0.5), (0.8, 0.4), (0.6, 0.3)]

FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
FourCorners2 = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
PCB_Width  = 960
PCB_Height = 700


def drawEdgeCuts():
    layer = 'Edge.Cuts'
    width = 2
    W = PCB_Width
    H = PCB_Height

    corners = []
    ### top
    corners.append( [((W/2,  0), 0), Round, [40]] )
    ### right
    corners.append( [((W, 100), 90), Round, [40]] )
    # USB
    pos, _ = kad.get_mod_pos_angle( 'J4' )
    corners.append( [((W+16, pos[1] - 180),   0), Round, [12]] )
    corners.append( [((W+38, pos[1]      ),  90), Round, [12]] )
    corners.append( [((W+16, pos[1] + 180), 180), Round, [12]] )
    corners.append( [((W,    H-100),         90), Round, [12]] )
    ### bottom
    corners.append( [((W/2, H), 180), Round, [40]] )
    ### left
    corners.append( [((0, H - 50), -90), Round, [40]] )
    if True:# LED (80mils in 200mils = 60mils each on above and below)
        pos, _ = kad.get_mod_pos_angle( 'D3' )
        corners.append( [((-20, pos[1] + 70), -117), BezierRound, [9]] )
        corners.append( [((-10, pos[1] + 40),    0), BezierRound, [9]] )
        corners.append( [((  0, pos[1]     ),  -90), Round, [9]] )
        corners.append( [((-10, pos[1] - 40),  180), Round, [9]] )
        corners.append( [((-20, pos[1] - 70),  -63), BezierRound, [9]] )
        corners.append( [((0, 50), -90), BezierRound, [9]] )
    # draw
    kad.draw_closed_corners( corners, layer, width )


def makeZones( rect ):
    layer_F_Cu = pcb.GetLayerID( 'F.Cu' )
    layer_B_Cu = pcb.GetLayerID( 'B.Cu' )
    zones = []
    for layer in [layer_F_Cu, layer_B_Cu]:
        zone, poly = kad.add_zone( rect, layer, len( zones ) )
        zone.SetZoneClearance( pcbnew.FromMils( 12 ) )
        #zone.SetMinThickness( pcbnew.FromMils( 10 ) )
        zone.SetThermalReliefGap( pcbnew.FromMils( 12 ) )
        #zone.SetThermalReliefCopperBridge( pcbnew.FromMils( 24 ) )
        zone.Hatch()
        #
        zones.append( zone )
        #polys.append( poly )

def main():
    kad.removeDrawings()
    kad.removeTracksAndVias()

    #PCB_Rect = map( lambda pt: (PCB_Width * pt[0], PCB_Height * pt[1]), FourCorners )
    #kad.drawRect( PCB_Rect, 'Edge.Cuts', R = 40 )
    drawEdgeCuts()

    Zone_Rect = map( lambda pt: ((PCB_Width + 50) * pt[0], (PCB_Height) * pt[1]), FourCorners )
    makeZones( Zone_Rect )

    kad.add_text( (470, 405), 0, '   STM32\n   F042K6\n     tiny\n   orihikarna\n200621', 'F.SilkS', (0.9, 0.9), 6,
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
        (None, (595, -5), 0, [
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
            (None, (0,  0), 0, [ ('D1', (0, 0), 0), ('R1', (0, 0), 0) ] ),
            (None, (0, 75), 0, [ ('D2', (0, 0), 0), ('R2', (0, 0), 0) ] ),
        ] ),
        # mcu
        (None, (30, 0), 0, [
            ('U1', (0, 0), -90),
            # pass caps
            (None, ( 245, -155), -90, [ ('C3', (0, 0), 0), ('C4', (0, 0), 0) ] ),
            (None, (-245,  155), +90, [ ('C5', (0, 0), 0), ('C6', (0, 0), 0) ] ),
            # Vcca pass caps
            (None, ( 100, -115), 0, [ ('C7', (0, 0), 0), ('C8', (0, -75), 0) ] ),
        ] ),
        # D3
        ('D3', (-280, 150), 0),
        # NRST
        ('C9', (-80, -190), 180),
        # USB DM/DP
        (None, (180, 115), 0, [ ('R6', (0, 0), 180), ('R7', (-20, 75), 180) ] ),
        # I2C pull-up's
        (None, (-80, 155), 0, [ ('R4', (0, 0), 90), ('R5', (75, 0), 90) ] ),
        # regulators
        (None, (-14, 0), 0, [
            ('U2', (   0, 6), 90),
            ('C1', ( 104, 0), 90),
            ('C2', (-104, 0), 90),
            ('L1', ( 215, +37.5),   0),
            ('F1', ( 235, -37.5), 180),
        ] ),
    ] )

    ###
    ### Wire mods
    ###
    kad.wire_mods( [
        ### mcu pass caps
        # mcu <--> Vcc x 2
        ('U1', '1', 'C3', '1', 24, (ZgZg, 90, 45)),# Vcc
        ('U1','32', 'C3', '2', 24, (ZgZg, 90, 45)),# Gnd
        ('U1','17', 'C5', '1', 24, (ZgZg, 90, 45)),# Vcc
        ('U1','16', 'C5', '2', 24, (ZgZg, 90, 45)),# Gnd
        # Vcca
        ('C7', '1', 'C8', '1', 24, (Strt)),
        ('C7', '2', 'C8', '2', 24, (Strt)),
        # Vcc <--> Vcca
        ('C4', '1', 'C8', '1', 24, (Dird, 0, ([(50, 90)], 0), 5)),# Vcc
        ('C4', '2', 'C7', '2', 24, (Dird, 0, 0)),
        ### pin headers
        # J3
        ('U1', '13', 'J3', '3', 20, (Dird, 90, -45)),# PA7
        ('U1', '12', 'J3', '2', 20, (Dird, 90, ([(20, -90)], -45))),# PA6
        ('U1', '11', 'J3', '1', 20, (Dird, 90, ([(20, -90), (80, -45), (56, -90)], -45))),# PA5
        # J2 front
        ('U1', '9', 'J2', '1', 20, (Dird, 0, +45)),# PA3
        ('U1', '8', 'J2', '2', 20, (Dird, 0, +45)),# PA2
        ('U1', '4', 'J2', '3', 20, (Dird, 0, ([(80, -135), (20, -90)], +45))),# NRST
        ('U1', '3', 'J2', '4', 20, (Dird, 0, +45)),# PF1
        ('U1', '2', 'J2', '5', 20, (Dird, 0, -45)),# PF0
        ('C3', '1', 'J2', '7', 24, (Dird, 135, 0)),# Vcc
        ('SW1','1', 'J2', '7', 16, (Dird, 90, +45)),# Vcc
        # J2 back
        ('C9', '1', 'J2', '3', 20, (Dird, 90, 45)),# NRST
        # J1 left back (I2C pull-up's)
        ('R4', '1', 'J1', '2', 20, (Dird, 0, -45)),# PA9
        ('R5', '1', 'J1', '3', 20, (Dird, 0, -45)),# PA10
        # J1 left front
        ('U1','19', 'J1', '2', 20, (Dird, 0, ([(80, -45), (56, -90)], -45))),# PA9
        ('U1','20', 'J1', '3', 20, (Dird, 0, -45)),# PA10
        ('U1','23', 'J1', '4', 20, (Dird, 0, -45)),# PA13
        ('U1','24', 'J1', '5', 20, (Dird, 0, +45)),# PA14
        # J1 right (separation = 30 mils, 30 * sin(22.5) = 11.48, (30 - 11.5) x 1.414 ~ 26.2)
        ('U1','26', 'J1', '6', 20, (Dird, ([(40,      90), (12,      45)], 0), 45)),# PB3
        ('U1','27', 'J1', '7', 20, (Dird, ([(40+11.5, 90), (12+26.2, 45)], 0), 45)),# PB4
        ('U1','28', 'J1', '8', 20, (Dird, ([(40+23.0, 90), (12+52.4, 45)], 0), ([(80, 45), (56, 90)], 45))),# PB5
        ### regulator
        ('F1', '2', 'L1', '2', 24, (ZgZg, 0, 70)),
        ('C1', '1', 'L1', '1', 24, (Strt)),
        ('U2', '1', 'C1', '1', 24, (Dird, 90, 0)),# 5V
        ('U2', '3', 'C1', '2', 24, (Dird, 90, 0)),# Gnd
        ('U2', '3', 'C2', '2', 24, (Dird, 90, 0)),# Gnd
        ('U2', '2', 'C2', '1', 24, (Dird, 90, 0)),# Vcc
        # Gnd: C1 <--> C7
        ('C1', '2', 'C7', '2', 24, (ZgZg, 90, 70)),
        # Vcc: C2 <--> C6
        ('C2', '1', 'C6', '1', 24, (Dird, ([(48, 90), (0, 0)], 0), -90, 25)),
        ### NRST C9
        ('C9', '2', 'C6', '2', 16, (Dird, 0, ([(18, -90)], 0), 25)),# Gnd
        ### I2C pull-up's
        ('R4', '2', 'R5', '2', 24, (Strt)),# 5V
        # 5V: regulator <--> I2C <--> J1
        ('R5', '2', 'U2', '1', 24, (ZgZg, 0, 60)),# 5V
        ('R4', '2', 'J1', '1', 24, (Dird, ([(50, 90)], 0), ([(56, 0)], -90), 25)),# 5V
        ### J4 (USB)
        # VBUS A4 <--> B4
        # ('J4', 'A4', 'J4', 'B4', 12.4, (Strt2,
        #     [(-3.1, 0), (15, 90), (24,  60), (40, 90), (40,  45)],
        #     [(+3.1, 0), (15, 90), (24, 120), (40, 90), (40, 135)], 5)),
        ('J4', 'A4', 'J4', 'B4', 20, (Strt2,
            [(-1, 0), (32, 90), (12,  60), (30, 90), (40,  45)],
            [(+1, 0), (32, 90), (12, 120), (30, 90), (40, 135)], 5)),
        # DM/DP
        ('J4', 'A7', 'J4', 'B7', 11.72, (Strt2, [(48, -90)], [(48, -90)], 9)),# DM
        ('J4', 'A6', 'J4', 'B6', 11.72, (Strt2, [(48, +90)], [(48, +90)], 9)),# DP
        # DM/DP <--> R6, R7
        ('J4', 'A7', 'R6',  '1', 11.72, (Dird, ([(118, -90), (75, 0), (20, -90)], 0), ([(26, +90)], 0), 10)),# DM
        ('J4', 'B6', 'R7',  '1', 11.72, (Dird, ([( 96, -90), (75, 0), (20, -90)], 0), ([(26, -90)], 0), 10)),# DP
        # Gnd: B1 <--> D1
        ('J4', 'B1', 'D1', '1', 23.5, (Dird, ([(58, -90), (85, 0)], 90), 135)),
        # Gnd: USB CC/BOOT0
        ('R8', '2', 'R9', '2', 20, (Strt)),
        ('R8', '2', 'R3', '2', 20, (Strt)),
        ### BOOT0: mcu <--> R3
        ('U1', '31', 'R3', '1', 16, (Dird, ([(50, 90), (10, 0), (60, 90), (-10, 0)], 90), 90, 30)),
        ### D3
        ('C5', '2', 'D3', '2', 20, (Dird, 90, ([(10, 0)], 90))),# Gnd
        ('D3', '4', 'J1', '1', 20, (Dird, ([(10, 0)], 90), 90)),# 5V
    ] )

    ###
    ### VIA
    ###
    layer_F_Cu = pcb.GetLayerID( 'F.Cu' )
    layer_B_Cu = pcb.GetLayerID( 'B.Cu' )

    # pad vias
    via_pads = [
        ('R1', '2'), ('R2', '2'),
        ('C3', '1'), ('C3', '2'),
        ('C5', '1'), ('C5', '2'),
    ]
    for mod_name, pad_name in via_pads:
        pos, net = kad.get_pad_pos_net( mod_name, pad_name )
        kad.add_via( pos, net, VIA_Size[1] )

    # Vcca
    kad.wire_mods_to_via( (60, 0), VIA_Size[0], [
        ('U1', '5', 24, (Dird, 90, 0)),
        ('C2', '1', 24, (Dird, 90, ([(48, 90), (0, 0)], 0), 25)),
        ('C7', '1', 24, (Dird, 90, 90)),
    ] )
    # Gnd: C3, J4/A1, J2/6
    kad.wire_mods_to_via( (-40, -65), VIA_Size[0], [
        ('C3', '2', 24, (Dird, -45, 90)),
        ('C4', '2', 24, (Dird, -45, 90)),
        ('J4', 'A1', 23.5, (Dird, 0, 90, 25)),
        ('J2', '6', 24, (Dird, 0, ([(15, 0)], 45), 0), 'B.Cu'),
    ] )
    # Gnd: U2
    kad.wire_mods_to_via( (0, +45), VIA_Size[1], [ ('U2', '3', 20, (Strt)) ] )
    kad.wire_mods_to_via( (0, -45), VIA_Size[1], [ ('U2', '3', 20, (Strt)) ] )
    # USB DM/DP <--> mcu
    kad.wire_mods_to_via( (-55, -26), VIA_Size[2], [
        ('U1', '21', 20, (Dird, 90, 0, 5)),
        ('R6',  '2', 20, (Dird, 0,  0, 5)),
    ] )
    kad.wire_mods_to_via( (55, 4), VIA_Size[2], [
        ('U1', '22', 20, (Dird, 90, 0, 5)),
        ('R7',  '2', 20, (Dird, 0,  0, 5)),
    ] )
    # J4/A4,B4 VBUS
    via_a = kad.wire_mods_to_via( (-55, 0), VIA_Size[1], [
        ('F1',  '1', 24, (Dird, -30, 0)),
        ('J4', 'A4', 23.5, (Dird, 90, 90, 30)),
    ] )
    via_b = kad.wire_mods_to_via( (-23, 59), VIA_Size[1], [
        ('J4', 'B4', 23.5, (Dird, 0, 90)),
        ('R1', '1',  20, (Dird, 0, ([(22, 90)], 0), 30)),
    ] )
    pos_a, net = kad.get_via_pos_net( via_a )
    pos_b, _   = kad.get_via_pos_net( via_b )
    kad.add_wire_zigzag( pos_a, pos_b, 90, 45, net, layer_F_Cu, 24, 5 )
    # J4: CC
    kad.wire_mods_to_via( (+22, -64), VIA_Size[2], [
        ('J4', 'A5', 11.72, (Dird, 0, ([(39, 90)], +60), 3)),
        ('R8',  '1', 16, (Dird, 90, 90, 25)),
    ] )
    kad.wire_mods_to_via( (-22, -64), VIA_Size[2], [
        ('J4', 'B5', 11.72, (Dird, 0, ([(39, 90)], -60), 3)),
        ('R9',  '1', 16, (Dird, 90, 90, 25)),
    ] )
    # SW1: BOOT0 <--> R3 pull-down
    kad.wire_mods_to_via( (0, 120), VIA_Size[2], [
        ('SW1', '2', 16, (Dird, 90, ([(130, -90)], 0), 15)),
        ('R3',  '1', 16, (Dird, 0, 0, 15)),
    ] )
    # mcu PA15 <--> R2
    via_a = kad.wire_mods_to_via( (135, 0), VIA_Size[1], [
        ('U1', '25', 20, (Dird, 90, 0)),# PA15
    ] )
    via_b = kad.wire_mods_to_via( (-60, -60), VIA_Size[1], [
        ('R2', '1', 20, (Dird, 90, 0, 100)),
    ] )
    pos_a, net = kad.get_via_pos_net( via_a )
    pos_b, _   = kad.get_via_pos_net( via_b )
    kad.add_wire_offsets_directed( (pos_a, [], 0), (pos_b, [], 90), net, layer_B_Cu, 20, 0 )
    # D3 <--> PB1
    kad.wire_mods_to_via( (40, -65), VIA_Size[2], [
        ('D3',  '3', 16, (Dird, 0, ([(10, 0)], 90), 10)),
        ('U1', '15', 16, (ZgZg, 0, 40)),
    ] )

    ###
    ### Ref
    ###
    refs = [
        ('C1', 115, 30,  90),
        ('C2', 100,  0,  90),
        ('C3', -60, 90, 180),
        ('C4',  60, 90, 180),
        ('C5', -60, 90, 180),
        ('C6', -70, 60, 180),
        ('C7',  90,  0,  90),
        ('C8',  90,  0,  90),
        ('C9', -90,  0,  -90),
        ('R1', -15, 0, 0),
        ('R2', -15, 0, 0),
        ('R4',  70, 60, 180),
        ('R5', -70,120, 180),
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
        ('D3', 70, 90, -90),
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
                pos1 = vec2.scale( [70, 50][idx], vec2.rotate( angle_pos1 ), pos )
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
