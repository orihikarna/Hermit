#include <qmk/keycode_jp.h>
#include "keyproc.hpp"
#include "log.h"

#define USE_JP

#ifdef USE_JP
#define UKC_COMM JP_COMM
#define UKC_DOT  JP_DOT
#else
#define UKC_COMM KC_COMM
#define UKC_DOT  KC_DOT
#endif


// emacs mode modifiers (use left keycods)
#define MOD_C MOD_BIT(KC_LCTL)
#define MOD_S MOD_BIT(KC_LSFT)
#define MOD_M MOD_BIT(KC_LALT)
#define MOD_G MOD_BIT(KC_LGUI)
#define MOD_CS (MOD_C|MOD_S)
#define MOD_CM (MOD_C|MOD_M)
#define MOD_SM (MOD_S|MOD_M)

// any modifiers (use right keycodes)
#define ANY_C MOD_BIT(KC_RCTL)
#define ANY_S MOD_BIT(KC_RSFT)
#define ANY_M MOD_BIT(KC_RALT)
#define ANY_G MOD_BIT(KC_RGUI)
#define ANY_SM (ANY_S|ANY_M)

// emacs mode type
#define MOD_TABLE MOD_BIT(KC_LGUI)
#define MOD_MACRO MOD_BIT(KC_RGUI)

namespace {// macros

  enum map_macros {
    EMM_OpenLine,
    EMM_KillLine,
    EMM_SwapChars,
    EMM_KillWord,
    EMM_MarkCancel,
    EMM_MarkCut,
    EMM_MarkCopy,
  };

  constexpr keycode_t macro_openline[]    = { KC_ENT, KC_UP, KC_END, KC_NO };
  constexpr keycode_t macro_killline[]    = { S(KC_END), C(KC_X), KC_NO };
  constexpr keycode_t macro_swapchars[]   = { S(KC_RGHT), C(KC_X), KC_LEFT, C(KC_V), KC_RGHT, KC_NO };
  constexpr keycode_t macro_killword[]    = { S(C(KC_RGHT)), C(KC_X), KC_NO };
  constexpr keycode_t macro_mark_cancel[] = { KC_RGHT, KC_NO };
  constexpr keycode_t macro_mark_cut[]    = { C(KC_X), KC_LEFT, KC_RGHT, KC_NO };
  constexpr keycode_t macro_mark_copy[]   = { C(KC_C), KC_LEFT, KC_NO };

  const keycode_t* macro_seqs[] = {
    [EMM_OpenLine]   = macro_openline,
    [EMM_KillLine]   = macro_killline,
    [EMM_SwapChars]  = macro_swapchars,
    [EMM_KillWord]   = macro_killword,
    [EMM_MarkCancel] = macro_mark_cancel,
    [EMM_MarkCut]    = macro_mark_cut,
    [EMM_MarkCopy]   = macro_mark_copy,
  };
}
namespace {// maps

  struct SMapEntry {
    uint8_t src_mods;// L: pressed, R: any
    uint8_t src_code;
    uint8_t dest_mods; // mapped mods, or mapped mode (macro, function)
    uint8_t dest_code;
  };

  constexpr uint8_t MAP_ENTRY_SIZE = sizeof( SMapEntry );

  struct SMapTable {
    const uint8_t (*m_table)[MAP_ENTRY_SIZE];
    uint8_t m_size;
  };

  enum map_table_index {
    EMTI_None = 0,
    EMTI_Default,
    EMTI_CxPrefix,
    EMTI_MarkSel,
    EMTI_Count,
  };

  constexpr uint8_t map_table_none[][MAP_ENTRY_SIZE] = {
    { MOD_C         , KC_Q,    MOD_TABLE, EMTI_Default },
  };

