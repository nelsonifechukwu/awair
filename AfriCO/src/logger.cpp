#include <logger.h>


File myFile;
String file_name;
Vector<char> image;

void logger_begin(){
    //EEPROM.write(fileN0_address,0); // for setup ONLY

    int fileN0 = EEPROM.read(fileN0_address);
    Serial.println("initializing SDcard"); 
    if (!SD.begin(SD_CS_pin)){
        Serial.println("initialization failed!");
        return;
    }
    Serial.println("initialization done."); 
  
    if(SD.exists("DATA_"+String(fileN0)+".csv")){
      fileN0++;
      // update file Number
      EEPROM.write(fileN0_address,fileN0);
    }
    file_name = "DATA_"+String(fileN0)+".csv";

    myFile = SD.open(file_name, FILE_WRITE);

    // if the file opened okay, write to it:
    if (myFile) {
        myFile.print("Date,");
        myFile.print("Time,");
        myFile.print("Longitude,");
        myFile.print("Latitude,");
        myFile.print("Temperature,");
        myFile.print("Humidity,");
        myFile.print("Rain fall,");
        myFile.print("CO2,");
        myFile.print("Air quality,");
        myFile.print("Wind Speed,");
        myFile.println("Wind Direction");
        // close the file:
        myFile.close();
        Serial.println("Data saved to "+file_name);
    } else {
        // if the file didn't open, print an error:
        Serial.println("error opening "+file_name);
    }
    
}

void log_data(Sensors_data data){
  myFile = SD.open(file_name, FILE_WRITE);

  // if the file opened okay, write to it:
  if (myFile) {
    myFile.print(data.date);
    myFile.print(",");
    myFile.print(data.time);
    myFile.print(",");
    myFile.print(data.longitude);
    myFile.print(",");
    myFile.print(data.latitude);
    myFile.print(",");
    myFile.print(data.temperature);
    myFile.print(",");
    myFile.print(data.humidity);
    myFile.print(",");
    myFile.print(data.rainfall);
    myFile.print(",");
    myFile.print(data.CO2);
    myFile.print(",");
    myFile.print(data.air_quality);
    myFile.print(",");
    myFile.print(data.wind_speed);
    myFile.print(",");
    myFile.println(data.wind_direction);

    // close the file:
    myFile.close();
    Serial.println("Data saved to "+file_name);
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening "+file_name);
  }
}