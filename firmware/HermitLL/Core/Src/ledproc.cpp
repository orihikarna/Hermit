//#define LOG_LEVEL LL_DEBUG
#include <array>
#include <algorithm>
#include "keymaps.hpp"
#include "ledproc.hpp"
#include "main.h"
#include "util.hpp"
#include "log.h"

namespace {
  constexpr std::array<uint8_t, EKeySW::NumSWs> s_led2sw_index = {
    L82, L83, L84,
    L91,
    L11, L21, L31, L41, L51,      L71,
    L72, L62, L52, L42, L32, L22, L12,
    L13, L23, L33, L43, L53, L63, L73,
         L64, L54, L44, L34, L24, L14,

    R82, R83, R84,
    R81,
    R11, R21, R31, R41, R51,      R71,
    R72, R62, R52, R42, R32, R22, R12,
    R13, R23, R33, R43, R53, R63, R73,
         R64, R54, R44, R34, R24, R14,
  };
  constexpr std::array<uint8_t, EKeySW::NumSWs> s_sw2led_index = {
        24, 25, 26, 27, 28, 29,      59, 58, 57, 56, 55, 54,
    23, 22, 21, 20, 19, 18, 17,      47, 48, 49, 50, 51, 52, 53,
    10, 11, 12, 13, 14, 15, 16,      46, 45, 44, 43, 42, 41, 40,
     9,      8,  7,  6,  5,  4,      34, 35, 36, 37, 38,     39,
                             3,      33,
                       0, 1, 2,      32, 31, 30,
  };

  constexpr int8_t s_sw_pos[30][4] = {
    {   67,  -65,  35,  -25 },// Alt, 26
    {   99,  -87,  20,  -25 },// Ctrl, 27
    {  127, -116,   5,    0 },// Lower, 28
    {  122,   16,  53,  -59 },// Del, 29
    {   84,    9,  54,  -47 },// B, 0
    {   50,   15,  63,  -40 },// V, 4
    {   12,   16,  73,  -33 },// C, 8
    {  -22,   12,  82,  -27 },// X, 12
    {  -62,   -6,  91,  -20 },// Z, 16
    { -113,   -6, 109,  -17 },// Shift, 23
    { -127,   30, 121,  -20 },// Tab, 24
    {  -92,   30, 109,  -23 },// ~/^, 20
    {  -58,   30,  97,  -26 },// A, 17
    {  -21,   45,  90,  -32 },// S, 13
    {   15,   49,  82,  -38 },// D, 9
    {   58,   47,  72,  -45 },// F, 5
    {   92,   41,  65,  -52 },// G, 1
    {   90,   75,  78,  -54 },// T, 2
    {   57,   80,  85,  -48 },// R, 6
    {   18,   83,  92,  -42 },// E, 10
    {  -20,   78, 100,  -36 },// W, 14
    {  -57,   63, 105,  -30 },// Q, 18
    {  -91,   63, 116,  -27 },// |/¥, 21
    { -126,   63, 127,  -24 },// Win, 25
    {  -90,   96, 124,  -30 },// ESC, 22
    {  -56,   96, 114,  -34 },// !/1, 19
    {  -19,  112, 110,  -39 },// "/2, 15
    {   15,  116, 104,  -44 },// #/3, 11
    {   53,  114,  98,  -49 },// $/4, 7
    {   87,  109,  92,  -55 },// %/5, 3
  };
}
namespace {// RGB effect patterns

  constexpr int16_t maxv = 255;

  // [0, NUM_RGB) --> [0, 256)
  void effect_snake( uint8_t* dat, uint16_t cnt )
  {
    constexpr int16_t N = 1024;// period
    constexpr int16_t scale = int16_t( 256.0f * 256 / NUM_RGB + 0.5f );
    const uint16_t ctr = cnt & (N - 1);
    for (int16_t n = 0; n < NUM_RGB; ++n) {
      dat[n] = ((ctr + 2) >> 2) + ((scale * n + 128) >> 8);
    }
  }

