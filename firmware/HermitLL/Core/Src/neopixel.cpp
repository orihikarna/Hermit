#include <array>
#include "neopixel.hpp"
#include "util.hpp"

//#define DEBUG

#ifdef DEBUG
extern "C" {
uint16_t debug_cnt1, debug_cnt2, debug_cnt3;
}
#endif

namespace {
	std::array<uint8_t, NeoPixel::NumBufferSize> s_pwm_dat;
}
namespace {
//#pragma GCC optimize( "Ofast" )
void conv_rgb2pwm( uint8_t* p, const uint8_t* rgb )
{
	//constexpr uint8_t LVAL = 4;
	//constexpr uint8_t HVAL = 8;

	for (int8_t i = 0; i < NeoPixel::NumPixelBytes; ++i) {
		uint8_t c = *rgb++;// GRB
#if 0
		*(p++) = (c & 0x80) ? HVAL : LVAL;
		*(p++) = (c & 0x40) ? HVAL : LVAL;
		*(p++) = (c & 0x20) ? HVAL : LVAL;
		*(p++) = (c & 0x10) ? HVAL : LVAL;
		*(p++) = (c & 0x08) ? HVAL : LVAL;
		*(p++) = (c & 0x04) ? HVAL : LVAL;
		*(p++) = (c & 0x02) ? HVAL : LVAL;
		*(p++) = (c & 0x01) ? HVAL : LVAL;
#elif 0
		uint8_t mask = 0x80;
		for (int8_t k = 0; k < 8; ++k) {
			*(p++) = (c & mask) ? HVAL : LVAL;
			mask >>= 1;
		}
#elif 0
		*(p++) = 4 << ((c >> 7) & 1);
		*(p++) = 4 << ((c >> 6) & 1);
		*(p++) = 4 << ((c >> 5) & 1);
		*(p++) = 4 << ((c >> 4) & 1);
		*(p++) = 4 << ((c >> 3) & 1);
		*(p++) = 4 << ((c >> 2) & 1);
		*(p++) = 4 << ((c >> 1) & 1);
		*(p++) = 4 << ((c     ) & 1);
#else
		for (int8_t k = 0; k < 8; ++k) {
			*(p++) = 4 << ((c >> 7) & 1);
			c <<= 1;
		}
#endif
	}
}
}

void NeoPixel::init( TIM_TypeDef* htim, uint8_t tim_ch_pos, DMA_TypeDef* hdma, uint32_t dma_ch )
{
	m_htim = htim;
	m_hdma = hdma;
	m_tim_ch_pos = tim_ch_pos;
	m_dma_ch = dma_ch;

	const uint32_t tim_ch = _LL_TIM_CHANNEL_CHp( tim_ch_pos );
	_LL_TIM_EnableDMAReq_CCp( m_htim, tim_ch_pos );
	LL_TIM_CC_EnableChannel( m_htim, tim_ch );
	LL_TIM_EnableAllOutputs( m_htim );
}

//#pragma GCC optimize( "Os" )
void NeoPixel::send( const uint8_t* rgb_dat, uint8_t rgb_cnt )
{
	if (rgb_cnt == 0) return;
	m_rgb_dat = rgb_dat;
	m_rgb_cnt = rgb_cnt;
	m_pwm_ridx = 0;// wait for half completion at first
	m_pwm_wpos = 0;
	// set the first two data
	fill_dma_buf();
	fill_dma_buf();
	// reset Timer count
	LL_TIM_SetCounter( m_htim, 0 );
	// start DMA
	LL_DMA_DisableChannel( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_GIx( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_HTx( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_TCx( m_hdma, m_dma_ch );
	//LL_DMA_EnableIT_HT( m_hdma, m_dma_ch );
	//LL_DMA_EnableIT_TC( m_hdma, m_dma_ch );
	volatile uint32_t* pccr = &_LL_TIM_CCRp( m_htim, m_tim_ch_pos );
	*pccr = 0;
	LL_DMA_SetPeriphAddress( m_hdma, m_dma_ch, (uint32_t) pccr );
	LL_DMA_SetMemoryAddress( m_hdma, m_dma_ch, (uint32_t) s_pwm_dat.data() );
	LL_DMA_SetDataLength( m_hdma, m_dma_ch, NumBufferSize );
	LL_DMA_EnableChannel( m_hdma, m_dma_ch );
	// start Timer
	LL_TIM_EnableCounter( m_htim );
	while (m_rgb_cnt > 0) {
		wait_for_dma();
		fill_dma_buf();
	}
	for (uint8_t n = 0; n < 1 + 3; ++n) {// write RESET 80us < 3 leds duration
		wait_for_dma();
		fill_dma_buf();
	}
	// stop Timer
	LL_TIM_DisableCounter( m_htim );
	// stop DMA
	LL_DMA_DisableChannel( m_hdma, m_dma_ch );
	//LL_DMA_DisableIT_HT( m_hdma, m_dma_ch );
	//LL_DMA_DisableIT_TC( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_GIx( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_TCx( m_hdma, m_dma_ch );
	_LL_DMA_ClearFlag_HTx( m_hdma, m_dma_ch );
}

//#pragma GCC optimize( "Os" )
void NeoPixel::wait_for_dma()
{
	if (m_pwm_ridx == 0) {
		while (_LL_DMA_IsActiveFlag_HTx( m_hdma, m_dma_ch ) == false) {
		}
		//asm( "NOP" );
		_LL_DMA_ClearFlag_HTx( m_hdma, m_dma_ch );
	} else {
		while (_LL_DMA_IsActiveFlag_TCx( m_hdma, m_dma_ch ) == false) {
		}
		//asm( "NOP" );
		_LL_DMA_ClearFlag_TCx( m_hdma, m_dma_ch );
	}
	m_pwm_ridx ^= 1;
}

//#pragma GCC optimize( "Ofast" )
void NeoPixel::fill_dma_buf()
{
	uint8_t* pwm = &s_pwm_dat[m_pwm_wpos];
	m_pwm_wpos ^= NumPixelBits;
	if (m_rgb_cnt > 0) {
		m_rgb_cnt -= 1;
		conv_rgb2pwm( pwm, m_rgb_dat );
		m_rgb_dat += NumPixelBytes;
	} else {
		for (uint8_t i = 0; i < NumPixelBits; ++i) {
			*(pwm++) = 0;
		}
	}
}
