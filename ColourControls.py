import machine
import struct
import time

class ColourControls:
    def __init__(self):
        self.red_ADC = machine.ADC(0)
        self.green_ADC = machine.ADC(1)
        self.blue_ADC = machine.ADC(2)
        self.old_red=-1
        self.old_green=-1
        self.old_blue=-1
        self.update()
        
    def update(self):
        self.red = round(self.red_ADC.read_u16()/256)
        self.green = round(self.green_ADC.read_u16()/256)
        self.blue = round(self.blue_ADC.read_u16()/256)
        if self.red==self.old_red and self.green==self.old_green\
            and self.blue==self.old_blue:
            return False
        self.old_red=self.red
        self.old_green=self.green
        self.old_blue=self.blue
        return True
        
    def test(self):
        while True:
            changed = self.update()
            if changed:
                self.dump()
            time.sleep(0.5)
            
    def pack(self):
        return struct.pack("<BBB", self.red,self.green,self.blue)
    
    def unpack(self, data):
        value = struct.unpack("<BBB", data)
        self.red=value[0]
        self.green=value[1]
        self.blue=value[2]
        
    def dump(self):
        print("Red:%3d Green:%3d Blue:%3d"%(self.red,self.green,self.blue));

if __name__ == "__main__":
    controls = ColourControls()
    controls.test()