  void effect_fall( uint8_t* dat, uint16_t cnt )
  {
    const uint8_t ctr = cnt >> 2;
    uint8_t* dat_L = &dat[0];
    uint8_t* dat_R = &dat[NUM_RGB/2];
    for (uint8_t n = 0; n < NUM_RGB / 2; ++n) {
      const uint8_t v = ctr - (s_sw_pos[n][1] >> 1);
      dat_L[n] = v;
      dat_R[n] = v;
    }
  }

  void effect_knight( uint8_t* dat, uint16_t cnt )
  {
    constexpr int16_t N = 1024;// period
    int16_t ctr = cnt & (N - 1);
    ctr = ((ctr >= N / 2) ? (N - ctr) : ctr) - N / 4;// +/- 256

    uint8_t* dat_L = &dat[0];
    uint8_t* dat_R = &dat[NUM_RGB/2];
    for (int8_t n = 0; n < NUM_RGB / 2; ++n) {
      const int16_t x = int16_t( s_sw_pos[n][0] ) - 127;// [-254, 0]
      const int16_t dL = (ctr - x) >> 2;// [-256, +510] /2 --> [-128, 255] /2 --> [-64, 127]
      const int16_t dR = (ctr + x) >> 2;// [-510, +256] /2 --> [-255, 128] /2 --> [-128, 64]
      dat_L[n] = 128 + dL;
      dat_R[n] = 128 + dR;
    }
  }

  void effect_windmill( uint8_t* dat, uint16_t cnt )
  {
    const int8_t ctr = cnt >> 2;
    uint8_t* dat_L = &dat[0];
    uint8_t* dat_R = &dat[NUM_RGB/2];
    for (int16_t n = 0; n < NUM_RGB / 2; ++n) {
      const int8_t deg = s_sw_pos[n][3];
      dat_L[n] = ctr - deg;
      dat_R[n] = ctr + deg - 128;
    }
  }

  void effect_circle( uint8_t* dat, uint16_t cnt )
  {
    const int8_t ctr = cnt >> 1;
    uint8_t* dat_L = &dat[0];
    uint8_t* dat_R = &dat[NUM_RGB/2];
    for (int16_t n = 0; n < NUM_RGB / 2; ++n) {
      const uint8_t d = ctr - (s_sw_pos[n][2] << 1);
      dat_L[n] = d;
      dat_R[n] = d;
    }
  }
}
namespace {// color conversion

  void set_hue( uint8_t* rgb, const uint8_t* dat, uint8_t sat = 255, uint8_t vis = 12 )
  {
    for (uint8_t n = 0; n < NUM_RGB / 2; ++n) {
      hsv2grb( dat[n] >> 1, sat, vis, rgb );
      rgb += NeoPixel::NumPixelBytes;
    }
  }

  void set_sat( uint8_t* rgb, const uint8_t* dat, uint8_t hue, uint8_t vis = 12 )
  {
    for (uint8_t n = 0; n < NUM_RGB / 2; ++n) {
      int16_t val = (int8_t) dat[n];
      val = std::abs( val );
      val = std::min<int16_t>( std::max<int16_t>( (val << 2) - 256, 0 ), 255 );
      hsv2grb( hue, val, vis, rgb );
      rgb += NeoPixel::NumPixelBytes;
    }
  }

  void set_rgb( uint8_t* rgb, const uint8_t* dat, bool red, bool green, bool blue )
  {
    const uint8_t r_mask = (red)   ? 0xff : 0;
    const uint8_t g_mask = (green) ? 0xff : 0;
    const uint8_t b_mask = (blue)  ? 0xff : 0;
    for (uint8_t n = 0; n < NUM_RGB / 2; ++n) {
      int8_t val = (int8_t) dat[n];
      val = std::abs( val ) - 96;
      val = std::max<int8_t>( val, 0 );
      *rgb++ = g_mask & val;
      *rgb++ = r_mask & val;
      *rgb++ = b_mask & val;
    }
  }
}

