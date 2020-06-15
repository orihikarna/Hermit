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

##
def sign( v ):
    if v > 0:
        return +1
    if v < 0:
        return -1
    return 0

# mod
def get_mod( mod_name ):
    return pcb.FindModuleByReference( mod_name )

def get_mod_layer( mod_name ):
    mod = get_mod( mod_name )
    return mod.GetLayer()

def get_mod_pos_angle( mod_name ):
    mod = get_mod( mod_name )
    return (pnt.unit2mils( mod.GetPosition() ), mod.GetOrientation() / 10)

def set_mod_pos_angle( mod_name, pos, angle ):
    mod = get_mod( mod_name )
    if pos != None:
        mod.SetPosition( pnt.mils2unit( vec2.round( pos ) ) )
    mod.SetOrientation( 10 * angle )
    return mod


# pad
def get_pad( mod_name, pad_name ):
    mod = get_mod( mod_name )
    return mod.FindPadByName( pad_name )

def get_pad_pos( mod_name, pad_name ):
    pad = get_pad( mod_name, pad_name )
    return pnt.unit2mils( pad.GetPosition() )

def get_pad_pos_net( mod_name, pad_name ):
    pad = get_pad( mod_name, pad_name )
    return pnt.unit2mils( pad.GetPosition() ), pad.GetNet()

def get_pad_pos_angle_net( mod_name, pad_name ):
    mod = get_mod( mod_name )
    pad = get_pad( mod_name, pad_name )
    return (pnt.unit2mils( pad.GetPosition() ), mod.GetOrientation() / 10, pad.GetNet())

# def get_pos_angle_from_pad( mod_name, pad_name, prms ):
#     pos, angle, _ = get_pad_pos_angle_net( mod_name, pad_name )
#     offset_angle, offset_length, dangle = prms
#     offset = vec2.scale( offset_length, vec2.rotate( angle + offset_angle ) )
#     return vec2.add( pos, offset ), angle + dangle

def wire_mods_to_via( offset_vec, size_via, tracks ):
    for idx, track in enumerate( tracks ):
        mod_name, pad_name, width, prms = track[:4]
        if len( track ) > 4:
            layer = pcb.GetLayerID( track[4] )
        else:
            layer = get_mod_layer( mod_name )
        pos, angle, net = get_pad_pos_angle_net( mod_name, pad_name )
        if idx == 0:
            angle_via = angle
            pos_via = vec2.mult( mat2.rotate( angle ), offset_vec, pos )
            via = kad.add_via( pos_via, net, size_via )
        kad.__add_wire( pos_via, angle_via, pos, angle, net, layer, width, prms )
    return via

def get_via_pos_net( via ):
    return pnt.unit2mils( via.GetPosition() ), via.GetNet()

##

# in mm
VIA_Size = [(1.1, 0.6), (0.9, 0.5), (0.8, 0.4)]

FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
FourCorners2 = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
PCB_Offset = (0, 0)
PCB_Width  = 950
PCB_Height = 700

def makeZones( rect ):
    layer_F_Cu = pcb.GetLayerID( 'F.Cu' )
    layer_B_Cu = pcb.GetLayerID( 'B.Cu' )
    zones = []
    for layer in [layer_F_Cu, layer_B_Cu]:
        zone, poly = kad.add_zone( rect, layer, len( zones ) )
        zone.SetZoneClearance( pcbnew.FromMils( 12 ) )
        zone.SetMinThickness( pcbnew.FromMils( 10 ) )
        zone.SetThermalReliefGap( pcbnew.FromMils( 12 ) )
        zone.SetThermalReliefCopperBridge( pcbnew.FromMils( 24 ) )
        zone.Hatch()
        #
        zones.append( zone )
        #polys.append( poly )

