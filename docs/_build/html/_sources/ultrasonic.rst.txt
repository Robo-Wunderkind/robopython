=================
Ultrasonic Sensor
=================

	
Get Distance
############

| get_distance(``self``)
| 
| Returns the current distance

::

	distance = Robo.Ultrasonic1.get_distance()

Get Sound Level
###############

| get_sound_level(``self``)
| 
| Returns the current sound level

::

	sound = Robo.Ultrasonic1.get_sound()	
	
Set Distance Trigger
####################

| set_trigger(``self``, ``value``,``comparitor``)
| 
| ``value`` is the trigger value in centimeters
| ``comparitor`` 0 sets less than, 1 sets greater than value

::

	Robo.Ultrasonic1.set_trigger(50, 1)  # sets the trigger to set off when a distance greater than 50 cm is seen
	
Set Sound Trigger
#################

| set_sound_trigger(``self``, ``value``,``comparitor``)
| 
| ``value`` is the trigger value
| ``comparitor`` 0 sets less than, 1 sets greater than value

::

	Robo.Ultrasonic1.set_sound_trigger(150, 1)  # sets the trigger to set off when the sound is greater than 150 
	
Check Distance Trigger
######################

| check_distance_trigger(``self``)
| 
| Returns 1 if the trigger has happened

::

	while not Robo.Ultrasonic1.check_distance_trigger():
		# do stuff

Check Sound Trigger
###################

| check_distance_trigger(``self``)
| 
| Returns 1 if the trigger has happened

::

	while not Robo.Ultrasonic1.check_sound_trigger():
		# do stuff
