#include <sensors.h>


OneWire oneWire(ONE_WIRE_BUS);
DS18B20 sensor(&oneWire);

#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void sensors_init()
{
    dht.begin();
    sensor.begin();
    sensor.setResolution(12);
}

void get_humidity(String* humid)
{
    float h = dht.readHumidity();
    
    if(isnan(h)){
        return;
    }
    *humid = String(h);
}

void get_temperature(String* temp){
    // sensor.requestTemperatures();
    // while (!sensor.isConversionComplete());
    // float t = sensor.getTempC();

    float t = dht.readTemperature();
    if(isnan(t)){
        return;
    }
    *temp = String(t);
}

void get_CO2(String* co2){
    *co2 = "---";
}

void get_air_quality(String* aq){
    *aq = "---";
}

void get_wind_speed(String* spd){
    *spd = "---";
}

void get_wind_dir(String* dir){
    *dir = "---";
}