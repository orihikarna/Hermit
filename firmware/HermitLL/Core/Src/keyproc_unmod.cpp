#include "keyproc.hpp"
#include "log.h"

void KeyUnmodProc::init()
{
}

bool KeyUnmodProc::process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out )
{
  if (kevb_in.can_pop() == 0) return false;
  if (kevb_out.can_push() < 5) return false;
  const auto kev = kevb_in.pop_front();
  const keycode_t kc = kev.m_code;
  const uint8_t mod = kc >> 8;
  auto kev_mod = kev;
  auto kev_key = kev;
  kev_key.m_code &= 0xff;
  if (kev.m_event == EKeyEvent::Pressed) {
    LOG_DEBUG( "pressed: kc = %x", kc );
    if (mod) {
      if (mod & (QK_LCTL >> 8)) { kev_mod.m_code = KC_LCTL; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LSFT >> 8)) { kev_mod.m_code = KC_LSFT; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LALT >> 8)) { kev_mod.m_code = KC_LALT; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LGUI >> 8)) { kev_mod.m_code = KC_LGUI; kevb_out.push_back( kev_mod ); }
    }
    kevb_out.push_back( kev_key );
  } else {
    LOG_DEBUG( "released: kc = %x", kc );
    kevb_out.push_back( kev_key );
    if (mod) {
      if (mod & (QK_LGUI >> 8)) { kev_mod.m_code = KC_LGUI; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LALT >> 8)) { kev_mod.m_code = KC_LALT; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LSFT >> 8)) { kev_mod.m_code = KC_LSFT; kevb_out.push_back( kev_mod ); }
      if (mod & (QK_LCTL >> 8)) { kev_mod.m_code = KC_LCTL; kevb_out.push_back( kev_mod ); }
    }
  }
  return true;
}
