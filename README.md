# PICO-Bluetooth-Flashlight
Bluetooth controlled light 

![Flash light and controller](images/remote.jpg)
This is the flashgun light and the controller built into a milkshake box. This is a companion project to [this one](https://github.com/CrazyRobMiles/PICO-Flash-Light), which creates a Wi-Fi controlled light that uses the PICO-W to host a website which can be used to adjust the colour of the light output. 

This project creates a remote control which uses Bluetooth to control the light. The code for the sender and the receiver are provided here. 
## Building a remote control

![Flash light parts](images/circuit.png)

This is the circuit for the device. 

You will need:

* An old box (or you can put the controller into anything you fancy).
* A Raspberry Pi PICO W.
* Three 10K linear potentiometers  
## Software
The software uses Micro Python. Install Micro Python and then copy all the .py files in this repository onto the device. 

If you want the device to be a controller, copy the file ble_sender.py to main.py. If you want the device to be light, copy the file ble_receiver.py to main.py.
## Light brightness
```
pixieLight = PixieLight(0.2)
```
The maximum brightness for the Pixie light is set in ble_receiver.py

The value that is used in the code is perfect for testing, but you must increase this from 0.2 to 1.0 if you want to use the light with full brightness. Just find the statement above in the file and make the change.

Have fun!

Rob Miles