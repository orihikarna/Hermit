#pragma once

#include "stm32f0xx_ll_i2c.h"

bool I2C_TransmitData( I2C_TypeDef* hi2c, uint8_t device_id, const uint8_t *data, uint8_t size, int16_t timeout );
bool I2C_RecieveData( I2C_TypeDef* hi2c, uint8_t device_id, uint8_t* data, uint8_t size, int16_t timeout );
