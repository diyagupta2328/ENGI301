# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Blink USR3
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

A simple blinking operation of the on board USR3 LED will occur at a 5 Hz frequency. 
This means that 5 on/off cycles will be completed within 1 second. 

--------------------------------------------------------------------------
"""


import Adafruit_BBIO.GPIO as GPIO
import time

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------


#This is the driver function that sets up the led as GPIO and then write HIGH/LOW to the LED with a certain frequency
if __name__ == "__main__":
    i = 3
    GPIO.setup("USR%d" % i, GPIO.OUT)

    # 1 secong/5 cycles/2 states = 0.1 seconds per state for 5 Hz frequency
    while True:
        GPIO.output("USR%d" % i, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output("USR%d" % i, GPIO.LOW)
        time.sleep(0.1)
   