  constexpr uint8_t map_table_default[][MAP_ENTRY_SIZE] = {
    { MOD_C         , KC_Q,    MOD_TABLE, EMTI_None },
    { MOD_C         , KC_X,    MOD_TABLE, EMTI_CxPrefix },
    { MOD_C         , KC_SPC,  MOD_TABLE, EMTI_MarkSel },
    { MOD_C         , KC_G,    0,         KC_ESC  },// Esc
    { MOD_C | ANY_SM, KC_M,    0,         KC_ENT  },// Enter
    { MOD_C | ANY_SM, KC_A,    0,         KC_HOME },// Home
    { MOD_C | ANY_SM, KC_E,    0,         KC_END  },// End
    { MOD_C | ANY_SM, KC_F,    0,         KC_RGHT },// Right
    { MOD_C | ANY_SM, KC_B,    0,         KC_LEFT },// Left
    { MOD_C | ANY_SM, KC_P,    0,         KC_UP   },// Up
    { MOD_C | ANY_SM, KC_N,    0,         KC_DOWN },// Down
    { MOD_C | ANY_SM, KC_R,    0,         KC_PGUP },// Page Up
    { MOD_C | ANY_SM, KC_V,    0,         KC_PGDN },// Page Down
    { MOD_M | ANY_S , KC_F,    MOD_C,     KC_RGHT },// next word
    { MOD_M | ANY_S , KC_B,    MOD_C,     KC_LEFT },// prev word
    { MOD_C | ANY_S , KC_D,    0,         KC_DEL  },// Del
    { MOD_C         , KC_H,    0,         KC_BSPC },// BS
    { MOD_C         , KC_S,    MOD_C,     KC_F    },// search (find)
    // macros
    { MOD_C         , KC_O,    MOD_MACRO, EMM_OpenLine },
    { MOD_C         , KC_K,    MOD_MACRO, EMM_KillLine },
    { MOD_C         , KC_T,    MOD_MACRO, EMM_SwapChars },
    { MOD_M         , KC_D,    MOD_MACRO, EMM_KillWord },
    { MOD_C | ANY_S , KC_I,    0,         KC_TAB  },// Tab
    { MOD_C         , KC_W,    MOD_C,     KC_X    },// cut
    { MOD_M         , KC_W,    MOD_C,     KC_C    },// copy
    { MOD_C         , KC_Y,    MOD_C,     KC_V    },// paste
    { MOD_M         , KC_Y,    MOD_C,     KC_Y    },// redo
    { MOD_SM        , UKC_COMM,MOD_C,     KC_HOME },// top
    { MOD_SM        , UKC_DOT, MOD_C,     KC_END  },// bottom
    // mac style
    { MOD_M         , KC_Z,    MOD_C,     KC_Z    },// undo
    { MOD_M         , KC_X,    MOD_C,     KC_X    },// cut
    { MOD_M         , KC_C,    MOD_C,     KC_C    },// copy
    { MOD_M         , KC_V,    MOD_C,     KC_V    },// paste
    { MOD_M         , KC_A,    MOD_C,     KC_A    },// All
    { MOD_M         , KC_S,    MOD_C,     KC_S    },// save
    { MOD_SM        , KC_Z,    MOD_C,     KC_Y    },// redo
    { MOD_M         , KC_N,    MOD_C,     KC_N    },// new
    { MOD_M         , KC_O,    MOD_C,     KC_O    },// open
    //  Ctrl+Num=Fn
    // { MOD_C | ANY_SM, KC_1,    0,         KC_F1   },// F1
    // { MOD_C | ANY_SM, KC_2,    0,         KC_F2   },// F2
    // { MOD_C | ANY_SM, KC_3,    0,         KC_F3   },// F3
    // { MOD_C | ANY_SM, KC_4,    0,         KC_F4   },// F4
    // { MOD_C | ANY_SM, KC_5,    0,         KC_F5   },// F5
    // { MOD_C | ANY_SM, KC_6,    0,         KC_F6   },// F6
    // { MOD_C | ANY_SM, KC_7,    0,         KC_F7   },// F7
    // { MOD_C | ANY_SM, KC_8,    0,         KC_F8   },// F8
    // { MOD_C | ANY_SM, KC_9,    0,         KC_F9   },// F9
    // { MOD_C | ANY_SM, KC_0,    0,         KC_F10  },// F10
#ifdef USE_JP
    { MOD_C         , JP_SCLN, 0,         JP_ZKHK },// IME
#endif
  };

