
"""
Mapping what is read by the various sensors to a letter (replce project.py with this )

"""
import Adafruit_BBIO.ADC as ADC
import pandas as pd

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

MIN_VALUE     = 0
MAX_VALUE     = 4095

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

PINS_1V8 = ["P1_19", "P1_21", "P1_23", "P1_25", "P1_27", "P2_36"]
df = pd.read_csv("signdata.csv")

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
            
        self.voltage = 1.8
            
        if pin not in PINS_1V8:
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
        # Read raw value from ADC
        return int(ADC.read_raw(self.pin))

    # End def

    
    def get_voltage(self):
        """ Get the voltage of the pin
        
           Returns:  Float in volts
        """
        return ((self.get_value() / MAX_VALUE) * self.voltage)
    
    # End def    
 
    
    def get_category(threshold_per_finger, value, finger):
        if value <= threshold_per_finger[finger][0]:
            return "low"
        if value <= threshold_per_finger[finger][1]:
            return "medium"
        else:
            return "high"

    #converts to {"lowmedium..":'A', "highlow..": 'B'} format
    def convert_df_to_dict():
        df_dict = df.to_dict('index')
        new_dict = dict()
        for keyouter, valueouter in df_dict.items():
            letter_string = ''
            for keyinner, valueinner in value.items():
                letter_string += valueinner
            new_dict[letter_string] = keyouter
        return(new_dict)
        
    
    def get_letter(category_sequence):
        letters_dict = convert_df_to_dict()
        
        #convert category_sequence (eg ["low", "low", "high"] into a string
        category_string = ''.join[item for item in category_sequence]
        
        if category_string in letters_dict:
            return letters_dict[category_string]
        else:
            return ("No letter match found!")
        
        
        
    def cleanup(self):
        """Cleanup the hardware components."""
        # Nothing to do for ADC
        pass        
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    print("FlexSensor Test")

    # Create instantiation of the flex sensors 
    sensor1 = FlexSensor("P1_19")
    sensor2 = FlexSensor("P1_21")
    sensor3 = FlexSensor("P1_23")
    sensor4 = FlexSensor ("P1_25")
    sensor5 = FlexSensor("P1_27")
    sensorlist = [sensor1, sensor2, sensor3, sensor4, sensor5]
    

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    print("Use Ctrl-C to Exit")
    
    
    #A = thumb, B = pointer, C = middle, D = ring, E = pinky
    tA1 = 2000
    tA2 = 3000
    tB1 = 2000
    tB2 = 3000
    tC1 = 2000
    tC2 = 3000
    tD1 = 2000
    tD2 = 3000
    tE1 = 2000
    tE2 = 3000
    threshold_per_finger = [[tA1, tA2], [tB1, tB2], [tC1, tC2], [tD1, tD2], [tE1, tE2]]
    
    category_sequence = list()
    for i in range(3):
        value = sensorlist[i].getvalue()
        category = value.get_category(threshold_per_finger, value, i)
        category_sequence.append(category)
    
    output = get_letter(category_sequence)
    print(output)
    
   
   '''     
    
    try:
        while(1):
            # Print flexsensor values
            print("Value1   = {0}".format(sensor1.get_value()))
            #print("Voltage1 = {0} V".format(sensor1.get_voltage()))
            
            print("Value2   = {0}".format(sensor2.get_value()))
            #print("Voltage2 = {0} V".format(sensor2.get_voltage()))
            
            print("Value3   = {0}".format(sensor3.get_value()))
            #print("Voltage3 = {0} V".format(sensor3.get_voltage()))
            
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        pass
        
    '''
    
    print("Test Complete")

