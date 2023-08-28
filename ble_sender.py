# Based on the BLE temperature example:
# https://github.com/raspberrypi/pico-micropython-examples
#
# Complete code here: https://github.com/CrazyRobMiles/PICO-Bluetooth-Flashlight

# Have fun!
# Rob Miles 2023


import bluetooth
import random
import struct
import time
import machine
import ubinascii
from ble_advertising import advertising_payload
from micropython import const
from machine import Pin
from ColourControls import ColourControls

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_TEMP_CHAR = (
    bluetooth.UUID(0x2A6E),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_TEMP_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

class BLE_sender:
    def __init__(self, controls, name=""):
        self.controls=controls
        self.led = Pin('LED', Pin.OUT)
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(self._ble.config('mac')[1],':').decode().upper()
        print('Sensor name %s' % name)
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID]
        )
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def update(self, notify=True, indicate=False):
        # Only send a new value when the old ones have changed
        if not self.controls.update():
            return
        self.led.toggle()
        self.controls.dump()
        data = self.controls.pack()
        self._ble.gatts_write(self._handle, data)
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

def run():
    print("Light sender starting")
    controls = ColourControls()
    sender = BLE_sender(controls)
    while True:
        sender.update()
        time.sleep_ms(20)

if __name__ == "__main__":
    run()

