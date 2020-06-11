import pcbnew
import pnt
import vec2
import mat2

pcb = pcbnew.GetBoard()

Straight = 0
Directed = 1
OffsetDirected = 2
ZigZag = 3

def sign( v ):
    if v > 0:
        return +1
    if v < 0:
        return -1
    return 0

##
## Drawings
##
def add_line_rawunit( a, b, layer = 'Edge.Cuts', width = 2):
    if a[0] == b[0] and a[1] == b[1]:
        print( "add_line_rawunit: identical", a )
        return None
    line = pcbnew.DRAWSEGMENT()
    line.SetStart( a )
    line.SetEnd(   b )
    line.SetLayer( pcb.GetLayerID( layer ) )
    line.SetWidth( pcbnew.FromMils( width ) )
    pcb.Add( line )
    return line

def add_line( a, b, layer = 'Edge.Cuts', width = 2):
    pnt_a = pnt.mils2unit( vec2.round( a ) )
    pnt_b = pnt.mils2unit( vec2.round( b ) )
    if True:
        aa = pnt.unit2mils( pnt_a )
        bb = pnt.unit2mils( pnt_b )
        length = vec2.distance( bb, aa )
        if length == 0:
            print( "add_line: identical", a )
            return
        elif length < 0.001:
            #print( length, a, b )
            None
    line = pcbnew.DRAWSEGMENT()
    line.SetStart( pnt_a )
    line.SetEnd(   pnt_b )
    line.SetLayer( pcb.GetLayerID( layer ) )
    line.SetWidth( pcbnew.FromMils( width ) )
    pcb.Add( line )
    return line

def add_arc( ctr, pos, angle, layer = 'Edge.Cuts', width = 2 ):
    pnt_ctr = pnt.mils2unit( vec2.round( ctr ) )
    pnt_pos = pnt.mils2unit( vec2.round( pos ) )
    arc = pcbnew.DRAWSEGMENT()
    arc.SetShape( pcbnew.S_ARC )
    arc.SetCenter( pnt_ctr )
    arc.SetArcStart( pnt_pos )
    arc.SetAngle( 10 * angle )
    arc.SetLayer( pcb.GetLayerID( layer ) )
    arc.SetWidth( pcbnew.FromMils( width ) )
    pcb.Add( arc )
    return arc

def add_arc2( ctr, pos, end, angle, layer = 'Edge.Cuts', width = 2 ):
    pnt_ctr = pnt.mils2unit( vec2.round( ctr ) )
    pnt_pos = pnt.mils2unit( vec2.round( pos ) )
    pnt_end = pnt.mils2unit( vec2.round( end ) )
    arc = pcbnew.DRAWSEGMENT()
    arc.SetShape( pcbnew.S_ARC )
    arc.SetCenter( pnt_ctr )
    arc.SetArcStart( pnt_pos )
    arc.SetAngle( 10 * angle )
    arc.SetLayer( pcb.GetLayerID( layer ) )
    arc.SetWidth( pcbnew.FromMils( width ) )
    pcb.Add( arc )
    arc_start = arc.GetArcStart()
    arc_end = arc.GetArcEnd()
    if arc_start[0] != pnt_pos[0] or arc_start[1] != pnt_pos[1]:
        print( 'add_arc2: arc_start != pnt_pos !!' )
    if arc_end[0] != pnt_end[0] or arc_end[1] != pnt_end[1]:
        #print( 'arc_end != pnt_end !!' )
        add_line_rawunit( arc_end, pnt_end, layer, width )
    return arc

def add_text( pos, angle, string, layer = 'F.SilkS', size = (1, 1), thick = 5, hjustify = None, vjustify = None ):
    text = pcbnew.TEXTE_PCB( pcb )
    text.SetPosition( pnt.mils2unit( vec2.round( pos ) ) )
    text.SetTextAngle( angle * 10 )
    text.SetText( string )
    text.SetLayer( pcb.GetLayerID( layer ) )
    text.SetTextSize( pcbnew.wxSizeMM( size[0], size[1] ) )
    text.SetThickness( pcbnew.FromMils( thick ) )
    text.SetMirrored( layer[0] == 'B' )
    if hjustify != None:
        text.SetHorizJustify( hjustify )
    if vjustify != None:
        text.SetVertJustify( vjustify )
    pcb.Add( text )
    return text

##
## Tracks & Vias
##
def add_track( a, b, net, layer, width ):
    pnt_a = pnt.mils2unit( vec2.round( a ) )
    pnt_b = pnt.mils2unit( vec2.round( b ) )
    track = pcbnew.TRACK( pcb )
    track.SetStart( pnt_a )
    track.SetEnd(   pnt_b )
    if net != None:
        track.SetNet( net )
    track.SetLayer( layer )
    track.SetWidth( pcbnew.FromMils( width ) )
    track.SetLocked( True )
    pcb.Add( track )
    return track

