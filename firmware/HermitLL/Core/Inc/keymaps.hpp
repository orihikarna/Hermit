#pragma once

#include <array>
#include <qmk/keycode_jp.h>
#include "keyevent.hpp"
#include "keyswitch.hpp"

#define CFG_SET_VAL( addr, x ) ((addr) | (x))
#define CFG_GET_VAL( kc ) ((kc) & 0x0f)
#define CFG_ADDR( kc ) (((kc) - ConfigStart) >> 4)

#define RGB_OFF         0
#define RGB_KEYDOWN     1
#define RGB_SNAKE       2
#define RGB_FALL        3
#define RGB_KNIGHT      4
#define RGB_WINDMILL    5
#define RGB_CIRCLE      6

#define CLR_RAINBOW     0
#define CLR_RED         1
#define CLR_GREEN       2
#define CLR_BLUE        3
#define CLR_WHITE       4
#define CLR_RED_SAT     5
#define CLR_GREEN_SAT   6
#define CLR_BLUE_SAT    7


enum custom_keycodes {
  // layers
  LayerStart = 0x8000,
  KL_Lowr = LayerStart,
  KL_Raiz,
  LayerEnd,
  NumLayerKeys = LayerEnd - LayerStart,

  // config memories
  ConfigStart  = 0x9000,
  CFG_RGB_TYPE = 0x9000,
  CFG_CLR_TYPE = 0x9010,
  ConfigEnd    = 0x9020,
  NumConfigAddrs = CFG_ADDR( ConfigEnd ),
  // RGB_TYPE
  CF_LOFF = CFG_SET_VAL( CFG_RGB_TYPE, RGB_OFF ),
  CF_LKEY = CFG_SET_VAL( CFG_RGB_TYPE, RGB_KEYDOWN ),
  CF_LSNK = CFG_SET_VAL( CFG_RGB_TYPE, RGB_SNAKE ),
  CF_LFAL = CFG_SET_VAL( CFG_RGB_TYPE, RGB_FALL ),
  CF_LKNT = CFG_SET_VAL( CFG_RGB_TYPE, RGB_KNIGHT ),
  CF_LWML = CFG_SET_VAL( CFG_RGB_TYPE, RGB_WINDMILL ),
  CF_LCRL = CFG_SET_VAL( CFG_RGB_TYPE, RGB_CIRCLE ),
  // CLR_TYPE
  CF_CRBW = CFG_SET_VAL( CFG_CLR_TYPE, CLR_RAINBOW ),
  CF_CRED = CFG_SET_VAL( CFG_CLR_TYPE, CLR_RED ),
  CF_CGRN = CFG_SET_VAL( CFG_CLR_TYPE, CLR_GREEN ),
  CF_CBLU = CFG_SET_VAL( CFG_CLR_TYPE, CLR_BLUE ),
  CF_CWHT = CFG_SET_VAL( CFG_CLR_TYPE, CLR_WHITE ),
  CF_CRDS = CFG_SET_VAL( CFG_CLR_TYPE, CLR_RED_SAT ),
  CF_CGRS = CFG_SET_VAL( CFG_CLR_TYPE, CLR_GREEN_SAT ),
  CF_CBLS = CFG_SET_VAL( CFG_CLR_TYPE, CLR_BLUE_SAT ),
  // RESET
  SC_REST = 0xa000,
};

enum EKeyLayer {
  Default = 0,
  Lower,
  Misc,
  NumLayers
};

extern std::array<uint8_t, NumConfigAddrs> g_config_data;
extern const keycode_t keymaps[EKeyLayer::NumLayers][EKeySW::NumSWs];

#define CONFIG_DATA( ADDR ) g_config_data[CFG_ADDR( ADDR )]
