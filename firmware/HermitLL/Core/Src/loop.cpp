//#define LOG_LEVEL LL_ERROR
#include <array>
#include "main.h"
#include "keyscanner.hpp"
#include "keyproc.hpp"
#include "ledproc.hpp"
#include "loop.hpp"
#include "util.hpp"
#include "log.h"

namespace {

KeyScanner scanner;

std::array<KeyEvent, 12> keva_input;// 1 rows + extra
std::array<KeyEvent, 12> keva_layer;
std::array<KeyEvent, 12> keva_emacs;
std::array<KeyEvent,  6> keva_unmod;

KeyEventBuffer kevb_input( keva_input.data(), keva_input.size() );
KeyEventBuffer kevb_layer( keva_layer.data(), keva_layer.size() );
KeyEventBuffer kevb_emacs( keva_emacs.data(), keva_emacs.size() );
KeyEventBuffer kevb_unmod( keva_unmod.data(), keva_unmod.size() );

LedProc led_proc;
KeyLayerProc proc_layer;
KeyEmacsProc proc_emacs;
KeyUnmodProc proc_unmod;
KeyNkroProc  proc_nkro;

uint16_t cnt = 0;


void _setup()
{
  // key scanner
  scanner.init();
  led_proc.init();
  // processors
  proc_layer.init();
  proc_emacs.init();
  proc_unmod.init();
  proc_nkro.init();
}

void _loop()
{
  //if (_LL_GetTick() & 1) return;// 2ms loop
  cnt += 1;
  if (cnt & 1) return;// 2ms loop
  ElapsedTimer et;

  // key matrix scan
  scanner.scan( &kevb_input );
  led_proc.process( scanner.getSwitchStateData() );

  KeyEventBuffer* pkevb_in = nullptr;
  KeyEventBuffer* pkevb_out = &kevb_input;

# define _set_kevb( kevb ) pkevb_in = pkevb_out; pkevb_out = &kevb
  _set_kevb( kevb_layer ); while (proc_layer.process( *pkevb_in, *pkevb_out )) {}
  _set_kevb( kevb_emacs ); while (proc_emacs.process( *pkevb_in, *pkevb_out )) {}
  _set_kevb( kevb_unmod ); while (proc_unmod.process( *pkevb_in, *pkevb_out )) {}
# undef _set_kevb

  // send one event every 8ms
  if ((cnt & 0x07) == 0) {
    if (pkevb_out->can_pop()) {
      const auto kev = pkevb_out->pop_front();
      if (kev.m_event == EKeyEvent::Pressed) {
        //LOG_DEBUG( "%d, %d, %d", kev.m_code, kev.m_event, kev.m_tick_ms );
      }
      proc_nkro.send_key( kev );
    }
  }

  if (false && (cnt & 0x0fff) == 0) {
    LOG_DEBUG( "sys tick = %d", _LL_GetTick() );
    LOG_DEBUG( "max used input = %d", kevb_input.getMaxUsedSize() );
    LOG_DEBUG( "max used layer = %d", kevb_layer.getMaxUsedSize() );
    LOG_DEBUG( "max used emacs = %d", kevb_emacs.getMaxUsedSize() );
    LOG_DEBUG( "max used unmod = %d", kevb_unmod.getMaxUsedSize() );
  }
  LOG_ERROR( "elapsed = %ld us", et.getElapsedMicroSec() );
}

#if 0
void _loop2()
{
	const uint8_t sw = LL_GPIO_IsInputPinSet( COLB_GPIO_Port, COLB_Pin );
	const uint8_t led_on = ((cnt >> 8) & 1) ^ (sw);
	_LL_GPIO_SetOutputPinValue( LED_GPIO_Port, LED_Pin, led_on );
	if (sw && !prev_sw) {
		puts( "Hello World" );
	}
	prev_sw = sw;
	// LED
	if (true) {
	}
}
#endif
}

extern "C" {
void setup() {
	_setup();
}
void loop() {
	_loop();
}
}
