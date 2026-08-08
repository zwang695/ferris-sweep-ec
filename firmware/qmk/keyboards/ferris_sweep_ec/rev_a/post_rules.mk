ifeq ($(strip $(MCU_FAMILY)),RP)
    SERIAL_DRIVER = vendor
else ifeq ($(strip $(MCU_FAMILY)),STM32)
    SERIAL_DRIVER = usart
endif
