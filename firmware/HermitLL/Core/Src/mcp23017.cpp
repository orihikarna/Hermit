#include "mcp23017.hpp"

// private functions
bool MCP23017::write_register( uint8_t reg, uint8_t value )
{
  uint8_t data[2];
  data[0] = reg;
  data[1] = value;
  return I2C_TransmitData( m_hi2c, m_addr, data, sizeof( data ), m_timeout );
}

bool MCP23017::read_register( uint8_t reg, uint8_t* pvalue )
{
  // first set the register pointer to the register wanted to be read
  if (I2C_TransmitData( m_hi2c, m_addr, &reg, 1, m_timeout ) == false) { return false; }
  // receive the 1 x 8bit data into the receive buffer
  return I2C_RecieveData( m_hi2c, m_addr, pvalue, 1, m_timeout );
}


// public functions
bool MCP23017::set_ctrl_reg( uint8_t val )
{
  //BANK   =  0 : sequential register addresses
  //MIRROR =  0 : use configureInterrupt
  //SEQOP  =  1 : sequential operation disabled, address pointer does not increment
  //DISSLW =  0 : slew rate enabled
  //HAEN   =  0 : hardware address pin is always enabled on 23017
  //ODR    =  0 : open drain output
  //INTPOL =  0 : interrupt active low
  //n/a
  return write_register( EMCP23017::IOCON, val );
}

bool MCP23017::set_port_mode( uint8_t port, uint8_t directions, uint8_t pullups, uint8_t inverted )
{
  if (write_register( EMCP23017::IODIR_A + port, directions ) == false) { return false; }
  if (write_register( EMCP23017::GPPU_A + port, pullups )     == false) { return false; }
  if (write_register( EMCP23017::IPOL_A + port, inverted )    == false) { return false; }
  return true;
}
