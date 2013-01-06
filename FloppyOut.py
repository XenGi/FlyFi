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
        self.ser = serial.Serial()
        self.ARDUINO_RESOLUTION = 40 # the timer of the arduino fires every 40 miliseconds

    def init_serial_com(self, com_port):
        self.ser.port = com_port 
        self.ser.baudrate = 9600 
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.open()
    
    def disconnect_serial(self, com_port):
        self.ser.close()
    
    
    def play_tone(self, channel, frequency):
        if frequency != 0:
            half_period = (1000000 / frequency) / (2 * self.ARDUINO_RESOLUTION) # period in microseconds
        else:
            half_period = 0

        # build 3 byte data packet for floppy
        # 1: channel
        # 2: half_period
        
        data = struct.pack('B', channel) + struct.pack('>H', int(half_period))
        self.ser.write(data)


def main():
    fl = FloppyOut()
    #fl.init_serial_com("/dev/ttyUSB3")
    

if __name__ == "__main__":
    main()
