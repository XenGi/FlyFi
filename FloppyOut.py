#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FlyFi - Floppy-Fidelity
=======

Created to fulfill all your floppy music needs.

Created on Tue 06-01-2013_05:17:42+0100
@author: Ricardo (XeN) Band <xen@c-base.org>,
         Stephan (coon) Thiele <coon@c-base.org>

    This file is part of FlyFi.

    FlyFi is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    FlyFi is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with FlyFi.  If not, see <http://www.gnu.org/licenses/>.

    Diese Datei ist Teil von FlyFi.

    FlyFi ist Freie Software: Sie können es unter den Bedingungen
    der GNU General Public License, wie von der Free Software Foundation,
    Version 3 der Lizenz oder (nach Ihrer Option) jeder späteren
    veröffentlichten Version, weiterverbreiten und/oder modifizieren.

    FlyFi wird in der Hoffnung, dass es nützlich sein wird, aber
    OHNE JEDE GEWÄHELEISTUNG, bereitgestellt; sogar ohne die implizite
    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
    Siehe die GNU General Public License für weitere Details.

    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
"""

__author__ = "Ricardo (XeN) Band <xen@c-base.org>, \
              Stephan (coon) Thiele <coon@c-base.org>"
__copyright__ = "Copyright (C) 2013 Ricardo Band, Stephan Thiele"
__revision__ = "$Id$"
__version__ = "0.1"


import serial
import struct


class FloppyOut():
    def __init__(self):
        self.MAX_CHANNELS = 16
        self.ARDUINO_RESOLUTION = 40 # the timer of the arduino fires every 40 miliseconds
        self._serial_ports = [] # a list of all available serial ports
        self._channel_ports = [] # the serial ports which are mapped to each channel


#       self._channel_ports = [serial.Serial() for i in range(self.MAX_CHANNELS)] # the serial ports which are mapped to each channel
#        for i in range(self.MAX_CHANNELS):

# TODO: Verschieben in onConnect()
#            self._channel_ports[i].baudrate = 9600
#            self._channel_ports[i].parity = serial.PARITY_NONE
#            self._channel_ports[i].stopbits = serial.STOPBITS_ONE
#            self._channel_ports[i].bytesize = serial.EIGHTBITS


    def set_serial_port_list(serial_port_list):
        _serial_ports = serial_port_list


    def connect_serial_port(port_id):
        self._serial_ports[port_id].open()

    def disconnect_serial_port(port_id):
        self._serial_ports[port_id].close()

    
    def map_serial_port_to_channel(self, channel, serial_port_id):
	self._channel_ports[channel - 1].port = self._serial_ports[serial_port_id]



    def play_tone(self, channel, frequency): 
        if channel < 1 or channel > self.MAX_CHANNELS:
            raise Exception("channel '%d' out of range. it has to be between 1 - %d" % (channel, self.MAX_CHANNELS) )

        if frequency != 0:
            half_period = (1000000.0 / frequency) / (2.0 * self.ARDUINO_RESOLUTION) # period in microseconds
        else:
            half_period = 0

        # build 3 byte data packet for floppy
        # 1: physical_pin (see microcontroller code for further information)
        # 2: half_period

        physical_pin = channel * 2
        data = struct.pack('B', physical_pin) + struct.pack('>H', int(half_period))
        self._channel_ports[channel - 1].write(data)


def main():
    fl = FloppyOut()
    fl.map_serial_port_to_channel(1, "/dev/ttyUSB0")
    fl.map_serial_port_to_channel(2, "/dev/ttyUSB0")
    fl.connect_serial_ports()

    fl.play_tone(1, 0)
    fl.play_tone(2, 0)


if __name__ == "__main__":
    main()
