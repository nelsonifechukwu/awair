# Awair

In Africa, the absence of an extensive meteorological device network has posed a significant challenge for environmental research, hindering accurate ground-truth data acquisition. This limitation affects various sectors, including government initiatives, urban planning, pollution control, and more.

Recognizing this gap, Awair emerges as a groundbreaking solution, offering an advanced, cloud-connected, real-time platform for environmental data. Awair aims to empower top universities, research labs, government agencies, and industrial applications in Africa by providing accurate meteorological insights, facilitating informed decision-making, and sustainable solutions for environmental challenges.

Awair's data awareness, research, and analytics capabilities present a transformative approach to addressing the pressing issues related to the environment in the African context.

# Hardware Design
  <h3>Electrical CAD</h3> 
  
  <ins>Requirements: </ins>
  - Basic Electronics
  - Hardware Materials:
    - ESP32
    - SD Card Module & SD Card
    - Female Header Pins
    - DHT 22 Temperature Sensor
    - BMP180 Pressure Sensor
    - Sim 800l EVB GPS/GSM/GPRS sensor
    - CO2 sensor
    - Pm 2.5 & Pm 10 Air Quality Sensors
    - Batteries (4x 3.7v Lipo Batteries)
    - Wires
    - 2x 12-5v Buck Converters
     
 <ins>How To: </ins>
 - Download the CAD files from ```.Awair/CAD/Electrical Design```
 - Use a printing service like JLC PCB to print the PCB. Or, use a CNC to cut the designed sketch
 - Mount the parts as shown in the PCB Diagram.

<h3>Mechanical CAD</h3>

 <ins>Requirements: </ins>
 - Basic CAD skills
 - Basic 3d Printing
   
 <ins>How To: </ins>
 - Download the CAD files from ```.Awair/CAD/Mechanical Design```
 - Use a 3d printer to print the files (battery pack, cover, enclosure).

<h3>Embedded Software</h3>

<ins>How To:</ins>
 - After setting up the hardware, open the file ```Awair/Embedded Code``` using platformIDE
 - Edit your variable ```uuid``` with the uuid obtained after registration
 - Edit the variable ```API-key``` with the API-Key obtained from the web application after registration
 - Upload the code to the ESP32
