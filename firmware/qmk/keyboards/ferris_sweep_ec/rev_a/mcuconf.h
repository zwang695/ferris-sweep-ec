/* Copyright 2023 ssbb
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 */

#pragma once

#include_next <mcuconf.h>

#if defined(MCU_RP)
#    undef RP_ADC_USE_ADC1
#    define RP_ADC_USE_ADC1 TRUE
#endif

#if defined(MCU_STM32)
#    undef STM32_ADC_USE_ADC1
#    define STM32_ADC_USE_ADC1 TRUE
#endif
