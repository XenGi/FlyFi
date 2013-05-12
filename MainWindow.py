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

from PySide import QtGui, QtCore
from SettingsWindow import SettingsWindow
from MidiIn import MidiIn
from FloppyOut import FloppyOut


class MainWindow(QtGui.QMainWindow):
    """
    The mainwindow containing options to fine tune things
    and start everything up.
    """
    
    def cb_midi_event(self, status, midi_note, velocity, midi_timestamp):
        # parsing the events
        # ==================
        # only note on, note off and pitch wheel range are
        # important for us, so the other midi events are just ignored.
        event_str = None
        
        channel = None
        
        if status >= 0x80 and status <= 0x8F: # Note Off
            channel = status - 0x80 + 1
            event_str = "Chan %s Note off" % channel
            
            self.fout.stop_note(channel)
        elif status >= 0x90 and status <= 0x9F: # Note On
            channel = status - 0x90 + 1
            event_str = "Chan %s Note on" % channel  
      
            if velocity > 0:
                self.fout.play_note(channel, midi_note)      
            else:
                self.fout.stop_note(channel) # a volume of 0 is the same as note off
             
        elif status >= 0xA0 and status <= 0xAF: # Polyphonic Aftertouch (ignore)
            return
        elif status >= 0xB0 and status <= 0xBF: # Chan Control mode change (ignore)
            return
        elif status >= 0xC0 and status <= 0xCF: # Chan Program change (ignore)
            return
        elif status >= 0xD0 and status <= 0xDF: # Channel Aftertouch (ignore)
            return
        elif status >= 0xE0 and status <= 0xEF: # pitch bend (TODO: don't ignore!)
            channel = status - 0xE0 + 1
            pitch_value = 128 * velocity
            event_str = "Chan %s pitch bend with value %s and" % (channel, pitch_value)     
        else:
            event_str = "unknown event (0x%0X)" % (status)
            print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, midi_timestamp)
            return
            
        if event_str != None:    
            pass
            #print "%s with note %s and velocity %s @ %s" % (event_str, midi_note, velocity, midi_timestamp)
        
        
    
    def __init__(self):
        """
        generate other windows, floppy output control and create the gui
        """
        super(MainWindow, self).__init__()

        self.midi_in = MidiIn(self.cb_midi_event)
        self.fout = FloppyOut()
        self.settingswindow = SettingsWindow(self.midi_in, self.fout)
         
        self.init_ui()
        
        #test
        #self.midi_in.start_midi_polling()


    def setFloatNum(self, float_num):
        self.lab_freq.setText( "%.2f" % (float_num / 100.0) )


    def init_ui(self):
        """
        create the gui and connect actions
        """
        self.resize(480, 320)
        self.setWindowTitle('FlyFi - Floppy-Fidelity')
        self.setWindowIcon(QtGui.QIcon('images/flyfi-logo.png'))
        self.center()

        self.statusBar().showMessage('Ready')

        act_exit = QtGui.QAction(QtGui.QIcon('images/exit.png'), '&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        act_settings = QtGui.QAction(QtGui.QIcon('images/settings.png'),
                                     '&Settings', self)
        act_settings.setShortcut('Ctrl+S')
        act_settings.setStatusTip('Configure FlyFi')
        act_settings.triggered.connect(self.cb_open_settings_window)


        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(act_settings)
        file_menu.addAction(act_exit)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(act_settings)
        toolbar.addAction(act_exit)


    def center(self):
        """
        center the window on the screen
        """
        frame_geo = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(desktop_center)
        self.move(frame_geo.topLeft())

    def pb_play_pressed(self):
        """
        send the current settings to floppy out and play the given tone
        """
        self.fout.play_tone(self.spb_channel.value(), float(self.lab_freq.text())) # todo: split presentation layer from datamodel(?)

    def pb_stop_pressed(self):
        """
        stop playing the current tone on the floppy
        """
        self.fout.play_tone(self.spb_channel.value(), 0) # playing a tone with 0hz will stop the floppy motor

    def cb_open_settings_window(self):
        self.settingswindow.show()
        self.settingswindow.cb_update_serial_ports()
        
