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
L Device:LED_Small D1
U 1 1 5D82BC0C
P 1425 2000
F 0 "D1" V 1471 1932 50  0000 R CNN
F 1 "LED" V 1380 1932 50  0000 R CNN
F 2 "Diode_SMD:D_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 1425 2000 50  0001 C CNN
F 3 "~" V 1425 2000 50  0001 C CNN
	1    1425 2000
	0    -1   -1   0   
$EndComp
Text GLabel 2975 2025 0    50   Input ~ 0
SDA
Text GLabel 2975 2125 0    50   Input ~ 0
SCL
Text Notes 1350 1650 0    50   ~ 10
LED
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
Text GLabel 1425 1900 1    50   Input ~ 0
LED
$Comp
L power:GND #PWR0116
U 1 1 5EE6D829
P 1425 2300
F 0 "#PWR0116" H 1425 2050 50  0001 C CNN
F 1 "GND" H 1430 2127 50  0000 C CNN
F 2 "" H 1425 2300 50  0001 C CNN
F 3 "" H 1425 2300 50  0001 C CNN
	1    1425 2300
	1    0    0    -1  
$EndComp
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
$Comp
L Device:R_Small R1
U 1 1 5D82BC12
P 1425 2200
F 0 "R1" V 1525 2200 50  0000 C CNN
F 1 "330" V 1425 2200 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 1425 2200 50  0001 C CNN
F 3 "~" H 1425 2200 50  0001 C CNN
	1    1425 2200
	-1   0    0    -1  
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
L Device:D_Small D13
U 1 1 5F32238F
P 3450 5350
F 0 "D13" V 3450 5282 50  0000 R CNN
F 1 "D_Small" V 3405 5282 50  0001 R CNN
F 2 "key-parts:D_SMD" V 3450 5350 50  0001 C CNN
F 3 "~" V 3450 5350 50  0001 C CNN
	1    3450 5350
	0    -1   -1   0   
$EndComp
$Comp
L Device:D_Small D14
U 1 1 5F32239B
P 3450 5675
F 0 "D14" V 3450 5607 50  0000 R CNN
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
Text GLabel 7325 3025 2    50   Input ~ 0
SDA
Text GLabel 7325 3125 2    50   Input ~ 0
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
$Comp
L Device:R_Small R6
U 1 1 5F2474F5
P 7375 2625
F 0 "R6" V 7275 2625 50  0000 C CNN
F 1 "5k1" V 7375 2625 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7375 2625 50  0001 C CNN
F 3 "~" H 7375 2625 50  0001 C CNN
	1    7375 2625
	0    -1   1    0   
$EndComp
$Comp
L Device:R_Small R7
U 1 1 5F2474FB
P 7375 2725
F 0 "R7" V 7475 2725 50  0000 C CNN
F 1 "5k1" V 7375 2725 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7375 2725 50  0001 C CNN
F 3 "~" H 7375 2725 50  0001 C CNN
	1    7375 2725
	0    -1   1    0   
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
Text GLabel 7150 4775 2    50   Input ~ 0
5V
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
L power:GND #PWR0111
U 1 1 5F3285E2
P 4850 5600
F 0 "#PWR0111" H 4850 5350 50  0001 C CNN
F 1 "GND" H 4855 5427 50  0000 C CNN
F 2 "" H 4850 5600 50  0001 C CNN
F 3 "" H 4850 5600 50  0001 C CNN
	1    4850 5600
	0    1    1    0   
$EndComp
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
Text GLabel 5375 5500 2    50   Input ~ 0
5V
$Comp
L Interface_Expansion:MCP23017_SS U1
U 1 1 5F366B9E
P 3675 2825
F 0 "U1" H 3675 4106 50  0000 C CNN
F 1 "MCP23017_SS" H 3675 4015 50  0000 C CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 3875 1825 50  0001 L CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf" H 3875 1725 50  0001 L CNN
	1    3675 2825
	1    0    0    -1  
