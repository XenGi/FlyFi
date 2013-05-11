#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FlyFi - Floppy-Fidelity
=======

Created to fulfill all your floppy music needs.

Created on Mon 11. May. 2013 03:43:42+0100
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
from thread import start_new_thread
import time

import midi

class MidiFileIn(object):
    def __init__(self):
        self.midi_file = None
        self.seconds_per_tick = None
        
        #debug
        pygame.midi.init()
        
    def _worker_thread(self):
        print "starting thread..."
        
        mout = pygame.midi.Output(pygame.midi.get_default_output_id())
       
        track_1 = self.midi_file[1]
        track_1.reverse()
     
        event = track_1.pop()
    
        while len(track_1):
            chord_list1 = []
            chord_complete = False
            first_note = True        
    
            while not chord_complete:            
                if first_note or event.tick == 0:
                    chord_list1.append(event)
                    
                    if len(track_1):
                        event = track_1.pop()
                    else:
                        chord_complete
                    
                    first_note = False
                else:     
                    chord_complete = True
 
 
            for note in chord_list1:
                if note.name == "Note On":
                    mout.note_on(note.pitch, note.velocity, note.channel)
                    print "%s:, pitch: %d, Volume: %d, tick: %d" % (note.name, note.pitch, note.velocity, note.tick)
                elif note.name == "Note Off":
                    mout.note_off(note.pitch, note.velocity, note.channel)
                    print "%s:, pitch: %d, Volume: %d, tick: %d" % (note.name, note.pitch, note.velocity, note.tick)
                else:
                    print "unknown event (%s)" % note.name
                
            time.sleep( self.seconds_per_tick * event.tick)
        
        print "closing thread..."        
                #self._poll_event()
        
    def _set_ms_per_tick_from_bpm(self, bpm):
        ticks_per_beat = self.midi_file.resolution
        beats_per_minute = bpm 
        self.seconds_per_tick = 1/((ticks_per_beat * beats_per_minute) / 60.0)
        
    def stop_midi_polling(self):
        pass
        
    def open_midi_file(self, path_to_file):
        self.midi_file = midi.read_midifile(path_to_file)
        self._set_ms_per_tick_from_bpm(120) # TODO: read temppo from file!
        
        print "opened midi file: %s" % path_to_file
        
        
        
    def get_num_tracks(self):
        return len(self.midi_file) - 1
    
    # starts reading the events of the midi file and
    # calls the specified callback with correct timings
    def play(self):
        #start_new_thread(self._worker_thread, ())
        
        self._worker_thread()
    
        
                    

def main():    
    mfin = MidiFileIn()
    mfin.open_midi_file("mary.mid")
    mfin.play()
    
    
   


if __name__ == "__main__":
    main()
