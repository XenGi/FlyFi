# -*- coding: utf-8 -*-
"""
FlyFi - Floppy-Fidelity

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

    FlyFi is using tango icons: <http://tango.freedesktop.org/>.
"""

from MidiFileIn import MidiFileIn
from FloppyOut import FloppyOut
import pygame.midi
import sys



def midi_event(self, status, data1, data2, tick):
    # parsing the events
    # ==================
    # only note on, note off and pitch wheel range are
    # important for us, so the other midi events are just ignored.
    event_str = None
    channel = None
    
    if status >= 0x80 and status <= 0x8F: # Note Off
        channel = status - 0x80 + 1
        midi_note = data1
        velocity = data2
        
        event_str = "Chan %s Note off" % channel
        
        fout.stop_note(channel)
        mout.note_off(midi_note, velocity, channel - 1) # only for debugging. remove later!!!
    elif status >= 0x90 and status <= 0x9F: # Note On
        channel = status - 0x90 + 1
        midi_note = data1
        velocity = data2
        
        event_str = "Chan %s Note on" % channel

        if velocity > 0:
            mout.note_on(midi_note, velocity, channel - 1) # only for debugging. remove later!!!
            fout.play_note(channel, midi_note)      
        else:
            mout.note_on(midi_note, velocity, channel - 1) # only for debugging. remove later!!!
            fout.stop_note(channel) # a volume of 0 is the same as note off
         
    elif status >= 0xA0 and status <= 0xAF: # Polyphonic Aftertouch (ignore)
        return
    elif status >= 0xB0 and status <= 0xBF: # Chan Control mode change (ignore)
        return
    elif status >= 0xC0 and status <= 0xCF: # Chan Program change (ignore)
        return #mout.set_instrument(event.data, event.channel)
    elif status >= 0xD0 and status <= 0xDF: # Channel Aftertouch (ignore)
        return
    elif status >= 0xE0 and status <= 0xEF: # pitch bend (TODO: don't ignore!)
        channel = status - 0xE0 + 1
        velocity = data2
        pitch_value = 128 * velocity
        event_str = "Chan %s pitch bend with value %s and" % (channel, pitch_value)     
    else:
        event_str = "unknown event (0x%0X)" % (status)
        print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, tick)
        return
        
    if event_str != None:    
        pass
        #print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, tick)
    
            
def main():
    fout = FloppyOut()
    midi_fin = MidiFileIn(midi_event, mout)
    
    def connect_to_serial_ports(self, serial_port):
        for i in range(0, 16):
            active = True
            floppy_channel = i
            port_str = serial_port
            fout.configure_midi_channel(i, active, floppy_channel, port_str)

    def playMidiFile(self):
        midi_fin.play()

            
    serial_port = sys.argv[1]
    midi_file = sys.argv[2]

    print "port: %s, midi_file: %s" % (serial_port, midi_file)
   
    connect_to_serial_ports(self, serial_port)     
    midi_fin.open_midi_file(midi_file)
    
    playMidiFile()

if __name__ == "__main__":
    main()