def add_via( pos, net, size ):# size [mm]
    pnt_ = pnt.mils2unit( vec2.round( pos ) )
    via = pcbnew.VIA( pcb )
    via.SetPosition( pnt_ )
    via.SetWidth( pcbnew.FromMM( size[0] ) )
    via.SetDrill( pcbnew.FromMM( size[1] ) )
    via.SetNet( net )
    #print( net.GetNetname() )
    via.SetLayerPair( pcb.GetLayerID( 'F.Cu' ), pcb.GetLayerID( 'B.Cu' ) )
    via.SetLocked( True )
    pcb.Add( via )
    return via


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
def move_mods( base_mod, base_pos, base_angle, mods ):
    set_mod_pos_angle( base_mod, base_pos, base_angle )
    mrot = mat2.rotate( base_angle )
    for mod_name, pos, angle in mods:
        npos = vec2.add( base_pos, vec2.mult( mrot, pos ) )
        nangle = base_angle + angle
        set_mod_pos_angle( mod_name, npos, nangle )

def move_mods2( base_pos, base_angle, mods ):
    mrot = mat2.rotate( base_angle )
    for vals in mods:
        name, pos, angle = vals[:3]
        npos = vec2.add( base_pos, vec2.mult( mrot, pos ) )
        nangle = base_angle + angle
        if name == None:
            move_mods2( npos, nangle, vals[3] )
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


# wires
def add_wire_straight( pnts, net, layer, width ):
    for idx, curr in enumerate( pnts ):
        if idx == 0:
            continue
        prev = pnts[idx-1]
        if vec2.distance( prev, curr ) > 1:
            add_track( prev, curr, net, layer, width )

def add_wire_directed( pos_a, angle_a, pos_b, angle_b, net, layer, width, diag ):
    dir_a = vec2.rotate( angle_a )
    dir_b = vec2.rotate( angle_b )
    xpos, ka, kb = vec2.find_intersection( pos_a, dir_a, pos_b, dir_b )
    length = min( diag, abs( ka ), abs( kb ) )
    pos_am = vec2.scale( -length * sign( ka ), dir_a, xpos )
    pos_bm = vec2.scale( -length * sign( kb ), dir_b, xpos )
    pnts = [pos_a, pos_am, pos_bm, pos_b]
    add_wire_straight( pnts, net, layer, width )

def add_wire_offset_directed( pos_a, angle_a, offset_a, pos_b, angle_b, offset_b, net, layer, width, diag ):
    dir_a = vec2.rotate( angle_a )
    dir_b = vec2.rotate( angle_b )
    apos = vec2.add( pos_a, offset_a )
    bpos = vec2.add( pos_b, offset_b )
    xpos, ka, kb = vec2.find_intersection( apos, dir_a, bpos, dir_b )
    len_a = min( diag, abs( ka ) / 2, vec2.length( offset_a ) )
    len_b = min( diag, abs( kb ) / 2, vec2.length( offset_b ) )
    len_m = min( diag, abs( ka ) / 2, abs( kb ) / 2 )
    pnts = []
    pnts.append( pos_a )
    if len_a > 1:
        pnts.append( vec2.scale( -len_a, vec2.normalize( offset_a )[0], apos ) )
    pnts.append( vec2.scale( len_a * sign( ka ), dir_a, apos ) )
    pnts.append( vec2.scale( -len_m * sign( ka ), dir_a, xpos ) )
    pnts.append( vec2.scale( -len_m * sign( kb ), dir_b, xpos ) )
    pnts.append( vec2.scale( len_b * sign( kb ), dir_b, bpos ) )
    if len_b > 1:
        pnts.append( vec2.scale( -len_b, vec2.normalize( offset_b )[0], bpos ) )
    pnts.append( pos_b )
    add_wire_straight( pnts, net, layer, width )

def add_wire_zigzag( pos_a, pos_b, angle, net, layer, width, diag ):
    mid_pos = vec2.scale( 0.5, vec2.add( pos_a, pos_b ) )
    _, ka1, _ = vec2.find_intersection( pos_a, vec2.rotate( angle ), mid_pos, vec2.rotate( angle + 45 ) )
    _, ka2, _ = vec2.find_intersection( pos_a, vec2.rotate( angle ), mid_pos, vec2.rotate( angle - 45 ) )
    mid_angle = (angle + 45) if abs( ka1 ) < abs( ka2 ) else (angle - 45)
    add_wire_directed( pos_a, angle, mid_pos, mid_angle, net, layer, width, diag )
    add_wire_directed( pos_b, angle, mid_pos, mid_angle, net, layer, width, diag )

