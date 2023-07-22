## Author: Puskar K C
## Description: This below code performs Create, Read, Update, Delete Data in Goolge Firebase Realtime Database

### I have created the virtual environment in Python 3.11.4 for this folder , Coded in Visual Studio Code
### python3 -m venv  .venv ## venv is the virtual environmet,  and after that..
### Installed Pyrebase to work with google firebase.
### pip install pyrebase4

import pyrebase
from datetime import datetime
import time

### the configuration details is always different for each Database and user and need to obtained from Firebase
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

### initialize database
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()


### lets create data
Person = "Person1"
date = datetime.today()
date = date.strftime("%m/%d/%Y")
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t) ### Getting Current Date and time details

BasicData = {"Age": 34, "Name": "Puskar", "IsFirstTime": True}
OxygenData = {"SubjectId":1, "OxygenLevel": 98,"RecordedTime": current_time, "Date:": date }

#database.push(data) ### this push the data to the firebase
## Creating the nodes/childs and pushing the data to Realtime Database
database.child("SubjectDetails").child(Person).child("BasicDetails").set(BasicData) 
database.child("SubjectDetails").child(Person).child("OxygenDetails").set(OxygenData)

##### Creating the nodes/childs and pushing the data to Realtime Database
database.child("SubjectDetails").child("Person2").child("BasicDetails").set(BasicData) 
database.child("SubjectDetails").child("Person2").child("OxygenDetails").set(OxygenData)

#### Reading data from Database
Person1 = database.child("SubjectDetails").child("Person1").get()
print(Person1.val())

#### Updating Data, # Lets Updata Person2 name to "Alan"
database.child("SubjectDetails").child("Person2").child("BasicDetails").update({"Name":"Alan", "Age":44})
### read the updated Data
Person2 = database.child("SubjectDetails").child("Person2").get()
print(Person2.val())

### Delete Whole node or Delete only the value like the person name, is same thing like calling as child 

print("--------------Performing Delete operation ------------")
ChkDelete = {"SubjectId":1, "OxygenLevel": 98,"RecordedTime": current_time, "Date:": date}
database.child("SubjectCheckDelete").child("Person1").child("OxygenDetails").set(ChkDelete)
chkdeletee = database.child("SubjectCheckDelete").child("Person1").child("OxygenDetails").get() ## reading data
print(chkdeletee.val())
### delete opr,, Removing OxygenLevel 
database.child("SubjectCheckDelete").child("Person1").child("OxygenDetails").child("OxygenLevel").remove()

print("--------------Result after Delete operation ------------")
chkdeletee = database.child("SubjectCheckDelete").child("Person1").child("OxygenDetails").get() ## reading data
print(chkdeletee.val())
