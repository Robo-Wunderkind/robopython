=======
BLED112
=======


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

| stop(``self``)
| 
| Stops the BLE dongle

::

	BLE.stop()
