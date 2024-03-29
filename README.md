# AWAIR

In Africa, the absence of an extensive meteorological device network has posed a significant challenge for environmental research, hindering accurate ground-truth data acquisition. This limitation affects various sectors, including government initiatives, urban planning, pollution control, etc.

Recognizing this gap, Awair emerges as a groundbreaking solution, offering an advanced, cloud-connected, real-time platform for environmental data. Awair aims to empower top universities, research labs, government agencies, and African industrial applications by providing accurate meteorological insights, facilitating informed decision-making, and sustainable solutions for environmental challenges.

Awair's data awareness, research, and analytics capabilities present a transformative approach to addressing the pressing issues related to the environment in the African context.

![Screenshot 2024-03-12 at 12 52 43](https://github.com/nelsonifechukwu/awair/assets/44223263/7242a7a4-d5e5-47b3-b3b1-7bc1c783e495)


# Table of Content
- [Testing](#Testing)
  - [Input temperature data](#input-tph-data)
  - [Input airqo data](#input-airqo-data)
  - [Input wind data](#input-wind-data)
  - [Input location data](#input-location-data)
- [Hardware Design](#hardware-design)
  - [Electrical CAD](#electrical-cad)
  - [Mechanical CAD](#mechanical-cad)
  - [Embedded Software](#embedded-software)
 
# Testing 
- Register at [Awair](https://awair.onrender.com/)
- Create a Device using any of these ID:
<br><img width="397" alt="Screenshot 2024-03-12 at 12 20 52" src="https://github.com/nelsonifechukwu/awair/assets/44223263/736d6651-d452-4ca9-a910-d51316c027ef"> 
- Start [sending](#sending-data)  
- Go to the analytics section to view forecast and visualize your data

<h3> Sending Data </h3>
Your hardware should use the following endpoints to interact with the platform: 

### Input tph data

- **URL:** `/temp`
- **Method:** `POST`
- **Description:** Allows users to insert data.
- **Request Body:**
```
body request: {
    "uuid":"8254f02a-1c06-46f0-8382-66ad5be70cb6",
    "temperature": "20",
    "humidity":"50",
    "pressure": "80"
}
```

- **Response:**

```json
created
```

### Input airqo data

- **URL:** `/airqo`
- **Method:** `POST`
- **Description:** Allows users to insert data.
- **Request Body:**
```
body request: {
    "uuid":"8254f02a-1c06-46f0-8382-66ad5be70cb6",
    "pm2.5":"11.3",
    "pm10":"25",
    "co_index": 10
}
```

- **Response:**

```json
created
```

### Input wind data

- **URL:** `/wind`
- **Method:** `POST`
- **Description:** Allows users to insert data.
- **Request Body:**
```
body request: {
    "uuid": "8254f02a-1c06-46f0-8382-66ad5be70cb6",
    "wind-speed":"23",
    "wind-direction":"40"
}
```

- **Response:**

```json
created
```
### Input location data

- **URL:** `/location`
- **Method:** `POST`
- **Description:** Allows users to insert data.
- **Request Body:**
```
body request: {
    "uuid":"8254f02a-1c06-46f0-8382-66ad5be70cb6",
    "location": "0,40",
    "battery":"50",
    "signal": "80"
}
```

- **Response:**

```json
created
```

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