def main():
    kad.removeDrawings()
    kad.removeTracksAndVias()

    PCB_Rect = map( lambda pt: vec2.add( PCB_Offset, (PCB_Width * pt[0], PCB_Height * pt[1]) ), FourCorners )

    kad.drawRect( PCB_Rect, 'Edge.Cuts', R = 60 )
    makeZones( PCB_Rect )

    #kad.add_text( (2370, 1045), 0, 'STM32F042K6\nBreakOut\n20/06/30', 'F.SilkS', (0.95, 0.95), 6,
    #    pcbnew.GR_TEXT_HJUSTIFY_RIGHT, pcbnew.GR_TEXT_VJUSTIFY_CENTER )

    angle_mcu = -98

    ###
    ### Set mod positios
    ###
    kad.move_mods( (300, 350), 0, [
        # Pin headers
        ('J1', (-235, +300), 90),
        ('J2', (-235, -300), 90),
        # USB connector
        (None, (580, 30), 0, [
            ('J3', (0,  0), -90),
            ('R4',  (-40, -100), 0),# BOOT0 pull-down
            ('R9',  (-40,    0), 0),
            ('R10', (-40, +100), 0),
        ] ),
        # mcu
        ('U1', (0, 0), angle_mcu),
        # pass caps
        (None, ( 250, -155),   0, [ ('C3', (0, 0), -90), ('C4', (0, 0), -90) ] ),
        (None, (-250,  155), 180, [ ('C5', (0, 0), -90), ('C6', (0, 0), -90) ] ),
        # Vdda pass caps
        (None, ( 100, -155),   0, [ ('C7', (0, 0), -90), ('C8', (75, 0), -90) ] ),
        # NRST
        ('C9', (-80, -175), 180),
        # D2, D3
        (None, (-250, -155), 0, [ ('D2', (0, 0), 90), ('R2', (0, 0), -90) ] ),
        (None, (-250,    0), 0, [ ('D3', (0, 0), 90), ('R3', (0, 0), -90) ] ),
        # USB DM/DP
        (None, ( 175, 120), 0, [ ('R7', (0, 0), 180), ('R8', (0, 75), 180) ] ),
        # I2C pull-up's
        (None, (-120, 155), 0, [ ('R5', (0, 0), 90), ('R6', (75, 0), 90) ] ),
        # regulators
        (None, (-10, 0), 0, [
            ('U2', (   0,  7), 90),
            ('C1', ( 110,  0), 90),
            ('C2', (-110,  0), 90),
            ('L1', ( 185,  0), 90),
            ('F1', ( 260,  0), 90),
        ] ),
        # BOOT0 (SW1)
        ('SW1', (525, -270), -90),
        # D1 (power)
        (None, (530, 300), 0, [ ('D1', (0, 0), 0), ('R1', (0, 0), 0)  ] ),
    ] )

    ###
    ### Wire mods
    ###
    PH_OFFSET = 20
    PH_ANGLE = 22

    kad.wire_mods( [
        ### mcu
        ## pass caps
        # Vcc x 2
        ('U1', '1', 'C3', '1', 20, (Dird, ([(-30, 0)], -45), ([], -90), 5)),
        ('U1','32', 'C3', '2', 20, (Dird, ([], 90), ([], -45), 5)),
        ('U1','17', 'C5', '1', 20, (Dird, ([(+30, 0)], -45), ([], -90), 5)),
        ('U1','16', 'C5', '2', 20, (Dird, ([], 90), ([], -45), 5)),
        # Vdda
        ('C7', '1', 'C8', '1', 24, (Strt)),
        ('C7', '2', 'C8', '2', 24, (Strt)),
        ### pin headers
        # J2 front
        ('U1', '9', 'J2', '1', 20, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# PA3
        ('U1', '8', 'J2', '2', 20, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# PA2
        ('U1', '7', 'J2', '3', 20, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA1
        ('U1', '4', 'J2', '4', 20, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# NRST
        ('U1', '1', 'J2', '5', 20, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# Vdd
        # J2 back
        ('C9', '1', 'J2', '4', 20, (Dird, ([], 90), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# NRST
        ('C8', '1', 'J2', '5', 24, (Dird, ([], 0), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# Vdd
        ('SW1', '1', 'J2', '7', 20, (Dird, ([], 90), ([], 0), 5)),# SW1 <--> VBUS
        # J1 left
        ('R5', '1', 'J1', '1', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA9 (pull-up)
        ('R6', '1', 'J1', '2', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA10 (pull-up)
        ('U1','19', 'J1', '1', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA9
        ('U1','20', 'J1', '2', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA10
        ('U1','23', 'J1', '3', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA13
        ('U1','24', 'J1', '4', 20, (Dird, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA14
        # J1 right
        ('U1','26', 'J1', '5', 20, (Dird, ([(35, 90)], 45), ([(PH_OFFSET, 0), ( 40, - 90 + PH_ANGLE)], 0), 10)),# PB3
        ('U1','27', 'J1', '6', 20, (Dird, ([(55, 90)], 45), ([(PH_OFFSET, 0), ( 30, 90 - PH_ANGLE)], 0), 10)),# PB4
        ('U1','28', 'J1', '7', 20, (Dird, ([(75, 90)], 45), ([(PH_OFFSET, 0), (100, 90 - PH_ANGLE)], 0), 10)),# PB5
        # NRST <--> D2/D3,C6
        ('C9', '2', 'D2', '1', 20, (Dird, ([], 0), ([(50, -90)], 0), 10)),# Gnd
        ('C9', '2', 'D3', '1', 20, (Dird, ([], 0), ([(50, -90)], 0), 10)),# Gnd
        ('C9', '2', 'C6', '2', 20, (Dird, ([], 0), ([(50, -90)], 0), 10)),# Gnd
        # I2C pull-up <--> 5V
        ('R5', '2', 'R6', '2', 24, (Strt)),
        ('U2', '1', 'R6', '2', 24, (Strt)),
        # LED D2,D3 <--> mcu
        ('U1', '10', 'R2', '2', 20, (Dird, ([], 90), ([], 0), 10)),
        ('U1', '15', 'R3', '2', 20, (Dird, ([], 90), ([], 0), 10)),
        # LED D2,D3 <--> pass cap
        #('C6', '2', 'D3', '1', 20, (Dird, ([], 90), ([], 0), 10)),# Gnd
        ### regulator
        ('F1', '2', 'L1', '2', 24, (Dird, ([], 0), ([], -90), 10)),
        ('C1', '1', 'L1', '1', 24, (Strt)),
        ('U2', '1', 'C1', '1', 24, (Dird, ([], 90), ([], 0), 10)),
        ('U2', '3', 'C1', '2', 24, (Dird, ([], 90), ([], 0), 10)),
        ('U2', '3', 'C2', '2', 24, (Dird, ([], 90), ([], 0), 10)),
        ('U2', '2', 'C2', '1', 24, (Dird, ([], 90), ([], 0), 10)),
        # pass cap C6 <--> C2
        ('C6', '1', 'C2', '1', 20, (Dird, ([], 90), ([(50, 90)], 0), 10)),# Vcc
        ### USB
        # DM/DP
        ('J3', 'A6', 'J3', 'B6', 11.72, (Strt2, [(40, +90)], [(40, +90)], 9)),# DP
        ('J3', 'A7', 'J3', 'B7', 11.72, (Strt2, [(40, -90)], [(40, -90)], 9)),# DM
        ('J3', 'B6', 'R8',  '1', 11.72, (Strt2, [(56, -90)], [(20, -90), (40, 180)], 5)),# DP
        ('J3', 'A7', 'R7',  '1', 11.72, (Strt2, [(70, -90)], [(20, +90), (40, 180)], 5)),# DM
    ] )

    ###
    ### VIA
    ###

    # pad vias
    via_pads = [
        ('R1', '2'),
        ('R2', '1'),
        ('R3', '1'),
        ('C3', '1'), ('C3', '2'),
        ('C5', '1'), ('C5', '2'),
    ]
    for mod_name, pad_name in via_pads:
        pos, net = kad.get_pad_pos_net( mod_name, pad_name )
        kad.add_via( pos, net, VIA_Size[1] )

    # Vdda
    wire_mods_to_via( (65, 0), VIA_Size[1], [
        ('U1', '5', 20, (Dird, ([], 90), ([], 0), 5)),
        ('C2', '1', 20, (Dird, ([], -angle_mcu), ([(50, +90)], 0), 5)),
        ('C7', '1', 20, (Dird, ([], -angle_mcu), ([(50, -90)], 0), 5)),
    ] )
    # Gnd: U2
    wire_mods_to_via( (0, +45), VIA_Size[1], [ ('U2', '3', 20, (Strt)) ] )
    wire_mods_to_via( (0, -45), VIA_Size[1], [ ('U2', '3', 20, (Strt)) ] )
    # Gnd: D1
    wire_mods_to_via( (15, -95), VIA_Size[0], [ ('D1', '1', 20, (Dird, ([], 0), ([], 90), 5)) ] )
    # USB DM/DP <--> mcu
    wire_mods_to_via( (-55, -30), VIA_Size[2], [
        ('U1', '21', 20, (Dird, ([], 90), ([], 0), 5)),
        ('R7',  '2', 20, (Dird, ([], 0), ([], 0), 5)),
    ] )
    wire_mods_to_via( (55, 5), VIA_Size[2], [
        ('U1', '22', 20, (Dird, ([], 90), ([], 0), 5)),
        ('R8',  '2', 20, (Dird, ([], 0), ([], 0), 5)),
    ] )
    # J3: CC
    wire_mods_to_via( (20, -55), VIA_Size[2], [
        ('J3', 'A5', 11.72, (Dird, ([], 45), ([], 90), 5)),
        ('R9',  '1', 16, (Dird, ([], 45), ([], 0), 5)),
    ] )
    wire_mods_to_via( (5, -55), VIA_Size[2], [
        ('J3', 'B5', 11.72, (Dird, ([], 45), ([], 90), 5)),
        ('R10', '1', 16, (Dird, ([], 45), ([], 0), 5)),
    ] )
    # J3: VBUS
    via_a = wire_mods_to_via( (15, 55), VIA_Size[1], [
        ('J3', 'A4', 23.6, (Dird, ([], 0), ([], 90), 5)),
        ('J2',  '7', 20, (Dird, ([(90, 180)], 135), ([(20, -90)], 0), 5), 'F.Cu'),
        ('F1',  '1', 24, (Dird, ([], 0), ([], 128), 5))
    ] )
    via_b = wire_mods_to_via( (-5, 55), VIA_Size[1], [
        ('J3', 'B4', 23.6, (Dird, ([], 0), ([], 90), 5)),
        ('R1',  '1', 20, (Dird, ([], 0), ([(60, 90)], 0), 15)),
    ] )
    pos_a, net = get_via_pos_net( via_a )
    pos_b, _   = get_via_pos_net( via_b )
    kad.add_wire_straight( [pos_a, pos_b], net, pcb.GetLayerID( 'F.Cu' ), 24 )
    # SW1: BOOT0 <--> mcu
    wire_mods_to_via( (55, 270), VIA_Size[2], [
        ('SW1', '2', 16, (Dird, ([], 90), ([(125, -90)], 0), 15)),
        ('U1', '31', 16, (Dird, ([(40, -90)], 0), ([(50, 90)], 180 - angle_mcu), 15)),
    ] )
    # SW1: BOOT0 <--> pull-down
    wire_mods_to_via( (25, 125), VIA_Size[2], [
        ('SW1', '2', 16, (Dird, ([], 90), ([(130, -90)], 0), 15)),
        ('R4',  '1', 16, (Dird, ([], 0), ([], 0), 15)),
    ] )

    # # GND Vias
    # GND = pcb.FindNet( 'GND' )
    # pos_gnds = []
    # pos_gnds.append( (vec2.find_intersection(
    #     kad.get_pad_pos( 'U1', '23' ), vec2.rotate( 180 - angle_uC ),
    #     kad.get_pad_pos( 'U1', '29' ), vec2.rotate(  90 - angle_uC ) )[0], 1) )
    # for pos_gnd, size_idx in pos_gnds:
    #     kad.add_via( pos_gnd, GND, VIA_Size[size_idx] )

    # ###
    # ### Ref
    # ###
    # for mod in pcb.GetModules():
    #     pos = pnt.unit2mils( mod.GetPosition() )
    #     angle = mod.GetOrientation() / 10
    #     ref = mod.Reference()
    #     ref.SetTextSize( pcbnew.wxSizeMM( 1, 1 ) )
    #     ref.SetThickness( pcbnew.FromMils( 7 ) )
    #     name = ref.GetText()
    #     if name[0] in ['C', 'R', 'D']:
    #         if name == 'C1':
    #             sign = -1 if name in ['F1'] else +1
    #             pos_ref = vec2.scale( sign * 60, vec2.rotate( 90 - angle ), pos )
    #             ref.SetTextAngle( 0 * 10 )
    #         else:
    #             sign = -1 if name in ['D1', 'R2', 'R3', 'R4', 'C1'] else +1
    #             pos_ref = vec2.scale( sign * 95, vec2.rotate( -angle ), pos )
    #             ref.SetTextAngle( - sign * 90 * 10 )
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )
    #         ref.SetKeepUpright( False )
    #     if name[0] in ['L', 'F']:
    #         sign = -1 if name in ['F1'] else +1
    #         pos_ref = vec2.scale( sign * 60, vec2.rotate( 90 - angle ), pos )
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )
    #         ref.SetTextAngle( 0 * 10 )
    #     if name in ['J1', 'J2', 'SW1', 'SW2']:
    #         ref.SetVisible( False )
    #     if name in ['J3']:
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos ) ) )
    #     if name in ['U1']:
    #         pos_ref = vec2.scale( 120, vec2.rotate( 135 + angle ), pos )
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )
    #     if name in ['U2']:
    #         pos_ref = vec2.scale( 75, vec2.rotate( 90 - angle ), pos )
    #         ref.SetPosition( pnt.mils2unit( vec2.round( pos_ref ) ) )

    # refs = [ ('J2', [
    #         ('1', '5V'),
    #         ('2', 'GND'),
    #         ('3', '3V3'),
    #         ('4', 'A8'),
    #         ('5', 'TX\nA9'),
    #         ('6', 'RX\nA10'),
    #         ('7', 'DIO\nA13'),
    #         ('8', 'CLK\nA14'),
    #         ('9', 'A15'),
    #         ('10', 'B3'),
    #         ('11', 'B4'),
    #         ('12', 'B5'),
    #         ('13', 'B6'),
    #         ('14', 'B7'),
    #     ] ), ('J1', [
    #         ('1', 'GND'),
    #         ('2', 'B1'),
    #         ('3', 'B0'),
    #         ('4', 'A7'),
    #         ('5', 'A6'),
    #         ('6', 'A5'),
    #         ('7', 'A4'),
    #         ('8', 'A3'),
    #         ('9', 'A2'),
    #         ('10', 'A1'),
    #         ('11', 'A0'),
    #         ('12', 'nRST'),
    #         ('13', 'SCL\nF1'),
    #         ('14', 'SDA\nF0'),
    #     ] ),
    # ]
    # for mod, pads in refs:
    #     for pad, text in pads:
    #         sign = +1 if mod == 'J2' else -1
    #         pos = kad.get_pad_pos( mod, pad )
    #         pos = vec2.scale( sign * 42, vec2.rotate( 90 ), pos )
    #         if pad == '13':
    #             pos = vec2.add( pos, (12, 0) )
    #         if pad == '14':
    #             pos = vec2.add( pos, (24, 0) )
    #         for layer in ('F.SilkS', 'B.SilkS'):
    #             kad.add_text( pos, 90 + sign * 90, text, layer, (0.85, 0.65), 6,
    #                 pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_BOTTOM  )

    # refs = [
    #     ('SW1', 'BOOT0', (0.55, 0.7)),
    #     ('SW2', 'RST',   (0.9, 0.7)),
    # ]
    # for mod, text, size in refs:
    #     pos = kad.get_mod_pos_angle( mod )[0]
    #     for layer in ('F.SilkS', 'B.SilkS'):
    #         kad.add_text( pos, 90, text, layer, size, 6 )

    pcbnew.Refresh()

if __name__=='__main__':
    main()
