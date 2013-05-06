#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FlyFi - Floppy-Fidelity
=======

Created to fulfill all your floppy music needs.

Created on Mon 06. May. 2013 18:16:42+0100
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


import pygame
import pygame.midi
from pygame.locals import *

class MidiIn():
    def __init__(self):
        pygame.init()

        pygame.fastevent.init()
        self.event_get = pygame.fastevent.get
        self.event_post = pygame.fastevent.post

        pygame.midi.init()
        input_id = pygame.midi.get_default_input_id()
        self.i = pygame.midi.Input( input_id )
        
    def __del__(self):
        self.i.close()
        pygame.midi.quit()
        pygame.quit()

    def poll_event(self):
        if self.i.poll(): # are there MIDI data?
            # read exactly one midi event from the queue. It is possible 
            # to read more midi events at once but it is alot easier to 
            # handle them when reading them one by one.
            midi_events = self.i.read(1) 
            
            # parse midi events
            status = midi_events[0][0][0]
            note = midi_events[0][0][1]
            velocity = midi_events[0][0][2] # velocity is not possible on one floppy. anyway this value is important for pitch bend
            midi_timestamp = midi_events[0][1]
            
           
            # parsing the events
            # ==================
            # only note on, note off and pitch wheel range are
            # important for us, so the other midi events are just ignored.
            event_str = None
            
            if status >= 0x80 and status <= 0x8F: # Note Off
                chan = status - 0x80
                event_str = "Chan %s Note off" % ( chan + 1)
            elif status >= 0x90 and status <= 0x9F: # Note On
                chan = status - 0x90
                event_str = "Chan %s Note on" % ( chan + 1)  
            elif status >= 0xA0 and status <= 0xAF: # Polyphonic Aftertouch (ignore)
                pass
            elif status >= 0xB0 and status <= 0xBF: # Chan Control mode change (ignore)
                pass
            elif status >= 0xC0 and status <= 0xCF: # Chan Program change (ignore)
                pass
            elif status >= 0xD0 and status <= 0xDF: # Channel Aftertouch (ignore)
                pass
            elif status >= 0xE0 and status <= 0xEF: # pitch bend (TODO: don't ignore!)
                chan = status - 0xE0
                pitch_value = 128 * velocity
                event_str = "Chan %s pitch bend with value %s and" % (chan + 1, pitch_value)     
            else:
                event_str = "unknown event (0x%0X)" % (status)
                
            if event_str != None:    
                print "%s with note %s and velocity %s @ %s" % (event_str, note, velocity, midi_timestamp)
                    

def main():    
    m = MidiIn()
    going = True
    
    while going:
        events = m.event_get()
        for e in events:
            if e.type in [QUIT]:
                going = False
            if e.type in [KEYDOWN]:
                going = False
                
        m.poll_event()
   


if __name__ == "__main__":
    main()
