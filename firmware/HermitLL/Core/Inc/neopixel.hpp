#pragma once

#include "stm32f042x6.h"

class NeoPixel {
public:
	static constexpr uint8_t NumPixelBytes = 3;
	static constexpr uint8_t NumPixelBits = NumPixelBytes << 3;
	static constexpr uint8_t NumBufferSize = NumPixelBits << 1;

private:
	TIM_TypeDef* m_htim = nullptr;
	DMA_TypeDef* m_hdma = nullptr;
	uint8_t  m_tim_ch_pos = 0;
	uint32_t m_dma_ch = 0;

	const uint8_t* m_rgb_dat;
	uint8_t m_rgb_cnt;
	uint8_t m_pwm_ridx;// read index
	uint8_t m_pwm_wpos;// write pos

public:
	void init( TIM_TypeDef* htim, uint8_t tim_ch_pos, DMA_TypeDef* hdma, uint32_t dma_ch );
	void send( const uint8_t* rgb_dat, uint8_t rgb_cnt );

private:
	void wait_for_dma();
	void fill_dma_buf();
};
