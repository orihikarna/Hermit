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
P 5575 1000
F 0 "L1" V 5780 1000 50  0000 C CNN
F 1 "BLM21" V 5689 1000 50  0000 C CNN
F 2 "Inductor_SMD:L_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5575 1000 50  0001 C CNN
F 3 "~" H 5575 1000 50  0001 C CNN
	1    5575 1000
	0    -1   -1   0   
$EndComp
$Comp
L Device:C_Small C1
U 1 1 5D58CD5E
P 4950 1150
F 0 "C1" H 5050 1150 50  0000 L CNN
F 1 "1uF" H 5050 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4950 1150 50  0001 C CNN
F 3 "~" H 4950 1150 50  0001 C CNN
	1    4950 1150
	1    0    0    -1  
$EndComp
Text GLabel 5175 2775 0    50   Input ~ 0
VBUS
$Comp
L power:GND #PWR0102
U 1 1 5D59D835
P 5775 4275
F 0 "#PWR0102" H 5775 4025 50  0001 C CNN
F 1 "GND" H 5780 4102 50  0000 C CNN
F 2 "" H 5775 4275 50  0001 C CNN
F 3 "" H 5775 4275 50  0001 C CNN
	1    5775 4275
	1    0    0    -1  
$EndComp
NoConn ~ 5175 3875
NoConn ~ 5175 3975
$Comp
L Device:R_Small R6
U 1 1 5D59E7C3
P 4650 3375
F 0 "R6" V 4550 3375 50  0000 C CNN
F 1 "22" V 4650 3375 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4650 3375 50  0001 C CNN
F 3 "~" H 4650 3375 50  0001 C CNN
	1    4650 3375
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R7
U 1 1 5D59EDC5
P 4650 3475
F 0 "R7" V 4750 3475 50  0000 C CNN
F 1 "22" V 4650 3475 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4650 3475 50  0001 C CNN
F 3 "~" H 4650 3475 50  0001 C CNN
	1    4650 3475
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5D5A0DCF
P 3550 3975
F 0 "#PWR0103" H 3550 3725 50  0001 C CNN
F 1 "GND" H 3555 3802 50  0000 C CNN
F 2 "" H 3550 3975 50  0001 C CNN
F 3 "" H 3550 3975 50  0001 C CNN
	1    3550 3975
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5D5A3A36
P 1250 5250
F 0 "#PWR0104" H 1250 5000 50  0001 C CNN
F 1 "GND" H 1255 5077 50  0000 C CNN
F 2 "" H 1250 5250 50  0001 C CNN
F 3 "" H 1250 5250 50  0001 C CNN
	1    1250 5250
	1    0    0    -1  
$EndComp
Text GLabel 3150 3775 0    50   Input ~ 0
BOOT0
Text GLabel 1050 5050 0    50   Input ~ 0
BOOT0
Wire Wire Line
	1050 5050 1250 5050
Text GLabel 3150 2275 0    50   Input ~ 0
NRST
Text GLabel 1900 4950 1    50   Input ~ 0
NRST
$Comp
L power:GND #PWR0105
U 1 1 5D5AC005
P 1900 5150
F 0 "#PWR0105" H 1900 4900 50  0001 C CNN
F 1 "GND" H 1905 4977 50  0000 C CNN
F 2 "" H 1900 5150 50  0001 C CNN
F 3 "" H 1900 5150 50  0001 C CNN
	1    1900 5150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5D5C7909
P 1250 3000
F 0 "#PWR0107" H 1250 2750 50  0001 C CNN
F 1 "GND" H 1255 2827 50  0000 C CNN
F 2 "" H 1250 3000 50  0001 C CNN
F 3 "" H 1250 3000 50  0001 C CNN
	1    1250 3000
	1    0    0    -1  
