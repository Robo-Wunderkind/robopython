=====
Robo
=====

Create Robo Instance

| BLE_Name = "Robo1" -- example BLE name

::

	my_robo = Robo(BLE_Name)

Battery Level 
##################

| battery_level(``self``)
| 
| Returns the battery level in % and the status. 

::

	>>> print my_robo.battery_level()
	>>> 80, Discharging
	
Change BLE Name
###############

| change_ble_name(``self``, ``name``)
| 
| ``name`` must be 16 characters or less e.g name = "Robo1"
| Robo will reboot once the command is received and the name is changed
| You can use an instance of BLED112 to scan() and see all discoverable devices or simply check on your phone that the new ble name has been taken	

::

	my_robo.change_ble_name("Robo2")
	
Check Drive Action 
##################

| check_drive_action(``self``)
| 
| returns the status of the drive action 1 = done, None = in progress, 0 = failed

::

	if my_robo.check_drive_action():
		print "Drive Action Complete"

Check Turn Action
#################

| check_turn_action(``self``)
|
| returns the status of the turn action 1 = done, None = in progress, 0 = failed	

::

	if my_robo.check_turn_action():
		print "Turn Action Complete"
	
Delay
#####

| delay(``self``, ``delay_time``)
|
| ``delay_time`` is the time in seconds to wait until function returns	

::

	my_robo.delay(1)
	
Display Text
############

| display_text(``self``, ``text``, ``matrices``)
|
| Cascaded diplay of text on one or more LED Matices
|	
| ``text`` is a string to be displayed on the matrices
| ``matrices`` is a list of Matrix objects that should participate in the text display

::

	my_robo.display_text("Welcome to Robo Wundrkind", [my_robo.Matrix1, my_robo.Matrix2, my_robo.Matrix3])
	
Drive
#####


| drive(``self``, ``vel``, ``distance``, ``direction``, ``wait=1``, ``motors=(1, 2)``, ``wd=89``)
| 
| drive is Robo's simplified command to have Robo drive a certain distance assuming a 2 motor configuration
| 	
| ``vel`` is the desired velocity from 0-100%
| ``distance`` is how far in centimeters Robo should drive
| ``direction`` will detirmine forward or backward
| ``wait`` is a flag that indicates if we wait in the function until the action is complete. set wait = 0 if we want to exit the function while driving
| ``motors`` is a tuple of the two motors used to drive Robo
| ``wd`` is the diameter of the wheels used, default is 89mm or 0x59mm in hex. 
| If you choose to change the wheels be sure to pass in the new wheel diameter

::

	my_robo.drive(80, 30, 1)

Drive Forever
#############

| drive_inf(``self``, ``vel``, ``direction``)
|
| ``vel`` is the desired velocity from 0-100%
| ``direction`` will detirmine forward or backward

::

	my_robo.drive_inf(80, 1)

Turn Forever
############

| turn_inf(``self``, ``vel``, ``direction``)
|
| ``vel`` is the desired velocity from 0-100%
| ``direction`` will detirmine forward or backward

::

	my_robo.turn_inf(80, 1)	

	
Firmware Version
################

| firmware(``self``)
|
| Returns the firmware version of Robo

::

	my_robo.firmware()	
	
Get Robo Build
##############

| get_build(``self``)
|
| returns a list of Robo Wunderkind moduels that are currently attached
| The is updated automatically upon initialization of Robo object as well as when there has been a change in the build
| The latest build is stored in self.build -> my_robo.build	

::

	build = my_robo.get_build()
	
Get BLE Characteristics
#######################

| get_characteristics(``self``)
|
| characteristics = my_robo.get_characteristics()
| returns a list of GATT characteristics 

::

	characteristics = my_robo.get_characteristics()

Get RSSI
########

| get_rssi(``self``)
|
| rssi = my_robo.get_rssi()
| returns the BLE signal strength rssi value	

::

	signal_strength = my_robo.get_rssi()
	
Set Drive Command
#################

| set_drive(``self``, ``motor_cmds``, ``vel``, ``distance``, ``action_id``, ``wd=0x59``)
|
| set_drive is Robo's generic command to set the velocity and distance commands to multiple motors at once
|
| ``motor_cmds`` is a list of motor objects folloed by the direction that motor should spin: [[1,0],[2,1],[3,0],[4,1]] motors from 1-6 are valid if connected
| ``vel`` is the desired velocity from 0-100%
| ``distance`` is the desired distance to travel in centimeters
| ``action_id`` is a unique identifier that is sent back once Robo has completed the action. Use the self.drive_id by default, use check_drive_action() to know when it is done
| ``wd`` is the diameter of the wheels used, default is 89mm or 0x59mm in hex. If you choose to change the wheels be sure to pass in the new wheel diameter

::	

	my_robo.set_drive([[1,0],[2,1],[3,0],[4,1]], 50, 100, my_robo.drive_id)

	
Sound Playback
##############

| sound(``self``, ``sound``)
|
| Plays the desired sound clip on the system cube speaker 0-7 are valid

::

	my_robo.sound(0)
	
	
Stop
####

| stop(``self``)
|
| stops all motors from moving

::

	my_robo.stop()

Stop All Actions
################

| stop_all(``self``)
| 
| stops all outputs 

::

	my_robo.stop_all()	
	
Turn
####

| turn(``self``, ``vel``, ``angle``, ``direction``, ``wait=1``, ``motors=(1, 2)``, ``wd=89``, ``turning_radius=91``)
| 
| turn is Robo's simplified command to have Robo turn a number of degrees assuming a 2 motor configuration
| 
| ``vel`` is the desired velocity from 0-100%
| ``angle`` is the amount to have Robo turn in degrees
| ``direction`` will detirmine clockwise or counter clockwise rotation
| ``wait`` is a flag that indicates if we wait in the function until the turn is complete. set wait = 0 if we want to exit the function while turning
| ``motors`` is a tuple of the two motors used to turn Robo
| ``wd`` is the diameter of the wheels used, default is 89mm or 0x59mm in hex. If you choose to change the wheels be sure to pass in the new wheel diameter
| ``turning_radius`` is the distance from the wheel to the centre of Robo's turning axle in millimeters

::

	my_robo.turn(40, 90, 1)
	

	

	

	
	
	