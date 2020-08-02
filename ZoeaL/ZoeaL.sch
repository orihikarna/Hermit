EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:L_Core_Ferrite_Small L1
U 1 1 5D58BBB6
P 4675 875
F 0 "L1" V 4880 875 50  0000 C CNN
F 1 "BLM21" V 4789 875 50  0000 C CNN
F 2 "Inductor_SMD:L_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4675 875 50  0001 C CNN
F 3 "~" H 4675 875 50  0001 C CNN
	1    4675 875 
	0    -1   -1   0   
$EndComp
$Comp
L Device:C_Small C1
U 1 1 5D58CD5E
P 4050 1025
F 0 "C1" H 4150 1025 50  0000 L CNN
F 1 "1uF" H 4150 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4050 1025 50  0001 C CNN
F 3 "~" H 4050 1025 50  0001 C CNN
	1    4050 1025
	1    0    0    -1  
$EndComp
Text GLabel 4850 2425 0    50   Input ~ 0
VBUS
$Comp
L power:GND #PWR0102
U 1 1 5D59D835
P 5450 3925
F 0 "#PWR0102" H 5450 3675 50  0001 C CNN
F 1 "GND" H 5455 3752 50  0000 C CNN
F 2 "" H 5450 3925 50  0001 C CNN
F 3 "" H 5450 3925 50  0001 C CNN
	1    5450 3925
	1    0    0    -1  
$EndComp
NoConn ~ 4850 3525
NoConn ~ 4850 3625
$Comp
L Device:R_Small R6
U 1 1 5D59E7C3
P 4325 3025
F 0 "R6" V 4225 3025 50  0000 C CNN
F 1 "22" V 4325 3025 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4325 3025 50  0001 C CNN
F 3 "~" H 4325 3025 50  0001 C CNN
	1    4325 3025
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R7
U 1 1 5D59EDC5
P 4325 3125
F 0 "R7" V 4425 3125 50  0000 C CNN
F 1 "22" V 4325 3125 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4325 3125 50  0001 C CNN
F 3 "~" H 4325 3125 50  0001 C CNN
	1    4325 3125
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5D5A0DCF
P 3175 3625
F 0 "#PWR0103" H 3175 3375 50  0001 C CNN
F 1 "GND" H 3180 3452 50  0000 C CNN
F 2 "" H 3175 3625 50  0001 C CNN
F 3 "" H 3175 3625 50  0001 C CNN
	1    3175 3625
	1    0    0    -1  
$EndComp
Text GLabel 2675 3425 0    50   Input ~ 0
BOOT0
Text GLabel 2675 1925 0    50   Input ~ 0
NRST
Text GLabel 925  3050 1    50   Input ~ 0
NRST
$Comp
L power:GND #PWR0105
U 1 1 5D5AC005
P 925 3250
F 0 "#PWR0105" H 925 3000 50  0001 C CNN
F 1 "GND" H 930 3077 50  0000 C CNN
F 2 "" H 925 3250 50  0001 C CNN
F 3 "" H 925 3250 50  0001 C CNN
	1    925  3250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5D5C7909
P 925 2350
F 0 "#PWR0107" H 925 2100 50  0001 C CNN
F 1 "GND" H 930 2177 50  0000 C CNN
F 2 "" H 925 2350 50  0001 C CNN
F 3 "" H 925 2350 50  0001 C CNN
	1    925  2350
	1    0    0    -1  
$EndComp
Text GLabel 3875 2125 2    50   Input ~ 0
TX
Text GLabel 3875 2225 2    50   Input ~ 0
RX
Text GLabel 3875 2825 2    50   Input ~ 0
SCL
Text GLabel 3875 2925 2    50   Input ~ 0
SDA
Text GLabel 3875 3225 2    50   Input ~ 0
SWDIO
Text GLabel 3875 3325 2    50   Input ~ 0
SWCLK
$Comp
L power:VCC #PWR0112
U 1 1 5D6C7F18
P 3175 1725
F 0 "#PWR0112" H 3175 1575 50  0001 C CNN
F 1 "VCC" H 3192 1898 50  0000 C CNN
F 2 "" H 3175 1725 50  0001 C CNN
F 3 "" H 3175 1725 50  0001 C CNN
	1    3175 1725
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0113
U 1 1 5D6C84C2
P 3000 875
F 0 "#PWR0113" H 3000 725 50  0001 C CNN
F 1 "VCC" V 3018 1002 50  0000 L CNN
F 2 "" H 3000 875 50  0001 C CNN
F 3 "" H 3000 875 50  0001 C CNN
	1    3000 875 
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED_Small D2
U 1 1 5D82BC0C
P 1425 2050
F 0 "D2" V 1471 1982 50  0000 R CNN
F 1 "LED" V 1380 1982 50  0000 R CNN
F 2 "Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 1425 2050 50  0001 C CNN
F 3 "~" V 1425 2050 50  0001 C CNN
	1    1425 2050
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3000 875  3100 875 
Wire Wire Line
	4050 925  4050 875 
Wire Wire Line
	4050 875  4400 875 
