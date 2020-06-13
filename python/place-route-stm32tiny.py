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
Dird  = kad.Directed # Directed
Dird2 = kad.OffsetDirected # Directed + Offsets
Strt2 = 10
ZgZg  = kad.ZigZag # ZigZag

Straight  = kad.Straight # Straight
Directed  = kad.Directed # Directed
OffsetStraight = 10
OffsetDirected = kad.OffsetDirected # Directed + Offsets
ZigZag  = kad.ZigZag # ZigZag
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

# mods
def move_mods( base_pos, base_angle, mods ):
    mrot = mat2.rotate( base_angle )
    for vals in mods:
        name, pos, angle = vals[:3]
        npos = vec2.add( base_pos, vec2.mult( mrot, pos ) )
        nangle = base_angle + angle
        if name == None:
            move_mods( npos, nangle, vals[3] )
        else:
            set_mod_pos_angle( name, npos, nangle )

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


# wires
def add_wire_straight( pnts, net, layer, width, radius = 0 ):
    rpnts = []
    for idx, curr in enumerate( pnts ):
        if idx == 0 or idx + 1 == len( pnts ):# first or last
            rpnts.append( curr )
            continue
        prev = pnts[idx-1]
        next = pnts[idx+1]
        vec_a = vec2.sub( prev, curr )
        vec_b = vec2.sub( next, curr )
        len_a = vec2.length( vec_a )
        len_b = vec2.length( vec_b )
        length = min( radius, len_a / 2, len_b / 2 )
        if length < 1:
            rpnts.append( curr )
        else:
            rpnts.append( vec2.scale( length / len_a, vec_a, curr ) )
            rpnts.append( vec2.scale( length / len_b, vec_b, curr ) )
    for idx, curr in enumerate( rpnts ):
        if idx == 0:
            continue
        prev = rpnts[idx-1]
        if vec2.distance( prev, curr ) > 1:
            kad.add_track( prev, curr, net, layer, width )

# params: (none)
def add_wire_directed( prms_a, prms_b, net, layer, width, radius ):
    pos_a, angle_a = prms_a
    pos_b, angle_b = prms_b
    dir_a = vec2.rotate( - angle_a )
    dir_b = vec2.rotate( - angle_b )
    xpos, _, _ = vec2.find_intersection( pos_a, dir_a, pos_b, dir_b )
    pnts = [pos_a, xpos, pos_b]
    add_wire_straight( pnts, net, layer, width, radius )

# params: pos, (offset length, offset angle) x n
def add_wire_offsets_straight( prms_a, prms_b, net, layer, width, radius ):
    pos_a, offsets_a = prms_a
    pos_b, offsets_b = prms_b
    pnts_a = [pos_a]
    pnts_b = [pos_b]
    for off_len_a, off_angle_a in offsets_a:
        pos_a = vec2.scale( off_len_a, vec2.rotate( - off_angle_a ), pos_a )
        pnts_a.append( pos_a )
    for off_len_b, off_angle_b in offsets_b:
        pos_b = vec2.scale( off_len_b, vec2.rotate( - off_angle_b ), pos_b )
        pnts_b.append( pos_b )
    pnts = pnts_a
    for pnt_b in reversed( pnts_b ):
        pnts.append( pnt_b )
    add_wire_straight( pnts, net, layer, width, radius )

# params: pos, (offset length, offset angle) x n, direction angle
def add_wire_offsets_directed( prms_a, prms_b, net, layer, width, radius ):
    # pos_a, off_len_a, off_angle_a, angle_a = prms_a
    # pos_b, off_len_b, off_angle_b, angle_b = prms_b
    pos_a, offsets_a, angle_a = prms_a
    pos_b, offsets_b, angle_b = prms_b
    pnts_a = [pos_a]
    pnts_b = [pos_b]
    for off_len_a, off_angle_a in offsets_a:
        pos_a = vec2.scale( off_len_a, vec2.rotate( - off_angle_a ), pos_a )
        pnts_a.append( pos_a )
    for off_len_b, off_angle_b in offsets_b:
        pos_b = vec2.scale( off_len_b, vec2.rotate( - off_angle_b ), pos_b )
        pnts_b.append( pos_b )
    # apos = vec2.scale( off_len_a, vec2.rotate( - off_angle_a ), pos_a )
    # bpos = vec2.scale( off_len_b, vec2.rotate( - off_angle_b ), pos_b )
    apos = pnts_a[-1]
    bpos = pnts_b[-1]
    dir_a = vec2.rotate( - angle_a )
    dir_b = vec2.rotate( - angle_b )
    xpos, _, _ = vec2.find_intersection( apos, dir_a, bpos, dir_b )
    # pnts = [pos_a, apos, xpos, bpos, pos_b]
    pnts = pnts_a
    pnts.append( xpos )
    for pnt_b in reversed( pnts_b ):
        pnts.append( pnt_b )
    add_wire_straight( pnts, net, layer, width, radius )