$EndComp
Text GLabel 3150 3475 0    50   Input ~ 0
PB5
Text GLabel 4150 2475 2    50   Input ~ 0
PA2
Text GLabel 4150 2575 2    50   Input ~ 0
PA3
Text GLabel 4150 3175 2    50   Input ~ 0
PA9
Text GLabel 4150 3275 2    50   Input ~ 0
PA10
Text GLabel 4150 3575 2    50   Input ~ 0
PA13
Text GLabel 4150 3675 2    50   Input ~ 0
PA14
$Comp
L power:VCC #PWR0112
U 1 1 5D6C7F18
P 3550 2075
F 0 "#PWR0112" H 3550 1925 50  0001 C CNN
F 1 "VCC" H 3567 2248 50  0000 C CNN
F 2 "" H 3550 2075 50  0001 C CNN
F 3 "" H 3550 2075 50  0001 C CNN
	1    3550 2075
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0113
U 1 1 5D6C84C2
P 3900 1000
F 0 "#PWR0113" H 3900 850 50  0001 C CNN
F 1 "VCC" V 3918 1127 50  0000 L CNN
F 2 "" H 3900 1000 50  0001 C CNN
F 3 "" H 3900 1000 50  0001 C CNN
	1    3900 1000
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED_Small D2
U 1 1 5D82BC0C
P 1750 2900
F 0 "D2" V 1796 2832 50  0000 R CNN
F 1 "LED" V 1705 2832 50  0000 R CNN
F 2 "Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 1750 2900 50  0001 C CNN
F 3 "~" V 1750 2900 50  0001 C CNN
	1    1750 2900
	0    -1   -1   0   
$EndComp
Text GLabel 3150 3275 0    50   Input ~ 0
PB3
Wire Wire Line
	3900 1000 4000 1000
Wire Wire Line
	4950 1050 4950 1000
Wire Wire Line
	4950 1000 5300 1000
Connection ~ 4000 1000
$Comp
L Device:R_Small R4
U 1 1 5D793A53
P 2325 2750
F 0 "R4" V 2425 2750 50  0000 C CNN
F 1 "2K2" V 2325 2750 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2325 2750 50  0001 C CNN
F 3 "~" H 2325 2750 50  0001 C CNN
	1    2325 2750
	-1   0    0    1   
$EndComp
$Comp
L Device:R_Small R5
U 1 1 5D793A59
P 2475 2750
F 0 "R5" V 2375 2750 50  0000 C CNN
F 1 "2K2" V 2475 2750 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2475 2750 50  0001 C CNN
F 3 "~" H 2475 2750 50  0001 C CNN
	1    2475 2750
	-1   0    0    1   
$EndComp
Text GLabel 2475 2850 3    50   Input ~ 0
PA10
Text GLabel 2325 2850 3    50   Input ~ 0
PA9
$Comp
L Device:C_Small C9
U 1 1 5D68E30A
P 1900 5050
F 0 "C9" H 1700 5050 50  0000 L CNN
F 1 "0.1uF" H 1650 4950 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1900 5050 50  0001 C CNN
F 3 "~" H 1900 5050 50  0001 C CNN
	1    1900 5050
	-1   0    0    -1  
$EndComp
Text Notes 2325 2300 0    50   ~ 10
I2C
Text Notes 1150 2300 0    50   ~ 10
Power
Text Notes 2100 1450 0    50   ~ 10
VDDIO2
Connection ~ 2400 1300
Connection ~ 2100 1300
Wire Wire Line
	2100 1300 2400 1300
Wire Wire Line
	2400 1250 2400 1300
Wire Wire Line
	2400 1000 2700 1000
Connection ~ 2400 1000
Wire Wire Line
	2400 1000 2400 1050
Connection ~ 2100 1000
Wire Wire Line
	2100 1000 2400 1000
$Comp
L Device:C_Small C6
U 1 1 5D82028A
P 2400 1150
F 0 "C6" H 2200 1150 50  0000 L CNN
F 1 "4.7uF" H 2150 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2400 1150 50  0001 C CNN
F 3 "~" H 2400 1150 50  0001 C CNN
	1    2400 1150
	1    0    0    -1  