Connection ~ 3100 875 
$Comp
L Device:R_Small R4
U 1 1 5D793A53
P 2000 2100
F 0 "R4" V 2100 2100 50  0000 C CNN
F 1 "2K2" V 2000 2100 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2000 2100 50  0001 C CNN
F 3 "~" H 2000 2100 50  0001 C CNN
	1    2000 2100
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Small R5
U 1 1 5D793A59
P 2150 2100
F 0 "R5" V 2050 2100 50  0000 C CNN
F 1 "2K2" V 2150 2100 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2150 2100 50  0001 C CNN
F 3 "~" H 2150 2100 50  0001 C CNN
	1    2150 2100
	-1   0    0    1   
$EndComp
Text GLabel 2150 2200 3    50   Input ~ 0
SDA
Text GLabel 2000 2200 3    50   Input ~ 0
SCL
$Comp
L Device:C_Small C9
U 1 1 5D68E30A
P 925 3150
F 0 "C9" H 725 3150 50  0000 L CNN
F 1 "0.1uF" H 675 3050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 925 3150 50  0001 C CNN
F 3 "~" H 925 3150 50  0001 C CNN
	1    925  3150
	-1   0    0    -1  
$EndComp
Text Notes 2000 1650 0    50   ~ 10
I2C
Text Notes 825  1650 0    50   ~ 10
Power
Text Notes 1525 1325 0    50   ~ 10
VDDIO2
Connection ~ 1825 1175
Connection ~ 1525 1175
Wire Wire Line
	1525 1175 1825 1175
Wire Wire Line
	1825 1125 1825 1175
Wire Wire Line
	1825 875  2125 875 
Connection ~ 1825 875 
Wire Wire Line
	1825 875  1825 925 
Connection ~ 1525 875 
Wire Wire Line
	1525 875  1825 875 
$Comp
L Device:C_Small C6
U 1 1 5D82028A
P 1825 1025
F 0 "C6" H 1625 1025 50  0000 L CNN
F 1 "4.7uF" H 1575 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1825 1025 50  0001 C CNN
F 3 "~" H 1825 1025 50  0001 C CNN
	1    1825 1025
	1    0    0    -1  
$EndComp
Text Notes 2125 1325 0    50   ~ 10
VDDA
Text Notes 975  1325 0    50   ~ 10
VDD
Connection ~ 2425 1175
Wire Wire Line
	2425 1175 2425 1225
Wire Wire Line
	2425 1175 2425 1125
Wire Wire Line
	2125 1175 2425 1175
Connection ~ 2125 875 
Wire Wire Line
	2425 875  2425 925 
Wire Wire Line
	2125 875  2425 875 
Wire Wire Line
	1225 1175 1525 1175
Connection ~ 1225 1175
Wire Wire Line
	1225 1125 1225 1175
Wire Wire Line
	925  1175 1225 1175
Wire Wire Line
	1225 875  1525 875 
Connection ~ 1225 875 
Wire Wire Line
	1225 925  1225 875 
Wire Wire Line
	925  875  925  925 
Connection ~ 925  875 
Wire Wire Line
	925  875  1225 875 
$Comp
L Device:C_Small C8
U 1 1 5D6549AB
P 2425 1025
F 0 "C8" H 2225 1025 50  0000 L CNN
F 1 "1uF" H 2225 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2425 1025 50  0001 C CNN
F 3 "~" H 2425 1025 50  0001 C CNN
	1    2425 1025
	-1   0    0    -1  
$EndComp
$Comp
L Device:C_Small C4
U 1 1 5D6508EA
P 1225 1025
F 0 "C4" H 1025 1025 50  0000 L CNN
F 1 "4.7uF" H 975 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1225 1025 50  0001 C CNN
F 3 "~" H 1225 1025 50  0001 C CNN
	1    1225 1025
	1    0    0    -1  
$EndComp
Wire Wire Line
	925  775  925  875 
$Comp
L power:VCC #PWR0109
U 1 1 5D6ACF37
P 925 775
F 0 "#PWR0109" H 925 625 50  0001 C CNN
F 1 "VCC" H 942 948 50  0000 C CNN
F 2 "" H 925 775 50  0001 C CNN
F 3 "" H 925 775 50  0001 C CNN
	1    925  775 
	1    0    0    -1  
$EndComp
Wire Wire Line
	925  1125 925  1175
Connection ~ 2125 1175
Wire Wire Line
	1525 1175 1525 1125
Wire Wire Line
	2125 1175 1825 1175
Wire Wire Line
	2125 1125 2125 1175
Wire Wire Line
	2125 875  2125 925 
Wire Wire Line
	1525 875  1525 925 
$Comp
L power:GND #PWR0106
U 1 1 5D5B3F90
P 2425 1225
F 0 "#PWR0106" H 2425 975 50  0001 C CNN
F 1 "GND" H 2430 1052 50  0000 C CNN
F 2 "" H 2425 1225 50  0001 C CNN
F 3 "" H 2425 1225 50  0001 C CNN
	1    2425 1225
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C7
U 1 1 5D5B29FC
P 2125 1025
F 0 "C7" H 1925 1025 50  0000 L CNN
F 1 "0.01uF" H 1825 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2125 1025 50  0001 C CNN
F 3 "~" H 2125 1025 50  0001 C CNN
	1    2125 1025
	-1   0    0    -1  
