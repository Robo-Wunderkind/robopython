==========
LED Matrix
==========

	
Display
#######

| set_display(``self``, ``rows``)
| 
| ``rows`` is an 8 element array of 8-bit strings. 
| Displays the given ``rows`` on the specified LED Matrix

::

	rows = ['00000000',
                '11000011',
                '11000011',
                '00000000',
                '10000001',
                '11000011',
                '00111100',
                '00000000'
               ],

	Robo.Matrix1.set_display(rows)
	
Timed Display
#############

| set_display(``self``, ``rows``, ``duration``)
| 
| ``rows`` is an 8 element array of 8-bit strings. 
| ``duration`` is the time in seconds
| Displays the given ``rows`` on the specified LED Matrix for the specified amount of time

::

	rows = ['00000000',
                '11000011',
                '11000011',
                '00000000',
                '10000001',
                '11000011',
                '00111100',
                '00000000'
               ],

	Robo.Matrix1.set_display(rows, 4)

Off
###

| off(``self``)
| 
| Turns off the LED Matrix 

::

	Robo.Matrix1.off()
	
Check Action
############

| check_action(``self``)
| 
| Returns 1 if the the action has completed

::

	while not Robo.Matrix1.check_action():
		# do stuff while the timed display is on

Rotate Right
############

| rotate_right(``self``, ``rows``)
| 
| Rotates the image to the right by 90 degrees

::

	image = Robo.Matrix1.rotate_right(rows)	
	
Rotate Left
###########

| rotate_left(``self``, ``rows``)
| 
| Rotates the image to the left by 90 degrees

::

	image = Robo.Matrix1.rotate_left(rows)		
	
Flip X
######

| flip_x(``self``, ``rows``)
| 
| Flips the image in the X axis

::

	image = Robo.Matrix1.flip_x(rows)		
	
Flip Y
######

| flip_y(``self``, ``rows``)
| 
| Flips the image in the Y axis

::

	image = Robo.Matrix1.flip_y(rows)		