# params: parallel lines direction angle
def add_wire_zigzag( pos_a, pos_b, angle, net, layer, width, radius ):
    mid_pos = vec2.scale( 0.5, vec2.add( pos_a, pos_b ) )
    dir = vec2.rotate( - angle )
    mid_dir1 = vec2.rotate( - angle + 45 )
    mid_dir2 = vec2.rotate( - angle - 45 )
    _, ka1, _ = vec2.find_intersection( pos_a, dir, mid_pos, mid_dir1 )
    _, ka2, _ = vec2.find_intersection( pos_a, dir, mid_pos, mid_dir2 )
    mid_angle = (angle - 45) if abs( ka1 ) < abs( ka2 ) else (angle + 45)
    add_wire_directed( (pos_a, angle), (mid_pos, mid_angle), net, layer, width, radius )
    add_wire_directed( (pos_b, angle), (mid_pos, mid_angle), net, layer, width, radius )

def wire_mods( tracks ):
    for mod_a, pad_a, mod_b, pad_b, width, prms in tracks:
        layer = get_mod_layer( mod_a )
        pos_a, angle_a, net = get_pad_pos_angle_net( mod_a, pad_a )
        pos_b, angle_b, _   = get_pad_pos_angle_net( mod_b, pad_b )
        if type( prms ) == type( Straight ) and prms == Straight:
            add_wire_straight( [pos_a, pos_b], net, layer, width )
        elif prms[0] == Directed:
            dangle_a, dangle_b, radius = prms[1:]
            prms_a = (pos_a, angle_a + dangle_a)
            prms_b = (pos_b, angle_b + dangle_b)
            add_wire_directed( prms_a, prms_b, net, layer, width, radius )
        elif prms[0] == OffsetStraight:
            prms_a, prms_b, radius = prms[1:]
            offsets_a = []
            offsets_b = []
            for off_len_a, off_angle_a in prms_a:
                offsets_a.append( (off_len_a, angle_a + off_angle_a) )
            for off_len_b, off_angle_b in prms_b:
                offsets_b.append( (off_len_b, angle_b + off_angle_b) )
            add_wire_offsets_straight( (pos_a, offsets_a), (pos_b, offsets_b), net, layer, width, radius )
        elif prms[0] == OffsetDirected:
            prms_a, prms_b, radius = prms[1:]
            # off_len_a, off_angle_a, dir_angle_a = prms_a
            # off_len_b, off_angle_b, dir_angle_b = prms_b
            # prms2_a = (pos_a, off_len_a, angle_a + off_angle_a, angle_a + dir_angle_a)
            # prms2_b = (pos_b, off_len_b, angle_b + off_angle_b, angle_b + dir_angle_b)
            # off_len_a, off_angle_a, dir_angle_a = prms_a
            # off_len_b, off_angle_b, dir_angle_b = prms_b
            dir_angle_a = prms_a[1]
            dir_angle_b = prms_b[1]
            offsets_a = []
            offsets_b = []
            for off_len_a, off_angle_a in prms_a[0]:
                offsets_a.append( (off_len_a, angle_a + off_angle_a) )
            for off_len_b, off_angle_b in prms_b[0]:
                offsets_b.append( (off_len_b, angle_b + off_angle_b) )
            prms2_a = (pos_a, offsets_a, angle_a + dir_angle_a)
            prms2_b = (pos_b, offsets_b, angle_b + dir_angle_b)
            add_wire_offsets_directed( prms2_a, prms2_b, net, layer, width, radius )
        elif prms[0] == ZigZag:
            dangle, radius = prms[1:]
            add_wire_zigzag( pos_a, pos_b, angle_a + dangle, net, layer, width, radius )