$EndComp
$Comp
L Device:C_Small C5
U 1 1 5D5B2561
P 1525 1025
F 0 "C5" H 1325 1025 50  0000 L CNN
F 1 "0.1uF" H 1275 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1525 1025 50  0001 C CNN
F 3 "~" H 1525 1025 50  0001 C CNN
	1    1525 1025
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C3
U 1 1 5D5ACDD5
P 925 1025
F 0 "C3" H 725 1025 50  0000 L CNN
F 1 "0.1uF" H 675 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 925 1025 50  0001 C CNN
F 3 "~" H 925 1025 50  0001 C CNN
	1    925  1025
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5D882AB2
P 3550 1175
F 0 "#PWR0114" H 3550 925 50  0001 C CNN
F 1 "GND" H 3555 1002 50  0000 C CNN
F 2 "" H 3550 1175 50  0001 C CNN
F 3 "" H 3550 1175 50  0001 C CNN
	1    3550 1175
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5D59331E
P 3100 1125
F 0 "#PWR0101" H 3100 875 50  0001 C CNN
F 1 "GND" H 3105 952 50  0000 C CNN
F 2 "" H 3100 1125 50  0001 C CNN
F 3 "" H 3100 1125 50  0001 C CNN
	1    3100 1125
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 925  3100 875 
$Comp
L Device:C_Small C2
U 1 1 5D59212D
P 3100 1025
F 0 "C2" H 2900 1025 50  0000 L CNN
F 1 "10uF" H 2850 925 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 3100 1025 50  0001 C CNN
F 3 "~" H 3100 1025 50  0001 C CNN
	1    3100 1025
	1    0    0    -1  
$EndComp
Connection ~ 4050 875 
Text Notes 1350 1650 0    50   ~ 10
LED
Text GLabel 4400 1125 3    50   Input ~ 0
5V
Text GLabel 2000 1875 1    50   Input ~ 0
5V
$Comp
L Device:R_Small R8
U 1 1 5EDECF8F
P 4750 2625
F 0 "R8" V 4650 2625 50  0000 C CNN
F 1 "5k1" V 4750 2625 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4750 2625 50  0001 C CNN
F 3 "~" H 4750 2625 50  0001 C CNN
	1    4750 2625
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R9
U 1 1 5EDECF95
P 4750 2725
F 0 "R9" V 4850 2725 50  0000 C CNN
F 1 "5k1" V 4750 2725 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4750 2725 50  0001 C CNN
F 3 "~" H 4750 2725 50  0001 C CNN
	1    4750 2725
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 5EE005A1
P 4650 2625
F 0 "#PWR0110" H 4650 2375 50  0001 C CNN
F 1 "GND" H 4655 2452 50  0000 C CNN
F 2 "" H 4650 2625 50  0001 C CNN
F 3 "" H 4650 2625 50  0001 C CNN
	1    4650 2625
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 5EE040F8
P 4650 2725
F 0 "#PWR0117" H 4650 2475 50  0001 C CNN
F 1 "GND" H 4655 2552 50  0000 C CNN
F 2 "" H 4650 2725 50  0001 C CNN
F 3 "" H 4650 2725 50  0001 C CNN
	1    4650 2725
	0    1    1    0   
$EndComp
Wire Wire Line
	4400 1125 4400 875 
Connection ~ 4400 875 
Wire Wire Line
	4400 875  4575 875 
NoConn ~ 3875 2725
NoConn ~ 2675 3325
Wire Wire Line
	3100 875  3250 875 
$Comp
L key-parts:AP7333 U2
U 1 1 5EE69AFC
P 3550 925
F 0 "U2" H 3550 1240 50  0000 C CNN
F 1 "AP7333" H 3550 1149 50  0000 C CNN
F 2 "key-parts:AP7333" H 3550 925 50  0001 C CNN
F 3 "" H 3550 925 50  0001 C CNN
	1    3550 925 
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3850 875  4050 875 
$Comp
L power:GND #PWR0119
U 1 1 5EE77B4D
P 4050 1125
F 0 "#PWR0119" H 4050 875 50  0001 C CNN
F 1 "GND" H 4055 952 50  0000 C CNN
F 2 "" H 4050 1125 50  0001 C CNN
F 3 "" H 4050 1125 50  0001 C CNN
	1    4050 1125
	1    0    0    -1  
$EndComp
Text GLabel 925  1950 1    50   Input ~ 0
VBUS
Wire Wire Line
	3275 3625 3175 3625
Wire Wire Line
	4425 3025 4850 3025
Wire Wire Line
	4425 3125 4850 3125
Wire Wire Line
	4850 2925 4850 3025
Wire Wire Line
	4850 3125 4850 3225
Wire Wire Line
	2000 2000 2000 1950
Wire Wire Line
	2000 1950 2150 1950
Wire Wire Line
	2150 1950 2150 2000
Connection ~ 2000 1950
Wire Wire Line
	2000 1950 2000 1875
Wire Wire Line
	4775 875  4925 875 
Wire Wire Line
	5125 875  5225 875 