$EndComp
Text GLabel 3675 1725 1    50   Input ~ 0
5V
$Comp
L power:GND #PWR0103
U 1 1 5F36CE58
P 3675 3925
F 0 "#PWR0103" H 3675 3675 50  0001 C CNN
F 1 "GND" H 3680 3752 50  0000 C CNN
F 2 "" H 3675 3925 50  0001 C CNN
F 3 "" H 3675 3925 50  0001 C CNN
	1    3675 3925
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5F36D6BE
P 2975 3425
F 0 "#PWR0105" H 2975 3175 50  0001 C CNN
F 1 "GND" H 2980 3252 50  0000 C CNN
F 2 "" H 2975 3425 50  0001 C CNN
F 3 "" H 2975 3425 50  0001 C CNN
	1    2975 3425
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5F36DC87
P 2975 3525
F 0 "#PWR0106" H 2975 3275 50  0001 C CNN
F 1 "GND" H 2980 3352 50  0000 C CNN
F 2 "" H 2975 3525 50  0001 C CNN
F 3 "" H 2975 3525 50  0001 C CNN
	1    2975 3525
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5F36DF53
P 2975 3625
F 0 "#PWR0107" H 2975 3375 50  0001 C CNN
F 1 "GND" H 2980 3452 50  0000 C CNN
F 2 "" H 2975 3625 50  0001 C CNN
F 3 "" H 2975 3625 50  0001 C CNN
	1    2975 3625
	0    1    1    0   
$EndComp
Text GLabel 2975 2925 0    50   Input ~ 0
5V
Text GLabel 4375 2425 2    50   Input ~ 0
ROW1
Text GLabel 4375 2325 2    50   Input ~ 0
ROW2
Text GLabel 4375 2225 2    50   Input ~ 0
ROW3
Text GLabel 4375 2125 2    50   Input ~ 0
ROW4
Text GLabel 4375 2925 2    50   Input ~ 0
COL1
Text GLabel 4375 3025 2    50   Input ~ 0
BOOT0
NoConn ~ 4375 3125
NoConn ~ 4375 3225
NoConn ~ 4375 3325
NoConn ~ 4375 3425
NoConn ~ 4375 3525
NoConn ~ 4375 3625
Text GLabel 4375 2025 2    50   Input ~ 0
LED
Text GLabel 4850 5500 0    50   Input ~ 0
LDI
NoConn ~ 7100 4950
$Comp
L power:GND #PWR0104
U 1 1 5F3A1287
P 5250 5025
F 0 "#PWR0104" H 5250 4775 50  0001 C CNN
F 1 "GND" H 5255 4852 50  0000 C CNN
F 2 "" H 5250 5025 50  0001 C CNN
F 3 "" H 5250 5025 50  0001 C CNN
	1    5250 5025
	0    1    1    0   
$EndComp
Text GLabel 1550 5900 0    50   Input ~ 0
5V
Text GLabel 2550 5175 1    50   Input ~ 0
5V
NoConn ~ 2975 2625
NoConn ~ 2975 2725
Text GLabel 975  2100 1    50   Input ~ 0
5V
$Comp
L power:GND #PWR0101
U 1 1 5F385690
P 975 2300
F 0 "#PWR0101" H 975 2050 50  0001 C CNN
F 1 "GND" H 980 2127 50  0000 C CNN
F 2 "" H 975 2300 50  0001 C CNN
F 3 "" H 975 2300 50  0001 C CNN
	1    975  2300
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C1
U 1 1 5F3862F2
P 975 2200
F 0 "C1" H 725 2200 50  0000 L CNN
F 1 "0.1u" H 825 2275 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 975 2200 50  0001 C CNN
F 3 "~" H 975 2200 50  0001 C CNN
	1    975  2200
	1    0    0    -1  
$EndComp
Text GLabel 7375 3625 2    50   Input ~ 0
LDI
NoConn ~ 4375 2525
NoConn ~ 4375 2625
NoConn ~ 4375 2725
$Comp
L key-parts:SK6812-MINI-E LB1
U 1 1 5F4E9B6E
P 5050 5550
F 0 "LB1" H 5050 5724 51  0000 C CNN
F 1 "SK6812-MINI-E" H 5050 5550 16  0001 C CNN
F 2 "key-parts:SK6812-MINI-E" H 5050 5550 60  0001 C CNN
F 3 "" H 5050 5550 60  0001 C CNN
	1    5050 5550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7375 3625 7275 3625
