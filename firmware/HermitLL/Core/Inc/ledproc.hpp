#pragma once

#include "keyscanner.hpp"
#include "neopixel.hpp"

constexpr uint8_t NUM_RGB = EKeySW::NumSWs;

class LedProc {
private:
  enum EStage {
    ES_UpdateLed,
    ES_UpdateColorLeft,
    ES_SendLeft,
    ES_UpdateColorRight,
    ES_SendRight,
    ES_Num,
  };
public:
  void init();
  void process( const uint8_t* sw_state );

private:
  void update_led( const uint8_t* sw_state );
  void update_color( bool is_left );

private:
  uint8_t m_stage;
  uint16_t m_counter;
  NeoPixel m_nxp_L;
  NeoPixel m_nxp_R;

  std::array<uint8_t, NUM_RGB> m_data;
  std::array<uint8_t, NUM_RGB / 2 * NeoPixel::NumPixelBytes> m_rgb;// half
};

