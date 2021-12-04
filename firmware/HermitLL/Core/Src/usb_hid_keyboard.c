/* This file is the part of the Lightweight USB device Stack for STM32 microcontrollers
 *
 * Copyright ©2016 Dmitry Filimonchuk <dmitrystu[at]gmail[dot]com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *   http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "usb_hid_keyboard.h"
#include "main.h"
#include "stm32.h"
#include "usb.h"
#include "usb_hid.h"
#include "hid_usage_desktop.h"
#include "hid_usage_button.h"
#include "hid_usage_keyboard.h"
#include "hid_usage_led.h"
#define LOG_LEVEL LL_NONE
#include "log.h"

#define HID_EP0_SIZE    0x40
#define HID_RIN_EP      0x81
#define HID_RIN_SZ      0x0a

#define HID_USE_IRQ   /* uncomment to build interrupt-based demo */

/* Declaration of the report descriptor */
struct hid_config {
    struct usb_config_descriptor        config;
    struct usb_interface_descriptor     hid;
    struct usb_hid_descriptor           hid_desc;
    struct usb_endpoint_descriptor      hid_ep_in;
} __attribute__((packed));

/* HID mouse report desscriptor. 2 axis 5 buttons */
static const uint8_t hid_report_desc[] = {
#if 0// mouse
    HID_USAGE_PAGE(HID_PAGE_DESKTOP),
    HID_USAGE(HID_DESKTOP_MOUSE),
    HID_COLLECTION(HID_APPLICATION_COLLECTION),
        HID_USAGE(HID_DESKTOP_POINTER),
        HID_COLLECTION(HID_PHYSICAL_COLLECTION),
            //HID_REPORT_ID(2),
            // buttons
            HID_USAGE_PAGE(HID_PAGE_BUTTON),
            HID_USAGE_MINIMUM(1),
            HID_USAGE_MAXIMUM(3),
            HID_LOGICAL_MINIMUM(0),
            HID_LOGICAL_MAXIMUM(1),
            HID_REPORT_SIZE(1),
            HID_REPORT_COUNT(3),
            HID_INPUT(HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE ),
            HID_REPORT_SIZE(1),
            HID_REPORT_COUNT((8-3)),
            HID_INPUT(HID_IOF_CONSTANT),
            // position
            HID_USAGE_PAGE(HID_PAGE_DESKTOP),
            HID_USAGE(HID_DESKTOP_X),
            HID_USAGE(HID_DESKTOP_Y),
            HID_USAGE(HID_DESKTOP_WHEEL),
            HID_LOGICAL_MINIMUM(-127),
            HID_LOGICAL_MAXIMUM(+127),
            HID_REPORT_SIZE(8),
            HID_REPORT_COUNT(3),
            HID_INPUT(HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_RELATIVE ),
        HID_END_COLLECTION,
    HID_END_COLLECTION,
#endif
#if 1// keyboard
    HID_USAGE_PAGE(HID_PAGE_DESKTOP),
    HID_USAGE(HID_DESKTOP_KEYBOARD),
    HID_COLLECTION(HID_APPLICATION_COLLECTION),
        //HID_REPORT_ID(1),
        //0x85, 0x01,                    //   REPORT_ID (1)
        HID_USAGE_PAGE(HID_PAGE_KEYBOARD),
        // Modifiers
        HID_USAGE_MINIMUM(HID_KEYBOARD_L_CTRL),
        HID_USAGE_MAXIMUM(HID_KEYBOARD_R_GUI),
        HID_LOGICAL_MINIMUM(0),
        HID_LOGICAL_MAXIMUM(1),
        HID_REPORT_SIZE(1),
        HID_REPORT_COUNT(8),
        HID_INPUT( HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE ),
        // Reserved
        HID_REPORT_SIZE(8),
        HID_REPORT_COUNT(1),
        HID_INPUT( HID_IOF_CONSTANT | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE ),
        // LED
        HID_REPORT_SIZE(1),
        HID_REPORT_COUNT(5),
        HID_USAGE_PAGE(HID_PAGE_LED),
        HID_USAGE_MINIMUM(HID_LED_NUM_LOCK),
        HID_USAGE_MAXIMUM(HID_LED_KANA),
        HID_OUTPUT( HID_IOF_DATA | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE ),
        HID_REPORT_SIZE(3),
        HID_REPORT_COUNT(1),
        HID_OUTPUT( HID_IOF_CONSTANT | HID_IOF_VARIABLE | HID_IOF_ABSOLUTE ),
        // keys
        HID_REPORT_SIZE(8),
        HID_REPORT_COUNT(6),
        HID_LOGICAL_MINIMUM(0),
        HID_LOGICAL_MAXIMUM(101),
        HID_USAGE_PAGE(HID_PAGE_KEYBOARD),
        HID_USAGE_MINIMUM(0),
        HID_USAGE_MAXIMUM(HID_KEYBOARD_EXSEL),
        HID_INPUT( HID_IOF_DATA | HID_IOF_ARRAY | HID_IOF_ABSOLUTE ),
    HID_END_COLLECTION,
#endif
};

