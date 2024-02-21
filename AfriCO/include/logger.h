#ifndef LOGGER_H
#define LOGGER_H

#include <Arduino.h>
#include <EEPROM.h>
#include <SPI.h>
#include <SD.h>
#include <vector.h>

#define fileN0_address 0
#define SD_CS_pin 4
typedef struct Senseors{
    String time;
    String date;
    String longitude;
    String latitude;
    String temperature;
    String humidity;
    String rainfall;
    String CO2;
    String air_quality;
    String wind_speed;
    String wind_direction;
}Sensors_data;

void logger_begin();
void log_data(Sensors_data data);


#endif