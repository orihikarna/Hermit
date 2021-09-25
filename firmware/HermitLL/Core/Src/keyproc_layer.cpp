#include <qmk/keycode.h>
#include "keyproc.hpp"
#include "keymaps.hpp"
#include "log.h"

std::array<uint8_t, NumConfigAddrs> g_config_data;

namespace {
  void init_config_data() {
    g_config_data.fill( 0 );
    //CONFIG_DATA( CFG_RGB_TYPE ) = RGB_OFF;
    //CONFIG_DATA( CFG_RGB_TYPE ) = RGB_SNAKE;
    //CONFIG_DATA( CFG_RGB_TYPE ) = RGB_FALL;
    //CONFIG_DATA( CFG_RGB_TYPE ) = RGB_KNIGHT;
    CONFIG_DATA( CFG_RGB_TYPE ) = RGB_WINDMILL;
    //CONFIG_DATA( CFG_RGB_TYPE ) = RGB_CIRCLE;
    CONFIG_DATA( CFG_CLR_TYPE ) = CLR_RAINBOW;
    //CONFIG_DATA( CFG_CLR_TYPE ) = CLR_RED;
  }
}

void KeyLayerProc::init()
{
  m_layer = EKeyLayer::Default;
  m_layer_key_counts.fill( 0 );
  m_keycodes.fill( KC_NO );
  //
  init_config_data();
}

bool KeyLayerProc::process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out )
{
  if (kevb_in.can_pop() == 0) return false;
  if (kevb_out.can_push() < 2) return false;
  const auto kev_raw = kevb_in.pop_front();
  keycode_t keycode = keymaps[m_layer][kev_raw.m_code];// translate
  if (keycode == KC_TRNS) {
    keycode = keymaps[0][kev_raw.m_code];// default layer
  }
  LOG_DEBUG( "keycode = %d, event = %d", keycode, kev_raw.m_event );
  if (keycode == SC_REST) {
    NVIC_SystemReset();
  }
  if (ConfigStart <= keycode && keycode < ConfigEnd) {
    CONFIG_DATA( keycode ) = CFG_GET_VAL( keycode );
  } else if (LayerStart <= keycode && keycode < LayerEnd) {
    {// increment / decrement counts
      const uint8_t layer = keycode - LayerStart;
      if (kev_raw.isPressed()) {
        m_layer_key_counts[layer] += 1;
      } else {
        m_layer_key_counts[layer] -= 1;
      }
    }
    {// change the layer
      const bool is_lower = (m_layer_key_counts[KL_Lowr - LayerStart] > 0);
      const bool is_raise = (m_layer_key_counts[KL_Raiz - LayerStart] > 0);
      if (is_lower && is_raise) {
        m_layer = EKeyLayer::Misc;
      } else if (is_lower || is_raise) {
        m_layer = EKeyLayer::Lower;
      } else {
        m_layer = EKeyLayer::Default;
      }
    }
    LOG_DEBUG( "layer = %d", m_layer );
  } else {
    auto kev_out = kev_raw;
    if (kev_raw.isPressed()) {// pressed
      kev_out.m_code = keycode;
      m_keycodes[kev_raw.m_code] = keycode;// remember
    } else {// released
      kev_out.m_code = m_keycodes[kev_raw.m_code];// recall
      m_keycodes[kev_raw.m_code] = KC_NO;// forget
    }
    kevb_out.push_back( kev_out );
  }
  return true;
}
