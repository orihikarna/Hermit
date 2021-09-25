#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include "mini-printf.h"

#define LOG_GLOBAL_ENABLE

#define LL_DEBUG 0
#define LL_ERROR 1
#define LL_NONE  2

// default log level
#ifndef LOG_LEVEL
//#define LOG_LEVEL LL_DEBUG
//#define LOG_LEVEL LL_ERROR
#define LOG_LEVEL LL_NONE
#endif

int mini_puts( char*s, int len, void* buf );
int mini_printf( const char* fmt, ... );

#if 0
#define _LOG_PRINTF( fmt, level, ... ) printf( "%s[%s:%s(%d)] " fmt "\n", level, __FILE__, __FUNCTION__, __LINE__, ##__VA_ARGS__ )
#else
#define _LOG_PRINTF( fmt, level, ... ) mini_printf( "%s[%s:%s(%d)] " fmt "\n", level, __FILE__, __FUNCTION__, __LINE__, ##__VA_ARGS__ )
#endif

#if defined( LOG_GLOBAL_ENABLE ) && LOG_LEVEL <= LL_DEBUG
  #define LOG_DEBUG( fmt, ... ) _LOG_PRINTF( fmt, "Debug", ##__VA_ARGS__ )
#else
  #define LOG_DEBUG( fmt, ... )
#endif

#if defined( LOG_GLOBAL_ENABLE ) && LOG_LEVEL <= LL_ERROR
  #define LOG_ERROR( fmt, ... ) _LOG_PRINTF( fmt, "Error", ##__VA_ARGS__ )
#else
  #define LOG_ERROR( fmt, ... )
#endif

#ifdef __cplusplus
}
#endif