$Comp
L Device:Polyfuse_Small F1
U 1 1 5D958CA7
P 5025 875
F 0 "F1" V 4820 875 50  0000 C CNN
F 1 "Polyfuse" V 4911 875 50  0000 C CNN
F 2 "Fuse:Fuse_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5075 675 50  0001 L CNN
F 3 "~" H 5025 875 50  0001 C CNN
	1    5025 875 
	0    1    1    0   
$EndComp
Text GLabel 5225 875  2    50   Input ~ 0
VBUS
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5EE08314
P 5225 1125
F 0 "#FLG0101" H 5225 1200 50  0001 C CNN
F 1 "PWR_FLAG" V 5225 1252 50  0000 L CNN
F 2 "" H 5225 1125 50  0001 C CNN
F 3 "~" H 5225 1125 50  0001 C CNN
	1    5225 1125
	0    -1   -1   0   
$EndComp
Text GLabel 5225 1125 2    50   Input ~ 0
VBUS
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5EE0C882
P 5225 1425
F 0 "#FLG0102" H 5225 1500 50  0001 C CNN
F 1 "PWR_FLAG" V 5225 1552 50  0000 L CNN
F 2 "" H 5225 1425 50  0001 C CNN
F 3 "~" H 5225 1425 50  0001 C CNN
	1    5225 1425
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 5EE0F27F
P 5225 1425
F 0 "#PWR0118" H 5225 1175 50  0001 C CNN
F 1 "GND" H 5230 1252 50  0000 C CNN
F 2 "" H 5225 1425 50  0001 C CNN
F 3 "" H 5225 1425 50  0001 C CNN
	1    5225 1425
	0    -1   -1   0   
$EndComp
Text GLabel 1425 1950 1    50   Input ~ 0
PA15
$Comp
L power:GND #PWR0116
U 1 1 5EE6D829
P 1425 2350
F 0 "#PWR0116" H 1425 2100 50  0001 C CNN
F 1 "GND" H 1430 2177 50  0000 C CNN
F 2 "" H 1425 2350 50  0001 C CNN
F 3 "" H 1425 2350 50  0001 C CNN
	1    1425 2350
	1    0    0    -1  
$EndComp
$Comp
L key-parts:USB_C_Receptacle_USB2.0 J2
U 1 1 5EE9945F
P 5450 3025
F 0 "J2" H 5500 3975 50  0000 R CNN
F 1 "USB_C_Receptacle_USB2.0" H 5950 3825 50  0000 R CNN
F 2 "key-parts:USB_C_Receptacle_Hirose_CX90M-16P" H 5600 3025 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 5600 3025 50  0001 C CNN
	1    5450 3025
	-1   0    0    -1  
$EndComp
Connection ~ 4850 3125
Connection ~ 4850 3025
Text GLabel 3875 3425 2    50   Input ~ 0
PA15
$Comp
L power:PWR_FLAG #FLG0103
U 1 1 5EECD08C
P 5225 1275
F 0 "#FLG0103" H 5225 1350 50  0001 C CNN
F 1 "PWR_FLAG" V 5225 1402 50  0000 L CNN
F 2 "" H 5225 1275 50  0001 C CNN
F 3 "~" H 5225 1275 50  0001 C CNN
	1    5225 1275
	0    -1   -1   0   
$EndComp
Text GLabel 5225 1275 2    50   Input ~ 0
5V
NoConn ~ 2675 3225
$Comp
L Device:R_Small R2
U 1 1 5D82BC12
P 1425 2250
F 0 "R2" V 1525 2250 50  0000 C CNN
F 1 "330" V 1425 2250 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1425 2250 50  0001 C CNN
F 3 "~" H 1425 2250 50  0001 C CNN
	1    1425 2250
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_Small R1
U 1 1 5D5C71CB
P 925 2250
F 0 "R1" V 1025 2250 50  0000 C CNN
F 1 "1K5" V 925 2250 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 925 2250 50  0001 C CNN
F 3 "~" H 925 2250 50  0001 C CNN
	1    925  2250
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED_Small D1
U 1 1 5D5C4E5A
P 925 2050
F 0 "D1" V 971 1982 50  0000 R CNN
F 1 "PW_LED" V 880 1982 50  0000 R CNN
F 2 "Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 925 2050 50  0001 C CNN
F 3 "~" V 925 2050 50  0001 C CNN
	1    925  2050
	0    1    -1   0   
$EndComp
$Comp
L power:GND #PWR0121
U 1 1 5EFB7ADD
P 5750 3925
F 0 "#PWR0121" H 5750 3675 50  0001 C CNN
F 1 "GND" H 5755 3752 50  0000 C CNN
F 2 "" H 5750 3925 50  0001 C CNN
F 3 "" H 5750 3925 50  0001 C CNN
	1    5750 3925
	1    0    0    -1  
$EndComp
$Comp
L Device:D_Small D11
U 1 1 5F27C416
P 3450 4700
F 0 "D11" V 3450 4632 50  0000 R CNN
F 1 "D_Small" V 3405 4632 50  0001 R CNN
F 2 "key-parts:D_SMD" V 3450 4700 50  0001 C CNN
F 3 "~" V 3450 4700 50  0001 C CNN
	1    3450 4700
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_Small R12
U 1 1 5F2705F9
P 3050 6250
F 0 "R12" H 3109 6296 50  0000 L CNN
F 1 "4k7" V 3050 6175 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 3050 6250 50  0001 C CNN
F 3 "~" H 3050 6250 50  0001 C CNN
	1    3050 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R11
