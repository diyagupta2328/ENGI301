# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Sign Talk Final Code
--------------------------------------------------------------------------
License:   
Copyright 2023 - <Diya Gupta>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

This python script is the final code for the SignTalk device I made for 
a project in my ENGI301 class. With this script, I read data from the 
flex sensors, classify that data and map to a letter output, and then 
program the OLED to display that output. This script contains the FlexSensor
class, some utility functions for data classification and mapping, and a main
driver function. 

--------------------------------------------------------------------------
"""

# ------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------

# Imports used in the script
import Adafruit_BBIO.ADC as ADC
import time  
import board
import busio
import adafruit_ssd1306
import digitalio
import os
from PIL import Image, ImageDraw, ImageFont



# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# define the maximum and minimum analog values (for input or output)
MIN_VALUE     = 0
MAX_VALUE     = 4095

# set dimensions of OLED display 
WIDTH = 128
HEIGHT = 32  
BORDER = 5

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# define which analog input pins on PocketBeagle can potentially be used
PINS_1V8 = ["P1_19", "P1_21", "P1_23", "P1_25", "P1_27", "P2_36"]
PINS_3V6 = ['P1_2']


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class FlexSensor():
    """  
    This FlexSensor class defines the behavior and state of a flex sensor
    object which will also be a hardware component for this project. 
    """
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
        """ Get the voltage of the pin from raw value
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


# Beginning of utility functions

def get_category(threshold_per_finger, value, finger):
    '''
    This functions categorizes the flex of each finger into one of three categories: low, medium, and high. 
    Parameters: threshhold_per_finger: a 2D array specifiying the raw analogue value cutoffs for low/medium/high
    bends of each finger, value: the raw analogue flex value of a finger, finger: which finger is being considered.
    Returns: The category of flex as a string. 
    '''
    if value <= threshold_per_finger[finger][0]:
        return "low"
    if value <= threshold_per_finger[finger][1]:
        return "medium"
    else:
        return "high"


def get_dict():
    '''
    Given a dictionary in the format shown in the initial_dict variable, this function,
    converts the dictionary to be in a format {"lowmedium..":'A', "highlow..": 'B'}. 
    This is because the initial format dictionary can be easily generated from a csv
    with sign data, but the second format dictionary is easier to index and read for 
    the purposes of this project. 
    Returns: A dictionary in the format {"lowmedium..":'A', "highlow..": 'B', etc}
    '''
    #  X is the letter that is matched to a high, or no flex, value for each finger
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
    '''
    This functions maps the letter that a sign represents based on the 
    different flex categories (lolw/medium/high) of each finger. 
    Parameters: category_sequence: a list of the bend categories of each finger
    Returns: A letter match as a string
    '''
    letters_dict = get_dict()
    # convert category_sequence (eg ["low", "low", "high"] into a string
    category_string = ''.join([item for item in category_sequence])
    
    if category_string in letters_dict:
        return letters_dict[category_string]
    else:
        return ("No letter match found!")
        
# End of utility functions
    

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------


if __name__ == '__main__':


    print("FlexSensor Test")

    # Create instantiation of the flex sensors 
    sensor1 = FlexSensor("P1_19")
    sensor2 = FlexSensor("P1_23")
    sensor3 = FlexSensor("P1_25")
    sensor4 = FlexSensor ("P1_27")
    sensor5 = FlexSensor("P1_2")
    sensorlist = [sensor1, sensor2, sensor3, sensor4, sensor5]
    
    '''
    A = thumb = finger 1
    B = pointer = finger 2
    C = middle = finger 3
    D = ring = finger 4
    E = pinky = finger 5 
    Set category threshold values for each finger through assigned variable below.
    There are 2 threshold values per finger. The first threshold value determines 
    the max value for a "low" category classification. The second threshold
    value determines a max value for a "medium" category classification. 
    '''
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
    
    # I2C OLED display instantiation
    i2c = busio.I2C(board.SCL, board.SDA)
    i2c = board.I2C()  # uses board.SCL and board.SDA
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

    
    while(1):
        
        # get letter output
        category_sequence = list()
        for i in range(5):
            value = sensorlist[i].get_value()
            category = get_category(threshold_per_finger, value, i)
            category_sequence.append(category)
        
        print(category_sequence)
        
        output = get_letter(category_sequence)
        print(output)
        
        
        
        # Clear display
        oled.fill(0)
        oled.show()
        
        # Create blank image for drawing
        # Image for 1-bit color
        image = Image.new("1", (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Load default font.
        font = ImageFont.load_default()
        
        # specify the output to be the text
        text = output
        (font_width, font_height) = (font.getmask(text).getbbox()[2], font.getmask(text).getbbox()[3])
        # draw the text 
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
        oled.image(image)
        oled.show()
        
        
        # wait for 0.5 secs in the loop
        time.sleep(0.5)
 
    print("Test Complete")