def __add_wire( pos_a, pos_b, angle_a, angle_b, net, layer, width, prms ):
    if type( prms ) == type( Straight ) and prms == Straight:
        add_wire_straight( [pos_a, pos_b], net, layer, width )
    elif prms[0] == Directed:
        dangle_a, dangle_b, diag = prms[1:]
        add_wire_directed( pos_a, angle_a + dangle_a, pos_b, angle_b + dangle_b, net, layer, width, diag )
    elif prms[0] == OffsetDirected:
        prms_a, prms_b, diag = prms[1:]
        off_angle_a, off_len_a, dangle_a = prms_a
        off_angle_b, off_len_b, dangle_b = prms_b
        offset_a = vec2.scale( off_len_a, vec2.rotate( angle_a + off_angle_a ) )
        offset_b = vec2.scale( off_len_b, vec2.rotate( angle_b + off_angle_b ) )
        add_wire_offset_directed( pos_a, angle_a + dangle_a, offset_a, pos_b, angle_b + dangle_b, offset_b, net, layer, width, diag )
    elif prms[0] == ZigZag:
        dangle, diag = prms[1:]
        add_wire_zigzag( pos_a, pos_b, dangle + angle_a, net, layer, width, diag )

def wire_mods( tracks ):
    for mod_a, pad_a, mod_b, pad_b, width, prms in tracks:
        layer = get_mod_layer( mod_a )
        pos_a, angle_a, net_a = get_pad_pos_angle_net( mod_a, pad_a )
        pos_b, angle_b, _     = get_pad_pos_angle_net( mod_b, pad_b )
        __add_wire( pos_a, pos_b, -angle_a, -angle_b, net_a, layer, width, prms )

# def wire_mods_layer( layer, tracks ):
#     for mod_a, pad_a, mod_b, pad_b, width, prms in tracks:
#         pos_a, net_a = get_pad_pos_net( mod_a, pad_a )
#         pos_b, _     = get_pad_pos_net( mod_b, pad_b )
#         __add_wire( pos_a, pos_b, net_a, layer, width, prms )

# def wire_mods_to_via( pos_via, size_via, tracks ):
#     via = None
#     for mod_name, pad_name, width, prms in tracks:
#         layer = get_mod_layer( mod_name )
#         pos, net = get_pad_pos_net( mod_name, pad_name )
#         if via == None:
#             via = add_via( pos_via, net, size_via )
#         __add_wire( pos_via, pos, net, layer, width, prms )
#     return via

# def wire_mods_to_via_layer( pos_via, size_via, tracks ):
#     via = None
#     for mod_name, pad_name, width, layer, prms in tracks:
#         pos, net = get_pad_pos_net( mod_name, pad_name )
#         if via == None:
#             via = add_via( pos_via, net, size_via )
#         __add_wire( pos_via, pos, net, layer, width, prms )
#     return via


# drawing
def removeDrawings():
    pcb.DeleteZONEOutlines()
    for draw in pcb.GetDrawings():
        pcb.Delete( draw )

def removeTracksAndVias():
    # Tracks & Vias
    for track in pcb.GetTracks():
        delete = False
        if track.IsLocked():# locked == placed by python
            delete = True
        # elif type( track ) is pcbnew.VIA:
        #     delete = True
        # elif type( track ) is pcbnew.TRACK:
        #     delete = True
        if delete:
            pcb.Delete( track )

def drawRect( pnts, layer, R = 75, width = 2 ):
    if R > 0:
        arcs = []
        for idx, a in enumerate( pnts ):
            b = pnts[idx-1]
            vec = vec2.sub( b, a )
            length = vec2.length( vec )
            delta = vec2.scale( R / length, vec )
            na = vec2.add( a, delta )
            nb = vec2.sub( b, delta )
            ctr = vec2.add( nb, (delta[1], -delta[0]) )
            arcs.append( (ctr, na, nb) )
            add_line( na, nb, layer, width )
        for idx, (ctr, na, nb) in enumerate( arcs ):
            arc = add_arc2( ctr, nb, arcs[idx-1][1], -90, layer, width )
            # print( "na   ", pnt.mils2unit( vec2.round( na ) ) )
            # print( "start", arc.GetArcStart() )
            # print( "nb   ", pnt.mils2unit( vec2.round( nb ) ) )
            # print( "end  ", arc.GetArcEnd() )
    else:
        for idx, a in enumerate( pnts ):
            b = pnts[idx-1]
            add_line( a, b, layer, width )

# zones
def add_zone( rect, layer, idx = 0, net_name = 'GND' ):
    pnts = map( lambda pt: pnt.mils2unit( vec2.round( pt ) ), rect )
    net = pcb.FindNet( net_name ).GetNet()
    zone = pcb.InsertArea( net, idx, layer, pnts[0][0], pnts[0][1], pcbnew.ZONE_CONTAINER.DIAGONAL_EDGE )
    poly = zone.Outline()
    for idx, pt in enumerate( pnts ):
        if idx == 0:
            continue
        poly.Append( pt[0], pt[1] )
    return zone, poly