Wire Wire Line
	7275 3525 7275 3625
Connection ~ 7275 3625
$Comp
L key-parts:SK6812-MINI-E L14
U 1 1 5F4EDDD8
P 5550 4900
F 0 "L14" H 5550 5074 51  0000 C CNN
F 1 "SK6812-MINI-E" H 5550 4900 16  0001 C CNN
F 2 "key-parts:SK6812-MINI-E" H 5550 4900 60  0001 C CNN
F 3 "" H 5550 4900 60  0001 C CNN
	1    5550 4900
	-1   0    0    -1  
$EndComp
$Comp
L key-parts:SK6812-MINI-E L13
U 1 1 5F4F357D
P 6000 4900
F 0 "L13" H 6000 5074 51  0000 C CNN
F 1 "SK6812-MINI-E" H 6000 4900 16  0001 C CNN
F 2 "key-parts:SK6812-MINI-E" H 6000 4900 60  0001 C CNN
F 3 "" H 6000 4900 60  0001 C CNN
	1    6000 4900
	-1   0    0    -1  
$EndComp
$Comp
L key-parts:SK6812-MINI-E L12
U 1 1 5F4F6046
P 6450 4900
F 0 "L12" H 6450 5074 51  0000 C CNN
F 1 "SK6812-MINI-E" H 6450 4900 16  0001 C CNN
F 2 "key-parts:SK6812-MINI-E" H 6450 4900 60  0001 C CNN
F 3 "" H 6450 4900 60  0001 C CNN
	1    6450 4900
	-1   0    0    -1  
$EndComp
$Comp
L key-parts:SK6812-MINI-E L11
U 1 1 5F4F8941
P 6900 4900
F 0 "L11" H 6900 5074 51  0000 C CNN
F 1 "SK6812-MINI-E" H 6900 4900 16  0001 C CNN
F 2 "key-parts:SK6812-MINI-E" H 6900 4900 60  0001 C CNN
F 3 "" H 6900 4900 60  0001 C CNN
	1    6900 4900
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5250 5500 5375 5500
Wire Wire Line
	7150 4775 7100 4775
Wire Wire Line
	5750 4775 5750 4850
Wire Wire Line
	6200 4850 6200 4775
Connection ~ 6200 4775
Wire Wire Line
	6200 4775 5750 4775
Wire Wire Line
	6650 4850 6650 4775
Connection ~ 6650 4775
Wire Wire Line
	6650 4775 6200 4775
Wire Wire Line
	7100 4850 7100 4775
Connection ~ 7100 4775
Wire Wire Line
	7100 4775 6650 4775
Wire Wire Line
	5250 5600 5300 5600
Wire Wire Line
	5300 5600 5300 4850
Wire Wire Line
	5300 4850 5350 4850
Wire Wire Line
	5250 5025 5350 5025
Wire Wire Line
	6700 5025 6700 4950
Wire Wire Line
	6250 4950 6250 5025
Connection ~ 6250 5025
Wire Wire Line
	6250 5025 6700 5025
Wire Wire Line
	5800 4950 5800 5025
Connection ~ 5800 5025
Wire Wire Line
	5800 5025 6250 5025
Wire Wire Line
	5350 4950 5350 5025
Connection ~ 5350 5025
Wire Wire Line
	5350 5025 5800 5025
Wire Wire Line
	5750 4950 5775 4950
Wire Wire Line
	5775 4950 5775 4850
Wire Wire Line
	5775 4850 5800 4850
Wire Wire Line
	6200 4950 6225 4950
Wire Wire Line
	6225 4950 6225 4850
Wire Wire Line
	6225 4850 6250 4850
Wire Wire Line
	6650 4950 6675 4950
Wire Wire Line
	6675 4950 6675 4850
