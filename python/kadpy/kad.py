import math
import pcbnew
import pnt
import vec2
import mat2

pcb = pcbnew.GetBoard()

# wire types
Straight = 0
OffsetStraight = 1
OffsetDirected = 2
ZigZag = 3


# draw corner types
Line   = 0
Linear = 1
Bezier = 2
BezierRound  = 3
Round  = 4


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

def get_via_pos_net( via ):
    return pnt.unit2mils( via.GetPosition() ), via.GetNet()


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

def get_pad_pos_angle_layer_net( mod_name, pad_name ):
    mod = get_mod( mod_name )
    pad = get_pad( mod_name, pad_name )
    layer = get_mod_layer( mod_name )
    return (pnt.unit2mils( pad.GetPosition() ), mod.GetOrientation() / 10, layer, pad.GetNet())

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
        length = min( abs( radius ),
            len_a / 2 if idx - 1 > 0 else len_a,
            len_b / 2 if idx + 1 < len( pnts ) - 1 else len_b )
        if length < 1:
            rpnts.append( curr )
        else:
            if radius < 0:# and abs( vec2.dot( vec_a, vec_b ) ) < len_a * len_b * 0.001:
                # bezier circle
                num_divs = 15
                cef = (math.sqrt( 0.5 ) - 0.5) / 3 * 8
                bpnts = []
                bpnts.append( vec2.scale( length / len_a,       vec_a, curr ) )
                bpnts.append( vec2.scale( length / len_a * cef, vec_a, curr ) )
                bpnts.append( vec2.scale( length / len_b * cef, vec_b, curr ) )
                bpnts.append( vec2.scale( length / len_b,       vec_b, curr ) )
                num_pnts = len( bpnts )
                tmp = [(0, 0) for n in range( num_pnts )]
                rpnts.append( bpnts[0] )
                for i in range( 1, num_divs ):
                    t = float( i ) / num_divs
                    s = 1 - t
                    for n in range( num_pnts ):
                        tmp[n] = bpnts[n]
                    for L in range( num_pnts - 1, 0, -1 ):
                        for n in range( L ):
                            tmp[n] = vec2.scale( s, tmp[n], vec2.scale( t, tmp[n+1] ) )
                    rpnts.append( tmp[0] )
                rpnts.append( bpnts[-1] )
            else:
                rpnts.append( vec2.scale( length / len_a, vec_a, curr ) )
                rpnts.append( vec2.scale( length / len_b, vec_b, curr ) )
    for idx, curr in enumerate( rpnts ):
        if idx == 0:
            continue
        prev = rpnts[idx-1]
        if vec2.distance( prev, curr ) > 0.01:
            add_track( prev, curr, net, layer, width )

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

# params: pos, angle
def add_wire_directed( prms_a, prms_b, net, layer, width, radius ):
    pos_a, angle_a = prms_a
    pos_b, angle_b = prms_b
    dir_a = vec2.rotate( - angle_a )
    dir_b = vec2.rotate( - angle_b )
    xpos, _, _ = vec2.find_intersection( pos_a, dir_a, pos_b, dir_b )
    pnts = [pos_a, xpos, pos_b]
    add_wire_straight( pnts, net, layer, width, radius )

# params: pos, (offset length, offset angle) x n, direction angle
def add_wire_offsets_directed( prms_a, prms_b, net, layer, width, radius ):
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
    apos = pnts_a[-1]
    bpos = pnts_b[-1]
    dir_a = vec2.rotate( - angle_a )
    dir_b = vec2.rotate( - angle_b )
    xpos, _, _ = vec2.find_intersection( apos, dir_a, bpos, dir_b )
    pnts = pnts_a
    pnts.append( xpos )
    for pnt_b in reversed( pnts_b ):
        pnts.append( pnt_b )
    add_wire_straight( pnts, net, layer, width, radius )

# params: parallel lines direction angle
def add_wire_zigzag( pos_a, pos_b, angle, delta_angle, net, layer, width, radius ):
    mid_pos = vec2.scale( 0.5, vec2.add( pos_a, pos_b ) )
    dir = vec2.rotate( - angle )
    mid_dir1 = vec2.rotate( - angle + delta_angle )
    mid_dir2 = vec2.rotate( - angle - delta_angle )
    _, ka1, _ = vec2.find_intersection( pos_a, dir, mid_pos, mid_dir1 )
    _, ka2, _ = vec2.find_intersection( pos_a, dir, mid_pos, mid_dir2 )
    mid_angle = (angle - delta_angle) if abs( ka1 ) < abs( ka2 ) else (angle + delta_angle)
    add_wire_directed( (pos_a, angle), (mid_pos, mid_angle), net, layer, width, radius )
    add_wire_directed( (pos_b, angle), (mid_pos, mid_angle), net, layer, width, radius )