  constexpr uint8_t map_table_cxprefix[][MAP_ENTRY_SIZE] = {
    { MOD_C         , KC_Q,    MOD_TABLE, EMTI_None },
    { MOD_C         , KC_X,    MOD_TABLE, EMTI_CxPrefix },// not to go back to default by chatters of X key
    { MOD_C         , KC_S,    MOD_C,     KC_S    },// save
    { MOD_C         , KC_F,    MOD_C,     KC_O    },// open
    { MOD_C         , KC_C,    MOD_M,     KC_F4   },// close
    { 0             , KC_U,    MOD_C,     KC_Z    },// undo
    { 0             , KC_H,    MOD_C,     KC_A    },// All
  };

  constexpr uint8_t map_table_marksel[][MAP_ENTRY_SIZE] = {
    { MOD_C         , KC_Q,    MOD_TABLE, EMTI_None },
    { MOD_C         , KC_G,    MOD_MACRO, EMM_MarkCancel },
    { MOD_C         , KC_W,    MOD_MACRO, EMM_MarkCut },// cut
    { MOD_M         , KC_W,    MOD_MACRO, EMM_MarkCopy },// copy
    { MOD_C         , KC_A,    MOD_S,     KC_HOME },
    { MOD_C         , KC_E,    MOD_S,     KC_END  },
    { MOD_C         , KC_F,    MOD_S,     KC_RGHT },
    { MOD_C         , KC_B,    MOD_S,     KC_LEFT },
    { MOD_C         , KC_P,    MOD_S,     KC_UP   },
    { MOD_C         , KC_N,    MOD_S,     KC_DOWN },
    { MOD_CS        , KC_V,    MOD_S,     KC_PGUP },
    { MOD_C         , KC_V,    MOD_S,     KC_PGDN },
    { MOD_M         , KC_F,    MOD_CS,    KC_RGHT },// next word
    { MOD_M         , KC_B,    MOD_CS,    KC_LEFT },// prev word
    { MOD_SM        , UKC_COMM,MOD_CS,    KC_HOME },
    { MOD_SM        , UKC_DOT, MOD_CS,    KC_END  },
    { 0             , KC_LEFT, MOD_S,     KC_LEFT },
    { 0             , KC_RGHT, MOD_S,     KC_RGHT },
    { 0             , KC_UP,   MOD_S,     KC_UP   },
    { 0             , KC_DOWN, MOD_S,     KC_DOWN },
  };

  constexpr uint8_t MAP_COUNT_NONE     = sizeof( map_table_none     ) / sizeof( map_table_none[0] );
  constexpr uint8_t MAP_COUNT_DEFAULT  = sizeof( map_table_default  ) / sizeof( map_table_default[0] );
  constexpr uint8_t MAP_COUNT_CXPREFIX = sizeof( map_table_cxprefix ) / sizeof( map_table_cxprefix[0] );
  constexpr uint8_t MAP_COUNT_MARKSEL  = sizeof( map_table_marksel  ) / sizeof( map_table_marksel[0] );

  constexpr SMapTable map_tables[EMTI_Count] = {
    [EMTI_None]     = (SMapTable) { map_table_none,     MAP_COUNT_NONE },
    [EMTI_Default]  = (SMapTable) { map_table_default,  MAP_COUNT_DEFAULT },
    [EMTI_CxPrefix] = (SMapTable) { map_table_cxprefix, MAP_COUNT_CXPREFIX },
    [EMTI_MarkSel]  = (SMapTable) { map_table_marksel,  MAP_COUNT_MARKSEL },
  };
}
namespace {// tap / hold

  enum tap_hold_state {
    ETHS_Released,
    ETHS_Pressed,
    ETHS_Tapped,
    ETHS_Held,
  };

  #define MOD_TAP_COUNT m_mod_taps.size()
  //(sizeof( mod_taps ) / sizeof( mod_taps[0] ))
}

