/*
  NTC Temperature Monitor | Arduino Uno R3 + LM358
  ------------------------------------------------
  Reconstructed and cleaned up from the original course project report.
  Hardware wiring: ../../hardware/WIRING.vi.md

  IMPORTANT:
  - NTC divider supply: 3.3 V.
  - LM358 power supply: 5 V (pin 8), GND (pin 4).
  - Arduino Uno ADC A0 reference: AVcc, nominally 5 V with DEFAULT.
  - Measure real VREF and AVcc and update constants for higher accuracy.
  - Output is educational and not safety/medical-grade.
*/

#include <math.h>

const uint8_t ANALOG_PIN = A0;

// Nominal electrical values; replace with measured values during calibration.
const float DIVIDER_SUPPLY_V = 3.3f;
const float ADC_REFERENCE_V = 5.0f;
const float VREF_V = 1.65f;  // LM358B buffered reference (pin 7)
const float R1_OHM = 10000.0f;  // Fixed lower NTC divider resistor
const float R2_OHM = 10000.0f;  // Reference to LM358A inverting input
const float R3_OHM = 5600.0f;   // LM358A feedback resistor

// Original report's Steinhart-Hart coefficients (check/calibrate your NTC).
const float SH_A = 0.001129148f;
const float SH_B = 0.000234125f;
const float SH_C = 0.0000000876741f;

const float EMA_ALPHA = 0.1f;
const unsigned long SAMPLE_PERIOD_MS = 500UL;

float emaAdc = 0.0f;
bool emaInitialized = false;
unsigned long lastSampleMs = 0UL;

bool adcToTemperature(float adc, float &vOut, float &vIn,
                      float &rNtc, float &temperatureC) {
  // Saturated ADC readings are suspicious; avoid misleading temperature.
  if (adc <= 0.0f || adc >= 1023.0f) {
    return false;
  }

  vOut = (adc / 1023.0f) * ADC_REFERENCE_V;
  const float feedbackRatio = R3_OHM / R2_OHM;
  vIn = (vOut + VREF_V * feedbackRatio) / (1.0f + feedbackRatio);

  // NTC (top leg) / R1 (bottom leg): Rntc = R1 * (Vdivider / Vin - 1).
  if (vIn <= 0.0f || vIn >= DIVIDER_SUPPLY_V) {
    return false;
  }
  rNtc = R1_OHM * (DIVIDER_SUPPLY_V / vIn - 1.0f);
  if (rNtc <= 0.0f) {
    return false;
  }

  const float logR = log(rNtc);
  const float inverseKelvin = SH_A + SH_B * logR + SH_C * logR * logR * logR;
  if (inverseKelvin <= 0.0f) {
    return false;
  }

  const float kelvin = 1.0f / inverseKelvin;
  if (kelvin <= 0.0f || kelvin >= 1000.0f) {
    return false;
  }
  temperatureC = kelvin - 273.15f;
  return true;
}

void setup() {
  analogReference(DEFAULT);  // AVcc, about 5 V on typical Uno R3
  Serial.begin(9600);
  Serial.println(F("NTC + LM358 monitor | 9600 baud"));
  Serial.println(F("Check power, 3.3V divider, VREF=1.65V and ADC reference."));
}

void loop() {
  const unsigned long now = millis();
  if (now - lastSampleMs < SAMPLE_PERIOD_MS) {
    return;
  }
  lastSampleMs = now;

  const int rawAdc = analogRead(ANALOG_PIN);
  if (!emaInitialized) {
    emaAdc = (float)rawAdc;  // No start-up ramp from zero
    emaInitialized = true;
  } else {
    emaAdc = EMA_ALPHA * (float)rawAdc + (1.0f - EMA_ALPHA) * emaAdc;
  }

  float vOut = 0.0f;
  float vIn = 0.0f;
  float rNtc = 0.0f;
  float tempC = 0.0f;

  Serial.print(F("ADC: "));
  Serial.print(rawAdc);
  if (!adcToTemperature(emaAdc, vOut, vIn, rNtc, tempC)) {
    Serial.println(F(" | ERROR: invalid ADC / voltage / resistance"));
    return;
  }

  Serial.print(F(" | Vout: "));
  Serial.print(vOut, 3);
  Serial.print(F(" V | Vin: "));
  Serial.print(vIn, 3);
  Serial.print(F(" V | R_NTC: "));
  Serial.print(rNtc, 0);
  Serial.print(F(" ohm | Temperature: "));
  Serial.print(tempC, 1);
  Serial.print(F(" C"));

  // Calibration points in report: 8, 29, 52 C. Extrapolation is less reliable.
  if (tempC < 8.0f || tempC > 52.0f) {
    Serial.print(F(" [outside reported calibration points]"));
  }
  Serial.println();
}
