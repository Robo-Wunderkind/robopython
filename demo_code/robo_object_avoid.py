from robopython import Robo
import random


if __name__ == '__main__':
    BLE_Name = "Robo24"
    Robo = Robo(BLE_Name)
    velocity = 30
    ultrasonic_trigger = 80
    ultrasonic_comparator = 0
    delay_time = 1
    Robo.drive(velocity, Robo.infinite, 1)
    Robo.Ultrasonic1.set_distance_trigger(ultrasonic_trigger, ultrasonic_comparator)
    Robo.RGB1.green()
    try:
        while True:
            if Robo.Ultrasonic1.check_ultrasonic_trigger():
                Robo.stop()
                Robo.RGB1.red()
                Robo.delay(delay_time)
                turn_angle = random.randint(90, 270)
                Robo.turn(velocity, turn_angle, 0)
                Robo.drive(velocity, Robo.infinite, 1)
                Robo.Ultrasonic1.set_distance_trigger(ultrasonic_trigger, ultrasonic_comparator)
                Robo.RGB1.green()

    except KeyboardInterrupt:
        pass

    finally:
        Robo.stop_all()
        Robo.BLE.stop()