// utility functions
void KeyEmacsProc::register_code( keycode_t kc )
{
  LOG_DEBUG( "kc = %x", kc );
  if (m_kevb_out->can_push()) {
    m_kevb_out->push_back( KeyEvent( kc, EKeyEvent::Pressed, m_ev_time ) );
  } else {
    LOG_ERROR( "buffer full" );
  }
  //LOG_ERROR( "leave" );
}

void KeyEmacsProc::unregister_code( keycode_t kc )
{
  LOG_DEBUG( "kc = %x", kc );
  if (m_kevb_out->can_push()) {
    m_kevb_out->push_back( KeyEvent( kc, EKeyEvent::Released, m_ev_time ) );
  } else {
    LOG_ERROR( "buffer full" );
  }
}

void KeyEmacsProc::register_mods( uint8_t mods )
{
  if (mods & MOD_BIT( KC_LALT )) register_code( KC_LALT );
  if (mods & MOD_BIT( KC_RALT )) register_code( KC_RALT );
  if (mods & MOD_BIT( KC_LCTL )) register_code( KC_LCTL );
  if (mods & MOD_BIT( KC_RCTL )) register_code( KC_RCTL );
  if (mods & MOD_BIT( KC_LSFT )) register_code( KC_LSFT );
  if (mods & MOD_BIT( KC_RSFT )) register_code( KC_RSFT );
}

void KeyEmacsProc::unregister_mods( uint8_t mods )
{
  if (mods & MOD_BIT( KC_RSFT )) unregister_code( KC_RSFT );
  if (mods & MOD_BIT( KC_LSFT )) unregister_code( KC_LSFT );
  if (mods & MOD_BIT( KC_RCTL )) unregister_code( KC_RCTL );
  if (mods & MOD_BIT( KC_LCTL )) unregister_code( KC_LCTL );
  if (mods & MOD_BIT( KC_RALT )) unregister_code( KC_RALT );
  if (mods & MOD_BIT( KC_LALT )) unregister_code( KC_LALT );
}

void KeyEmacsProc::swap_mods( uint8_t new_mods, uint8_t old_mods )
{
  const uint8_t unreg_mods = old_mods & ~new_mods;
  const uint8_t reg_mods = new_mods & ~old_mods;
  if (unreg_mods) unregister_mods( unreg_mods );
  if (reg_mods) register_mods( reg_mods );
}

// constructer
KeyEmacsProc::KeyEmacsProc()
  : m_map_table_index( EMTI_Default )
  , m_next_map_table_index( EMTI_Default )
  , m_pressed_mods( 0 )
  , m_pressed_keycode( KC_NO )
  , m_registered_mods( 0 )
  , m_mapped_mods( 0 )
  , m_mapped_keycode( KC_NO )
  , m_mod_taps( { {
    { KC_LCTL, ETHS_Released, 0 },
    { KC_RCTL, ETHS_Released, 0 },
    { KC_LALT, ETHS_Released, 0 },
    { KC_RALT, ETHS_Released, 0 },
  } } )
{
  assert( m_mod_taps.size() == 4 );
}

void KeyEmacsProc::init()
{
}

void KeyEmacsProc::on_enter_map_table( uint8_t table_index )
{
  switch (table_index) {
    case EMTI_None:
      swap_mods( m_pressed_mods, m_registered_mods );
      m_registered_mods = m_pressed_mods;
      break;
    case EMTI_Default:
      break;
    case EMTI_CxPrefix:
      break;
    case EMTI_MarkSel:
      //backlight_enable();
      break;
  }
}

void KeyEmacsProc::on_search_map_table( uint8_t table_index, uint8_t entry_index )
{
  switch (table_index) {
    case EMTI_None:
      break;
    case EMTI_Default:
      break;
    case EMTI_CxPrefix:
      m_next_map_table_index = EMTI_Default;
      break;
    case EMTI_MarkSel:
      if (entry_index < 4 || MAP_COUNT_MARKSEL <= entry_index) {
        m_next_map_table_index = EMTI_Default;
        //backlight_disable();
      }
      break;
  }
}

