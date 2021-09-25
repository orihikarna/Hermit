#pragma once

#include <util_ll_i2c.hpp>

enum EMCP23017 {
  IODIR_A   = 0x00,     ///< Controls the direction of the data I/O for port A.
  IODIR_B   = 0x01,     ///< Controls the direction of the data I/O for port B.
  IPOL_A    = 0x02,     ///< Configures the polarity on the corresponding GPIO_ port bits for port A.
  IPOL_B    = 0x03,     ///< Configures the polarity on the corresponding GPIO_ port bits for port B.
  GPINTEN_A = 0x04,     ///< Controls the interrupt-on-change for each pin of port A.
  GPINTEN_B = 0x05,     ///< Controls the interrupt-on-change for each pin of port B.
  DEFVAL_A  = 0x06,     ///< Controls the default comparaison value for interrupt-on-change for port A.
  DEFVAL_B  = 0x07,     ///< Controls the default comparaison value for interrupt-on-change for port B.
  INTCON_A  = 0x08,     ///< Controls how the associated pin value is compared for the interrupt-on-change for port A.
  INTCON_B  = 0x09,     ///< Controls how the associated pin value is compared for the interrupt-on-change for port B.
  IOCON     = 0x0A,     ///< Controls the device.
  GPPU_A    = 0x0C,     ///< Controls the pull-up resistors for the port A pins.
  GPPU_B    = 0x0D,     ///< Controls the pull-up resistors for the port B pins.
  INTF_A    = 0x0E,     ///< Reflects the interrupt condition on the port A pins.
  INTF_B    = 0x0F,     ///< Reflects the interrupt condition on the port B pins.
  INTCAP_A  = 0x10,     ///< Captures the port A value at the time the interrupt occured.
  INTCAP_B  = 0x11,     ///< Captures the port B value at the time the interrupt occured.
  GPIO_A    = 0x12,     ///< Reflects the value on the port A.
  GPIO_B    = 0x13,     ///< Reflects the value on the port B.
  OLAT_A    = 0x14,     ///< Provides access to the port A output latches.
  OLAT_B    = 0x15,     ///< Provides access to the port B output latches.
};

class MCP23017 {
public:
  enum Port {
    A = 0,
    B = 1,
  };

private:
  static constexpr int16_t m_timeout = 10;//ms

  I2C_TypeDef* const m_hi2c;
  const uint8_t m_addr;

public:
  MCP23017( I2C_TypeDef* hi2c, uint8_t addr ) : m_hi2c( hi2c ), m_addr( addr ) {};
  void enable() { LL_I2C_Enable( m_hi2c ); }
  void disable() { LL_I2C_Disable( m_hi2c ); }
  bool set_ctrl_reg( uint8_t val );
  bool set_port_mode( uint8_t port, uint8_t directions, uint8_t pullups, uint8_t inverted = 0 );

  inline bool read_port( uint8_t port, uint8_t* pvalue ) {
    return read_register( EMCP23017::GPIO_A + port, pvalue );
  }
  inline bool write_port( uint8_t port, uint8_t value ) {
    return write_register( EMCP23017::GPIO_A + port, value );
  }

private:
  bool read_register( uint8_t reg, uint8_t* pvalue );
  bool write_register( uint8_t reg, uint8_t value );
};

