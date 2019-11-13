from time import sleep
from robopython import Robo, BLED112

RW =['11100000',
     '10100000',  
     '11000000',
     '10100000',
     '00010001',
     '00010101',
     '00011111',
     '00001110'
    ]

if __name__ == '__main__':
    BLE_Name = "ROBO_12"       # Replace this if your Robo Wunderkind's BLE is named different
    Robo_BLE = Robo(BLE_Name)

    Robo_BLE.RGB1.blink(0x00, 0xff, 0x00, 255, 200)
    Robo_BLE.Motor1.spin_distance(100, 65535)
    Robo_BLE.Matrix1.set_display(RW)
    Robo_BLE.Button1.set_trigger(0) # checks for rising edge (press)

    try:
    	while True:
            Robo_BLE.Servo1.set_angle(90)
            sleep(1)

            LT_Values = Robo_BLE.LT1.get_sensor_values()
            Light_Value = Robo_BLE.Light1.get_light()
            Motion_State = Robo_BLE.Motion1.get_motion()
            Sound_Value = Robo_BLE.Ultrasonic1.get_sound()
            Distance_Value = Robo_BLE.Ultrasonic1.get_distance()

            print("Line Tracker Sensor Values L-C-R    " + str(LT_Values[0]) + "-" + str(LT_Values[1]) + "-" + str(LT_Values[2]))
            print("Light Sensor Reading: " + str(Light_Value))
            print("Motion State: " + str(Motion_State))
            print("Sound Level: " + str(Sound_Value))
            print("Distance in cm: " + str(Distance_Value))
            print("Has the button been triggered? " + str(Robo_BLE.Button1.check_trigger()))

            Robo_BLE.Servo1.set_angle(0)
            sleep(1)

    except KeyboardInterrupt:
    	print("Program Terminated")
    finally:
    	print("Exiting Main Program")
        Robo_BLE.stop_all()