$EndComp
Text Notes 2700 1450 0    50   ~ 10
VDDA
Text Notes 1550 1450 0    50   ~ 10
VDD
Connection ~ 3000 1300
Wire Wire Line
	3000 1300 3000 1350
Wire Wire Line
	3000 1300 3000 1250
Wire Wire Line
	2700 1300 3000 1300
Connection ~ 2700 1000
Wire Wire Line
	3000 1000 3000 1050
Wire Wire Line
	2700 1000 3000 1000
Wire Wire Line
	1800 1300 2100 1300
Connection ~ 1800 1300
Wire Wire Line
	1800 1250 1800 1300
Wire Wire Line
	1500 1300 1800 1300
Wire Wire Line
	1800 1000 2100 1000
Connection ~ 1800 1000
Wire Wire Line
	1800 1050 1800 1000
Wire Wire Line
	1500 1000 1500 1050
Connection ~ 1500 1000
Wire Wire Line
	1500 1000 1800 1000
$Comp
L Device:C_Small C8
U 1 1 5D6549AB
P 3000 1150
F 0 "C8" H 2800 1150 50  0000 L CNN
F 1 "1uF" H 2800 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 3000 1150 50  0001 C CNN
F 3 "~" H 3000 1150 50  0001 C CNN
	1    3000 1150
	-1   0    0    -1  
$EndComp
$Comp
L Device:C_Small C4
U 1 1 5D6508EA
P 1800 1150
F 0 "C4" H 1600 1150 50  0000 L CNN
F 1 "4.7uF" H 1550 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1800 1150 50  0001 C CNN
F 3 "~" H 1800 1150 50  0001 C CNN
	1    1800 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 900  1500 1000
$Comp
L power:VCC #PWR0109
U 1 1 5D6ACF37
P 1500 900
F 0 "#PWR0109" H 1500 750 50  0001 C CNN
F 1 "VCC" H 1517 1073 50  0000 C CNN
F 2 "" H 1500 900 50  0001 C CNN
F 3 "" H 1500 900 50  0001 C CNN
	1    1500 900 
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 1250 1500 1300
Connection ~ 2700 1300
Wire Wire Line
	2100 1300 2100 1250
Wire Wire Line
	2700 1300 2400 1300
Wire Wire Line
	2700 1250 2700 1300
Wire Wire Line
	2700 1000 2700 1050
Wire Wire Line
	2100 1000 2100 1050
$Comp
L power:GND #PWR0106
U 1 1 5D5B3F90
P 3000 1350
F 0 "#PWR0106" H 3000 1100 50  0001 C CNN
F 1 "GND" H 3005 1177 50  0000 C CNN
F 2 "" H 3000 1350 50  0001 C CNN
F 3 "" H 3000 1350 50  0001 C CNN
	1    3000 1350
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C7
U 1 1 5D5B29FC
P 2700 1150
F 0 "C7" H 2500 1150 50  0000 L CNN
F 1 "0.01uF" H 2400 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2700 1150 50  0001 C CNN
F 3 "~" H 2700 1150 50  0001 C CNN
	1    2700 1150
	-1   0    0    -1  
$EndComp
$Comp
L Device:C_Small C5
U 1 1 5D5B2561
P 2100 1150
F 0 "C5" H 1900 1150 50  0000 L CNN
F 1 "0.1uF" H 1850 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2100 1150 50  0001 C CNN
F 3 "~" H 2100 1150 50  0001 C CNN
	1    2100 1150
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C3
U 1 1 5D5ACDD5
P 1500 1150
F 0 "C3" H 1300 1150 50  0000 L CNN
F 1 "0.1uF" H 1250 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1500 1150 50  0001 C CNN
F 3 "~" H 1500 1150 50  0001 C CNN
	1    1500 1150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5D882AB2
P 4450 1300
F 0 "#PWR0114" H 4450 1050 50  0001 C CNN
F 1 "GND" H 4455 1127 50  0000 C CNN
F 2 "" H 4450 1300 50  0001 C CNN
F 3 "" H 4450 1300 50  0001 C CNN
	1    4450 1300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5D59331E