// mapping functions
bool KeyEmacsProc::match_mods( uint8_t pressed, uint8_t mods, uint8_t* any_mods )
{
  pressed = (pressed | (pressed >> 4)) & 0x07;// combine Left & Right, ignore GUI
  const uint8_t req = mods & 0x0f;
  const uint8_t any = (mods >> 4) & 0x0f;
  *any_mods = pressed & any;
  return ((pressed & ~any) == (req & ~any));
}

void KeyEmacsProc::map_key( uint8_t mods, uint8_t keycode )
{
  if (mods == MOD_TABLE) {
    m_next_map_table_index = keycode;
  } else if (mods == MOD_MACRO) {
    // release the currrent mods
    unregister_mods( m_registered_mods );
    {// send the macro sequence
      const keycode_t* seq = macro_seqs[keycode];
      uint8_t n = 0;
      while (seq[n] != KC_NO) {
        tap_code( seq[n] );
        n += 1;
      }
    }
  } else {
    // release the currrent mods
    // press the mapped key/mods
    swap_mods( mods, m_registered_mods );
    register_code( keycode );
  }
  m_mapped_mods = mods;
  m_mapped_keycode = keycode;
}

// returns true when unmapped
bool KeyEmacsProc::unmap_key()
{
  if (m_mapped_mods == 0 && m_mapped_keycode == KC_NO) {
    return false;
  }
  if (m_mapped_mods == MOD_TABLE) {
    // do nothing
  } else if (m_mapped_mods == MOD_MACRO) {
    // restore the mod keys
    register_mods( m_registered_mods );
  } else {
    // release the mapped key/mods
    unregister_code( m_mapped_keycode );
    swap_mods( m_registered_mods, m_mapped_mods );
  }
  m_mapped_mods = 0;
  m_mapped_keycode = KC_NO;
  return true;
}

void KeyEmacsProc::modtap_on_press( const KeyEvent& kev )
{
  LOG_DEBUG( "enter" );
  bool to_register = true;
  for (uint8_t n = 0; n < m_mod_taps.size(); ++n) {
    SModTapHold* tap = &m_mod_taps[n];
    if (tap->modcode != kev.m_code) continue;
    to_register = false;
    const bool is_tap = modtap_is_tap( tap, kev );
    tap->time = kev.m_tick_ms;
    switch (tap->state) {
      case ETHS_Released:
        tap->state = ETHS_Pressed;
        break;

      case ETHS_Tapped:
        if (is_tap) {
          tap->state = ETHS_Held;
          to_register = true;
        } else {
          tap->state = ETHS_Pressed;
        }
        break;
    }
    break;
  }
  if (to_register) {
    LOG_DEBUG( "register" );
    m_registered_mods |= MOD_BIT( kev.m_code );
    register_code( kev.m_code );
  }
  LOG_DEBUG( "leave" );
}

void KeyEmacsProc::modtap_on_release( const KeyEvent& kev )
{
  for (uint8_t n = 0; n < m_mod_taps.size(); ++n) {
    SModTapHold* tap = &m_mod_taps[n];
    if (tap->modcode != kev.m_code) continue;
    const bool is_tap = modtap_is_tap( tap, kev );
    tap->time = kev.m_tick_ms;
    switch (tap->state) {
      case ETHS_Pressed:
        if (is_tap) {
          tap->state = ETHS_Tapped;
        } else {
          tap->state = ETHS_Released;
        }
        break;

      case ETHS_Held:
        tap->state = ETHS_Released;
        break;
    }
    break;
  }
  if (m_registered_mods & MOD_BIT( kev.m_code )) {
    m_registered_mods &= ~MOD_BIT( kev.m_code );
    unregister_code( kev.m_code );
  }
}

void KeyEmacsProc::modtap_hold_mods_if_pressed( uint8_t mods_mask )
{
  for (uint8_t n = 0; n < MOD_TAP_COUNT; ++n) {
    SModTapHold* tap = &m_mod_taps[n];
    const uint8_t mod_bit = MOD_BIT( tap->modcode );
    if ((mod_bit & mods_mask) == 0) continue;// not a target
    if ((mod_bit & m_pressed_mods) == 0) continue;// not pressed
    if (mod_bit & m_registered_mods) continue;// already held
    if (tap->state == ETHS_Pressed) {
      tap->state = ETHS_Held;
      m_registered_mods |= mod_bit;
      register_code( tap->modcode );
    }
  }
}

