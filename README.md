# Serial Fwd for dump1090

Dump 1090 is a Mode S decoder specifically designed for RTLSDR devices.

The main features are:

* Robust decoding of weak messages, with mode1090 many users observed
  improved range compared to other popular decoders.
* Network support: TCP30003 stream (MSG5...), Raw packets, HTTP.
* Embedded HTTP server that displays the currently detected aircrafts on
  Google Map.
* Single bit errors correction using the 24 bit CRC.
* Ability to decode DF11, DF17 messages.
* Ability to decode DF formats like DF0, DF4, DF5, DF16, DF20 and DF21
  where the checksum is xored with the ICAO address by brute forcing the
  checksum field using recently seen ICAO addresses.
* Decode raw IQ samples from file (using --ifile command line switch).
* Interactive command-line-interfae mode where aircrafts currently detected
  are shown as a list refreshing as more data arrives.
* CPR coordinates decoding and track calculation from velocity.
* TCP server streaming and recceiving raw data to/from connected clients
  (using --net).

Normal usage
---

Type > python dump1090-serialFwd.py 

Requirements
---

* pyserial

Can be install via > apt install python-serial or pip install pyserial

Arguments
---

* --host		dump1090 IP address default: localhost
* --tcp			TCP port to connect to default: 30003 (SBS-1)
* --port		Serial Port to use default: /dev/serial0
* --baud		Serial Baudrate default: 115200
* --delayed		Delay start in seconds (for Cron use) default: 0

Auto start via Cron
---

I recommend specifying at least 30 seconds of delayed start to allow the raspberrypi to boot up and start network services

Type > crontab -e

Add line >>> 

@reboot	python *PATH_TO_SCRIPT*/dump1090-serialFwd.py --host localhost --tcp 30003 --port /dev/serial0 --baud 115200 --delayed 30