Wire Wire Line
	6675 4850 6700 4850
Text GLabel 6150 5675 0    50   Input ~ 0
5V
$Comp
L power:GND #PWR0102
U 1 1 5F508D2B
P 6150 5875
F 0 "#PWR0102" H 6150 5625 50  0001 C CNN
F 1 "GND" H 6155 5702 50  0000 C CNN
F 2 "" H 6150 5875 50  0001 C CNN
F 3 "" H 6150 5875 50  0001 C CNN
	1    6150 5875
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small CLB1
U 1 1 5F508D31
P 6225 5775
F 0 "CLB1" H 6250 5850 50  0000 L CNN
F 1 "0.1u" H 6250 5700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 6225 5775 50  0001 C CNN
F 3 "~" H 6225 5775 50  0001 C CNN
	1    6225 5775
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small CL14
U 1 1 5F50B0C2
P 6450 5775
F 0 "CL14" H 6475 5850 50  0000 L CNN
F 1 "0.1u" H 6475 5700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 6450 5775 50  0001 C CNN
F 3 "~" H 6450 5775 50  0001 C CNN
	1    6450 5775
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small CL13
U 1 1 5F50B5A4
P 6675 5775
F 0 "CL13" H 6700 5850 50  0000 L CNN
F 1 "0.1u" H 6700 5700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 6675 5775 50  0001 C CNN
F 3 "~" H 6675 5775 50  0001 C CNN
	1    6675 5775
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small CL12
U 1 1 5F50BAE3
P 6900 5775
F 0 "CL12" H 6925 5850 50  0000 L CNN
F 1 "0.1u" H 6925 5700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 6900 5775 50  0001 C CNN
F 3 "~" H 6900 5775 50  0001 C CNN
	1    6900 5775
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small CL11
U 1 1 5F50BF26
P 7125 5775
F 0 "CL11" H 7150 5850 50  0000 L CNN
F 1 "0.1u" H 7150 5700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7125 5775 50  0001 C CNN
F 3 "~" H 7125 5775 50  0001 C CNN
	1    7125 5775
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 5675 6225 5675
Connection ~ 6225 5675
Wire Wire Line
	6225 5675 6450 5675
Connection ~ 6450 5675
Wire Wire Line
	6450 5675 6675 5675
Connection ~ 6675 5675
Wire Wire Line
	6675 5675 6900 5675
Connection ~ 6900 5675
Wire Wire Line
	6900 5675 7125 5675
Wire Wire Line
	6150 5875 6225 5875
Connection ~ 6225 5875
Wire Wire Line
	6225 5875 6450 5875
Connection ~ 6450 5875
Wire Wire Line
	6450 5875 6675 5875
Connection ~ 6675 5875
Wire Wire Line
	6675 5875 6900 5875
Connection ~ 6900 5875
Wire Wire Line
	6900 5875 7125 5875
Text GLabel 1500 3925 0    50   Input ~ 0
5V
Text GLabel 1500 3825 0    50   Input ~ 0
SDA
Text GLabel 1500 3725 0    50   Input ~ 0
SCL
$Comp
L power:GND #PWR0109
U 1 1 5F531520
P 1500 3525
F 0 "#PWR0109" H 1500 3275 50  0001 C CNN
F 1 "GND" H 1505 3352 50  0000 C CNN
F 2 "" H 1500 3525 50  0001 C CNN
F 3 "" H 1500 3525 50  0001 C CNN
	1    1500 3525
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x05 J3
U 1 1 5F534A64
P 1700 3725
F 0 "J3" H 1780 3767 50  0000 L CNN
F 1 "Conn_01x05" H 1780 3676 50  0000 L CNN
F 2 "key-parts:PinHeader_1x05_P2.54mm_Vertical" H 1700 3725 50  0001 C CNN
F 3 "~" H 1700 3725 50  0001 C CNN
	1    1700 3725
	1    0    0    -1  
$EndComp
Text GLabel 1500 3625 0    50   Input ~ 0
LDI
$EndSCHEMATC
