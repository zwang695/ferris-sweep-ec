/* Copyright 2023 ssbb
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

#pragma once

#define MATRIX_ROWS 8
#define MATRIX_COLS 5
#define EC_DEBUG true

#define DIODE_DIRECTION COL2ROW

// Calibration:
// Baseline read - what you see in console when keyboard IDLE.
//
// EC_LOW_THRESHOLD[][] = BASELINE_READ + 100
// EC_HIGH_THRESHOLD[][] = HIGH_THRESHOLD + 300
//
// You could change 300 to something else to adjust actuation depth.

// clang-format off
#define EC_HIGH_THRESHOLD_LEFT {  \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }  \
}

#define EC_HIGH_THRESHOLD_RIGHT { \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }, \
    { 700, 700, 700, 700, 700 }  \
}

#define EC_LOW_THRESHOLD_LEFT { \
    { 650, 650, 650, 650, 650 }, \
    { 650, 650, 650, 650, 650 }, \
    { 650, 650, 650, 650, 650 }, \
    { 650, 650, 650, 650, 650 }  \
}

#define EC_LOW_THRESHOLD_RIGHT { \
    { 650, 650, 650, 650, 650 },  \
    { 650, 650, 650, 650, 650 },  \
    { 650, 650, 650, 650, 650 },  \
    { 650, 650, 650, 650, 650 }   \
}
// clang-format on
