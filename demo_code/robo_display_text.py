from robopython import Robo

BLE_Name = "Robo24"
Robo = Robo(BLE_Name)
try:
    while True:
        Robo.display_text("Welcome to Robo Wunderkind!", [Robo.Matrix1])

except KeyboardInterrupt:
    print "Exiting"

finally:
    Robo.stop_all()
    Robo.BLE.stop()