U 1 1 5F27F3A4
P 2900 6100
F 0 "R11" V 2975 6100 50  0000 C CNN
F 1 "10k" V 2900 6100 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2900 6100 50  0001 C CNN
F 3 "~" H 2900 6100 50  0001 C CNN
	1    2900 6100
	0    1    1    0   
$EndComp
Text GLabel 2700 6100 0    50   Input ~ 0
COL1
Wire Wire Line
	2750 6100 2800 6100
$Comp
L Device:R_Small RB2
U 1 1 5F2B884A
P 2150 6250
F 0 "RB2" H 2209 6296 50  0000 L CNN
F 1 "4k7" V 2150 6175 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2150 6250 50  0001 C CNN
F 3 "~" H 2150 6250 50  0001 C CNN
	1    2150 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small RB1
U 1 1 5F2B8850
P 2000 6100
F 0 "RB1" V 2075 6100 50  0000 C CNN
F 1 "10k" V 2000 6100 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2000 6100 50  0001 C CNN
F 3 "~" H 2000 6100 50  0001 C CNN
	1    2000 6100
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small CB1
U 1 1 5F2B8856
P 1850 6000
F 0 "CB1" H 1600 6000 50  0000 L CNN
F 1 "33n" H 1700 6075 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1850 6000 50  0001 C CNN
F 3 "~" H 1850 6000 50  0001 C CNN
	1    1850 6000
	1    0    0    -1  
$EndComp
Text GLabel 1800 6100 0    50   Input ~ 0
BOOT0
Wire Wire Line
	1850 6100 1900 6100
Text GLabel 3900 4925 2    50   Input ~ 0
ROW2
Text GLabel 3900 4600 2    50   Input ~ 0
ROW1
$Comp
L Device:C_Small C11
U 1 1 5F27129C
P 2750 6000
F 0 "C11" H 2500 6000 50  0000 L CNN
F 1 "33n" H 2600 6075 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2750 6000 50  0001 C CNN
F 3 "~" H 2750 6000 50  0001 C CNN
	1    2750 6000
	1    0    0    -1  
$EndComp
$Comp
L Device:D_Small D12
U 1 1 5F31DFD5
P 3450 5025
F 0 "D12" V 3450 4957 50  0000 R CNN
F 1 "D_Small" V 3405 4957 50  0001 R CNN
F 2 "key-parts:D_SMD" V 3450 5025 50  0001 C CNN
F 3 "~" V 3450 5025 50  0001 C CNN
	1    3450 5025
	0    -1   -1   0   
$EndComp
$Comp
L Device:D_Small D21
U 1 1 5F32238F
P 3450 5350
F 0 "D21" V 3450 5282 50  0000 R CNN
F 1 "D_Small" V 3405 5282 50  0001 R CNN
F 2 "key-parts:D_SMD" V 3450 5350 50  0001 C CNN
F 3 "~" V 3450 5350 50  0001 C CNN
	1    3450 5350
	0    -1   -1   0   
$EndComp
$Comp
L Device:D_Small D22
U 1 1 5F32239B
P 3450 5675
F 0 "D22" V 3450 5607 50  0000 R CNN
F 1 "D_Small" V 3405 5607 50  0001 R CNN
F 2 "key-parts:D_SMD" V 3450 5675 50  0001 C CNN
F 3 "~" V 3450 5675 50  0001 C CNN
	1    3450 5675
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5F343F61
P 3050 6350
F 0 "#PWR0108" H 3050 6100 50  0001 C CNN
F 1 "GND" H 3055 6177 50  0000 C CNN
F 2 "" H 3050 6350 50  0001 C CNN
F 3 "" H 3050 6350 50  0001 C CNN
	1    3050 6350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0115
U 1 1 5F344492
P 2150 6350
F 0 "#PWR0115" H 2150 6100 50  0001 C CNN
F 1 "GND" H 2155 6177 50  0000 C CNN
F 2 "" H 2150 6350 50  0001 C CNN
F 3 "" H 2150 6350 50  0001 C CNN
	1    2150 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 6100 2750 6100
Connection ~ 2750 6100
Wire Wire Line
	1850 6100 1800 6100
Connection ~ 1850 6100
$Comp
L key-parts:USB_C_Receptacle_USB2.0 J1
U 1 1 5F3B2099
P 6675 3025
F 0 "J1" H 6725 3975 50  0000 R CNN
F 1 "USB_C_Receptacle_USB2.0" H 7175 3825 50  0000 R CNN
F 2 "key-parts:USB_C_Receptacle_Hirose_CX90M-16P" H 6825 3025 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 6825 3025 50  0001 C CNN
	1    6675 3025
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0123
U 1 1 5F3D4915
P 6375 3925
F 0 "#PWR0123" H 6375 3675 50  0001 C CNN
F 1 "GND" H 6380 3752 50  0000 C CNN
F 2 "" H 6375 3925 50  0001 C CNN
F 3 "" H 6375 3925 50  0001 C CNN
	1    6375 3925
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0124
U 1 1 5F3D491B
P 6675 3925
F 0 "#PWR0124" H 6675 3675 50  0001 C CNN
F 1 "GND" H 6680 3752 50  0000 C CNN
F 2 "" H 6675 3925 50  0001 C CNN
F 3 "" H 6675 3925 50  0001 C CNN
	1    6675 3925
	1    0    0    -1  
