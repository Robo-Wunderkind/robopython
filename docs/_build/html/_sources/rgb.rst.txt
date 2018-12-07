=======
RGB LED
=======

	
Set Colour
##########

| set_rgb(``self``, ``red``, ``green``, ``blue``)
| 
| Sets the RGB to the desired colour using a combination of red, green blue colour intensities 
|
| ``red`` 0-255 value for the red colour intensity
| ``green`` 0-255 value for the green colour intensity
| ``blue`` 0-255 value for the blue colour intensity

::

	Robo.RGB1.set_rgb(120,25,255)

Blink RGB
#########

| blink_rgb(``self``, ``red``, ``green``, ``blue``, ``num_blinks``,``period`` )
| 
| ``red`` 0-255 value for the red colour intensity
| ``green`` 0-255 value for the green colour intensity
| ``blue`` 0-255 value for the blue colour intensity
| ``num_blinks`` number of blinks
| ``period`` period in milliseconds 

::

	Robo.RGB1.blink_rgb(255, 255, 255, 5, 1000)	# blink white 5 times
	
Timed RGB
#########

| timed_rgb(``self``, ``red``, ``green``, ``blue``, ``time`` )
| 
| ``red`` 0-255 value for the red colour intensity
| ``green`` 0-255 value for the green colour intensity
| ``blue`` 0-255 value for the blue colour intensity
| ``time`` LED on time in seconds


::

	Robo.RGB1.timed_rgb(255, 255, 255, 2)	# white light for 2 seconds

Off
###

| off(``self``)
| 
| Turns off the LED

::

	Robo.RGB1.off()
	
Red
###

| red(``self``)
| 
| Turns the LED Red

::

	Robo.RGB1.red()

Green
#####

| green(``self``)
| 
| Turns the LED Green

::

	Robo.RGB1.green()

Blue
####

| blue(``self``)
| 
| Turns the LED Blue

::

	Robo.RGB1.blue()

Yellow
######

| yellow(``self``)
| 
| Turns the LED Yellow

::

	Robo.RGB1.yellow()
	
Orange
######

| orange(``self``)
| 
| Turns the LED Orange

::

	Robo.RGB1.orange()

White
#####

| white(``self``)
| 
| Turns the LED White

::

	Robo.RGB1.white()
	
Random Colour
#############

| random(``self``)
| 
| Shows a random colour on the LED

::

	Robo.RGB1.random()
	
Check LED Action
################

| check_action(``self``)
| 
| Returns 1 if the action is completed

::

	while not Robo.RGB1.check_action():
		# do stuff