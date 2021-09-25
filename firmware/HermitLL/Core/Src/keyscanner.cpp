//#define LOG_LEVEL LL_DEBUG
#include "main.h"
#include "keyscanner.hpp"
#include "log.h"

namespace {
//////////
// Left Hand
GPIO_TypeDef* left_row_ports[NUM_ROWS] = {
  ROW1_GPIO_Port,
  ROW2_GPIO_Port,
  ROW3_GPIO_Port,
  ROW4_GPIO_Port,
};
const uint16_t left_row_pins[NUM_ROWS] = {
  ROW1_Pin,
  ROW2_Pin,
  ROW3_Pin,
  ROW4_Pin,
};

inline void write_left_row_pin( uint8_t row, uint8_t val ) {
  _LL_GPIO_SetOutputPinValue( left_row_ports[row], left_row_pins[row], val );
}

#if 0
GPIO_TypeDef* left_col_ports[NUM_COLS + 1] = {
  COL1_GPIO_Port,
  COL2_GPIO_Port,
  COL3_GPIO_Port,
  COL4_GPIO_Port,
  COL5_GPIO_Port,
  COL6_GPIO_Port,
  COL7_GPIO_Port,
  COL8_GPIO_Port,
  COLB_GPIO_Port,
};
const uint16_t left_col_pins[NUM_COLS + 1] = {
  COL1_Pin,
  COL2_Pin,
  COL3_Pin,
  COL4_Pin,
  COL5_Pin,
  COL6_Pin,
  COL7_Pin,
  COL8_Pin,
  COLB_Pin,
};

inline bool read_left_col_pin( uint8_t col ) {
  return LL_GPIO_IsInputPinSet( left_col_ports[col], left_col_pins[col] );
}
#endif

constexpr uint8_t get_gpio_bitsh( uint32_t pin ) {
  for (uint8_t sh = 0; sh < 16; ++sh) {
    if ((pin >> sh) & 1) {
      return sh;
    }
  }
  return 32;
}

#define _GPIO_PORT_OFFSET( port ) (((port) == GPIOB) ? 16 : 0)

const uint8_t left_col_bits[NUM_COLS + 1] = {
  _GPIO_PORT_OFFSET( COL1_GPIO_Port ) + get_gpio_bitsh( COL1_Pin ),
  _GPIO_PORT_OFFSET( COL2_GPIO_Port ) + get_gpio_bitsh( COL2_Pin ),
  _GPIO_PORT_OFFSET( COL3_GPIO_Port ) + get_gpio_bitsh( COL3_Pin ),
  _GPIO_PORT_OFFSET( COL4_GPIO_Port ) + get_gpio_bitsh( COL4_Pin ),
  _GPIO_PORT_OFFSET( COL5_GPIO_Port ) + get_gpio_bitsh( COL5_Pin ),
  _GPIO_PORT_OFFSET( COL6_GPIO_Port ) + get_gpio_bitsh( COL6_Pin ),
  _GPIO_PORT_OFFSET( COL7_GPIO_Port ) + get_gpio_bitsh( COL7_Pin ),
  _GPIO_PORT_OFFSET( COL8_GPIO_Port ) + get_gpio_bitsh( COL8_Pin ),
  _GPIO_PORT_OFFSET( COLB_GPIO_Port ) + get_gpio_bitsh( COLB_Pin ),
};

#define COLB NUM_COLS

inline uint32_t read_left_col_pins() {
  return GPIOA->IDR | (GPIOB->IDR << 16);
}

inline uint8_t get_left_col_bit( uint32_t left_cols, uint8_t col ) {
  return (left_cols >> left_col_bits[col]) & 1;
}

//////////
// Right Hand

// GPB0: LED
// GPB1: ROW4
// GPB2: ROW3
// GPB3: ROW2
// GPB4: ROW1
const uint8_t right_row_masks[NUM_ROWS] = {
  1 << 4,
  1 << 3,
  1 << 2,
  1 << 1,
};

#define RIGHT_LED_MASK (1 << 0)

// GPA0: COL8
// GPA1: COL1
// GPA2: COL2
// GPA3: COL3
// GPA4: COL4
// GPA5: COL5
// GPA6: COL6
// GPA7: COL7
#if 1
const uint8_t right_col_bits[NUM_COLS] = {
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  0,
};

inline uint8_t get_right_col_bit( uint8_t val, int8_t col ) {
  return (val >> right_col_bits[col]) & 1;
}
#else
inline uint8_t get_right_col_bit( uint8_t val, int8_t col ) {
  return (val >> ((col + 1) & 7)) & 1;
}
#endif
}



//////////
// private functions
uint8_t KeyScanner::read_right_col_port()
{
  uint8_t col = 0;
  if (m_mcp_init) {
    if (m_mcp.read_port( MCP23017::Port::A, &col ) == false) {
      m_mcp_init = false;
    }
  }
  return col;
}

void KeyScanner::write_right_row_port( int8_t row, uint8_t led )
{
  uint8_t val = right_row_masks[row];
  if (led) {
    val |= RIGHT_LED_MASK;
  }
  if (m_mcp_init) {
    if (m_mcp.write_port( MCP23017::Port::B, val ) == false) {
      m_mcp_init = false;
    }
  }
}