def __add_wire( pos_a, angle_a, pos_b, angle_b, net, layer, width, prms ):
    if type( prms ) == type( Straight ) and prms == Straight:
        add_wire_straight( [pos_a, pos_b], net, layer, width )
    elif prms[0] == OffsetStraight:
        prms_a, prms_b, radius = prms[1:]
        offsets_a = []
        offsets_b = []
        for off_len_a, off_angle_a in prms_a:
            offsets_a.append( (off_len_a, angle_a + off_angle_a) )
        for off_len_b, off_angle_b in prms_b:
            offsets_b.append( (off_len_b, angle_b + off_angle_b) )
        prms2_a = (pos_a, offsets_a)
        prms2_b = (pos_b, offsets_b)
        add_wire_offsets_straight( prms2_a, prms2_b, net, layer, width, radius )
    elif prms[0] == OffsetDirected:
        prms_a, prms_b = prms[1:3]
        radius = prms[3] if len( prms ) > 3 else 0
        offsets_a = []
        offsets_b = []
        if type( prms_a ) == type( () ):# tuple
            for off_len_a, off_angle_a in prms_a[0]:
                offsets_a.append( (off_len_a, angle_a + off_angle_a) )
            dir_angle_a = prms_a[1]
        else:
            dir_angle_a = prms_a
        if type( prms_b ) == type( () ):# tuple
            for off_len_b, off_angle_b in prms_b[0]:
                offsets_b.append( (off_len_b, angle_b + off_angle_b) )
            dir_angle_b = prms_b[1]
        else:
            dir_angle_b = prms_b
        prms2_a = (pos_a, offsets_a, angle_a + dir_angle_a)
        prms2_b = (pos_b, offsets_b, angle_b + dir_angle_b)
        add_wire_offsets_directed( prms2_a, prms2_b, net, layer, width, radius )
    elif prms[0] == ZigZag:
        dangle, delta_angle = prms[1:3]
        radius = prms[3] if len( prms ) > 3 else 0
        add_wire_zigzag( pos_a, pos_b, angle_a + dangle, delta_angle, net, layer, width, radius )

def wire_mods( tracks ):
    for mod_a, pad_a, mod_b, pad_b, width, prms in tracks:
        pos_a, angle_a, layer, net = get_pad_pos_angle_layer_net( mod_a, pad_a )
        pos_b, angle_b, _,     _   = get_pad_pos_angle_layer_net( mod_b, pad_b )
        layer = get_mod_layer( mod_a )
        __add_wire( pos_a, angle_a, pos_b, angle_b, net, layer, width, prms )

def wire_mods_to_via( offset_vec, size_via, tracks ):
    for idx, track in enumerate( tracks ):
        mod_name, pad_name, width, prms = track[:4]
        pos, angle, layer, net = get_pad_pos_angle_layer_net( mod_name, pad_name )
        if len( track ) > 4:
            layer = pcb.GetLayerID( track[4] )
        if idx == 0:
            angle_via = angle
            pos_via = vec2.mult( mat2.rotate( angle ), offset_vec, pos )
            via = add_via( pos_via, net, size_via )
        __add_wire( pos_via, angle_via, pos, angle, net, layer, width, prms )
    return via


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


# edge.cut drawing
def is_supported_round_angle( angle ):
    # integer?
    if angle - round( angle ) != 0:
        return False
    # multiple of 90?
    deg = int( angle )
    if (deg % 90) != 0:
        return False
    return True

def add_draw_bezier( pnts, num_divs, layer, width, debug = False ):
    num_pnts = len( pnts )
    tmp = [(0, 0) for n in range( num_pnts )]
    curv = [pnts[0]]
    for i in range( 1, num_divs ):
        t = float( i ) / num_divs
        s = 1 - t
        for n in range( num_pnts ):
            tmp[n] = pnts[n]
        for L in range( num_pnts - 1, 0, -1 ):
            for n in range( L ):
                tmp[n] = vec2.scale( s, tmp[n], vec2.scale( t, tmp[n+1] ) )
        curv.append( tmp[0] )
    curv.append( pnts[-1] )
    for idx, pnt in enumerate( curv ):
        if idx == 0:
            continue
        add_line( curv[idx-1], pnt, layer, width )
    if debug:# debug
        for pnt in pnts:
            add_arc( pnt, vec2.add( pnt, (20, 0) ), 360, 'F.Fab', 4 )

