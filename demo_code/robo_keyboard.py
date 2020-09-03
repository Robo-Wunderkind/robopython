from robopython import Robo
import msvcrt
import time


def drive_demo(Robo):
    velocity = 50
    previous_cmd = ''
    commands = ['w', 'q', 'a', 's', 'd', 'r', 'g', 'b', 'o', '1', '2', '3', '4', '5', '6', '7', '8']

    try:
        while True:
            if msvcrt.kbhit():
                input_char = msvcrt.getwch()

                if input_char not in commands:
                    continue

                if input_char == 'q':
                    print("Exiting Drive Demo")
                    break

                if input_char == 'w' and previous_cmd != 'w':
                    Robo.drive(velocity, Robo.infinite, 1)
                    previous_cmd = input_char
                    continue

                if input_char == 's'and previous_cmd != 's':
                    Robo.drive(velocity, Robo.infinite, 0)
                    previous_cmd = input_char
                    continue

                if input_char == 'd' and previous_cmd != 'd':
                    Robo.turn(velocity, Robo.infinite, 1)
                    previous_cmd = input_char
                    continue

                if input_char == 'a' and previous_cmd != 'a':
                    Robo.turn(velocity, Robo.infinite, 0)
                    previous_cmd = input_char
                    continue

                if input_char == 'r' and previous_cmd != 'r':
                    Robo.RGB1.set_rgb(255, 0, 0)
                    previous_cmd = input_char
                    continue

                if input_char == 'g' and previous_cmd != 'g':
                    Robo.RGB1.set_rgb(0, 255, 0)
                    previous_cmd = input_char
                    continue

                if input_char == 'b' and previous_cmd != 'b':
                    Robo.RGB1.set_rgb(0, 0, 255)
                    previous_cmd = input_char
                    continue

                if input_char == 'o' and previous_cmd != 'o':
                    Robo.RGB1.off()
                    previous_cmd = input_char
                    continue

                if input_char == '1' and previous_cmd != '1':
                    Robo.System.play_sound(Robo.System.sounds[0])
                    previous_cmd = input_char
                    continue

                if input_char == '2' and previous_cmd != '2':
                    Robo.System.play_sound(Robo.System.sounds[1])
                    previous_cmd = input_char
                    continue

                if input_char == '3' and previous_cmd != '3':
                    Robo.System.play_sound(Robo.System.sounds[2])
                    previous_cmd = input_char
                    continue

                if input_char == '4' and previous_cmd != '4':
                    Robo.System.play_sound(Robo.System.sounds[3])
                    previous_cmd = input_char
                    continue

                if input_char == '5' and previous_cmd != '5':
                    Robo.System.play_sound(Robo.System.sounds[4])
                    previous_cmd = input_char
                    continue

                if input_char == '6' and previous_cmd != '6':
                    Robo.System.play_sound(Robo.System.sounds[5])
                    previous_cmd = input_char
                    continue

                if input_char == '7' and previous_cmd != '7':
                    Robo.System.play_sound(Robo.System.sounds[6])
                    previous_cmd = input_char
                    continue

                if input_char == '8' and previous_cmd != '8':
                    Robo.System.play_sound(Robo.System.sounds[7])
                    previous_cmd = input_char
                    continue

            time.sleep(0.3)
            if msvcrt.kbhit() != 1:
                previous_cmd = ''
                Robo.stop()

    except KeyboardInterrupt:
        pass

    finally:
        Robo.stop_all()
        Robo.BLE.stop()


if __name__ == '__main__':
    BLE_Name = "Robo24"
    Robo = Robo(BLE_Name)
    drive_demo(Robo)