// the processor function
bool KeyEmacsProc::process( KeyEventBuffer& kevb_in, KeyEventBuffer& kevb_out )
{
  static_assert( sizeof( SMapEntry ) == MAP_ENTRY_SIZE, "sizeof( SMapEntry ) != MAP_ENTRY_SIZE" );
  if (kevb_in.can_pop() == 0) return false;
  if (kevb_out.can_push() <= 8) return false;
  m_kevb_out = &kevb_out;
  const KeyEvent kev = kevb_in.pop_front();
  const keycode_t keycode = kev.m_code;
  m_ev_time = kev.m_tick_ms;
  //
  bool proc = false;
  bool mapped = false;
  bool unmapped = false;
  if (IS_MOD( keycode )) {
    if (keycode == KC_LGUI || keycode == KC_RGUI) {
      // no processing
    } else {
      // keep tracking the mod key state
      if (kev.m_event == EKeyEvent::Pressed) {// pressed
        LOG_DEBUG( "mod pressed %x", keycode );
        m_pressed_mods |= MOD_BIT( keycode );
        if (m_map_table_index == EMTI_None) {
          m_registered_mods = m_pressed_mods;
          // what if unmap_key() returns true?
        } else {
          modtap_on_press( kev );
          proc = true;
        }
      } else {// released
        LOG_DEBUG( "mod released %x", keycode );
        m_pressed_mods &= ~MOD_BIT( keycode );
        if (m_map_table_index == EMTI_None) {
          m_registered_mods = m_pressed_mods;
        } else {
          modtap_on_release( kev );
          proc = true;
        }
      }
      unmapped = unmap_key();
    }
  } else if (IS_KEY( keycode )) {
    LOG_DEBUG( "is_key, kev.m_code = %x, table = %d", kev.m_code, m_map_table_index );
    if (kev.m_event == EKeyEvent::Pressed) {// pressed
      unmapped = unmap_key();
      {// search table for mapping
        uint8_t index = 0;
        const SMapTable* map_table = &map_tables[m_map_table_index];
        const uint8_t num_entries = map_table->m_size;
        for (; index < num_entries; ++index) {
          const SMapEntry* map = (const SMapEntry*) map_table->m_table[index];
          uint8_t any_mods = 0;
          if (keycode == map->src_code && match_mods( m_pressed_mods, map->src_mods, &any_mods )) {// found!
            map_key( map->dest_mods | any_mods, map->dest_code );
            m_pressed_keycode = keycode;
            mapped = true;
            LOG_DEBUG( "mapped, table = %d, entry = %d", m_map_table_index, index );
            break;
          }
        }
        on_search_map_table( m_map_table_index, index );
        if (m_next_map_table_index != m_map_table_index) {
          on_enter_map_table( m_map_table_index );
          m_map_table_index = m_next_map_table_index;
        }
      }
      if (m_pressed_keycode == KC_NO && mapped == false && m_map_table_index == EMTI_Default && m_pressed_mods != 0) {
        if (keycode == KC_TAB) {// special for Ctl-Tab, Alt-Tab
          const uint8_t mods = (m_pressed_mods & (MOD_MASK_CTRL | MOD_MASK_ALT));
          if (mods) {
            modtap_hold_mods_if_pressed( mods );
          }
        }
        map_key( m_pressed_mods, keycode );
        m_pressed_keycode = keycode;
        mapped = true;
      }
      if (mapped) {
        proc = true;
      }
    } else {// released
      if (m_pressed_keycode != KC_NO && m_pressed_keycode == keycode) {
        m_pressed_keycode = KC_NO;
        unmapped = unmap_key();
        proc = unmapped;
      }
    }
  }
  if (proc == false) {
    kevb_out.push_back( kev );
  }
  LOG_DEBUG( "proc = %d, mapped = %d, unmapped = %d, kev.m_code = %x", proc, mapped, unmapped, kev.m_code );
  return true;
}
