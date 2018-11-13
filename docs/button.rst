======
Button
======

	
Get Button State
################

| get_state(``self``)
| 
| Returns the current state of the button

::

	state = Robo.Button1.get_state()

Set Button Trigger
##################

| set_trigger(``self``, ``comparitor``)
| 
| ``comparitor`` 0 sets pressed, -1 sets released, 1-254 defines the number of clicks before triggered

::

	Robo.Button1.set_trigger(5) # sets the trigger for 5 clicks
	
Check Button Trigger
####################

| check_trigger(``self``)
| 
| Returns 1 if the trigger has happened

::

	while not Robo.Button1.check_trigger():
		# do stuff

