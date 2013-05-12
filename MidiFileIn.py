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
    def __init__(self, midi_event_callback):
        self.midi_file = None
        self.seconds_per_tick = None
        self.midi_event_callback = midi_event_callback
            
            
    # (depricated) dirty sleep solution which results in a high cpu load. (but is very accurate)            
    def _dirty_sleep(self, seconds):
        start = int(time.clock() * 1000 * 1000)
        
        micros = 0
        while True:
            micros = int(time.clock() * 1000 * 1000)
            if (micros - start) >= seconds * 1000 * 1000:
                break
        
    def _midi_tick(self):
        end_of_track = True
        event_list = [] # event list of current tick
                   
        for track_index, track in enumerate(self.midi_file):
            while len(track) and track[-1].tick == 0:
                event_list.append(track.pop())

            # since the python-midi library seems not to be consistent (sometimes the channels of the events are missing), 
            # the callback will only be called on Note On, Note Off (and later pitch bend) events.
            for event in event_list:  
                if self.midi_event_callback is not None:
                    if event.name == "Note On" or event.name == "Note Off":
                        self.midi_event_callback(event.statusmsg + event.channel, event.data[0], event.data[1], event.tick)
                

            if len(track):
                track[-1].tick -= 1
                end_of_track = False
         
        return end_of_track
        
        
    def _worker_thread(self): 
        end_of_track = False    
    
        # so .pop() can be used    
        for track in self.midi_file:
            track.reverse()
                   
        # This is the mainloop for playing the midi-file.
        # Previously this dirty sleep function has been layed out to a function
        # and was called at the end of the loop.
        # This resulted in slowdowns of the song on very complex midi files like the imperial march, where 
        # the function already needs much of the midi-tick time while generating the midi-event lists.
        #
        # In this new way, only the rest of the time (or no if late) has to be wait at the end of the loop, 
        # so slowdowns of a song will be minimized. 
        
        while not end_of_track: # every loop is one midi tick
            start = int(time.clock() * 1000 * 1000)
        
            end_of_track = self._midi_tick()
            
            micros = 0
            while (micros - start) < self.seconds_per_tick * 1000 * 1000:
                micros = int(time.clock() * 1000 * 1000)
            
            
        
    def _set_ms_per_tick_from_bpm(self, bpm):
        ticks_per_beat = self.midi_file.resolution
        beats_per_minute = bpm 
        self.seconds_per_tick = 1.0/((ticks_per_beat * beats_per_minute) / 60.0)
        
    def stop_midi_polling(self):
        pass
        
    def open_midi_file(self, path_to_file):
        self.midi_file = midi.read_midifile(path_to_file)
        self._set_ms_per_tick_from_bpm(200) # TODO: read temppo from file!
        
        print "opened midi file: %s" % path_to_file
        
        
        
    def get_num_tracks(self):
        return len(self.midi_file) - 1
    
    # starts reading the events of the midi file and
    # calls the specified callback with correct timings
    def play(self):
        #start_new_thread(self._worker_thread, ())
        
        print "start playing..."
        self._worker_thread()
        print "finished."
    
        
                    

def main():    

    pygame.midi.init() #debug
    mout = pygame.midi.Output(pygame.midi.get_default_output_id())


    def cb_midi_event(status, data1, data2, tick):
        # parsing the events
        # ==================
        # only note on, note off and pitch wheel range are
        # important for us, so the other midi events are just ignored.
        event_str = None
        
        channel = None
        
        if status >= 0x80 and status <= 0x8F: # Note Off
            channel = status - 0x80 + 1
            midi_note = data1;
            velocity = data2
            
            event_str = "Chan %s Note off" % channel
            
            #self.fout.stop_note(channel)
            mout.note_off(midi_note, velocity, channel) # only for debugging. remove later!!!
        elif status >= 0x90 and status <= 0x9F: # Note On
            channel = status - 0x90 + 1
            midi_note = data1;
            velocity = data2
            
            event_str = "Chan %s Note on" % channel  

            if velocity > 0:
                mout.note_on(midi_note, velocity, channel) # only for debugging. remove later!!!
                #self.fout.play_note(channel, midi_note)      
            else:
                mout.note_on(midi_note, velocity, channel) # only for debugging. remove later!!!
                #self.fout.stop_note(channel) # a volume of 0 is the same as note off
             
        elif status >= 0xA0 and status <= 0xAF: # Polyphonic Aftertouch (ignore)
            return
        elif status >= 0xB0 and status <= 0xBF: # Chan Control mode change (ignore)
            return
        elif status >= 0xC0 and status <= 0xCF: # Chan Program change (ignore)
            mout.set_instrument(event.data, event.channel)
        elif status >= 0xD0 and status <= 0xDF: # Channel Aftertouch (ignore)
            return
        elif status >= 0xE0 and status <= 0xEF: # pitch bend (TODO: don't ignore!)
            channel = status - 0xE0 + 1
            pitch_value = 128 * velocity
            event_str = "Chan %s pitch bend with value %s and" % (channel, pitch_value)     
        else:
            event_str = "unknown event (0x%0X)" % (status)
            print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, tick)
            return
            
        if event_str != None:    
            #pass
            print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, tick)





    mfin = MidiFileIn(cb_midi_event)
    mfin.open_midi_file("fish2.mid")
    mfin.play()
    
    
   


if __name__ == "__main__":
    main()
