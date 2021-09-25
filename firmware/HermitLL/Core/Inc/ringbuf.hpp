#pragma once

#include <stdint.h>
#include "log.h"

template<typename T>
class RingBuffer {
private:
  T* m_buff;
  uint8_t m_size;
  uint8_t m_read_idx;
  uint8_t m_write_idx;
  uint8_t m_max_used_size;

public:
  RingBuffer( T* buff, uint8_t size )
  : m_buff( buff ), m_size( size ), m_read_idx( 0 ), m_write_idx( 0 ), m_max_used_size( 0 ) {
    //assert( size < 128 );
  };

  uint8_t getMaxUsedSize() const { return m_max_used_size; }

  void push_back( const T& v ) {
    if (can_push() == 0) LOG_ERROR( "buffer is FULL!" );
    if (false) {
      int8_t used = m_write_idx - m_read_idx;
      if (used < 0) used += m_size;
      if (m_max_used_size < used) {
        m_max_used_size = used;
      }
    }
    m_buff[m_write_idx] = v;
    m_write_idx = incr( m_write_idx );
  }

  T pop_front() {
    if (can_pop() == 0) LOG_ERROR( "buffer is EMPTY!" );
    const T ret = m_buff[m_read_idx];
    m_read_idx = incr( m_read_idx );
    return ret;
  }

  uint8_t can_pop() const {
    int8_t avail = m_write_idx - m_read_idx;
    if (avail < 0) {
      avail += m_size;
    }
    return avail;
  }

  uint8_t can_push() const {
    const uint8_t write_next = incr( m_write_idx );
    int8_t vacant = m_read_idx - write_next;
    if (vacant < 0) {
      vacant += m_size;
    }
    return vacant;
  }

private:
  inline uint8_t incr( uint8_t idx ) const {
    idx += 1;
    if (idx == m_size) {
      idx = 0;
    }
    return idx;
  }
};
