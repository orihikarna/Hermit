#include <util_ll_i2c.hpp>
#include "main.h"

namespace {
  inline bool check_timeout( int16_t tick_start, int16_t timeout ) {
    return (_LL_GetTick() - tick_start < timeout);
  }
}

// 1 byte memory address
// up to 254 byte data
bool I2C_TransmitData( I2C_TypeDef* hi2c, uint8_t device_id, const uint8_t* data, uint8_t size, int16_t timeout )
{
  const int16_t tick_start = _LL_GetTick() + 1;
  while (LL_I2C_IsActiveFlag_BUSY( hi2c )) {
    if (check_timeout( tick_start, timeout ) == false) { return false; }
  }

  // use AUTOEND assuming size <= 255 byte
  LL_I2C_HandleTransfer( hi2c, device_id, LL_I2C_ADDRSLAVE_7BIT, size, LL_I2C_MODE_AUTOEND, LL_I2C_GENERATE_START_WRITE );

  // write data
  for (uint8_t i = 0; i < size; ++i) {
    while (LL_I2C_IsActiveFlag_TXE( hi2c ) == RESET) {
      if (check_timeout( tick_start, timeout ) == false) { return false; }
    }
    LL_I2C_TransmitData8( hi2c, *data++ );
  }

  while (LL_I2C_IsActiveFlag_STOP( hi2c ) == RESET) {
    if (check_timeout( tick_start, timeout ) == false) { return false; }
  }
  LL_I2C_ClearFlag_STOP( hi2c );

  // reset config
  hi2c->CR2 &= ~(uint32_t) ((uint32_t)(I2C_CR2_SADD | I2C_CR2_HEAD10R | I2C_CR2_NBYTES | I2C_CR2_RELOAD | I2C_CR2_RD_WRN));

  return true;
}

// 1 byte memory address
// up to 254 byte data
bool I2C_RecieveData( I2C_TypeDef* hi2c, uint8_t device_id, uint8_t* data, uint8_t size, int16_t timeout )
{
  const int16_t tick_start = _LL_GetTick() + 1;
  while (LL_I2C_IsActiveFlag_BUSY( hi2c )) {
    if (check_timeout( tick_start, timeout ) == false) { return false; }
  }

  // use AUTOEND assuming size <= 255 byte
  LL_I2C_HandleTransfer( hi2c, device_id, LL_I2C_ADDRSLAVE_7BIT, size, LL_I2C_MODE_AUTOEND, LL_I2C_GENERATE_START_READ );

  // read data
  for (uint8_t i = 0; i < size; ++i) {
    while (LL_I2C_IsActiveFlag_RXNE( hi2c ) == RESET) {
      if (check_timeout( tick_start, timeout ) == false) { return false; }
    }
    *data++ = LL_I2C_ReceiveData8( hi2c );
  }

  while (LL_I2C_IsActiveFlag_STOP( hi2c ) == RESET) {
    if (check_timeout( tick_start, timeout ) == false) { return false; }
  }
  LL_I2C_ClearFlag_STOP( hi2c );

  // reset config
  hi2c->CR2 &= ~(uint32_t) ((uint32_t)(I2C_CR2_SADD | I2C_CR2_HEAD10R | I2C_CR2_NBYTES | I2C_CR2_RELOAD | I2C_CR2_RD_WRN));

  return true;
}
