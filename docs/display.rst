=======
Display
=======

Pre-Programmed Image
####################

| image(``self``, ``image_num``, ``orientation``, ``delay``)
| 
| ``image_num`` is the index of the pre-programmed image 0-4
| ``orientation`` is the desired orientation to display the image. 0 - 3 -> 0 - 270 degrees
| ``delay`` is the time in milliseconds that the image will be displayed for 0->65535
| Displays the pre-programmed ``image_num`` on the LED Display cube

::

	Robo.Display1.image(0, 2, 1000)


Custom Image
############

| custom_image(``self``, ``image``, ``orientation``, ``delay``)
| 
| ``image`` is a 32 element array of 8-bit numbers representing the 16 rows of the desired image. 
| ``orientation`` is the desired orientation to display the image. 0 - 3 -> 0 - 270 degrees
| ``delay`` is the time in milliseconds that the image will be displayed for 0->65535
| Displays the given ``image`` on the LED Display cube

::

	Robo_Logo = [0xff, 0xfc, 0xff, 0xfe, 0xef, 0xf7, 0xc7, 0xe3, 0xc4, 0x23, 0xee, 0x77, 0xff, 0xfe, 0xff, 0xfc, 0x00, 0x00, 0xfe, 0x3c, 0xfe, 0x7e, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0x7e, 0xfe, 0x3c ]

	Robo.Display1.custom_image(Robo_Logo, 1, 1000)

Pre-Programmed Animation
########################

| animate(``self``, ``animation_num``, ``repeats``, ``reverse``, ``orientation``)
| 
| ``animation_num`` is the index of the pre-programmed animation 0-2
| ``repeats`` number of times to repeat the animation
| ``reverse`` 0 or 1 to indicate if the animation should play forwards then backwards or just forwards
| ``orientation`` is the desired orientation to display the image. 0 - 3 -> 0 - 270 degrees
| ``delay`` is the time in milliseconds that the image will be displayed 0->65535
| Displays the pre-programmed ``animation_num`` on the LED Display cube

::

	Robo.Display1.animate(0, 5, 1, 0)

Custom Animation
################
| custom_animation(``self``, ``animation``, ``repeats``, ``reverse``, ``orientation``, ``frame_rate``)
| 
| ``animation`` is a list of images: 32 element arrays of 8-bit numbers representing the 16 rows of the desired images. 
| ``repeats`` number of times to repeat the animation
| ``reverse`` 0 or 1 to indicate if the animation should play forwards then backwards or just forwards
| ``orientation`` is the desired orientation to display the image. 0 - 3 -> 0 - 270 degrees
| ``frame_rate`` is the time in milliseconds that the image frame will be displayed 0->65535
| Displays the given ``animation`` on the LED Display cube

::

	Robo_Logo = [0xff, 0xfc, 0xff, 0xfe, 0xef, 0xf7, 0xc7, 0xe3, 0xc4, 0x23, 0xee, 0x77, 0xff, 0xfe, 0xff, 0xfc, 0x00, 0x00, 0xfe, 0x3c, 0xfe, 0x7e, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0xff, 0xfe, 0x7e, 0xfe, 0x3c ]
	One = [0x07, 0xc0, 0x0f, 0xc0, 0x1d, 0xc0, 0x19, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x01, 0xc0, 0x1f, 0xfc, 0x1f, 0xfc, 0x1f, 0xfc]
	Two = [0x07, 0x80, 0x0f, 0xc0, 0x1c, 0xe0, 0x18, 0x70, 0x18, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x70, 0x00, 0x70, 0x00, 0xf0, 0x03, 0xc0, 0x07, 0xc0, 0x0f, 0xfc, 0x0f, 0xfc]
	Three = [0x0f, 0xfe, 0x0f, 0xfe, 0x0f, 0x1e, 0x0e, 0x0e, 0x00, 0x0e, 0x00, 0x0e, 0x00, 0x0e, 0x00, 0xfe, 0x00, 0xfe, 0x00, 0xfe, 0x00, 0x0e, 0x00, 0x0e, 0x0e, 0x0e, 0x0f, 0x1e, 0x0f, 0xfe, 0x0f, 0xfe]

	animation = [Robo_Logo, One, Two, Three]

	Robo.Display1.custom_animation(animation, 1, 0, 0, 1000)

Reset
#####

| reset(``self``)
| 
| Clears and resets the LED Display cube

::

	Robo.Display1.reset()