#include <algorithm>
#include <qmk/keycode.h>
#include "keyproc.hpp"
#include "util.hpp"
#include "log.h"

void KeyNkroProc::init()
{
  m_mods = 0;
  m_codes.fill( KC_NO );

  /*
  //m_kbrd.m_report_id = 1;
  m_kbrd.m_modifiers = 0;
  m_kbrd.m_reserved = 0;
  for (int i = 0; i < SIZE_HID_KEYS; ++i) {
    m_kbrd.m_keys[i] = 0;
  }
  */
  /*
  m_mouse.m_report_id = 2;
  m_mouse.m_buttons = 0;
  m_mouse.m_x = 0;
  m_mouse.m_y = 0;
  m_mouse.m_wheel = 0;
  */
}

static inline bool is_modifier( uint16_t code ) {
  //return KC_LCTRL <= code && code <= KC_RGUI;
  return IS_MOD( code );
}

// NKRO, Weak-modifiers
void KeyNkroProc::send_key( const KeyEvent& kev )
{
  LOG_DEBUG( "kev.m_code: %04x, event = %d", kev.m_code, kev.m_event );
  if (is_modifier( kev.m_code )) {// modifier keys
    const uint8_t mod_mask = MOD_BIT( kev.m_code );//1 << (kev.m_code - KC_LCTRL);
    if (kev.m_event == EKeyEvent::Pressed) {
      m_mods |= mod_mask;
    } else {
      m_mods &= ~mod_mask;
    }
  } else {// usual keys
    bool push_back = false;
    if (kev.m_event == EKeyEvent::Pressed) {// pressed
#if 0
      if (std::find( m_codes.begin(), m_codes.end(), KC_NO ) == m_codes.end()) {
#else
      bool avail = false;
      for (int8_t i = 0; i < SIZE_HID_KEYS; ++i) {
        if (m_codes[i] == KC_NO) {
          avail = true;
        }
      }
      if (avail == false) {
#endif
        m_codes[0] = KC_NO;// discard the front
      }
      push_back = true;
    } else {// released
      for (int8_t i = 0; i < SIZE_HID_KEYS; ++i) {
        if (m_codes[i] == kev.m_code) {
          m_codes[i] = KC_NO;
        }
      }
    }
    int8_t no_idx = 0;// KC_NO index
#if 0
    int8_t kc_idx = 0;// !KC_NO index
    do {// bring !KC_NO keys to the front
      for (; no_idx < SIZE_HID_KEYS; ++no_idx) {
        if (m_codes[no_idx] == KC_NO) {
          kc_idx = no_idx + 1;
          break;
        }
      }
      for (; kc_idx < SIZE_HID_KEYS; ++kc_idx) {
        if (m_codes[kc_idx] != KC_NO) {
          m_codes[no_idx] = m_codes[kc_idx];
          m_codes[kc_idx] = KC_NO;
          no_idx += 1;
        }
      }
    } while (kc_idx < SIZE_HID_KEYS);
#else
    {// bring !KC_NO keys to the front
      int8_t idx = 0;
      const auto codes = m_codes;
      for (auto code : codes) {
        if (code != KC_NO) {
          m_codes[idx++] = code;
        }
      }
      no_idx = idx;
      while (idx < SIZE_HID_KEYS) {
        m_codes[idx++] = KC_NO;
      }
    }
#endif
    if (push_back /*&& avail < SIZE_HID_KEYS*/) {
      m_codes[no_idx] = kev.m_code;
    }
  }
  {// send
    KeyboardHID kbrd;
    //kbrd.m_report_id = 1;
    kbrd.m_reserved = 0;
    kbrd.m_modifiers = m_mods;
    for (int i = 0; i < SIZE_HID_KEYS; ++i) {
      kbrd.m_modifiers |= m_codes[i] >> 8;
      kbrd.m_keys[i] = m_codes[i] & 0xff;
    }
    set_keyboard_report( &kbrd );
  }
}
