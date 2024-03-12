# AWAIR

In Africa, the absence of an extensive meteorological device network has posed a significant challenge for environmental research, hindering accurate ground-truth data acquisition. This limitation affects various sectors, including government initiatives, urban planning, pollution control, etc.

Recognizing this gap, Awair emerges as a groundbreaking solution, offering an advanced, cloud-connected, real-time platform for environmental data. Awair aims to empower top universities, research labs, government agencies, and African industrial applications by providing accurate meteorological insights, facilitating informed decision-making, and sustainable solutions for environmental challenges.

Awair's data awareness, research, and analytics capabilities present a transformative approach to addressing the pressing issues related to the environment in the African context.

# Table of Content
- [Description](#Description)
- - [Endpoints](#endpoints)
  - [Input temperature data](#user-signup)
  - [Input airqo data](#user-login)
  - [Input wind data](#create-a-blog-post)
  - [Input location data](#like-a-blog-post)
  - [Follow a user](#follow-a-user)
 
# Testing 
- Register at [Awair](https://awair.onrender.com/)
- Create a Device using this ID: ``` ```


## Sending Data
The following endpoints should be used by your hardware to interact with the platform: 

### Input temperature data

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
