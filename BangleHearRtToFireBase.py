### Code to Start Bangle using Java Script and Post Heart Rate and Temperature in Google Firebase.
### Author : Puskar K C
### Python inerfacing code, referenced from Bangle.js official documentatin.

import asyncio
import array
import time
import pyrebase
from datetime import datetime
from bleak import BleakClient

###  Firebase Config. the configuration details is always different for each Database and user and need to obtained from Firebase
firebaseConfig = {
  "apiKey": "AIzaSyA8W4ioDBpqh5XC76AwQp_mfnFdbliAY8Y",
  "authDomain": "uc-proj.firebaseapp.com",
  "databaseURL": "https://uc-proj-default-rtdb.firebaseio.com",
  "projectId": "uc-proj",
  "storageBucket": "uc-proj.appspot.com",
  "messagingSenderId": "109029043316",
  "appId": "1:109029043316:web:59f15c494d81c24208b521",
  "measurementId": "G-QEF2F2PHW5"
}

### initialize database of Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
###------------------------- Above code is required for firebase connection

### Bangle.Js Watch Address. The below 3 lines is mandatory code which is just the address of the WATCH
address = "E43D4199-EB93-DBE8-4565-0E8F0C3202A1"
UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" ### Bangle Code to Transmit/Push Data
UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" ### Banlge code or Unique ID to Receive Data.

###  b"var currentDate = new Date(); print('D'+currentDate.toISOString());"
#### Using Javascript to pass command to Bangle.Js
command = (b"\x03\x10 reset()"
          b"\n\x10 clearInterval()"
          b"\n\x10 setInterval(function()"
          b"{ var temp = E.getTemperature();"
          b"temp = 'T'+temp + '-';  "
          b"Bangle.setHRMPower(1) "
          b"Bangle.on('HRM',function(hrm) { "
          b"var d = ['H',hrm.bpm,hrm.confidence]; "
          b"print(temp + d.join());})}, 1000);"
          b"\n\x10print( 'Fresh Data Start')\n")

### Variables declaration
SkinTemperature = None
HeartData = None
sample = 1
person = "Puskar"
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t) ### Not in used this for Now -- for time
sampleCount = 0 ### Variable for counter
hrtData = None
def uart_data_received(sender, data):
  global sampleCount
  received_data = data.decode().strip() ## decode the bytes to string
 # print("Temperature", received_data)
 
  if(received_data.startswith("T")): ## Receiving the line that starts with "T"
      received_data = received_data.split("-")
      # print(f'reccev o {received_data[0]}')
      WorkHeartData = received_data[1].split("\n")
      # print(f'reccev 1 {WorkHeartData[0]}')
    
      global hrtData
      hrtData = WorkHeartData[0]
      tempy= received_data[0]
     
      try:
        tempy = float(tempy[1:]) ### Getting the Temperature value
      except ValueError:
         tempy = 0.0
      tempy = (tempy *9/5)+32 ### Converting to Farenheit
      print(f' Temperature in Farenheit:  {tempy}')
      SkinTemperature = {"DataIdentifier": "T", "Temperature ": tempy}
      database.child(person).child("Temperature Reading").child(sampleCount).set(SkinTemperature)
      sampleCount = sampleCount +1
  elif(hrtData.startswith("H")): ## Receiving the line that starts with "H"
      heart= hrtData.split(",")
      if len(heart) >= 3:
        try:
          BPM = float(heart[1])
          confidence = float(heart[2])
        except ValueError:
          BPM = 0.0
          confidence = 0.0
        print(f'BPM : {BPM} Confidence : {confidence}')
        HeartData = {"DataIdentifier": "H", "BPM": BPM, "Confidence": confidence}
        database.child(person).child("Heart Reading").child(sampleCount).set(HeartData)
        sampleCount = sampleCount +1
      else:
         print(f'Data not received {heart}')    
print("Connecting...")

### from here -Samelessly used sample code from Expurino documentation
async def run(address, loop):  
    async with BleakClient(address, loop=loop) as client:
        print("Connected")
        
        await client.start_notify(UUID_NORDIC_RX, uart_data_received)
        
        print("Writing command")
        c = command
        while len(c) > 0: ### sending 2 bytes as Watch only transmit 20 bytes
            await client.write_gatt_char(UUID_NORDIC_TX, bytearray(c[0:2]), True)
            c = c[2:]
        print("Waiting for data")
        
        await asyncio.sleep(50.0,loop)  # wait for a response
        await client.stop_notify(UUID_NORDIC_RX) 
        print("Done!")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))

### Write Code to exit the program. (Like Pressing any Key or Button to exit the Program)
