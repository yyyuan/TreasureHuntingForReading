# Treasure Box Side 

This repository contains codes for treasure box side app (mostly Arduino).

## Some work-in-progress notes

### Arduino side

- Currently the arduino program would communicate with the localhost through port 9600 by print the current total points registered at the physical treasure box;
- All the tokens and reward card are hard coded and use block 4 to record their value
- The barrier current for a reward card is 50 points
- Need to install Adafruit PN532 library for the RFID shield

### Requirment for Flask app 

- Need to install psyerial library to get the serial communication going
- Currently the update was through the endpoint /update - which return a JSON file with the current points sent from Arduino
- **TODO** Figure how to use the JSON file to update the points in the database
- Also a simulator for serial communication was added to this repo - run it to simulate the Arduino sending number of total points