$EndComp
Text GLabel 7275 2425 2    50   Input ~ 0
5V
Text GLabel 7275 3625 2    50   Input ~ 0
LDO
Text GLabel 7275 3525 2    50   Input ~ 0
LCO
Text GLabel 7325 3125 2    50   Input ~ 0
SDA
Text GLabel 7325 3025 2    50   Input ~ 0
SCL
Wire Wire Line
	7275 2925 7275 3025
Wire Wire Line
	7275 3025 7325 3025
Connection ~ 7275 3025
Wire Wire Line
	7325 3125 7275 3125
Wire Wire Line
	7275 3225 7275 3125
Connection ~ 7275 3125
Text GLabel 6575 1500 0    50   Input ~ 0
NRST
$Comp
L power:GND #PWR0125
U 1 1 5F40307C
P 6575 1600
F 0 "#PWR0125" H 6575 1350 50  0001 C CNN
F 1 "GND" H 6580 1427 50  0000 C CNN
F 2 "" H 6575 1600 50  0001 C CNN
F 3 "" H 6575 1600 50  0001 C CNN
	1    6575 1600
	0    1    1    0   
$EndComp
Text GLabel 6575 1300 0    50   Input ~ 0
SWDIO
Text GLabel 6575 1400 0    50   Input ~ 0
SWCLK
$Comp
L key-parts:STM32F042K6Tx U1
U 1 1 5F431E19
P 3275 2625
F 0 "U1" H 3475 1650 50  0000 C CNN
F 1 "STM32F042K6Tx" H 3850 1650 50  0000 C CNN
F 2 "Package_QFP:LQFP-32_7x7mm_P0.8mm" H 2875 1725 50  0001 R CNN
F 3 "http://www.st.com/st-web-ui/static/active/en/resource/technical/document/datasheet/DM00105814.pdf" H 3275 2625 50  0001 C CNN
	1    3275 2625
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 J3
U 1 1 5F441FB8
P 6775 1300
F 0 "J3" H 6855 1292 50  0000 L CNN
F 1 "Conn_01x06" H 6855 1201 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical" H 6775 1300 50  0001 C CNN
F 3 "~" H 6775 1300 50  0001 C CNN
	1    6775 1300
	1    0    0    -1  
$EndComp
Text GLabel 6575 1100 0    50   Input ~ 0
TX
Text GLabel 6575 1200 0    50   Input ~ 0
RX
NoConn ~ 3875 2525
NoConn ~ 3875 2625
NoConn ~ 2675 2425
NoConn ~ 2675 2525
$Comp
L power:VCC #PWR0126
U 1 1 5F461294
P 1550 5900
F 0 "#PWR0126" H 1550 5750 50  0001 C CNN
F 1 "VCC" H 1567 6073 50  0000 C CNN
F 2 "" H 1550 5900 50  0001 C CNN
F 3 "" H 1550 5900 50  0001 C CNN
	1    1550 5900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1550 5900 1850 5900
Wire Wire Line
	2100 6100 2150 6100
Connection ~ 2150 6100
Wire Wire Line
	2150 6100 2150 6150
Wire Wire Line
	3000 6100 3050 6100
Connection ~ 3050 6100
Wire Wire Line
	3050 6100 3050 6150
Text GLabel 2675 3125 0    50   Input ~ 0
LDI
Text GLabel 2675 2925 0    50   Input ~ 0
LCI
NoConn ~ 2675 3025
Text GLabel 2675 2725 0    50   Input ~ 0
COL1
Text GLabel 3875 2025 2    50   Input ~ 0
ROW2
Text GLabel 3875 1925 2    50   Input ~ 0
ROW1
$Comp
L Device:R_Small R91
U 1 1 5F2474F5
P 7375 2625
F 0 "R91" V 7275 2625 50  0000 C CNN
F 1 "5k1" V 7375 2625 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7375 2625 50  0001 C CNN
F 3 "~" H 7375 2625 50  0001 C CNN
	1    7375 2625
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R92
U 1 1 5F2474FB
P 7375 2725
F 0 "R92" V 7475 2725 50  0000 C CNN
F 1 "5k1" V 7375 2725 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7375 2725 50  0001 C CNN
F 3 "~" H 7375 2725 50  0001 C CNN
	1    7375 2725
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0127
U 1 1 5F247501
P 7475 2625
F 0 "#PWR0127" H 7475 2375 50  0001 C CNN
F 1 "GND" H 7480 2452 50  0000 C CNN
F 2 "" H 7475 2625 50  0001 C CNN
F 3 "" H 7475 2625 50  0001 C CNN
	1    7475 2625
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0128
U 1 1 5F247507
P 7475 2725
F 0 "#PWR0128" H 7475 2475 50  0001 C CNN
F 1 "GND" H 7480 2552 50  0000 C CNN
F 2 "" H 7475 2725 50  0001 C CNN
F 3 "" H 7475 2725 50  0001 C CNN
	1    7475 2725
	0    -1   -1   0   
