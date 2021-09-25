#pragma once

#include <array>
#include <stdint.h>
#include "keyevent.hpp"
#include "keyswitch.hpp"
#include "keymaps.hpp"
#include "usb_hid_keyboard.h"


//class KeyProc {
//public:
//  virtual bool process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out ) = 0;
//};


class KeyLayerProc {
public:
  void init();
  bool process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out );

protected:
  uint8_t m_layer;
  std::array<uint8_t, NumLayerKeys> m_layer_key_counts;// pressed counter
  std::array<uint16_t, EKeySW::NumSWs> m_keycodes;// remember the last translation
};


class KeyEmacsProc {
private:
  struct SModTapHold {
    uint8_t modcode;
    uint8_t state;
    uint16_t time;
  };

public:
  KeyEmacsProc();
  void init();
  bool process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out );

private:
  KeyEventBuffer* m_kevb_out;
  int16_t m_ev_time;

private:
  uint8_t m_map_table_index;
  uint8_t m_next_map_table_index;
  uint8_t m_pressed_mods;
  uint8_t m_pressed_keycode;
  uint8_t m_registered_mods;
  uint8_t m_mapped_mods;
  uint8_t m_mapped_keycode;
  std::array<SModTapHold, 4> m_mod_taps;

private:// utilities
  void register_code( keycode_t kc );
  void unregister_code( keycode_t kc );
  inline void tap_code( keycode_t kc ) {
    register_code( kc );
    unregister_code( kc );
  }

  void register_mods( uint8_t mods );
  void unregister_mods( uint8_t mods );
  void swap_mods( uint8_t new_mods, uint8_t old_mods );

private:// map tables
  void on_enter_map_table( uint8_t table_index );
  void on_search_map_table( uint8_t table_index, uint8_t entry_index );

private:// key mapping
  bool match_mods( uint8_t pressed, uint8_t mods, uint8_t* any_mods );
  void map_key( uint8_t mods, uint8_t keycode );
  bool unmap_key();

private:// mod tap
  void modtap_on_press( const KeyEvent& kev );
  void modtap_on_release( const KeyEvent& kev );
  void modtap_hold_mods_if_pressed( uint8_t mods_mask );
  static inline bool modtap_is_tap( const SModTapHold* tap, const KeyEvent& kev ) {
      const int16_t tdiff = kev.m_tick_ms - tap->time;
      return (10 <= tdiff && tdiff < 300);
  }
};

class KeyUnmodProc {
public:
  void init();
  bool process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out );
};

class KeyNkroProc {
public:
  void init();
  void send_key( const KeyEvent& kev );

private:
  uint8_t m_mods;
  std::array<keycode_t, SIZE_HID_KEYS> m_codes;
  //KeyboardHID m_kbrd;
  //MouseHID m_mouse;
};
