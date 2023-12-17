# SignTalk Project
All the code to run this program should is in the folder sign_talk_project_01. The code should be downloaded and implemented in the PocketBeagle Cloud9 program. All the hardware and hardware implementation can be found in the hackster.io page: 

## Steps to Setup and Run
1. Wire components as per the block diagram and images on the Hackster page. 
2. Connect the PocketBeagle to the internet.
3. Set up the PocketBeagle to run Python by running:
      a. sudo apt-get install python3-pip
      b. pip3 install adafruit-circuitpython-ssd1306
      c. sudo apt-get install python3-pil
      d. sudo apt-get install python3-numpy
      e. sudo apt-get install libopenjp2-7
4. Run final1.py

## Code Files
The main files that are called within the system are:
[!button, text = "final1.py"]: This file contains all the code for the project. It imports needed libraries, creates a Flex Sensor class, defines functions, and has a main script where the class and functions are called. 
[!button, text = "run"]: Downloading and running this file in your cloud9 directory allows the code to be loaded on the PocketBeagle so that the [!button, text = "final1.py"] program is automatically run once the PocketBeagle is powered up. 

## Sources (for Code and Setup)
OLED setup: https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
OLED code: https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2
Debugging PIL install: https://stackoverflow.com/questions/48012582/pillow-libopenjp2-so-7-cannot-open-shared-object-file-no-such-file-or-directo
Modifying OLED code: https://pillow.readthedocs.io/en/stable/deprecations.html