$EndComp
Text GLabel 5200 5500 0    50   Input ~ 0
LCO
Text GLabel 5200 5600 0    50   Input ~ 0
LDO
Text GLabel 7100 4950 2    50   Input ~ 0
LCI
Text GLabel 7100 5050 2    50   Input ~ 0
LDI
Wire Wire Line
	5750 4850 5750 4700
$Comp
L power:GND #PWR0122
U 1 1 5F36D82A
P 7150 4700
F 0 "#PWR0122" H 7150 4450 50  0001 C CNN
F 1 "GND" H 7155 4527 50  0000 C CNN
F 2 "" H 7150 4700 50  0001 C CNN
F 3 "" H 7150 4700 50  0001 C CNN
	1    7150 4700
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5350 4850 5350 4750
Wire Wire Line
	5300 4750 5350 4750
Text GLabel 5300 4750 0    50   Input ~ 0
5V
Wire Wire Line
	5750 5050 5800 5050
Wire Wire Line
	5750 4950 5800 4950
Wire Wire Line
	3450 4600 3900 4600
Wire Wire Line
	3450 4925 3900 4925
Text GLabel 3900 5250 2    50   Input ~ 0
ROW3
Text GLabel 3900 5575 2    50   Input ~ 0
ROW4
Wire Wire Line
	3450 5575 3900 5575
Wire Wire Line
	3450 5250 3900 5250
Connection ~ 1850 5900
Wire Wire Line
	1850 5900 2750 5900
$Comp
L power:VCC #PWR0104
U 1 1 5F2C5F12
P 2550 5175
F 0 "#PWR0104" H 2550 5025 50  0001 C CNN
F 1 "VCC" H 2567 5348 50  0000 C CNN
F 2 "" H 2550 5175 50  0001 C CNN
F 3 "" H 2550 5175 50  0001 C CNN
	1    2550 5175
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 4700 6200 4700
Wire Wire Line
	6200 4850 6200 4700
Connection ~ 6200 4700
Wire Wire Line
	6200 4700 6650 4700
Wire Wire Line
	5350 4750 5800 4750
Wire Wire Line
	5800 4750 5800 4850
Connection ~ 5350 4750
Wire Wire Line
	6200 4950 6250 4950
Wire Wire Line
	6200 5050 6250 5050
Wire Wire Line
	5800 4750 6250 4750
Wire Wire Line
	6250 4750 6250 4850
Connection ~ 5800 4750
Wire Wire Line
	6650 4950 6700 4950
Wire Wire Line
	6650 5050 6700 5050
Wire Wire Line
	6250 4750 6700 4750
Wire Wire Line
	6700 4750 6700 4850
Connection ~ 6250 4750
Wire Wire Line
	6650 4850 6650 4700
Connection ~ 6650 4700
Wire Wire Line
	6650 4700 7100 4700
Wire Wire Line
	7100 4850 7100 4700
Connection ~ 7100 4700
Wire Wire Line
	7100 4700 7150 4700
Text GLabel 5200 5400 0    50   Input ~ 0
5V
$Comp
L power:GND #PWR0111
U 1 1 5F3285E2
P 5600 5400
F 0 "#PWR0111" H 5600 5150 50  0001 C CNN
F 1 "GND" H 5605 5227 50  0000 C CNN
F 2 "" H 5600 5400 50  0001 C CNN
F 3 "" H 5600 5400 50  0001 C CNN
	1    5600 5400
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5350 4950 5300 4950
Wire Wire Line
	5300 4950 5300 5150
Wire Wire Line
	5300 5150 5900 5150
Wire Wire Line
	5900 5150 5900 5500
Wire Wire Line
	5900 5500 5600 5500
Wire Wire Line
	5350 5050 5350 5200
Wire Wire Line
	5350 5200 5850 5200
Wire Wire Line
	5850 5200 5850 5600
Wire Wire Line
	5850 5600 5600 5600
NoConn ~ 2675 2825
Text GLabel 3875 2425 2    50   Input ~ 0
ROW4
Text GLabel 3875 2325 2    50   Input ~ 0
ROW3
$Comp
L key-parts:SW_ChocV2 SW11
U 1 1 5F360028
P 3250 4800
F 0 "SW11" H 3250 4993 50  0000 C CNN
F 1 "SW_ChocV2" H 3250 4740 50  0001 C CNN
F 2 "key-parts:ChocV2" H 3250 5000 50  0001 C CNN
F 3 "~" H 3250 5000 50  0001 C CNN
	1    3250 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 4800 3050 5125
$Comp
L key-parts:SW_ChocV2 SW12
U 1 1 5F361FBB
P 3250 5125
F 0 "SW12" H 3250 5318 50  0000 C CNN
F 1 "SW_ChocV2" H 3250 5065 50  0001 C CNN
F 2 "key-parts:ChocV2" H 3250 5325 50  0001 C CNN
F 3 "~" H 3250 5325 50  0001 C CNN
	1    3250 5125
	1    0    0    -1  
