
"""
Mapping what is read by the various sensors to a letter (replce project.py with this )

"""
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import time

import board
import busio
#which bus is default?
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
#adding hardware reset pin
import digitalio

#reset_pin = digitalio.DigitalInOut(board.D4) # any pin!
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""


import os
from PIL import Image, ImageDraw, ImageFont

# Define the Reset Pin
#oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

MIN_VALUE     = 0
MAX_VALUE     = 4095

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

PINS_1V8 = ["P1_19", "P1_21", "P1_23", "P1_25", "P1_27", "P2_36"]
PINS_3V6 = ['P1_2']


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class FlexSensor():
    """ Button Class """
    pin             = None
    voltage         = None
    
    def __init__(self, pin=None, voltage=1.8):
        """ Initialize variables and set up the flexsensor """
        if (pin == None):
            raise ValueError("Pin not provided for FlexSensor()")
        else:
            self.pin = pin
            
        if pin in PINS_1V8:
            self.voltage = 1.8
        else:
            self.voltage = 3.6
            
        if pin not in PINS_1V8 and pin not in PINS_3V6:
            print("WARNING:  Unknown pin {0}.  Setting voltage to 1.8V.".format(pin))
        
        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Analog Input
        ADC.setup()

    # End def


    def get_value(self):
        """ Get the value of the FlexSensor
        
           Returns:  Integer in [0, 4095]
        """
        try:
            # Read raw value from ADC
            return int(ADC.read_raw(self.pin))
        except:
            # Due to a bug in the Adafruit_BBIO.ADC library, AIN6 is not mapped correctly
            # Hard coding to return the "read_raw" value of AIN6 if the above command fails
            return int(os.popen("cat /sys/bus/iio/devices/iio\:device0/in_voltage6_raw").read())

    # End def

    
    def get_voltage(self):
        """ Get the voltage of the pin
        
           Returns:  Float in volts
        """
        return ((self.get_value() / MAX_VALUE) * self.voltage)
    
    # End def    
 
    
        
        
    def cleanup(self):
        """Cleanup the hardware components."""
        # Nothing to do for ADC
        pass        
        
    # End def

# End class


def get_category(threshold_per_finger, value, finger):
    if value <= threshold_per_finger[finger][0]:
        return "low"
    if value <= threshold_per_finger[finger][1]:
        return "medium"
    else:
        return "high"

#converts to {"lowmedium..":'A', "highlow..": 'B'} format
def get_dict():
    initial_dict = {"A":{"Thumb": "high" , "Pointer": "medium", "Middle":"medium", "Ring": "medium", "Pinky": "medium"}, "D":{"Thumb": "medium" , "Pointer": "high",
    "Middle":"medium", "Ring": "medium", "Pinky": "medium"}, "I":{"Thumb": "medium" , "Pointer": "medium", "Middle":"medium", "Ring": "medium", "Pinky": "high"}, 
    "Y":{"Thumb": "high" , "Pointer": "medium", "Middle":"medium", "Ring": "medium", "Pinky": "high"}, 
    "X":{"Thumb": "high" , "Pointer": "high", "Middle":"high", "Ring": "high", "Pinky": "high"}}
    new_dict = dict()
    for keyouter, valueouter in initial_dict.items():
        letter_string = ''
        for keyinner, valueinner in valueouter.items():
            letter_string += valueinner
        new_dict[letter_string] = keyouter
    return(new_dict)
    

def get_letter(category_sequence):
    #print(category_sequence)
    letters_dict = get_dict()
    
    #convert category_sequence (eg ["low", "low", "high"] into a string
    category_string = ''.join([item for item in category_sequence])
    
    if category_string in letters_dict:
        return letters_dict[category_string]
    else:
        return ("No letter match found!")
    

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------


if __name__ == '__main__':
    import time

    print("FlexSensor Test")

    # Create instantiation of the flex sensors 
    sensor1 = FlexSensor("P1_19")
    sensor2 = FlexSensor("P1_23")
    sensor3 = FlexSensor("P1_25")
    sensor4 = FlexSensor ("P1_27")
    sensor5 = FlexSensor("P1_2")
    sensorlist = [sensor1, sensor2, sensor3, sensor4, sensor5]
    
    
    #A = thumb, B = pointer, C = middle, D = ring, E = pinky
    tA1 = 600
    tA2 = 900
    tB1 = 500
    tB2 = 900
    tC1 = 500
    tC2 = 900
    tD1 = 500
    tD2 = 900
    tE1 = 200
    tE2 = 280
    threshold_per_finger = [[tA1, tA2], [tB1, tB2], [tC1, tC2], [tD1, tD2], [tE1, tE2]]
    
    while(1):
        category_sequence = list()
        for i in range(5):
            value = sensorlist[i].get_value()
            category = get_category(threshold_per_finger, value, i)
            category_sequence.append(category)
        
        print(category_sequence)
        
        output = get_letter(category_sequence)
        print(output)
        
        # Clear display.
        oled.fill(0)
        oled.show()
        
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (oled.width, oled.height))
        
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        
        '''
        # Draw a white background
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        
        # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        
        
        '''
        '''
        # Draw Some Text
        text = "Hello World!"
        (font_width, font_height) = font.getlength(text)
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
        '''
        
        # Load default font.
        font = ImageFont.load_default()
        
        # Draw Some Text
        text = output
        (font_width, font_height) = (font.getmask(text).getbbox()[2], font.getmask(text).getbbox()[3])
        #print(font_width)
        #print(font_height)
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
        
        
        # Display image
        oled.image(image)
        oled.show()

        time.sleep(0.5)
 
    print("Test Complete")