static MouseHID hid_report_mouse_data;
static KeyboardHID s_hid_report_keyboard_data[2] = { 0 };

static int8_t s_hid_report_idx = 0;

void set_keyboard_report( const KeyboardHID* report ) {
  s_hid_report_keyboard_data[s_hid_report_idx^1] = *report;
  s_hid_report_idx ^= 1;
}

KeyboardHID* get_keyboard_report() {
  return &s_hid_report_keyboard_data[s_hid_report_idx];
}

/* Device descriptor */
static const struct usb_device_descriptor device_desc = {
    .bLength            = sizeof(struct usb_device_descriptor),
    .bDescriptorType    = USB_DTYPE_DEVICE,
    .bcdUSB             = VERSION_BCD(2,0,0),
    .bDeviceClass       = USB_CLASS_PER_INTERFACE,
    .bDeviceSubClass    = USB_SUBCLASS_NONE,
    .bDeviceProtocol    = USB_PROTO_NONE,
    .bMaxPacketSize0    = HID_EP0_SIZE,
    .idVendor           = 1155,
    .idProduct          = 22352,
    .bcdDevice          = VERSION_BCD(2,0,0),
    .iManufacturer      = 1,
    .iProduct           = 2,
    .iSerialNumber      = INTSERIALNO_DESCRIPTOR,//3,
    .bNumConfigurations = 1,
};

/* Device configuration descriptor */
static const struct hid_config config_desc = {
    .config = {
        .bLength                = sizeof(struct usb_config_descriptor),
        .bDescriptorType        = USB_DTYPE_CONFIGURATION,
        .wTotalLength           = sizeof(struct hid_config),
        .bNumInterfaces         = 1,
        .bConfigurationValue    = 1,
        .iConfiguration         = NO_DESCRIPTOR,
        .bmAttributes           = USB_CFG_ATTR_RESERVED | USB_CFG_ATTR_SELFPOWERED,
        .bMaxPower              = USB_CFG_POWER_MA(200),
    },
    .hid = {
        .bLength                = sizeof(struct usb_interface_descriptor),
        .bDescriptorType        = USB_DTYPE_INTERFACE,
        .bInterfaceNumber       = 0,
        .bAlternateSetting      = 0,
        .bNumEndpoints          = 1,
        .bInterfaceClass        = USB_CLASS_HID,
        .bInterfaceSubClass     = USB_HID_SUBCLASS_NONBOOT,
        .bInterfaceProtocol     = USB_HID_PROTO_NONBOOT,
        .iInterface             = NO_DESCRIPTOR,
    },
    .hid_desc = {
        .bLength                = sizeof(struct usb_hid_descriptor),
        .bDescriptorType        = USB_DTYPE_HID,
        .bcdHID                 = VERSION_BCD(1,1,1),
        .bCountryCode           = USB_HID_COUNTRY_NONE,
        .bNumDescriptors        = 1,
        .bDescriptorType0       = USB_DTYPE_HID_REPORT,
        .wDescriptorLength0     = sizeof(hid_report_desc),
    },
    .hid_ep_in = {
        .bLength                = sizeof(struct usb_endpoint_descriptor),
        .bDescriptorType        = USB_DTYPE_ENDPOINT,
        .bEndpointAddress       = HID_RIN_EP,
        .bmAttributes           = USB_EPTYPE_INTERRUPT,
        .wMaxPacketSize         = HID_RIN_SZ,
        .bInterval              = 6,
    },
};

static const struct usb_string_descriptor lang_desc     = USB_ARRAY_DESC(USB_LANGID_ENG_US);
static const struct usb_string_descriptor manuf_desc_en = USB_STRING_DESC("STMicroelectronics");
static const struct usb_string_descriptor prod_desc_en  = USB_STRING_DESC("Hermit keyboard by orihikarna");
static const struct usb_string_descriptor *const dtable[] = {
    &lang_desc,
    &manuf_desc_en,
    &prod_desc_en,
};

usbd_device udev;

