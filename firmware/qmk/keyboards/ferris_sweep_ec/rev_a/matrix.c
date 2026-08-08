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

#include "matrix.h"
#include "keyboard.h"
#include "split_common/split_util.h"
#include "../ec_switch_matrix.h"

uint16_t low_threshold[MATRIX_ROWS][MATRIX_COLS]  = EC_LOW_THRESHOLD_LEFT;
uint16_t high_threshold[MATRIX_ROWS][MATRIX_COLS] = EC_HIGH_THRESHOLD_LEFT;

void matrix_init_custom(void) {
    ecsm_config_t ecsm_config;

    if (!is_keyboard_left()) {
        const uint16_t low_right[MATRIX_ROWS][MATRIX_COLS]  = EC_LOW_THRESHOLD_RIGHT;
        const uint16_t high_right[MATRIX_ROWS][MATRIX_COLS] = EC_HIGH_THRESHOLD_RIGHT;

        for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
            for (uint8_t col = 0; col < MATRIX_COLS; col++) {
                low_threshold[row][col]  = low_right[row][col];
                high_threshold[row][col] = high_right[row][col];
            }
        }
    }

    for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
        for (uint8_t col = 0; col < MATRIX_COLS; col++) {
            ecsm_config.low_threshold_matrix[row][col]  = low_threshold[row][col];
            ecsm_config.high_threshold_matrix[row][col] = high_threshold[row][col];
        }
    }

    ecsm_init(&ecsm_config);
}

bool matrix_scan_custom(matrix_row_t current_matrix[]) {
    bool updated = ecsm_matrix_scan(current_matrix);

// RAW matrix values on console
#ifdef CONSOLE_ENABLE
    static int cnt = 0;
    if (cnt++ == 300) {
        cnt = 0;
        ecsm_print_matrix();
    }
#endif

    return updated;
}