P 4000 1250
F 0 "#PWR0101" H 4000 1000 50  0001 C CNN
F 1 "GND" H 4005 1077 50  0000 C CNN
F 2 "" H 4000 1250 50  0001 C CNN
F 3 "" H 4000 1250 50  0001 C CNN
	1    4000 1250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 1050 4000 1000
$Comp
L Device:C_Small C2
U 1 1 5D59212D
P 4000 1150
F 0 "C2" H 3800 1150 50  0000 L CNN
F 1 "10uF" H 3750 1050 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 4000 1150 50  0001 C CNN
F 3 "~" H 4000 1150 50  0001 C CNN
	1    4000 1150
	1    0    0    -1  
$EndComp
Text GLabel 4150 5450 2    50   Input ~ 0
PA3
Text GLabel 4150 5650 2    50   Input ~ 0
NRST
Text GLabel 3250 6150 0    50   Input ~ 0
PB5
Text GLabel 3250 5750 0    50   Input ~ 0
PA13
$Comp
L power:GND #PWR0108
U 1 1 5D657E62
P 4150 5950
F 0 "#PWR0108" H 4150 5700 50  0001 C CNN
F 1 "GND" H 4155 5777 50  0000 C CNN
F 2 "" H 4150 5950 50  0001 C CNN
F 3 "" H 4150 5950 50  0001 C CNN
	1    4150 5950
	0    -1   -1   0   
$EndComp
Text GLabel 3250 6050 0    50   Input ~ 0
PB4
Text GLabel 3250 5950 0    50   Input ~ 0
PB3
Text GLabel 3250 5850 0    50   Input ~ 0
PA14
$Comp
L power:VCC #PWR0115
U 1 1 5DA6520E
P 4150 6050
F 0 "#PWR0115" H 4150 5900 50  0001 C CNN
F 1 "VCC" H 4167 6223 50  0000 C CNN
F 2 "" H 4150 6050 50  0001 C CNN
F 3 "" H 4150 6050 50  0001 C CNN
	1    4150 6050
	0    1    1    0   
$EndComp
Connection ~ 4950 1000
Text Notes 1675 2300 0    50   ~ 10
LED
Wire Wire Line
	4150 3375 4550 3375
Wire Wire Line
	4150 3475 4550 3475
Text GLabel 5300 1250 3    50   Input ~ 0
5V
Text GLabel 2325 2525 1    50   Input ~ 0
5V
NoConn ~ 6075 4275
$Comp
L Device:R_Small R8
U 1 1 5EDECF8F
P 5075 2975
F 0 "R8" V 4975 2975 50  0000 C CNN
F 1 "5k1" V 5075 2975 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5075 2975 50  0001 C CNN
F 3 "~" H 5075 2975 50  0001 C CNN
	1    5075 2975
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R9
U 1 1 5EDECF95
P 5075 3075
F 0 "R9" V 5175 3075 50  0000 C CNN
F 1 "5k1" V 5075 3075 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5075 3075 50  0001 C CNN
F 3 "~" H 5075 3075 50  0001 C CNN
	1    5075 3075
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 5EE005A1
P 4975 2975
F 0 "#PWR0110" H 4975 2725 50  0001 C CNN
F 1 "GND" H 4980 2802 50  0000 C CNN
F 2 "" H 4975 2975 50  0001 C CNN
F 3 "" H 4975 2975 50  0001 C CNN
	1    4975 2975
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 5EE040F8
P 4975 3075
F 0 "#PWR0117" H 4975 2825 50  0001 C CNN
F 1 "GND" H 4980 2902 50  0000 C CNN
F 2 "" H 4975 3075 50  0001 C CNN
F 3 "" H 4975 3075 50  0001 C CNN
	1    4975 3075
	0    1    1    0   
$EndComp
Wire Wire Line
	5300 1250 5300 1000
Connection ~ 5300 1000
Wire Wire Line
	5300 1000 5475 1000
