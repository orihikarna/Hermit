#include <qmk/keycode.h>
#include "keymaps.hpp"

const keycode_t keymaps[EKeyLayer::NumLayers][EKeySW::NumSWs] = {
  [EKeyLayer::Default] = {
             KC_ESC,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,         KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    JP_MINS,
    KC_LGUI, JP_YEN,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,         KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    JP_AT,   JP_LBRC,
    JP_CIRC, KC_TAB,  KC_A,    KC_S,    KC_D,    KC_F,    KC_G,         KC_H,    KC_J,    KC_K,    KC_L,    JP_SCLN, JP_COLN, JP_RBRC,
    KC_LSFT,          KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,         KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH,          JP_BSLS,
                                                            KC_DEL,   KC_ENT,
                                        KC_LALT, KC_LCTL, KL_Lowr,      KL_Raiz, KC_RSFT, KC_SPC,
  },
  [EKeyLayer::Lower] = {
             _______, KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,        KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  _______,
    _______, _______, JP_EXLM, JP_DQUO, JP_HASH, JP_DLR,  JP_PERC,      JP_AMPR, JP_QUOT, JP_LPRN, JP_RPRN, KC_P,    _______, _______,
    _______, _______, KC_1,    KC_2,    KC_3,    KC_4,    KC_5,         KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    _______, _______,
    _______,          _______, _______, _______, _______, KC_PSCR,      _______, KC_LEFT, KC_UP,   KC_DOWN, KC_RGHT,          _______,
                                                            KC_F11,   KC_F12,
                                        _______, _______, _______,      _______, _______, _______,
  },
  [EKeyLayer::Misc] = {
             _______, CF_LOFF, CF_LKEY, CF_LSNK, CF_LFAL, CF_LKNT,      CF_LWML, CF_LCRL, _______, _______, _______, _______,
    _______, _______, CF_CRBW, CF_CRED, CF_CGRN, CF_CBLU, CF_CWHT,      CF_CRDS, CF_CGRS, CF_CBLS, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______, _______,      _______, _______, _______, _______, _______, _______, _______,
    _______,          _______, _______, _______, _______, _______,      _______, _______, _______, _______, _______,          _______,
                                                            _______,  SC_REST,
                                        _______, _______, _______,      _______, _______, _______,
  },
};
