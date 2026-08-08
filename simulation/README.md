# Simulation

Synthetic ADC classifier coverage lives in `tests/test_adc_classifier.py`.
It exercises the exact 650/700 hysteresis contract without pretending to know
the physical sensor capacitance.

An absolute analog model is deliberately deferred until a selected dome,
spring, housing, PCB finish, and assembled stack provide measured released and
bottomed-out readings. Without those boundary conditions, a capacitance sweep
would create precise-looking but unvalidated signal margins.
