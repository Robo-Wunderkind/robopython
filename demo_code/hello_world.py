from robopython import Robo
from time import sleep


BLE_Name = "ROBO"  # Put the BLE name of your Robo here
Robo = Robo(BLE_Name)
Robo.System.play_sound(0)