$EndComp
Connection ~ 3050 5125
Wire Wire Line
	3050 5125 3050 5450
$Comp
L key-parts:SW_ChocV2 SW13
U 1 1 5F362478
P 3250 5450
F 0 "SW13" H 3250 5643 50  0000 C CNN
F 1 "SW_ChocV2" H 3250 5390 50  0001 C CNN
F 2 "key-parts:ChocV2" H 3250 5650 50  0001 C CNN
F 3 "~" H 3250 5650 50  0001 C CNN
	1    3250 5450
	1    0    0    -1  
$EndComp
Connection ~ 3050 5450
Wire Wire Line
	3050 5450 3050 5775
$Comp
L key-parts:SW_ChocV2 SW14
U 1 1 5F362A91
P 3250 5775
F 0 "SW14" H 3250 5968 50  0000 C CNN
F 1 "SW_ChocV2" H 3250 5715 50  0001 C CNN
F 2 "key-parts:ChocV2" H 3250 5975 50  0001 C CNN
F 3 "~" H 3250 5975 50  0001 C CNN
	1    3250 5775
	1    0    0    -1  
$EndComp
Connection ~ 3050 5775
Wire Wire Line
	3050 5775 3050 6100
$Comp
L power:GND #PWR0120
U 1 1 5F363FED
P 3350 5825
F 0 "#PWR0120" H 3350 5575 50  0001 C CNN
F 1 "GND" H 3355 5652 50  0000 C CNN
F 2 "" H 3350 5825 50  0001 C CNN
F 3 "" H 3350 5825 50  0001 C CNN
	1    3350 5825
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 5825 3350 5500
Connection ~ 3350 5825
Connection ~ 3350 5175
Wire Wire Line
	3350 5175 3350 4850
Connection ~ 3350 5500
Wire Wire Line
	3350 5500 3350 5175
$Comp
L key-parts:SW_ChocV2 SWB1
U 1 1 5F3947D1
P 2350 5475
F 0 "SWB1" H 2250 5675 50  0000 L CNN
F 1 "SW_ChocV2" H 2350 5625 50  0001 C CNN
F 2 "key-parts:ChocV2" H 2350 5675 50  0001 C CNN
F 3 "~" H 2350 5675 50  0001 C CNN
	1    2350 5475
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0129
U 1 1 5F39CC3E
P 2450 5525
F 0 "#PWR0129" H 2450 5275 50  0001 C CNN
F 1 "GND" H 2455 5352 50  0000 C CNN
F 2 "" H 2450 5525 50  0001 C CNN
F 3 "" H 2450 5525 50  0001 C CNN
	1    2450 5525
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 5475 2150 6100
Wire Wire Line
	2550 5175 2550 5475
Wire Wire Line
	3275 1725 3375 1725
Connection ~ 3175 3625
Wire Wire Line
	3175 1725 3275 1725
Connection ~ 3175 1725
Connection ~ 3275 1725
Wire Wire Line
	3875 3025 4225 3025
Wire Wire Line
	3875 3125 4225 3125
$Comp
L key-parts:LC8822 L11
U 1 1 5F26E33C
P 6900 4950
F 0 "L11" H 6900 5212 51  0000 C CNN
F 1 "LC8822" H 6900 5147 16  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 6900 4950 60  0001 C CNN
F 3 "" H 6900 4950 60  0001 C CNN
	1    6900 4950
	1    0    0    -1  
$EndComp
$Comp
L key-parts:LC8822 L12
U 1 1 5F272A89
P 6450 4950
F 0 "L12" H 6450 5212 51  0000 C CNN
F 1 "LC8822" H 6450 5147 16  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 6450 4950 60  0001 C CNN
F 3 "" H 6450 4950 60  0001 C CNN
	1    6450 4950
	1    0    0    -1  
$EndComp
$Comp
L key-parts:LC8822 L13
U 1 1 5F272FE2
P 6000 4950
F 0 "L13" H 6000 5212 51  0000 C CNN
F 1 "LC8822" H 6000 5147 16  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 6000 4950 60  0001 C CNN
F 3 "" H 6000 4950 60  0001 C CNN
	1    6000 4950
	1    0    0    -1  
$EndComp
$Comp
L key-parts:LC8822 L14
U 1 1 5F273558
P 5550 4950
F 0 "L14" H 5550 5212 51  0000 C CNN
F 1 "LC8822" H 5550 5147 16  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 5550 4950 60  0001 C CNN
F 3 "" H 5550 4950 60  0001 C CNN
	1    5550 4950
	1    0    0    -1  
$EndComp
$Comp
L key-parts:LC8822 LB1
U 1 1 5F273C47
P 5400 5500
F 0 "LB1" H 5400 5762 51  0000 C CNN
F 1 "LC8822" H 5400 5697 16  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 5400 5500 60  0001 C CNN
F 3 "" H 5400 5500 60  0001 C CNN
	1    5400 5500
	1    0    0    -1  
$EndComp
$EndSCHEMATC