def draw_corner( cnr_type, a, cnr_data, b, layer, width ):
    apos, aangle = a
    bpos, bangle = b
    avec = vec2.rotate( aangle )
    bvec = vec2.rotate( bangle + 180 )
    if cnr_type != Bezier and abs( vec2.dot( avec, bvec ) ) > 0.999:
        cnr_type = Line
        #print( avec, bvec )
    if cnr_type == Line:
        add_line( apos, bpos, layer, width )
    elif cnr_type == Linear:
        xpos, alen, blen = vec2.find_intersection( apos, avec, bpos, bvec )
        if cnr_data == None:
            add_line( apos, xpos, layer, width )
            add_line( bpos, xpos, layer, width )
        else:
            delta = cnr_data[0]
            #print( delta, alen, xpos )
            amid = vec2.scale( alen - delta, avec, apos )
            bmid = vec2.scale( blen - delta, bvec, bpos )
            add_line( apos, amid, layer, width )
            add_line( bpos, bmid, layer, width )
            add_line( amid, bmid, layer, width )
    elif cnr_type == Bezier:
        num_data = len( cnr_data )
        alen = cnr_data[0]
        blen = cnr_data[-2]
        ndivs = cnr_data[-1]
        apos2 = vec2.scale( alen, avec, apos )
        bpos2 = vec2.scale( blen, bvec, bpos )
        pnts = [apos, apos2]
        if num_data > 3:
            for pt in cnr_data[1:num_data-2]:
                pnts.append( pt )
        pnts.append( bpos2 )
        pnts.append( bpos )
        add_draw_bezier( pnts, ndivs, layer, width )
    elif cnr_type == BezierRound:
        radius = cnr_data[0]
        _, alen, blen = vec2.find_intersection( apos, avec, bpos, bvec )
        debug = False
        if alen <= radius:
            print( 'BezierRound: alen < radius, {} < {}, at {}'.format( alen, radius, apos ) )
            debug = True
        if blen <= radius:
            print( 'BezierRound: alen < radius, {} < {}, at {}'.format( blen, radius, bpos ) )
            debug = True
        amid = vec2.scale( alen - radius, avec, apos )
        bmid = vec2.scale( blen - radius, bvec, bpos )
        add_line( apos, amid, layer, width )
        add_line( bpos, bmid, layer, width )
        angle = vec2.angle( avec, bvec )
        if angle < 0:
            #angle += 360
            angle *= -1
        ndivs = int( round( angle / 4.5 ) )
        #print( 'BezierRound: angle = {}, ndivs = {}'.format( angle, ndivs ) )
        coeff = (math.sqrt( 0.5 ) - 0.5) / 3 * 8
        #print( 'coeff = {}'.format( coeff ) )
        actrl = vec2.scale( alen + (coeff - 1) * radius, avec, apos )
        bctrl = vec2.scale( blen + (coeff - 1) * radius, bvec, bpos )
        pnts = [amid, actrl, bctrl, bmid]
        add_draw_bezier( pnts, ndivs, layer, width, debug )
    elif cnr_type == Round:
        radius = cnr_data[0]
        xpos, alen, blen = vec2.find_intersection( apos, avec, bpos, bvec )
        # print( 'Round: radius = {}'.format( radius ) )
        debug = False
        if not is_supported_round_angle( aangle ):
            print( 'Round: warning aangle = {}'.format( aangle ) )
            debug = True
        if not is_supported_round_angle( bangle ):
            print( 'Round: warning bangle = {}'.format( bangle ) )
            debug = True
        if alen < radius:
            print( 'Round: alen < radius, {} < {}'.format( alen, radius ) )
            debug = True
        if blen < radius:
            print( 'Round: blen < radius, {} < {}'.format( blen, radius ) )
            debug = True
        if debug:
            kad.add_arc( xpos, vec2.add( xpos, (10, 0) ), 360, layer, width )
            return b
        angle = vec2.angle( avec, bvec )
        angle = math.ceil( angle * 10 ) / 10
        tangent = math.tan( abs( angle ) / 2 / 180 * math.pi )
        side_len = radius / tangent
        # print( 'angle = {}, radius = {}, side_len = {}, tangent = {}'.format( angle, radius, side_len, tangent ) )

        amid = vec2.scale( -side_len, avec, xpos )
        bmid = vec2.scale( -side_len, bvec, xpos )
        add_line( apos, amid, layer, width )
        add_line( bpos, bmid, layer, width )

        aperp = (-avec[1], avec[0])
        if angle >= 0:
            ctr = vec2.scale( -radius, aperp, amid )
            add_arc2( ctr, bmid, amid, 180 - angle, layer, width )
        else:
            ctr = vec2.scale( +radius, aperp, amid )
            add_arc2( ctr, amid, bmid, 180 + angle, layer, width )
    return b

def draw_closed_corners( corners, layer, width ):
    a = corners[-1][0]
    for (b, cnr_type, cnr_data) in corners:
        a = draw_corner( cnr_type, a, cnr_data, b, layer, width )
        #break



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
