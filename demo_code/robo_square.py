from robopython import Robo

if __name__ == '__main__':
    BLE_Name = "Robo24"
    Robo = Robo(BLE_Name)
    try:
        while True:
            Robo.drive(75, 30, 1)
            Robo.delay(0.25)
            Robo.turn(35, 90, 1)
            Robo.delay(0.25)

    except KeyboardInterrupt:
        pass

    finally:
        Robo.Motor1.stop()
        Robo.Motor2.stop()
        Robo.BLE.stop()