void LedProc::init()
{
  m_stage = ES_UpdateLed;
  m_counter = 0;
  m_nxp_L.init( TIM3, _LL_TIM_CH4_POS, DMA1, LL_DMA_CHANNEL_3 );
  m_nxp_R.init( TIM3, _LL_TIM_CH3_POS, DMA1, LL_DMA_CHANNEL_2 );

#if 0
  for (uint8_t n = 0; n < EKeySW::NumSWs; ++n) {
    s_sw2led_index[s_led2sw_index[n]] = n;
  }
  for (uint8_t n = 0; n < EKeySW::NumSWs; ++n) {
    printf( "%d, ", s_sw2led_index[n] );
  }
  printf( "\n" );
#endif
}

// output [0, 128)
void LedProc::update_led( const uint8_t* sw_state )
{
  switch (uint8_t( CONFIG_DATA( CFG_RGB_TYPE ) ) ) {
    case RGB_KEYDOWN:
      for (uint8_t n = 0; n < EKeySW::NumSWs; ++n) {
        const uint8_t idx = s_sw2led_index[n];
        if (sw_state[n] & ESwitchState::IsPressed) {
          m_data[idx] = 127;
        } else if ((m_counter & 3) == 0) {// fade
          uint8_t v = m_data[idx];
          if (v > 0) {
            v -= 1;
          }
          m_data[idx] = v;
        }
      }
      break;

    case RGB_SNAKE:    effect_snake(    m_data.data(), m_counter );   break;
    case RGB_FALL:     effect_fall(     m_data.data(), m_counter );   break;
    case RGB_KNIGHT:   effect_knight(   m_data.data(), m_counter );   break;
    case RGB_WINDMILL: effect_windmill( m_data.data(), m_counter );   break;
    case RGB_CIRCLE:   effect_circle(   m_data.data(), m_counter );   break;
  }
  m_counter += 1;
}

void LedProc::update_color( bool is_left )
{
  if (CONFIG_DATA( CFG_RGB_TYPE ) == RGB_OFF) {
    m_rgb.fill( 0 );
    return;
  }
  const uint8_t* src = &m_data[(is_left) ? 0 : (NUM_RGB/2)];
  uint8_t* dst = m_rgb.data();
  switch (uint8_t( CONFIG_DATA( CFG_CLR_TYPE ) )) {
    case CLR_RAINBOW:     set_hue( dst, src );                        break;
    case CLR_RED:         set_rgb( dst, src, true, false, false );    break;
    case CLR_GREEN:       set_rgb( dst, src, false, true, false );    break;
    case CLR_BLUE:        set_rgb( dst, src, false, false, true );    break;
    case CLR_WHITE:       set_rgb( dst, src, true, true, true );      break;
    case CLR_RED_SAT:     set_sat( dst, src, 0 );                     break;
    case CLR_GREEN_SAT:   set_sat( dst, src, 43 );                    break;
    case CLR_BLUE_SAT:    set_sat( dst, src, 85 );                    break;
  }
}

void LedProc::process( const uint8_t* sw_state )
{
  ElapsedTimer et;
  switch (m_stage) {
    case ES_UpdateLed:        update_led( sw_state );                     break;
    case ES_UpdateColorLeft:  update_color( true );                       break;
    case ES_SendLeft:         m_nxp_L.send( m_rgb.data(), NUM_RGB / 2 );  break;
    case ES_UpdateColorRight: update_color( false );                      break;
    case ES_SendRight:        m_nxp_R.send( m_rgb.data(), NUM_RGB / 2 );  break;
  }
  if (m_stage == ES_UpdateLed)
  LOG_DEBUG( "m_stage = %d, elapsed = %ld us", m_stage, et.getElapsedMicroSec() );
  // update stage
  m_stage += 1;
  if (m_stage == ES_Num) {
    m_stage = ES_UpdateLed;
  }
}
