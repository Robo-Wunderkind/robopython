=====
Servo
=====


Set Angle
#########

| set_angle(``self``, ``angle``)
| 
| ``angle`` must be between 0 and 255
| 
| Sets the servo to be positioned at the desired angle

::

	Robo.Motor1.set_angle(90) 
	
Check Servo Action
##################

| check_action(``self``)
| 
| Returns 1 if the action is completed

::

	while not Robo.Servo1.check_action():
		# do stuff