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
