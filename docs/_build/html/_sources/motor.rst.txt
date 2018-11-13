=====
Motor
=====


Set PWM
#######

| set_pwm(``self``, ``pwm``)
| 
| ``pwm`` must be between 0 and 255; where 127 = 100% CW and 129 = 100% CCW
| 0-100% CW -> 0-127 pwm 0-100% CCW -> 255-129
| Sets a constant torque PWM signal to the motor

::

	Robo.Motor1.set_pwm(60) 

Spin Distance
#############

| spin_distance(``self``, ``vel``, ``distance``, ``wd=89``)
|
| ``vel`` must be between 0 and 100%
| ``distance`` must be an integer in centimeters
| ``wd`` is the wheel diameter and is by default the diameter of the large wheel. 
| If different wheels are attached please specify the diamter in mm
|
| Robo will spin the motor at a constant velocity for the specified distance. If resistance is applied the motor will increase torque to try and maintain the velocity. 
| When approaching the end distance the motor slows down to ensure it covers the specified distance and does not overshoot

::

	Robo.Motor1.set_distance(60, 80) 
	
Spin Velocity
#############

| spin_velocity(``self``, ``vel``)
|
| ``vel`` must be between 0 and 100%
|
| Robo will spin the motor at a constant velocity. If resistance is applied the motor will increase torque to try and maintain the velocity. 

::

	Robo.Motor1.set_velocity(60) 

Stop
####

| stop(``self``)
| 
| Stops the motor

::

	Robo.Motor1.stop()
	
Check Motor Action
##################

| check_action(``self``)
| 
| Returns 1 if the action is completed

::

	while not Robo.Motor1.check_action():
		# do stuff