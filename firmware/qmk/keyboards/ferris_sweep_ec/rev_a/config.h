/* Copyright 2023 ssbb
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 */

#pragma once

#define MATRIX_ROW_PINS \
    { D4, C6, D7, B2 }
#define MATRIX_ROW_PINS_RIGHT \
    { F4, F5, F7, B3 }

#define MATRIX_COL_CHANNELS \
    { 4, 6, 2, 1, 3 }
#define MATRIX_COL_CHANNELS_RIGHT \
    { 2, 4, 6, 7, 5 }

#define MUX_SEL_PINS \
    { F4, F5, F7 }
#define MUX_SEL_PINS_RIGHT \
    { B5, B4, E6 }

#define APLEX_EN_PIN B6
#define APLEX_EN_PIN_RIGHT D4

#define DISCHARGE_PIN B3
#define DISCHARGE_PIN_RIGHT D7

#define ANALOG_PORT F6

#define SPLIT_HAND_PIN D2
#define SERIAL_USART_TX_PIN D3

#define POWER_PIN B1
#define POWER_PIN_RIGHT C6
