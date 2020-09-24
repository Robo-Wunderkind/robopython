===============
Line Tracker LT
===============

	
Get Sensor Values
#################

| get_sensor_values(``self``)
| 
| Returns a list of all three values of the lintracker IR sensors
| [left, center, right]

::

	values = Robo.LT1.get_sensor_values()

Get Right Value
###############

| get_right_value(``self``)
| 
| Returns the lintracker's right IR sensor value

::

	value = Robo.LT1.get_right_value()

Get Center Value
################

| get_center_value(``self``)
| 
| Returns the lintracker's center IR sensor value

::

	value = Robo.LT1.get_center_value()

Get Left Value
##############

| get_left_value(``self``)
| 
| Returns the lintracker's left IR sensor value

::

	value = Robo.LT1.get_left_value()

Track Line
##########
| track(``self``,``direction``,``speed``)
| ``direction`` must be 0 or 1 to indicate forwards or backwards
| ``speed`` must be between 0 and 100%

::

	Robo.LT1.track(0,75)


Check Line Tracker Action
#########################

| check_action(``self``)
| 
| Returns 1 if the action is completed

::

	while not Robo.LT1.check_action():
		# do stuff