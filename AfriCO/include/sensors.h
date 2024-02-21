#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

#include "DHT.h"
#define DHTPIN 3 
// #define DHTTYPE DHT22
// DHT dht(DHTPIN, DHTTYPE);

#include <OneWire.h>
#include <DS18B20.h>
#define ONE_WIRE_BUS 2
// OneWire oneWire(ONE_WIRE_BUS);
// DS18B20 sensor(&oneWire);

#define CO2_pin A0


void sensors_init();

void get_humidity(String* humid);

void get_temperature(String* temp);

void get_CO2(String* co2);

void get_air_quality(String* aq);

void get_wind_speed(String* spd);

void get_wind_dir(String* dir);


#endif