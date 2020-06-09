import math
import vec2

unit = ((1, 0), (0, 1))

def invert( m ):
    (ma, mc), (mb, md) = m
    d = 1.0 / (ma * md - mb * mc)
    return ((md * d, -mc * d), (- mb * d, ma * d))

def rotate( angle ):
    vec = vec2.rotate( angle )
    return ((vec[0], -vec[1]), (vec[1], vec[0]))