NoConn ~ 4150 3075
NoConn ~ 3150 3675
$Comp
L Switch:SW_Push SW1
U 1 1 5EDA24EE
P 1250 4850
F 0 "SW1" V 1204 4998 50  0000 L CNN
F 1 "SW_Push" V 1295 4998 50  0000 L CNN
F 2 "key-parts:SW_SMD_5x3" H 1250 5050 50  0001 C CNN
F 3 "~" H 1250 5050 50  0001 C CNN
	1    1250 4850
	0    1    1    0   
$EndComp
$Comp
L MCU_ST_STM32F0:STM32F042K6Tx U1
U 1 1 5D58187C
P 3650 2975
F 0 "U1" H 4000 1975 50  0000 C CNN
F 1 "STM32F042K6Tx" H 4000 1875 50  0000 C CNN
F 2 "Package_QFP:LQFP-32_7x7mm_P0.8mm" H 3250 2075 50  0001 R CNN
F 3 "http://www.st.com/st-web-ui/static/active/en/resource/technical/document/datasheet/DM00105814.pdf" H 3650 2975 50  0001 C CNN
	1    3650 2975
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 1000 4150 1000
$Comp
L key-parts:AP7333 U2
U 1 1 5EE69AFC
P 4450 1050
F 0 "U2" H 4450 1365 50  0000 C CNN
F 1 "AP7333" H 4450 1274 50  0000 C CNN
F 2 "key-parts:AP7333" H 4450 1050 50  0001 C CNN
F 3 "" H 4450 1050 50  0001 C CNN
	1    4450 1050
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4750 1000 4950 1000
$Comp
L power:GND #PWR0119
U 1 1 5EE77B4D
P 4950 1250
F 0 "#PWR0119" H 4950 1000 50  0001 C CNN
F 1 "GND" H 4955 1077 50  0000 C CNN
F 2 "" H 4950 1250 50  0001 C CNN
F 3 "" H 4950 1250 50  0001 C CNN
	1    4950 1250
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x07 J2
U 1 1 5EF3336E
P 3950 5750
F 0 "J2" H 3868 6267 50  0000 C CNN
F 1 "Conn_01x07" H 3868 6176 50  0000 C CNN
F 2 "key-parts:PinHeader_1x07_P2.54mm_Vertical" H 3950 5750 50  0001 C CNN
F 3 "~" H 3950 5750 50  0001 C CNN
	1    3950 5750
	-1   0    0    -1  
$EndComp
Text GLabel 1250 2600 1    50   Input ~ 0
VBUS
Wire Wire Line
	3550 2075 3650 2075
Connection ~ 3550 2075
Connection ~ 3650 2075
Wire Wire Line
	3650 2075 3750 2075
Wire Wire Line
	3650 3975 3550 3975
Connection ~ 3550 3975
Wire Wire Line
	4750 3375 5175 3375
Wire Wire Line
	4750 3475 5175 3475
Wire Wire Line
	5175 3275 5175 3375
Wire Wire Line
	5175 3475 5175 3575
Wire Wire Line
	2325 2650 2325 2600
Wire Wire Line
	2325 2600 2475 2600
Wire Wire Line
	2475 2600 2475 2650
Connection ~ 2325 2600
Wire Wire Line
	2325 2600 2325 2525
Wire Wire Line
	5675 1000 5825 1000
Wire Wire Line
	6025 1000 6125 1000
$Comp
L Device:Polyfuse_Small F1
U 1 1 5D958CA7
P 5925 1000
F 0 "F1" V 5720 1000 50  0000 C CNN
F 1 "Polyfuse" V 5811 1000 50  0000 C CNN
F 2 "Fuse:Fuse_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5975 800 50  0001 L CNN
F 3 "~" H 5925 1000 50  0001 C CNN
	1    5925 1000
	0    1    1    0   
$EndComp
Text GLabel 6125 1000 2    50   Input ~ 0
VBUS
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5EE08314
P 6125 1425
F 0 "#FLG0101" H 6125 1500 50  0001 C CNN
F 1 "PWR_FLAG" V 6125 1552 50  0000 L CNN
F 2 "" H 6125 1425 50  0001 C CNN
F 3 "~" H 6125 1425 50  0001 C CNN
	1    6125 1425
	0    -1   -1   0   
