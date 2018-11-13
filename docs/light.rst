============
Light Sensor
============

	
Get Light Value
###############

| get_light(``self``)
| 
| Returns the light value in lx of the specified light cube

::

	light = Robo.Light1.get_light()

Set Light Trigger
#################

| set_trigger(``self``, ``value``, ``comparitor``)
| 
| ``value`` is the lx value you want to se the trigger to
| ``comparitor`` 0 is less than, 1 is greater than the set value

::

	Robo.Light1.set_trigger(500, 0)
	
Check Light Trigger
###################

| check_trigger(``self``)
| 
| Returns 1 if the trigger has happened

::

	while not Robo.Light1.check_trigger():
		# do stuff

