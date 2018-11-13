=================
Motion Sensor PIR
=================

	
Get Motion State
################

| get_state(``self``)
| 
| Returns the current state of the PIR

::

	state = Robo.Motion1.get_state()

Set Motion Trigger
##################

| set_trigger(``self``, ``comparitor``)
| 
| ``comparitor`` 0 sets no motion, 1 sets motion

::

	Robo.Motion1.set_trigger(1) # sets the trigger to set off with motion
	
Check Motion Trigger
####################

| check_trigger(``self``)
| 
| Returns 1 if the trigger has happened

::

	while not Robo.Motion1.check_trigger():
		# do stuff

