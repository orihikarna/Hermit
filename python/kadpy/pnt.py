import pcbnew

# unit conversion utility

def mm2unit( a ):
    return pcbnew.wxPointMM( a[0], a[1] )

def mils2unit( a ):
    return pcbnew.wxPointMils( a[0], a[1] )

def unit2mm( pnt ):
    return (pcbnew.ToMM( pnt[0] ), pcbnew.ToMM( pnt[1] ) )

def unit2mils( pnt ):
    return (pcbnew.ToMils( pnt[0] ), pcbnew.ToMils( pnt[1] ) )

def to_unit( a, mm_or_mils ):
    if mm_or_mils:
        return mm2unit( a )
    else:
        return mils2unit( a )

def from_unit( a, mm_or_mils ):
    if mm_or_mils:
        return unit2mm( a )
    else:
        return unit2mils( a )
