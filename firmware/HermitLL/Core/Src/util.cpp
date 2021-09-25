#include "util.hpp"

// wait
void delay_us( uint32_t i ) {
    while (i > 0) {
        // NOP x48@48MHz ~ 1us
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP"); asm("NOP");
        i--;
    }
}

void hsv2grb( uint16_t h, uint8_t s, uint8_t v, uint8_t* pgrb )
{
  //h = h % 192;
  h &= 127;
  h += (h + 1) >> 1;
  const uint8_t rgn = h >> 5;
  const uint8_t f = h & 31;
  const uint8_t delta = (v * s + 128) >> 8;
  const uint8_t frac = (delta * f + 16) >> 5;
  const uint8_t vhi = v;
  const uint8_t vlo = vhi - delta;
  const uint8_t vdw = vhi - frac;
  const uint8_t vup = vlo + frac;

  uint8_t r, g, b;
  switch (rgn) {
    //default:
    case 0: r = vhi; g = vup; b = vlo; break;
    case 1: r = vdw; g = vhi; b = vlo; break;
    case 2: r = vlo; g = vhi; b = vup; break;
    case 3: r = vlo; g = vdw; b = vhi; break;
    case 4: r = vup; g = vlo; b = vhi; break;
    case 5: r = vhi; g = vlo; b = vdw; break;
  }

  *pgrb++ = g;
  *pgrb++ = r;
  *pgrb++ = b;
}

void hsv2grbw( uint16_t h, uint8_t s, uint8_t v, uint8_t white, uint8_t* pgrbw )
{
  hsv2grb( h, s, v, pgrbw );
  pgrbw[3] = white;
}
