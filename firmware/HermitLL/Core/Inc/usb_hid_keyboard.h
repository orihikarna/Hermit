#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#define SIZE_HID_KEYS 6

typedef struct {
  //uint8_t m_report_id;
  uint8_t m_modifiers;
  uint8_t m_reserved;
  uint8_t m_keys[6];
} __attribute__((packed)) KeyboardHID;

typedef struct {
  //uint8_t m_report_id;
  uint8_t m_buttons;
  int8_t m_x;
  int8_t m_y;
  int8_t m_wheel;
} __attribute__((packed)) MouseHID;

void set_keyboard_report( const KeyboardHID* report );

#ifdef __cplusplus
}
#endif
