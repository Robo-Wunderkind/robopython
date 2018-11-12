=============
BLED112 Class
=============

Create BLED112 Instance::

	BLE = BLED112(com_port=None)
	The Robo Class initiates its own instance of BLED112 when initialized.

start()::

	Activates the connected BLED112 USB Dongle

stop()::
	
	Turns off BLED112 USB Dongle

	
=============
BLED112 Class
=============

Create BLED112 Instance

::

	BLE = BLED112(com_port=None)
	
Connect to Device
#################

| connect_ble(``self``, ``name``)
| 
| Connects to the BLE device with the name passed into the function if it exists

::

	BLE.connect_ble("Robo")

Scan
####

| scan(``self``)
| 
| Scans for nearby BLE devices and returns a list of dictionaries containing BLE device data

::

	BLE.scan()	
	
Start
#####

| start(``self``)
| 
| Starts the BLE dongle

::

	BLE.start()

Stop
####

| start(``self``)
| 
| Starts the BLE dongle

::

	BLE.start()