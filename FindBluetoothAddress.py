#### Discover the bangle
#### Find the BAngle Address from this code output and copy paste in address vairables of BAngleHeartRtToFireBase.py
import asyncio
import array
from bleak import discover
from bleak import BleakClient
from bleak import BleakScanner


### Get the device name/Discover the avaliable devices
async def scanBangle():
    devices = await BleakScanner.discover()
    for device in devices:
        print()
        print(f"Name: \033[92m{device.name}\033[0m") ### Adding Green on Name
        print(f"Address: {device.address}")
        print(f"Details: {device.details}")
        print(f"Metadata: {device.metadata}")
        print(f"RSSI: {device.rssi}")
        
asyncio.run(scanBangle())