void KeyScanner::update_key_state( KeyEventBuffer* fifo, uint8_t idx, uint8_t val )
{
  const uint8_t old_state = m_sw_state[idx];
  const uint8_t is_on = (val) ? ESwitchState::IsON : 0;
  const uint8_t is_pressed = ((old_state & 1) == 1 && is_on) ? ESwitchState::IsPressed : 0;// keysw was on for continuous two times
  const uint8_t new_state = is_pressed | ((old_state << 1) & ~ESwitchState::IsPressed) | is_on;
  m_sw_state[idx] = new_state;
  // push fifo
  if ((~old_state & new_state) & ESwitchState::IsPressed) {
    //printf( "[%s] Pressed: idx = %x\n", __FUNCTION__, idx );
    fifo->push_back( KeyEvent( idx, EKeyEvent::Pressed, _LL_GetTick() ) );
  } else if ((old_state & ~new_state) & ESwitchState::IsPressed) {
    //printf( "[%s] Released: idx = %x\n", __FUNCTION__, idx );
    fifo->push_back( KeyEvent( idx, EKeyEvent::Released, _LL_GetTick() ) );
  }
}


//////////
// public functions
KeyScanner::KeyScanner()
 : m_mcp( I2C1, 0x20 << 1 )// A2A1A0 = 000
{
}

void KeyScanner::init()
{
  m_mcp_init = false;

  m_sw_state.fill( 0 );

  m_row_idx = 0;
  m_led_RL = 0;
}

void KeyScanner::init_mcp()
{
  if (m_mcp_init) { return; }
  m_mcp.disable();
  LL_mDelay( 1 );
  m_mcp.enable();
  LL_mDelay( 1 );
  if (m_mcp.set_ctrl_reg(0b00100000 ) == false) { return; }
  if (m_mcp.set_port_mode( MCP23017::Port::A, 0xff/*directions*/, 0x00/*pullups*/ ) == false) { return; }//Port A as input
  if (m_mcp.set_port_mode( MCP23017::Port::B, 0x00/*directions*/, 0x00/*pullups*/ ) == false) { return; }//Port B as output
  LOG_DEBUG( "(init_mcp)" );
  m_mcp_init = true;
}

void KeyScanner::scan( KeyEventBuffer* fifo )
{
  if (fifo->can_push() < NUM_COLS) { return; }// buffer vacancy is not enough
  ElapsedTimer et;

  init_mcp();// init mcp if timed out last time

  ////////
  // minimize delay between read and write to allow the debounce circuit for more settling time
  const uint8_t curr_row = m_row_idx;
  {// increment row index
    m_row_idx += 1;
    if (m_row_idx == NUM_ROWS) {
      m_row_idx = 0;
    }
  }
  const uint8_t next_row = m_row_idx;

  ////////
  // left GPIO
  const uint32_t left_cols = read_left_col_pins();// read left columns
  write_left_row_pin( curr_row, RESET );// reset left row line
  write_left_row_pin( next_row, SET   );// set left row line
  //_LL_GPIO_SetOutputPinValue( LED_GPIO_Port, LED_Pin, (m_led_RL & ELED::LALL) == 0 );// set left LED

  ////////
  // right I2C
  const uint8_t right_cols = read_right_col_port();// read right columns
  write_right_row_port( next_row, (m_led_RL & ELED::RALL) != 0 );// reset & set right row line, set right LED

  ////////
  // scan
  m_led_RL &= ~((ELED::L0 | ELED::R0) << curr_row);
  {// read col lines
    const uint8_t* keysw_col2idx_L = keysw_rowcol2idx_L[curr_row];
    const uint8_t* keysw_col2idx_R = keysw_rowcol2idx_R[curr_row];
    for (uint8_t col = 0; col < NUM_COLS; ++col) {
      const uint8_t keysw_L = keysw_col2idx_L[col];
      const uint8_t keysw_R = keysw_col2idx_R[col];
      if (keysw_L < 255) {
        //update_key_state( fifo, keysw_L, read_left_col_pin( col ) );
        update_key_state( fifo, keysw_L, get_left_col_bit( left_cols, col ) );
        if (is_pressed( keysw_L )) m_led_RL |= ELED::L0 << curr_row;
      }
      if (keysw_R < 255) {
        update_key_state( fifo, keysw_R, get_right_col_bit( right_cols, col ) );
        if (is_pressed( keysw_R )) m_led_RL |= ELED::R0 << curr_row;
      }
    }
    if (curr_row == NUM_ROWS - 1) {// BOOT0
      //update_key_state( fifo, EKeySW::L91, read_left_col_pin( COLB ) );
      update_key_state( fifo, EKeySW::L91, get_left_col_bit( left_cols, COLB ) );
      if (is_pressed( EKeySW::L91 )) m_led_RL |= ELED::L0 << curr_row;
    }
  }
  LOG_DEBUG( "elapsed = %ld us", et.getElapsedMicroSec() );
}
