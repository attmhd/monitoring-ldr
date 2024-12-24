
# Send data from NodeMCU esp 8266 to MySQL database (LDR sensor)

This is the project for Module 9 in the Embedded Systems course.
## Tech Stack

[![My Skills](https://skillicons.dev/icons?i=fastapi,mysql,arduino)](https://skillicons.dev)

- FastAPI 
- Streamlit
- Arduino IDE

## Installation


Clone project

```bash
https://github.com/attmhd/monitoring-ldr.git
```
Go to project directory

```bash
  cd monitoring-ldr
```

Open Arduino IDE & import ***arduino.c*** file

Ensure the circuit is properly set up and the code is successfully uploaded to the Arduino.

Install depedencies

```bash
pip install -r requirements.txt
```

Import ***db.sql*** to mysql database

Running project

```bash
fastapi dev main.py
streamlit run dashboard.py
```    

API Documentation

```bash
https://127.0.0.1:8000/docs
```    
    
## Authors

- [@attmhd](https://github.com/attnmhd/) 
- @fahreza