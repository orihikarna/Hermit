import __builtin__
import math
import mat2

zero = (0, 0)

# vectors utility
def length2( a ):      ax, ay = a;   return ax * ax + ay * ay
def length( a ):       return math.sqrt( length2( a ) )
def add( a, b ):       ax, ay = a;   bx, by = b;   return (ax + bx, ay + by)
def sub( a, b ):       ax, ay = a;   bx, by = b;   return (ax - bx, ay - by)
def dot( a, b ):       ax, ay = a;   bx, by = b;   return ax * bx + ay * by
def area( a, b ):      ax, ay = a;   bx, by = b;   return ax * by - ay * bx
def angle( a, b ):     return math.atan2( area( a, b ), dot( a, b ) ) / math.pi * 180
def scale( scale, a, b = (0, 0) ):   ax, ay = a;   bx, by = b;   return (scale * ax + bx, scale * ay + by)

def distance2( a, b ): return length2( sub( a, b ) )
def distance( a, b ):  return math.sqrt( distance2( a, b ) )
def proj( a, n ):      return scale( dot( a, n ) / length2( n ), n )
def perp( a, n ):      return sub( a, proj( a, n ) )
def round( a, ndigits = 1 ):   return (__builtin__.round( a[0], ndigits ), __builtin__.round( a[1], ndigits ))

def normalize( a ):
    l = length( a )
    return scale( 1 / l, a ), l

def mult( m, a, b = (0, 0) ):
    (ma, mc), (mb, md) = m
    ax, ay = a
    bx, by = b
    return (ma * ax + mb * ay + bx, mc * ax + md * ay + by)

def rotate( angle ):
    th = math.pi * angle / 180
    co = math.cos( th )
    si = math.sin( th )
    return (co, si)



# lines
# k0 * t0 + p0 = k1 * t1 + p1
# t0 * k0 - t1 * k1 = p1 - p0
def find_intersection( p0, t0, p1, t1, tolerance = 1 ):
    if True:# exclude if nearly parallel
        degree = abs( angle( t0, t1 ) )
        if degree < tolerance or 180 - tolerance < degree:
            return ((None, None), None, None)
        #print( 'degree = {}'.format( degree ) )
    A = (t0, t1)
    R = mat2.invert( A )
    B = sub( p1, p0 )
    k0, k1 = mult( R, B )
    q0 = scale( k0, t0, p0 )
    q1 = scale(-k1, t1, p1 )
    dq = length( sub( q0, q1 ) )
    if dq > 1e-3:
        print( 'ERROR |q0 - q1| = {}'.format( dq ) )
    return (q1, k0, -k1)
