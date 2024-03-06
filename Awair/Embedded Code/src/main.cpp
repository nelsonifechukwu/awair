#include <main.hpp>
#include <vector.h>

/* Pin definition start*/
#define status_led 13

/*end of pin definition*/

#define log_time_interval 10000 // 10s


long ct,task1,task2,task3,task4;
char c;
GPS_Data gps_data;
Sensors_data All_sensors;
Vector<int> list;

HardwareSerial* GPS_Serial = &Serial2;

void setup() {
  pinMode(status_led,OUTPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  GPS_Serial->begin(9600);
  sensors_init();
  delay(4000);
  logger_begin();
}

int rx_complete;
void loop() {
  ct = millis();
  if((ct-task1)>1000){
    digitalWrite(status_led,!digitalRead(status_led));
    get_temperature(&All_sensors.temperature);
    get_humidity(&All_sensors.humidity);
    Serial.print("Temp: "+ All_sensors.temperature);
    Serial.println("\tR.H: "+All_sensors.humidity);
    task1 = ct;
  }

  if((ct-task2)> log_time_interval){
    All_sensors.longitude = gps_data._long;
    All_sensors.latitude = gps_data._lat;
    All_sensors.time = gps_data.time;
    All_sensors.date = gps_data.date;
    All_sensors.wind_speed = gps_data.speed;
    All_sensors.wind_direction = (String)gps_data.direction_NS;
    get_air_quality(&All_sensors.air_quality);
    get_CO2(&All_sensors.CO2);
    get_wind_speed(&All_sensors.wind_speed);
    get_wind_dir(&All_sensors.wind_direction);
    log_data(All_sensors);
    task2 = ct;
  }
  

  if(rx_complete==GPRMC){
    // Serial.print("Lat: "+String(gps_data._lat));
    // Serial.print(" Lon: "+String(gps_data._long));
    // Serial.print(" Time: "+String(gps_data.time));
    // Serial.print(" Date: "+String(gps_data.date));
    // Serial.println(" Speed: "+String(gps_data.speed));

    rx_complete = false;
  }

  while(GPS_Serial->available()){
    c = (char)GPS_Serial->read();
    //Serial.print(c);
    rx_complete = Process_GPS_Data(c,&gps_data,GPRMC);
  }
}