static usbd_respond hid_getdesc(usbd_ctlreq *req, void **address, uint16_t *length) {
    const uint8_t dtype = req->wValue >> 8;
    const uint8_t dnumber = req->wValue & 0xFF;
    //printf( "getdesc: dtype = %02x, dnumber = %02x, address = %p\n", dtype, dnumber, address );
    const void* desc;
    uint16_t len = 0;
    switch (dtype) {
    case USB_DTYPE_DEVICE:
        desc = &device_desc;
        break;
    case USB_DTYPE_CONFIGURATION:
        desc = &config_desc;
        len = sizeof(config_desc);
        break;
    case USB_DTYPE_STRING:
        if (dnumber < 3) {
            desc = dtable[dnumber];
        } else {
            return usbd_fail;
        }
        break;
    default:
        return usbd_fail;
    }
    if (len == 0) {
        len = ((struct usb_header_descriptor*)desc)->bLength;
    }
    *address = (void*)desc;
    *length = len;
    return usbd_ack;
}


static usbd_respond hid_control(usbd_device *dev, usbd_ctlreq *req, usbd_rqc_callback *callback) {
    if (((USB_REQ_RECIPIENT | USB_REQ_TYPE) & req->bmRequestType) == (USB_REQ_INTERFACE | USB_REQ_CLASS)
        && req->wIndex == 0 ) {
        LOG_DEBUG( "control CLASS: reqtype = %02x, req = %02x, value = %04x", req->bmRequestType, req->bRequest, req->wValue );
        switch (req->bRequest) {
        case USB_HID_SETIDLE:// 0x0A
            return usbd_ack;
        case USB_HID_GETREPORT:// 0x01
            if (0) {
              dev->status.data_ptr = &hid_report_mouse_data;
              dev->status.data_count = sizeof(hid_report_mouse_data);
            } else {
              dev->status.data_ptr = get_keyboard_report();
              dev->status.data_count = sizeof(KeyboardHID);
            }
            return usbd_ack;
        case USB_HID_SETREPORT:// 0x09
            LOG_DEBUG( "control CLASS SetReport: cnt = %d, ptr = %p, [0] = %d, [1] = %d", dev->status.data_count, dev->status.data_ptr,
                ((uint8_t*)dev->status.data_ptr)[0], ((uint8_t*)dev->status.data_ptr)[1] );
            set_led_state( LED_LEFT, ((uint8_t*)dev->status.data_ptr)[0] );
            return usbd_ack;
        default:
            return usbd_fail;
        }
    }
    if (((USB_REQ_RECIPIENT | USB_REQ_TYPE) & req->bmRequestType) == (USB_REQ_INTERFACE | USB_REQ_STANDARD)
        && req->wIndex == 0) {
        LOG_DEBUG( "control STANDARD: reqtype = %02x, req = %02x, value = %04x", req->bmRequestType, req->bRequest, req->wValue );
        if (req->bRequest == USB_STD_GET_DESCRIPTOR) {
            switch (req->wValue >> 8) {
            case USB_DTYPE_HID:// 0x21
                dev->status.data_ptr = (uint8_t*)&(config_desc.hid_desc);
                dev->status.data_count = sizeof(config_desc.hid_desc);
                return usbd_ack;
            case USB_DTYPE_HID_REPORT:// 0x22
                dev->status.data_ptr = (uint8_t*)hid_report_desc;
                dev->status.data_count = sizeof(hid_report_desc);
                return usbd_ack;
            default:
                return usbd_fail;
            }
            LOG_DEBUG( "control STANDARD GetDesc: value = %04x", req->wValue );
        }
    }
    LOG_DEBUG( "control no_proc: reqtype = %02x, index = %04x, req = %02x, value = %04x", req->bmRequestType, req->wIndex, req->bRequest, req->wValue );
    return usbd_fail;
}

/* HID mouse IN endpoint callback */
static void hid_mouse_move(usbd_device *dev, uint8_t event, uint8_t ep) {
    static uint8_t t = 0;
    if (t < 0x10) {
        hid_report_mouse_data.m_x = 1;
        hid_report_mouse_data.m_y = 0;
    } else if (t < 0x20) {
        hid_report_mouse_data.m_x = 1;
        hid_report_mouse_data.m_y = 1;
    } else if (t < 0x30) {
        hid_report_mouse_data.m_x = 0;
        hid_report_mouse_data.m_y = 1;
    } else if (t < 0x40) {
        hid_report_mouse_data.m_x = -1;
        hid_report_mouse_data.m_y = 1;
    } else if (t < 0x50) {
        hid_report_mouse_data.m_x = -1;
        hid_report_mouse_data.m_y = 0;
    } else if (t < 0x60) {
        hid_report_mouse_data.m_x = -1;
        hid_report_mouse_data.m_y = -1;
    } else if (t < 0x70) {
        hid_report_mouse_data.m_x = 0;
        hid_report_mouse_data.m_y = -1;
    } else  {
        hid_report_mouse_data.m_x = 1;
        hid_report_mouse_data.m_y = -1;
    }
    t = (t + 1) & 0x7F;
    usbd_ep_write(dev, ep, &hid_report_mouse_data, sizeof(hid_report_mouse_data));
}