##

# in mm
VIA_Size = [(1.0, 0.6), (0.8, 0.5), (0.7, 0.4)]

FourCorners = [(0, 0), (1, 0), (1, 1), (0, 1)]
FourCorners2 = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
PCB_Offset = (0, 0)
PCB_Width  = 1000
PCB_Height =  700

#angle_reg = 45
#angle_uC  = 45
#angle_jp = 18.36
#offset_jp = 26

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

    kad.drawRect( PCB_Rect, 'Edge.Cuts' )
    makeZones( PCB_Rect )

    #kad.add_text( (2370, 1045), 0, 'STM32F042K6\nBreakOut\n20/06/30', 'F.SilkS', (0.95, 0.95), 6,
    #    pcbnew.GR_TEXT_HJUSTIFY_RIGHT, pcbnew.GR_TEXT_VJUSTIFY_CENTER )

    ###
    ### Set mod positios
    ###
    kad.move_mods( (320, 350), 0, [
        # Pin headers
        ('J1', (-220, +300), 90),
        ('J2', (-220, -300), 90),
        # USB connector
        (None, (580, 0), 0, [
            ('J3', (0,  0), -90),
            ('R9',  (-40, -40), 0),
            ('R10', (-40, +40), 0),
        ] ),
        # mcu
        ('U1', (0, 0), -90),
        # pass caps
        (None, ( 222, -185),   0, [ ('C3', (0, 0), 0), ('C4', (0, 0), 0) ] ),
        (None, (-222,  185), 180, [ ('C5', (0, 0), 0), ('C6', (0, 0), 0) ] ),
        (None, (  60, -185),   0, [ ('C7', (0, 0), 0), ('C8', (0, 75), 0) ] ),
        # USB DM/DP
        (None, (160, 120), 0, [ ('R7', (0, 0), 180), ('R8', (0, 75), 180) ] ),
        # I2C pull-up's
        (None, (-100, 155), 0, [ ('R5', (0, 0), 90), ('R6', (75, 0), 90) ] ),
        # regulators
        (None, (0, 0), 0, [
            ('U2', (   0,  7), 90),
            ('C1', ( 100,  0), 90),
            ('C2', (-100,  0), 90),
            ('L1', ( 175,  0), 90),
            ('F1', ( 222, -110), 180),
        ] ),
        # NRST
        ('C9', (-120, -180), 180),
        # SW1 (BOOT0)
        ('SW1', (550, -280), -90),
        ('R4', (250, -50), 90),
        # D1 (power)
        (None, (530, 300), 0, [ ('D1', (0, 0), 180), ('R1', (0, 0), 0)  ] ),
        # D2, D3
        (None, (-250, -120), 0, [ ('D2', (0, 0), 90), ('R2', (0, 0), -90) ] ),
        (None, (-250,   50), 0, [ ('D3', (0, 0), 90), ('R3', (0, 0), -90) ] ),
    ] )

    ###
    ### Wire mods
    ###

    PH_OFFSET = 20
    PH_ANGLE = 22

    wire_mods( [
        ### mcu
        # I2C pull-up
        ('U2', '1', 'R6', '2', 24, (Dird2, ([(8, 180)], -60), ([(9, -90)], 150), 0)),
        ('R5', '2', 'R6', '2', 24, (Strt)),
        # pass caps
        ('U1', '1', 'C3', '1', 20, (ZgZg, +90, 5)),
        ('U1','32', 'C3', '2', 20, (Dird2, ([(-27, 0)], -90), ([], 45), 5)),
        ('U1','17', 'C5', '1', 20, (ZgZg, -90, 5)),
        ('U1','16', 'C5', '2', 20, (Dird2, ([(+27, 0)], -90), ([], 45), 5)),
        # pass caps: Vdda
        ('U1', '5', 'C8', '1', 20, (Dird, 0, 0, 5)),
        ('U1','32', 'C8', '2', 20, (Dird, 0, 0, 5)),
        ('C7', '1', 'C8', '1', 24, (Strt)),
        ('C7', '2', 'C8', '2', 24, (Strt)),
        # I/Os
        # J2 front
        ('U1', '8', 'J2', '2', 20, (Dird2, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# PA2
        ('U1', '9', 'J2', '1', 20, (Dird2, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# PA3
        ('U1', '4', 'J2', '3', 20, (Dird2, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# NRST
        ('U1', '1', 'J2', '4', 20, (Dird2, ([], 0), ([(-PH_OFFSET, 0)], - 90 - PH_ANGLE), 5)),# Vdd
        # J2 back
        ('C9', '1', 'J2', '3', 20, (Dird2, ([], 90), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# NRST
        ('C7', '1', 'J2', '4', 20, (Dird2, ([], 90), ([(-PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# Vdd
        # J1 left
        ('U1','19', 'J1', '1', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA9
        ('U1','20', 'J1', '2', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA10
        ('U1','23', 'J1', '3', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA13
        ('U1','24', 'J1', '4', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA14
        # J1 right
        ('U1','26', 'J1', '5', 20, (Dird2, ([(35, 90)], 45), ([(PH_OFFSET, 0), ( 40, - 90 + PH_ANGLE)], 0), 15)),# PB3
        ('U1','27', 'J1', '6', 20, (Dird2, ([(55, 90)], 45), ([(PH_OFFSET, 0), ( 30, 90 - PH_ANGLE)], 0), 15)),# PB4
        ('U1','28', 'J1', '7', 20, (Dird2, ([(75, 90)], 45), ([(PH_OFFSET, 0), (100, 90 - PH_ANGLE)], 0), 15)),# PB5
        # I2C pull-up's
        ('R5', '1', 'J1', '1', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA9
        ('R6', '1', 'J1', '2', 20, (Dird2, ([], 0), ([(PH_OFFSET, 0)], - 90 + PH_ANGLE), 5)),# PA10
        # BOOT0
        #('SW1', '1', 'J2', '7', 20, (Dird, 90, 45, 5)),
        # LED D2&D3
        ('U1', '10', 'R2', '2', 20, (Dird, 90, 0, 10)),
        ('U1', '15', 'R3', '2', 20, (Dird, 90, 0, 10)),
        ### regulator
        #('J3','B9', 'F1', '1', 24, (ZgZg, 90, 10)),
        ('J3','B9', 'F1', '1', 24, (Dird2, ([(70, -90)], 0), ([],   0), 10)),
        ('J3','B9', 'J2', '6', 24, (Dird2, ([(70, -90)], 0), ([], 210), 10)),
        ('F1', '2', 'L1', '2', 24, (Dird, 90, -90, 10)),
        ('C1', '1', 'L1', '1', 24, (Strt)),
        ('C1', '2', 'L1', '2', 24, (Strt)),
        ('U2', '1', 'C1', '1', 24, (Dird, 90, 0, 10)),
        ('U2', '3', 'C1', '2', 24, (Dird, 90, 0, 10)),
        ('U2', '3', 'C2', '2', 24, (Dird, 90, 0, 10)),
        ('U2', '2', 'C2', '1', 24, (Dird, 90, 0, 10)),
        #
        ('C6', '1', 'C2', '1', 24, (Dird2, ([(-20, 0)], 90), ([], -90), 10)),
        ('C6', '1', 'C8', '1', 24, (Dird2, ([(-20, 0)], 90), ([(15, -90)], 0), 10)),
        ### USB
        # Type-C CC
        ('R9', '2', 'R10', '2', 24, (Strt)),
        # VBUS
        ('J3', 'A9', 'J3', 'B9', 14.8, (Strt2, [(19.9, 90), (40, 122), (30, 150)], [(19.9, 90), (40, 58), (30, 30)], 0)),
        # DM/DP
        ('J3', 'A6', 'J3', 'B6', 12, (Strt2, [(40, +90)], [(40, +90)], 9)),# DP
        ('J3', 'A7', 'J3', 'B7', 12, (Strt2, [(40, -90)], [(40, -90)], 9)),# DM
        # ('J3', 'B6', 'R8', '1', 12, (Dird2, (33, -90, -40), (20, -90, 0), 5)),# DP
        # ('J3', 'A7', 'R7', '1', 12, (Dird2, (47, -90, -40), (20, +90, 0), 5)),# DM
        ('J3', 'B6', 'R8', '1', 12, (Strt2, [(36, -90)], [(20, -90), (40, 180)], 5)),# DP
        ('J3', 'A7', 'R7', '1', 12, (Strt2, [(50, -90)], [(20, +90), (40, 180)], 5)),# DM
    ] )
    # USB: VBUS
    # pos_a, angle_a, net_a = kad.get_pad_pos_angle_net( 'J3', 'A9' )
    # pos_b, angle_b, net_b = kad.get_pad_pos_angle_net( 'J3', 'B9' )
    # pos, angle = kad.get_mod_pos_angle( 'J3' )
    # mid_pos = vec2.scale( -50, vec2.rotate( - angle ), pos )
    # add_wire_directed( (mid_pos, angle, , angle - 90, net_a, layer, 20, 5 )

    # # SW1
    # kad.wire_mods( [
    #     ('C6', '1',  'SW1', '1', 20, (Dird2, (0, 0), (35, 0), 0, 90 - angle_jp, 15)),
    #     ('U1', '31', 'SW1', '2', 20, (Dird2, (0, 0), (98, 0), -90 - angle_uC, angle_jp, 20)),
    # ] )
    # D1
    # kad.wire_mods( [
    #     ('R1', '2', 'J3', 'A9', 20, (Dird2, (0, 50, -90), (-90, 100, 10), 15)),# VBUS
    # ] )


    ###
    ### VIA
    ###

    # pad vias
    via_pads = [
        ('R1', '2'),
        ('R2', '1'),
        ('R3', '1'),
        ('C2', '2'),
        ('C3', '1'), ('C3', '2'),
        ('C5', '1'), ('C5', '2'),
        ('C8', '1'), ('C8', '2'),
    ]
    for mod_name, pad_name in via_pads:
        pos, net = kad.get_pad_pos_net( mod_name, pad_name )
        kad.add_via( pos, net, VIA_Size[1] )

    # # BOOT0
    # pos_via = vec2.scale( 86, vec2.rotate( -90 - angle_uC ), kad.get_pad_pos( 'U1', '31' ) )
    # pos_via = vec2.add( pos_via, (-1, 0) )
    # via_boot0 = kad.wire_mods_to_via( pos_via, VIA_Size[2], [
    #     #('U1', '31', 10, (Dird, 0, 90 - angle_uC, 15)),
    #     ('R4', '2', 20, (Dird, -angle_uC, angle_uC, 15)),
    # ] )
    # # VCC1
    # pos_via = vec2.scale( 55, vec2.rotate( 90 ), kad.get_pad_pos( 'C5', '1' ) )
    # via_vcc1 = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('U1', '1', 23, (Dird, - 135 - angle_uC, - 180 - angle_uC, 15)),
    #     ('C5', '1', 30, (Dird, -45, 90, 15)),
    #     ('R6', '2', 30, (Dird, 90, 0, 15)),
    # ] )
    # # GND1
    # pos_via = vec2.scale( -55, vec2.rotate( 90 ), kad.get_pad_pos( 'C5', '2' ) )
    # via_gnd1 = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('U1', '32', 23, (Dird, -135 - angle_uC, 90 - angle_uC, 15)),
    #     ('C5', '2',  30, (Dird, -45, 90, 15)),
    # ] )
    # # VCCA
    # pos_via = vec2.scale( -60, vec2.rotate( 180 - angle_uC ), kad.get_pad_pos( 'U1', '5' ) )
    # via_vcca = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('U1', '5',  23, (Strt)),
    #     ('U1', '1',  23, (Dird2, (0, 0), vec2.scale( 45, vec2.rotate( -angle_uC ) ), - 90 - angle_uC, 0, 10)),
    #     ('U1', '17', 23, (Dird, 0, - angle_uC, 10)),
    #     ('C7', '1',  30, (Dird, - angle_uC, 90 - angle_uC, 10)),
    #     ('C8', '1',  30, (Strt)),
    # ] )
    # # VCC reg
    # pos_via = (1980, 760)
    # via_vcc_reg = kad.wire_mods_to_via( pos_via, VIA_Size[2], [
    #     ('J2', '3',  20, (Dird2, (0, 0), (0, offset_jp), 0, -angle_jp, 10)),
    #     ('U2', '4',  20, (Dird, 0, 180 - angle_reg, 10)),
    # ] )
    # # NRST
    # pos_r6, _ = kad.get_mod_pos_angle( 'R6' )
    # pos_via, _, _ = vec2.find_intersection( pos_r6, vec2.rotate( 0 ), kad.get_pad_pos( 'U1', '4' ), vec2.rotate( -angle_uC ) )
    # pos_via = vec2.add( pos_via, (1, 0) )
    # via_nrst = kad.wire_mods_to_via( pos_via, VIA_Size[2], [
    #     ('U1', '4', 20, (Dird, 90, - angle_uC , 15) ),
    #     ('C9', '1', 15, (Dird, 0, -45, 15)),
    # ] )
    # # D1
    # pos_via = vec2.scale( 50, vec2.rotate( 0 ), kad.get_pad_pos( 'D1', '2' ) )
    # via_d1 = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('D1', '2', 20, (Strt)),
    #     ('R1', '1', 20, (Strt)),
    # ] )
    # # D2 & D3
    # pos_via = vec2.scale( 50, vec2.rotate( 90 ), kad.get_pad_pos( 'D2', '2' ) )
    # via_d2 = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('D2', '2', 20, (Strt)),
    #     ('R2', '1', 20, (Strt)),
    # ] )
    # pos_via = vec2.scale( 50, vec2.rotate( 90 ), kad.get_pad_pos( 'D3', '2' ) )
    # via_d3 = kad.wire_mods_to_via( pos_via, VIA_Size[1], [
    #     ('D3', '2', 20, (Strt)),
    #     ('R3', '1', 20, (Strt)),
    # ] )
    # # D+/- <--> U1
    # pos_via = vec2.scale( 85, vec2.rotate( 180 - angle_uC ), kad.get_pad_pos( 'U1', '22' ) )
    # via_dp = kad.wire_mods_to_via( pos_via, VIA_Size[2], [
    #     ('U1', '22', 20, (Strt)),
    #     ('R8', '2',  20, (Dird2,
    #         vec2.scale( 20, vec2.rotate( 180 - angle_uC ) ),
    #         vec2.scale( +10, vec2.rotate( - angle_reg ) ),
    #         90, 90 - angle_reg, 15 )),
    # ] )
    # pos_via = vec2.scale( 60, vec2.rotate( 180 - angle_uC ), kad.get_pad_pos( 'U1', '21' ) )
    # pos_via = vec2.add( pos_via, (0, 1) )
    # via_dn = kad.wire_mods_to_via( pos_via, VIA_Size[2], [
    #     ('U1', '21', 20, (Dird, 0, - angle_uC, 15 )),
    #     ('R7', '2',  20, (Dird2,
    #         vec2.scale( 20, vec2.rotate( 180 - angle_uC ) ),
    #         vec2.scale( -10, vec2.rotate( - angle_reg ) ),
    #         90, 90 - angle_reg, 15 )),
    # ] )
    # # D+/- <--> J3
    # via_dp2 = kad.wire_mods_to_via( (1830, 1225), VIA_Size[2], [
    #     ('R8', '1', 15.5, (Dird2, (0, 0), vec2.scale( +20, vec2.rotate( - angle_reg ) ), 0, 90 - angle_reg, 15 )),
    #     ('J3', '3', 15.5, (Dird2, (0, 0), (-48, 0), 0, 180 - angle_reg, 5 )),
    # ] )
    # via_dn2 = kad.wire_mods_to_via( (1830, 1200), VIA_Size[2], [
    #     ('R7', '1', 15.5, (Dird2, (0, 0), vec2.scale( -20, vec2.rotate( - angle_reg ) ), 0, 90 - angle_reg, 15 )),
    #     ('J3', '2', 15.5, (Dird2, (0, 0), (-60, 0), 0, 180 - angle_reg, 5 )),
    # ] )
    # pcb.Delete( via_vcc_reg )
    # pcb.Delete( via_dp2 )
    # pcb.Delete( via_dn2 )

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
