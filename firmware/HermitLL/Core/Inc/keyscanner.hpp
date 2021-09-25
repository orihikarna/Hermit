#pragma once

#include <array>
#include "keyevent.hpp"
#include "keyswitch.hpp"
#include "mcp23017.hpp"

enum ESwitchState {
  IsON       = 0x01,
  // 0x02-0x40 = old IsOn
  IsPressed  = 0x80,
};

class KeyScanner {
public:
  enum ELED {
    L0 = 0x01,
    R0 = 0x10,
    LALL = 0x0f,
    RALL = 0xf0,
  };
private:
  MCP23017 m_mcp;
  bool m_mcp_init;
  uint8_t m_row_idx;
  uint8_t m_led_RL;// bit0 = L, bit1 = R
  std::array<uint8_t, EKeySW::NumSWs> m_sw_state;

public:
  KeyScanner();
  void init();
  void scan( KeyEventBuffer* fifo );
  inline bool is_pressed( uint8_t swidx ) const {
    return m_sw_state[swidx] & ESwitchState::IsPressed;
  }
  inline uint8_t* getSwitchStateData() { return m_sw_state.data(); }

private:
  void init_mcp();
  inline uint8_t read_right_col_port();
  inline void write_right_row_port( int8_t row, uint8_t led );
  void update_key_state( KeyEventBuffer* fifo, uint8_t idx, uint8_t val );
};