/* HID keyboard IN endpoint callback */
static void hid_keyboard_input(usbd_device *dev, uint8_t event, uint8_t ep) {
    if (event != usbd_evt_eptx) {
        LOG_DEBUG( "hid_keyboard_input: event = %d", event );
        return;
    }
#if 0
    memset( &hid_report_keyboard_data, 0, sizeof(hid_report_keyboard_data) );

    static uint16_t t = 0;
    if (t < 0x10) {
        hid_report_keyboard_data.m_modifiers = 0x02;//LSHIFT
        //hid_report_keyboard_data.m_keys[0] = HID_KEYBOARD_CAPS_LOCK;//HID_KEYPAD_NUMLOCK
        //hid_report_keyboard_data.m_keys[0] = HID_KEYBOARD_A;
    }
    usbd_ep_write(dev, ep, &hid_report_keyboard_data, sizeof(KeyboardHID));
    t = (t + 1) & 0x03ff;
    if (t == 0) {
      //printf( "t = %d\n", t );
    }
#else
    usbd_ep_write(dev, ep, get_keyboard_report(), sizeof(KeyboardHID));
#endif
}

static usbd_respond hid_setconf(usbd_device *dev, uint8_t cfg) {
    switch (cfg) {
    case 0:
        /* deconfiguring device */
        usbd_ep_deconfig(dev, HID_RIN_EP);
        usbd_reg_endpoint(dev, HID_RIN_EP, NULL);
        return usbd_ack;
    case 1:
        usbd_ep_config(dev, HID_RIN_EP, USB_EPTYPE_INTERRUPT, HID_RIN_SZ);
        //usbd_reg_endpoint(dev, HID_RIN_EP, hid_mouse_move);
        usbd_reg_endpoint(dev, HID_RIN_EP, hid_keyboard_input);
        usbd_ep_write(dev, HID_RIN_EP, 0, 0);
        return usbd_ack;
    default:
        return usbd_fail;
    }
}

uint32_t ubuf[4];
static void hid_init_usbd(void) {
    usbd_init(&udev, &usbd_hw, HID_EP0_SIZE, ubuf, sizeof(ubuf));
    usbd_reg_config(&udev, hid_setconf);
    usbd_reg_control(&udev, hid_control);
    usbd_reg_descr(&udev, hid_getdesc);
}

#if defined(HID_USE_IRQ)
#if defined(STM32L052xx) || defined(STM32F070xB) || \
	defined(STM32F042x6)
#define USB_HANDLER     USB_IRQHandler
    #define USB_NVIC_IRQ    USB_IRQn
#elif defined(STM32L100xC) || defined(STM32G4)
    #define USB_HANDLER     USB_LP_IRQHandler
    #define USB_NVIC_IRQ    USB_LP_IRQn
#elif defined(USBD_PRIMARY_OTGHS) && \
    (defined(STM32F446xx) || defined(STM32F429xx))
    #define USB_HANDLER     OTG_HS_IRQHandler
    #define USB_NVIC_IRQ    OTG_HS_IRQn
    /* WA. With __WFI/__WFE interrupt will not be fired
     * faced with F4 series and OTGHS only
     */
    #undef  __WFI
    #define __WFI __NOP
#elif defined(STM32L476xx) || defined(STM32F429xx) || \
      defined(STM32F105xC) || defined(STM32F107xC) || \
      defined(STM32F446xx)
    #define USB_HANDLER     OTG_FS_IRQHandler
    #define USB_NVIC_IRQ    OTG_FS_IRQn
#elif defined(STM32F103x6)
    #define USB_HANDLER     USB_LP_CAN1_RX0_IRQHandler
    #define USB_NVIC_IRQ    USB_LP_CAN1_RX0_IRQn
#elif defined(STM32F103xE)
    #define USB_HANDLER     USB_LP_CAN1_RX0_IRQHandler
    #define USB_NVIC_IRQ    USB_LP_CAN1_RX0_IRQn
#else
    #error Not supported
#endif

void USB_HANDLER( void ) {
    usbd_poll(&udev);
}

void usb_setup() {
  hid_init_usbd();
  NVIC_EnableIRQ(USB_NVIC_IRQ);
  usbd_enable(&udev, true);
  usbd_connect(&udev, true);
}

void usb_loop(void) {
    while(1) {
        __WFI();
    }
}
#else
void usb_setup(void) {
  hid_init_usbd();
  usbd_enable(&udev, true);
  usbd_connect(&udev, true);
}
void usb_loop(void) {
  usbd_poll(&udev);
}
#endif
