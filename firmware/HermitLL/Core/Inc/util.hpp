#pragma once

#include <stdint.h>
#include "stm32f042x6.h"
#include "stm32f0xx_ll_dma.h"
#include "stm32f0xx_ll_tim.h"

// GPIO
__STATIC_INLINE void _LL_GPIO_SetOutputPinValue( GPIO_TypeDef *GPIOx, uint32_t PinMask, bool set ) {
  if (set) {
    WRITE_REG( GPIOx->BSRR, PinMask );
  } else {
    WRITE_REG( GPIOx->BRR, PinMask );
  }
}


// DMA
__STATIC_INLINE bool _LL_DMA_IsActiveFlag_TCx(DMA_TypeDef *DMAx, uint32_t ch) { return READ_BIT(DMAx->ISR, DMA_ISR_TCIF1 << ((ch - LL_DMA_CHANNEL_1) << 2)) != 0; }
__STATIC_INLINE bool _LL_DMA_IsActiveFlag_HTx(DMA_TypeDef *DMAx, uint32_t ch) { return READ_BIT(DMAx->ISR, DMA_ISR_HTIF1 << ((ch - LL_DMA_CHANNEL_1) << 2)) != 0; }

__STATIC_INLINE void _LL_DMA_ClearFlag_GIx(DMA_TypeDef *DMAx, uint32_t ch) { WRITE_REG(DMAx->IFCR, DMA_IFCR_CGIF1  << ((ch - LL_DMA_CHANNEL_1) << 2)); }
__STATIC_INLINE void _LL_DMA_ClearFlag_TCx(DMA_TypeDef *DMAx, uint32_t ch) { WRITE_REG(DMAx->IFCR, DMA_IFCR_CTCIF1 << ((ch - LL_DMA_CHANNEL_1) << 2)); }
__STATIC_INLINE void _LL_DMA_ClearFlag_HTx(DMA_TypeDef *DMAx, uint32_t ch) { WRITE_REG(DMAx->IFCR, DMA_IFCR_CHTIF1 << ((ch - LL_DMA_CHANNEL_1) << 2)); }
//#define _LL_DMA_CCR( DMAx, ch ) (((DMA_Channel_TypeDef *)((uint32_t)((uint32_t)DMAx + CHANNEL_OFFSET_TAB[ch - 1])))->CCR)


// Timer
#define _LL_TIM_CH1_POS  TIM_CCER_CC1E_Pos
#define _LL_TIM_CH2_POS  TIM_CCER_CC2E_Pos
#define _LL_TIM_CH3_POS  TIM_CCER_CC3E_Pos
#define _LL_TIM_CH4_POS  TIM_CCER_CC4E_Pos

#define _LL_TIM_CHANNEL_CHp( ch_pos ) (0x1UL << (ch_pos))
__STATIC_INLINE uint32_t& _LL_TIM_CCRp(TIM_TypeDef *TIMx, uint8_t ch_pos ) { return *(uint32_t*)((uint32_t)&TIMx->CCR1 + ch_pos); }
__STATIC_INLINE void _LL_TIM_EnableDMAReq_CCp(TIM_TypeDef *TIMx, uint8_t ch_pos) { SET_BIT( TIMx->DIER, 0x1UL << ((ch_pos >> 2) + TIM_DIER_CC1DE_Pos) ); }


// Utilities
void delay_us( uint32_t i );

void hsv2grb( uint16_t h, uint8_t s, uint8_t v, uint8_t* prgb );
void hsv2grbw( uint16_t h, uint8_t s, uint8_t v, uint8_t white, uint8_t* pgrbw );

inline uint32_t _LL_GetMicroSec() { return LL_TIM_GetCounter( TIM2 ); }

class ElapsedTimer {
public:
  ElapsedTimer() : m_start( _LL_GetMicroSec() ) {}
  uint32_t getElapsedMicroSec() const { return _LL_GetMicroSec() - m_start; }

private:
  const uint32_t m_start;
};