$EndComp
Text GLabel 6125 1425 2    50   Input ~ 0
VBUS
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5EE0C882
P 6125 1725
F 0 "#FLG0102" H 6125 1800 50  0001 C CNN
F 1 "PWR_FLAG" V 6125 1852 50  0000 L CNN
F 2 "" H 6125 1725 50  0001 C CNN
F 3 "~" H 6125 1725 50  0001 C CNN
	1    6125 1725
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 5EE0F27F
P 6125 1725
F 0 "#PWR0118" H 6125 1475 50  0001 C CNN
F 1 "GND" H 6130 1552 50  0000 C CNN
F 2 "" H 6125 1725 50  0001 C CNN
F 3 "" H 6125 1725 50  0001 C CNN
	1    6125 1725
	0    -1   -1   0   
$EndComp
Text GLabel 1750 2600 1    50   Input ~ 0
PA15
$Comp
L power:GND #PWR0116
U 1 1 5EE6D829
P 1750 3000
F 0 "#PWR0116" H 1750 2750 50  0001 C CNN
F 1 "GND" H 1755 2827 50  0000 C CNN
F 2 "" H 1750 3000 50  0001 C CNN
F 3 "" H 1750 3000 50  0001 C CNN
	1    1750 3000
	1    0    0    -1  
$EndComp
$Comp
L key-parts:USB_C_Receptacle_USB2.0 J4
U 1 1 5EE9945F
P 5775 3375
F 0 "J4" H 5345 3314 50  0000 R CNN
F 1 "USB_C_Receptacle_USB2.0" H 5345 3223 50  0000 R CNN
F 2 "key-parts:USB_C_Receptacle_Neltron_5077CR" H 5925 3375 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 5925 3375 50  0001 C CNN
	1    5775 3375
	-1   0    0    -1  
$EndComp
Connection ~ 5175 3475
Connection ~ 5175 3375
$Comp
L Connector_Generic:Conn_01x08 J1
U 1 1 5EE8A871
P 3450 5750
F 0 "J1" H 3400 6275 50  0000 L CNN
F 1 "Conn_01x08" H 3225 6175 50  0000 L CNN
F 2 "key-parts:PinHeader_1x08_P2.54mm_Vertical" H 3450 5750 50  0001 C CNN
F 3 "~" H 3450 5750 50  0001 C CNN
	1    3450 5750
	1    0    0    -1  
$EndComp
Text GLabel 4150 5750 2    50   Input ~ 0
PF1
Text GLabel 4150 5850 2    50   Input ~ 0
PF0
Text GLabel 3150 2775 0    50   Input ~ 0
PF0
Text GLabel 3150 2875 0    50   Input ~ 0
PF1
$Comp
L power:VCC #PWR0111
U 1 1 5EE99F50
P 1250 4650
F 0 "#PWR0111" H 1250 4500 50  0001 C CNN
F 1 "VCC" H 1267 4823 50  0000 C CNN
F 2 "" H 1250 4650 50  0001 C CNN
F 3 "" H 1250 4650 50  0001 C CNN
	1    1250 4650
	1    0    0    -1  
$EndComp
Text GLabel 3250 5450 0    50   Input ~ 0
5V
Text GLabel 4150 5550 2    50   Input ~ 0
PA2
Text GLabel 4150 2775 2    50   Input ~ 0
PA5
Text GLabel 3250 5650 0    50   Input ~ 0
PA10
Text GLabel 3250 5550 0    50   Input ~ 0
PA9
Text GLabel 3625 4825 1    50   Input ~ 0
PA6
Text GLabel 3725 4825 1    50   Input ~ 0
PA5
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 5EEC9E21
P 3625 5025
F 0 "J3" V 3497 5205 50  0000 L CNN
F 1 "Conn_01x03" V 3588 5205 50  0000 L CNN
F 2 "key-parts:PinHeader_1x03_P2.54mm_Vertical" H 3625 5025 50  0001 C CNN
F 3 "~" H 3625 5025 50  0001 C CNN
	1    3625 5025
	0    1    1    0   
