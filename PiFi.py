#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FlyFi - Floppy-Fidelity
=======

Created to fulfill all your floppy music needs.

Created on Tue 30-05-2013_01:57:42+0100
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

__author__ = "Ricardo (XeN) Band <xen@c-base.org>, \
              Stephan (coon) Thiele <coon@c-base.org>"
__copyright__ = "Copyright (C) 2013 Ricardo Band, Stephan Thiele"
__revision__ = "$Id$"
__version__ = "0.1"

import sys
import pygame
import random
import pygame.midi
from Menu.menu import *
from Menu.image import *
from MidiFileIn import MidiFileIn
from FloppyOut import FloppyOut

    
    
class PiFiHelper(object):
    def __init__(self):
        self.fout = FloppyOut()
        self.midi_fin = MidiFileIn(self.cb_midi_event_list)
        pygame.midi.init() #debug
        self.mout = pygame.midi.Output(pygame.midi.get_default_output_id()) # debug
    
    
    def connect_to_serial_ports(self, serial_port):
        for i in range(0, 16):
            active = True
            floppy_channel = i + 1
            port_str = serial_port
            self.fout.configure_midi_channel(i, active, floppy_channel, port_str)

        self.fout.connect_to_serial_ports()
        
        
    def cb_midi_event_list(self, event_list):
        # parsing the events
        # ==================
        # only note on, note off and pitch wheel range are
        # important for us, so the other midi events are just ignored.
        
        # status, data1, data2, tick
        
        event_str = None
        channel = None
        
        for event in event_list:
            status = event.statusmsg
            tick = event.tick
            
            # also note off events will be stored here. They will just get a frequency of 0.
            note_on_list = [] # [ [channel, tone], [channel, tone] ... ]
        
            if event.name == "Note Off":
                status += event.channel # due to buggy python-midi lib
            
                channel = status - 0x80 + 1
                midi_note = event.data[0]
                velocity = event.data[1]
                
                event_str = "Chan %s Note off" % channel
                
                note_on_list.append([channel, 0])
                self.mout.note_off(midi_note, velocity, channel - 1) # only for debugging. remove later!!!
                
            elif event.name == "Note On":
                status += event.channel # due to buggy python-midi lib
                
                channel = status - 0x90 + 1
                midi_note = event.data[0]
                velocity = event.data[1]
                
                event_str = "Chan %s Note on" % channel
                self.mout.note_on(midi_note, velocity, channel - 1) # only for debugging. remove later!!!      
                
                if velocity > 0:
                    note_on_list.append([channel, midi_note])
                else:
                    note_on_list.append([channel, 0]) # note off
                    self.fout.stop_note(channel) # a volume of 0 is the same as note off
                 
            elif event.name == "Set Tempo":
                self.midi_fin.set_bpm(event.bpm)
              
            elif event.name == "Program Change": # Chan Program change (change instrument)
                if self.mout is not None:
                    self.mout.set_instrument(event.data[0], event.channel)

    #            elif status >= 0xE0 and status <= 0xEF: # pitch bend (TODO: don't ignore!)
    #                channel = status - 0xE0 + 1
    #                velocity = event.data[1]
    #                pitch_value = 128 * velocity
    #                event_str = "Chan %s pitch bend with value %s and" % (channel, pitch_value)     
            else:
                event_str = "unknown event (0x%0X)" % (status)
                
            if event_str != None:
                if event.name == "Note On" or event.name == "Note Off":
                    midi_note = event.data[0]
                    velocity = event.data[1]
                
                   # print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, tick)
        
                self.fout.play_notes(note_on_list)
    

