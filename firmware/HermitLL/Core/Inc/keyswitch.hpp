#pragma once

#include "stdint.h"

enum EKeySW {
       L64, L54, L44, L34, L24, L14,            R14, R24, R34, R44, R54, R64,
  L73, L63, L53, L43, L33, L23, L13,            R13, R23, R33, R43, R53, R63, R73,
  L72, L62, L52, L42, L32, L22, L12,            R12, R22, R32, R42, R52, R62, R72,
  L71,      L51, L41, L31, L21, L11,            R11, R21, R31, R41, R51,      R71,
                                     L91,  R81,
                           L82, L83, L84,  R84, R83, R82,
  NumSWs
};

constexpr uint8_t NUM_ROWS = 4;
constexpr uint8_t NUM_COLS = 8;

#define ___ 255

constexpr uint8_t keysw_rowcol2idx_L[NUM_ROWS][NUM_COLS] = {
  { L11, L21, L31, L41, L51, ___, L71, ___ },
  { L12, L22, L32, L42, L52, L62, L72, L82 },
  { L13, L23, L33, L43, L53, L63, L73, L83 },
  { L14, L24, L34, L44, L54, L64, ___, L84 },
};

constexpr uint8_t keysw_rowcol2idx_R[NUM_ROWS][NUM_COLS] = {
  { R11, R21, R31, R41, R51, ___, R71, R81 },
  { R12, R22, R32, R42, R52, R62, R72, R82 },
  { R13, R23, R33, R43, R53, R63, R73, R83 },
  { R14, R24, R34, R44, R54, R64, ___, R84 },
};

#undef ___