$EndComp
Text GLabel 3525 4825 1    50   Input ~ 0
PA7
Text GLabel 4150 2875 2    50   Input ~ 0
PA6
Text GLabel 4150 2975 2    50   Input ~ 0
PA7
Text GLabel 4150 3775 2    50   Input ~ 0
PA15
$Comp
L power:GND #PWR0120
U 1 1 5EEB7993
P 1550 3625
F 0 "#PWR0120" H 1550 3375 50  0001 C CNN
F 1 "GND" H 1555 3452 50  0000 C CNN
F 2 "" H 1550 3625 50  0001 C CNN
F 3 "" H 1550 3625 50  0001 C CNN
	1    1550 3625
	0    1    1    0   
$EndComp
Text GLabel 1950 3525 2    50   Input ~ 0
5V
NoConn ~ 1550 3525
Text GLabel 3150 3175 0    50   Input ~ 0
PB1
$Comp
L key-parts:SK6812-2020 D3
U 1 1 5EEBCF65
P 1750 3575
F 0 "D3" H 1750 3749 51  0000 C CNN
F 1 "SK6812-2020" H 1750 3575 16  0001 C CNN
F 2 "key-parts:WS2812B_2020_Vertical" H 1750 3575 60  0001 C CNN
F 3 "" H 1750 3575 60  0001 C CNN
	1    1750 3575
	1    0    0    -1  
$EndComp
Text GLabel 1950 3625 2    50   Input ~ 0
PB1
Text GLabel 3150 3375 0    50   Input ~ 0
PB4
NoConn ~ 4150 2275
NoConn ~ 4150 2375
NoConn ~ 4150 2675
NoConn ~ 3150 3075
$Comp
L power:PWR_FLAG #FLG0103
U 1 1 5EECD08C
P 6125 1575
F 0 "#FLG0103" H 6125 1650 50  0001 C CNN
F 1 "PWR_FLAG" V 6125 1702 50  0000 L CNN
F 2 "" H 6125 1575 50  0001 C CNN
F 3 "~" H 6125 1575 50  0001 C CNN
	1    6125 1575
	0    -1   -1   0   
$EndComp
Text GLabel 6125 1575 2    50   Input ~ 0
5V
Connection ~ 1250 5050
NoConn ~ 3150 3575
$Comp
L Device:R_Small R2
U 1 1 5D82BC12
P 1750 2700
F 0 "R2" V 1850 2700 50  0000 C CNN
F 1 "1K" V 1750 2700 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1750 2700 50  0001 C CNN
F 3 "~" H 1750 2700 50  0001 C CNN
	1    1750 2700
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_Small R1
U 1 1 5D5C71CB
P 1250 2700
F 0 "R1" V 1350 2700 50  0000 C CNN
F 1 "1K" V 1250 2700 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1250 2700 50  0001 C CNN
F 3 "~" H 1250 2700 50  0001 C CNN
	1    1250 2700
	-1   0    0    -1  
$EndComp
$Comp
L Device:LED_Small D1
U 1 1 5D5C4E5A
P 1250 2900
F 0 "D1" V 1296 2832 50  0000 R CNN
F 1 "PW_LED" V 1205 2832 50  0000 R CNN
F 2 "Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 1250 2900 50  0001 C CNN
F 3 "~" V 1250 2900 50  0001 C CNN
	1    1250 2900
	0    1    -1   0   
$EndComp
$Comp
L Device:R_Small R3
U 1 1 5D5A2DBD
P 1250 5150
F 0 "R3" V 1350 5150 50  0000 C CNN
F 1 "10K" V 1250 5150 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1250 5150 50  0001 C CNN
F 3 "~" H 1250 5150 50  0001 C CNN
	1    1250 5150
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
