/* Copyright 2023 ssbb
 * Copyright 2023 Cipulot
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "quantum.h"
#include "ec_switch_matrix.h"
#include "analog.h"
#include "atomic_util.h"
#include "print.h"
#include "wait.h"
#include "split_common/split_util.h"
#include "ec_analog.h"

#if defined(MCU_RP)
#    include "hardware/gpio.h"
#endif

#define SUPPORTS_OPEN_DRAIN defined(PAL_MODE_OUTPUT_OPENDRAIN)

#define WAIT_DISCHARGE()
#define WAIT_CHARGE()

/* Pin and port array */
pin_t row_pins[]     = MATRIX_ROW_PINS;
pin_t col_channels[] = MATRIX_COL_CHANNELS;
pin_t mux_sel_pins[] = MUX_SEL_PINS;
pin_t aplex_en_pin   = APLEX_EN_PIN;
pin_t discharge_pin  = DISCHARGE_PIN;
pin_t power_pin      = POWER_PIN;

const int rows_len = sizeof row_pins / sizeof row_pins[0];
const int cols_len = sizeof col_channels / sizeof col_channels[0];

static ecsm_config_t config;
static int16_t       ecsm_sw_value[MATRIX_ROWS][MATRIX_COLS];

static adc_mux adcMux;

static inline void init_mux_sel(void) {
    for (int idx = 0; idx < 3; idx++) {
        gpio_set_pin_output(mux_sel_pins[idx]);
    }
}

static inline void select_mux(uint8_t col) {
    uint8_t ch = col_channels[col];
    gpio_write_pin(mux_sel_pins[0], ch & 1);
    gpio_write_pin(mux_sel_pins[1], ch & 2);
    gpio_write_pin(mux_sel_pins[2], ch & 4);
}

static inline void init_row(void) {
    for (int idx = 0; idx < rows_len; idx++) {
        gpio_set_pin_output(row_pins[idx]);
        gpio_write_pin_low(row_pins[idx]);
    }
}

/* Initialize the peripherals pins */
int ecsm_init(ecsm_config_t const* const ecsm_config) {
    // Initialize config
    config = *ecsm_config;

    if (!is_keyboard_left()) {
#ifdef MATRIX_ROW_PINS_RIGHT
        const pin_t row_pins_right[] = MATRIX_ROW_PINS_RIGHT;
        for (uint8_t i = 0; i < (sizeof(row_pins_right) / sizeof(row_pins_right[0])); i++) {
            row_pins[i] = row_pins_right[i];
        }
#endif

#ifdef MATRIX_COL_CHANNELS_RIGHT
        const pin_t col_channels_right[] = MATRIX_COL_CHANNELS_RIGHT;
        for (uint8_t i = 0; i < (sizeof(col_channels_right) / sizeof(col_channels_right[0])); i++) {
            col_channels[i] = col_channels_right[i];
        }
#endif

#ifdef MUX_SEL_PINS_RIGHT
        const pin_t mux_sel_pins_right[] = MUX_SEL_PINS_RIGHT;
        for (uint8_t i = 0; i < (sizeof(mux_sel_pins_right) / sizeof(mux_sel_pins_right[0])); i++) {
            mux_sel_pins[i] = mux_sel_pins_right[i];
        }
#endif

#ifdef APLEX_EN_PIN_RIGHT
        aplex_en_pin = APLEX_EN_PIN_RIGHT;
#endif

#ifdef DISCHARGE_PIN_RIGHT
        discharge_pin = DISCHARGE_PIN_RIGHT;
#endif

#ifdef POWER_PIN_RIGHT
        power_pin = POWER_PIN_RIGHT;
#endif
    }

#ifdef MCU_STM32
    palSetLineMode(ANALOG_PORT, PAL_MODE_INPUT_ANALOG);
#endif

    gpio_set_pin_output(power_pin);
    gpio_write_pin_high(power_pin);

    adcMux = pinToMux(ANALOG_PORT);
    ec_adc_read(adcMux, true);

    gpio_write_pin_low(discharge_pin);

#if SUPPORTS_OPEN_DRAIN
    gpio_set_pin_output_open_drain(discharge_pin);
#else
    gpio_set_pin_output(discharge_pin);
#endif

    // Init drive lines
    init_row();

    // Init mux select select pin
    init_mux_sel();

    /* Enable AMUX */
    gpio_set_pin_output(aplex_en_pin);
    gpio_write_pin_low(aplex_en_pin);

    return 0;
}

int ecsm_update(ecsm_config_t const* const ecsm_config) {
    // Save config
    config = *ecsm_config;
    return 0;
}

// Read the capacitive sensor value
int16_t ecsm_readkey_raw(uint8_t row, uint8_t col) {
    int16_t sw_value = 0;

    gpio_write_pin_high(aplex_en_pin);
    select_mux(col);
    gpio_write_pin_low(aplex_en_pin);

    // Set strobe pins to low state
    gpio_write_pin_low(row_pins[row]);

    ATOMIC_BLOCK_FORCEON {
#if SUPPORTS_OPEN_DRAIN
        gpio_write_pin_high(discharge_pin);
#else
        gpio_set_pin_input(discharge_pin);
#endif
        gpio_write_pin_high(row_pins[row]);

        WAIT_CHARGE();

        sw_value = ec_adc_read(adcMux, false);
    }

    // Discharge peak hold capacitor
#if SUPPORTS_OPEN_DRAIN
    gpio_write_pin_low(discharge_pin);
#else
    gpio_write_pin_low(discharge_pin);
    gpio_set_pin_output(discharge_pin);
#endif
    wait_us(10);

    return sw_value;
}

// Update press/release state of key
bool ecsm_update_key(matrix_row_t* current_row, uint8_t row, uint8_t col, uint16_t sw_value) {
    bool current_state = (*current_row >> col) & 1;

    // Press to release
    if (current_state && sw_value < config.low_threshold_matrix[row][col]) {
        *current_row &= ~(1 << col);
        return true;
    }

    // Release to press
    if ((!current_state) && sw_value > config.high_threshold_matrix[row][col]) {
        *current_row |= (1 << col);
        return true;
    }

    return false;
}

// Scan key values and update matrix state
bool ecsm_matrix_scan(matrix_row_t current_matrix[]) {
    bool updated = false;

    for (int col = 0; col < cols_len; col++) {
        for (int row = 0; row < rows_len; row++) {
            ecsm_sw_value[row][col] = ecsm_readkey_raw(row, col);
            updated |= ecsm_update_key(&current_matrix[row], row, col, ecsm_sw_value[row][col]);
        }
    }

    return updated;
}

// Debug print key values
void ecsm_print_matrix(void) {
    for (int row = 0; row < rows_len; row++) {
        for (int col = 0; col < cols_len; col++) {
            uprintf("%4d", ecsm_sw_value[row][col]);
            if (col < (cols_len - 1)) {
                print(",");
            }
        }
        print("\n");
    }
    print("\n");
}
