/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f0xx_ll_dma.h"
#include "stm32f0xx_ll_i2c.h"
#include "stm32f0xx_ll_crs.h"
#include "stm32f0xx_ll_rcc.h"
#include "stm32f0xx_ll_bus.h"
#include "stm32f0xx_ll_system.h"
#include "stm32f0xx_ll_exti.h"
#include "stm32f0xx_ll_cortex.h"
#include "stm32f0xx_ll_utils.h"
#include "stm32f0xx_ll_pwr.h"
#include "stm32f0xx_ll_tim.h"
#include "stm32f0xx_ll_usart.h"
#include "stm32f0xx_ll_gpio.h"

#if defined(USE_FULL_ASSERT)
#include "stm32_assert.h"
#endif /* USE_FULL_ASSERT */

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */
/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define COL8_Pin LL_GPIO_PIN_0
#define COL8_GPIO_Port GPIOA
#define LED_Pin LL_GPIO_PIN_1
#define LED_GPIO_Port GPIOA
#define ROW2_Pin LL_GPIO_PIN_4
#define ROW2_GPIO_Port GPIOA
#define ROW3_Pin LL_GPIO_PIN_5
#define ROW3_GPIO_Port GPIOA
#define ROW4_Pin LL_GPIO_PIN_6
#define ROW4_GPIO_Port GPIOA
#define RDI_Pin LL_GPIO_PIN_0
#define RDI_GPIO_Port GPIOB
#define LDI_Pin LL_GPIO_PIN_1
#define LDI_GPIO_Port GPIOB
#define COL7_Pin LL_GPIO_PIN_9
#define COL7_GPIO_Port GPIOA
#define COL6_Pin LL_GPIO_PIN_10
#define COL6_GPIO_Port GPIOA
#define COL5_Pin LL_GPIO_PIN_15
#define COL5_GPIO_Port GPIOA
#define COL4_Pin LL_GPIO_PIN_3
#define COL4_GPIO_Port GPIOB
#define COL3_Pin LL_GPIO_PIN_4
#define COL3_GPIO_Port GPIOB
#define ROW1_Pin LL_GPIO_PIN_5
#define ROW1_GPIO_Port GPIOB
#define COL2_Pin LL_GPIO_PIN_6
#define COL2_GPIO_Port GPIOB
#define COL1_Pin LL_GPIO_PIN_7
#define COL1_GPIO_Port GPIOB
#define COLB_Pin LL_GPIO_PIN_8
#define COLB_GPIO_Port GPIOB
#ifndef NVIC_PRIORITYGROUP_0
#define NVIC_PRIORITYGROUP_0         ((uint32_t)0x00000007) /*!< 0 bit  for pre-emption priority,
                                                                 4 bits for subpriority */
#define NVIC_PRIORITYGROUP_1         ((uint32_t)0x00000006) /*!< 1 bit  for pre-emption priority,
                                                                 3 bits for subpriority */
#define NVIC_PRIORITYGROUP_2         ((uint32_t)0x00000005) /*!< 2 bits for pre-emption priority,
                                                                 2 bits for subpriority */
#define NVIC_PRIORITYGROUP_3         ((uint32_t)0x00000004) /*!< 3 bits for pre-emption priority,
                                                                 1 bit  for subpriority */
#define NVIC_PRIORITYGROUP_4         ((uint32_t)0x00000003) /*!< 4 bits for pre-emption priority,
                                                                 0 bit  for subpriority */
#endif
/* USER CODE BEGIN Private defines */
extern volatile uint8_t g_timer_flag;
extern volatile int16_t g_timer_counter;
extern uint16_t debug_cnt1, debug_cnt2, debug_cnt3;

__STATIC_INLINE int16_t _LL_GetTick() { return g_timer_counter; }

enum {
  LED_LEFT  = 0,
  LED_RIGHT = 1,
};

void set_led_state( uint8_t index, uint8_t state );
uint8_t get_led_state( uint8_t index );
/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