def main():
    serial_port = sys.argv[1]
    
    pifi = PiFiHelper()
    pifi.connect_to_serial_ports(serial_port)
    
    
    eventnr_filename_dict = {}
    # Uncomment this to center the window on the computer screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Uncomment this to position the screen x_ and y_ pixels from the top left
    # corner of the monitor/screen
    #x_ = 560
    #y_ = 100
    #if os.name != 'mac':
    #   os.environ['SDL_VIDEO_WINDOW_POS'] = str(x_) + "," + str(y_)

    # Initialize Pygame
    pygame.init()
    
    # Create a window of 800x600 pixels
    screen = pygame.display.set_mode((800, 600))

    # Set the window caption
    pygame.display.set_caption("FlyFi Menu - (c) coon")

    # Load some images to use for sample buttons
    image1  = load_image('1.png', 'images')
    image2  = load_image('2.png', 'images')
    image3  = load_image('3.png', 'images')
    image4  = load_image('4.png', 'images')
    image5  = load_image('5.png', 'images')
    bkg = load_image('bkg.jpg', 'images')

    # Set a background image - this is to show that the buttons will be
    # transparent around the text/image so it is safe to use this menu over a
    # picture - just make sure that the picture it will be written to is on the
    # screen that you pass into as the background for the menu when it is
    # created.  We must draw everything we want onto the surface before creating
    # the button if we want the background to be applied correctly.
    screen.blit(bkg, (0, 0))
    pygame.display.flip()

    # Create 3 diffrent menus.  One of them is only text, another one is only
    # images, and a third is -gasp- a mix of images and text buttons!  To
    # understand the input factors, see the menu file
    menu0 = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                  [('Play Midi', 100, None),
                  ('Exit', 9, None)])

    eventnr_filename_dict = {}
   
    entries = []
    entries.append(('Previous Menu', 0, None))
   
    file_entries = [(filename, state_index + 101, None) for state_index, filename in enumerate([f for f in os.listdir("./music/.") if f.endswith(".mid")])]
    entries.extend(file_entries)
   
    entries.append(('Exit', 9, None))
   
    for i, entry in enumerate(file_entries):
        eventnr_filename_dict[i + 101] = entry[0]
                 
    menu_play_midi = cMenu(50, 50, 20, 5, 'vertical', 100, screen, entries)
                 
    menu1 = cMenu(20, 400, 20, 5, 'horizontal', 4, screen,
                [('Previous Menu',  0, None),
                 ('Midi 1.mid',     2, None),
                 ('Menu 0',         0, None),
                 ('Menu 2 (Next)',  2, None),
                 ('Menu 3',         3, None),
                 ('Next Menu',      2, None),
                 ('Next Menu',      2, None),
                 ('Exit',           9, None)])

    menu2 = cMenu(0, 0, 5, 5, 'horizontal', 7, screen,
                [('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2),
                 ('Next Menu', 3, image3),
                 ('Next Menu', 3, image4),
                 ('Next Menu', 3, image5),
                 ('Next Menu', 3, image1),
                 ('Next Menu', 3, image2)])

    menu3 = cMenu(25, 15, 20, 5, 'vertical', 7, screen,
                [('Prev Menu',          2, None),
                 ('Add',                4, None),
                 ('Center',             5, None),
                 ('Set (0, 0)',         6, None),
                 ('Rand Colors',        7, None),
                 ('Rand Config',        8, None),
                 ('Next Menu',          0, None),
                 ('Image',              0, image1),
                 ('Image',              0, image2),
                 ('Image',              0, image3),
                 ('Image',              0, image4),
                 ('Image',              0, image5),
                 ('Next Menu',          1, None),
                 ('Exit',               9, None)])

    # Center menu2 at the center of the draw_surface (the entire screen here)
    menu2.set_center(True, True)

    # Create the state variables (make them different so that the user event is
    # triggered at the start of the "while 1" loop so that the initial display
    # does not wait for user input)
    state = 0
    prev_state = 1

    # rect_list is the list of pygame.Rect's that will tell pygame where to
    # update the screen (there is no point in updating the entire screen if only
    # a small portion of it changed!)
    rect_list = []

    # Ignore mouse motion (greatly reduces resources when not needed)
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    # seen the random number generator (used here for choosing random colors
    # in one of the menu when that button is selected)
    random.seed()

    
    
    
    # The main while loop
    while 1:
        pifi.midi_fin.tick()
        
        # Check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

            if state in [0, 1, 2, 3]:
                # Reset the screen before going to the next menu.  Also, put a
                # caption at the bottom to tell the user what is going one
                screen.blit(bkg, (0, 0))
                screen.blit(TEXT[state][0], (15, 530))
                screen.blit(TEXT[state][1], (15, 550))
                screen.blit(TEXT[state][2], (15, 570))
                pygame.display.flip()

        # Get the next event
        e = pygame.event.poll()
        
        
        # Update the menu, based on which "state" we are in - When using the menu
        # in a more complex program, definitely make the states global variables
        # so that you can refer to them by a name
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                rect_list, state = menu0.update(e, state)
            elif state == 1:
                rect_list, state = menu1.update(e, state)
            elif state == 2:
                rect_list, state = menu2.update(e, state)
            elif state == 3:
                rect_list, state = menu3.update(e, state)
            elif state == 4:
                menu3.add_buttons([('A-Nothing!', 3, None),
                                   ('A-Menu 0',   0, None),
                                   ('A-Exit',     9, None)])
                state = 3
            elif state == 5:
                menu3.set_center(True, True)
                state = 3
            elif state == 6:
                menu3.set_center(False, False)
                menu3.set_position(0, 0)
                state = 3
            elif state == 7:
                RGB_available_colors = xrange(0,255)

                new_color = (random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors))
                menu3.set_unselected_color(new_color)
                print 'New Unselected Color = ', new_color

                new_color = (random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors))
                menu3.set_selected_color(new_color)
                print 'New Selected Color = ', new_color

                new_color = (random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors),
                            random.choice(RGB_available_colors))
                menu3.set_image_highlight_color(new_color)
                print 'New Image Highlight Color = ', new_color

                print ' '
                state = 3
            elif state == 8:
                new_thickness = random.choice((1, 2, 3, 4, 5, 6, 7, 8))
                menu3.set_image_highlight_thickness(new_thickness)
                print 'New Image Highlight Thickness = ', new_thickness

                new_h_pad = random.choice(xrange(0, 20))
                new_v_pad = random.choice(xrange(0, 20))
                menu3.set_padding(new_h_pad, new_v_pad)
                print 'New Horizontal Padding = ', new_h_pad
                print 'New Vertical Padding = ', new_v_pad

                new_orientation = random.choice(('vertical', 'horizontal'))
                menu3.set_orientation(new_orientation)
                if new_orientation == 'vertical':
                    new_change_number = random.choice(xrange(5, 12))
                elif new_orientation == 'horizontal':
                    new_change_number = random.choice(xrange(2, 5))
                    print 'New Orientation = ', new_orientation

                menu3.set_change_number(new_change_number)
                print 'New Change Number = ', new_change_number

                new_v_alignment = random.choice(('top', 'center', 'bottom'))
                new_h_alignment = random.choice(('left', 'center', 'right'))
                menu3.set_alignment(new_v_alignment, new_h_alignment)
                print 'New Vertical Alignment = ',   new_v_alignment
                print 'New Horizontal Alignment = ', new_h_alignment

                print ' '
                state = 3
            
            elif state == 100:
                rect_list, state = menu_play_midi.update(e, state)
            
            elif state > 100:
                # play midi here!
                
                # TODO: stop midi playback
                
                
                filename = eventnr_filename_dict[state]
                print "Filename: %s" % filename
                
                midi_file = "./music/%s" % filename
                pifi.midi_fin.open_midi_file(midi_file)
                pifi.midi_fin.play()
            
                state = 100 # back to file select menu
            
            else:
                pygame.quit()
                sys.exit()

        # Quit if the user presses the exit button
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Update the screen
        pygame.display.update(rect_list)


if __name__ == "__main__":
    main()
