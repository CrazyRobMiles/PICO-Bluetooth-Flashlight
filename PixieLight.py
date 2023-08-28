from machine import Pin,UART
from Pixie import Pixie
import time
import struct

class PixieLight:
    
    def __init__(self, brightness, txPinNo=4, rxPinNo=5):
        uart = UART(1,tx=Pin(txPinNo),rx=Pin(rxPinNo), baudrate=115200)
        self.pixies = Pixie(uart, 1, brightness=brightness)
        self.last_update_ticks = time.ticks_ms()
        self.update_tick_interval = 200
        self.old_red=-1
        self.old_green=-1
        self.old_blue=-1
        self.red=0
        self.green=255
        self.blue=0
        self.pixies[0] = (0, 255, 0)
    
    def render(self):
        self.pixies.fill((self.red,self.green,self.blue))
        
    def set_colours(self,red,green,blue):
        if red==self.old_red and green==self.old_green\
            and blue==self.old_blue:
            return False
        self.red = red
        self.green = green
        self.blue = blue
        self.old_red=self.red
        self.old_green=self.green
        self.old_blue=self.blue
        self.render()
        return True
    
    def unpack(self, data):
        value = struct.unpack("<BBB", data)
        if self.set_colours(value[0],value[1],value[2]):
            self.dump()
            
    def dump(self):
        print("Red:%3d Green:%3d Blue:%3d"%(self.red,self.green,self.blue))
 
    def test(self):
        while True:
            self.pixies.fill((255,0,0))
            time.sleep(0.5)
            self.pixies.fill((0,255,0))
            time.sleep(0.5)
            self.pixies.fill((0,0,255))
            time.sleep(0.5)
            
    def update(self):
        millis = time.ticks_ms()
        interval = time.ticks_diff(millis, self.last_update_ticks)
        if interval>self.update_tick_interval:
            self.render()
            self.last_update_ticks = millis

if __name__ == "__main__":
    light = PixieLight(0.1)
    light.test()

