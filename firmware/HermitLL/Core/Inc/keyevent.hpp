#pragma once

#include "ringbuf.hpp"
#include "util.hpp"

enum EKeyEvent {
  Released = 0x01,
  Pressed  = 0x02,
};

typedef uint16_t keycode_t;

struct KeyEvent {
  KeyEvent() : m_code( 0 ), m_event( 0 ), m_tick_ms( 0 ) {}
  KeyEvent( keycode_t code, uint8_t event, int16_t tick_ms = 0 )
  : m_code( code ), m_event( event ), m_tick_ms( tick_ms ) {}
  keycode_t m_code;
  uint8_t m_event;
  int16_t m_tick_ms;

  inline bool isPressed() const { return m_event == EKeyEvent::Pressed; }
};

typedef RingBuffer<KeyEvent> KeyEventBuffer;
