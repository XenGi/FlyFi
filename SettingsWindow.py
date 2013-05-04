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
#import serial.tools.list_ports
import serial
import glob
import ConfigParser
import os, platform
import FloppyOut

#self.settingswindow.cb_update_serial_ports()


class SettingsWindow(QtGui.QMainWindow):
    def __init__(self, floppy_out):
        super(SettingsWindow, self).__init__()

        self.fout = floppy_out
        self.config = ConfigParser.SafeConfigParser()
        #if os.path.isfile(os.path.expanduser('~/.flyfirc')):
        #    self.config.read(os.path.expanduser('~/.flyfirc'))
        #elif os.path.isfile('/etc/flyfirc'):
        #    self.config.read('/etc/flyfirc')
        #    fp = open(os.path.expanduser('~/.flyfirc'), 'w')
        #    self.config.write(fp)
        #    fp.close()
        #else:
            # only needed in dev env
        self.config.read(os.path.join(os.getcwd(), 'flyfirc'))
        fp = open(os.path.expanduser('~/.flyfirc'), 'w')
        self.config.write(fp)
        fp.close()

        self.init_ui()
        
    def init_ui(self):
        self.resize(650, 700)
        self.setWindowTitle('FlyFi - Settings')
        self.setWindowIcon(QtGui.QIcon('images/settings.png'))
        self.center()

        centralwidget = QtGui.QTabWidget()
        tab_channel = QtGui.QWidget()
        tab_serial_ports = QtGui.QWidget()

        # channel tab
        channel_vbox = QtGui.QVBoxLayout()
        self.channel_table = QtGui.QTableWidget(16, 3)
        self.channel_table.cellClicked.connect(self.cell_clicked)
        self.channel_table.setHorizontalHeaderLabels(['Active', 'Floppychannel', 'Serial Port'])


        for row in range(0, 16):
            self.channel_table.setCellWidget(row, 0, QtGui.QCheckBox())
            self.channel_table.setCellWidget(row, 1, QtGui.QComboBox())
            self.channel_table.setCellWidget(row, 2, QtGui.QComboBox())

            self.channel_table.cellWidget(row, 0).setCheckState(
                                   QtCore.Qt.CheckState.Checked if self.fout.midi_channels[row].active else
                                   QtCore.Qt.CheckState.Unchecked )
            self.channel_table.cellWidget(row, 1).addItems( [ str(s) for s in range(1, 16 + 1)] )
            self.channel_table.cellWidget(row, 1).setCurrentIndex(self.fout.midi_channels[row].floppy_channel - 1)
           
                             
        self.pb_connect_to_serial_ports = QtGui.QPushButton('Connect to selected serial ports')
        self.pb_connect_to_serial_ports.clicked.connect(self.cb_connect_to_serial_ports)

        self.pb_update_serial_ports = QtGui.QPushButton('Refresh available serial ports')
        self.pb_update_serial_ports.clicked.connect(self.cb_update_serial_ports)
        
        lb_note = QtGui.QLabel("Note: Serial ports which are already in use by another program won't be dislayed!")      
        channel_vbox.addWidget(lb_note)
        
        set_all_ports_hbox = QtGui.QHBoxLayout()
        lb_set_all_ports_to = QtGui.QLabel('Set all floppies to serial port:')
        self.cbx_set_all_ports = QtGui.QComboBox()
        pb_set_all_ports = QtGui.QPushButton('ok')
        set_all_ports_hbox.addWidget(lb_set_all_ports_to)
        set_all_ports_hbox.addWidget(self.cbx_set_all_ports)        
        set_all_ports_hbox.addWidget(pb_set_all_ports)
        pb_set_all_ports.clicked.connect(self.cb_set_all_serial_ports)


        channel_vbox.addLayout(set_all_ports_hbox)
        channel_vbox.addWidget(self.channel_table)
        channel_vbox.addWidget(self.pb_connect_to_serial_ports)
        channel_vbox.addWidget(self.pb_update_serial_ports)

        tab_channel.setLayout(channel_vbox)

                


        # benchmark tab
	benchmark_vbox = QtGui.QVBoxLayout()
        lb_note = QtGui.QLabel('Todo: Floppies will be tested here!')
        benchmark_vbox.addWidget(lb_note)

#        self.serial_ports_table = QtGui.QTableWidget(0, 2)
#        self.serial_ports_table.setHorizontalHeaderLabels(['Serial Port', 'Connection'])
#        self.serial_ports_table.cellClicked.connect(self.cell_clicked)                
#        tab_serial_ports.setLayout(serial_ports_vbox)


        # create tabs
        centralwidget.addTab(tab_channel, "MIDI Channels")
        centralwidget.addTab(tab_serial_ports, "Benchmark")
 
        self.setCentralWidget(centralwidget)
        

    def center(self):
        frame_geo = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(desktop_center)
        self.move(frame_geo.topLeft())

    def cell_clicked(self, row, col):
        if col == 0:
            self.channel_table.cellWidget(row, 0).toggle()

   
    # A function that tries to list serial ports on most common platforms
    def list_serial_ports(self):
        system_name = platform.system()
        if system_name == "Windows": # TODO: dont use system()
            # Scan for available ports.
            available = []
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    available.append(s.portstr)
                    s.close()
                except serial.SerialException:
                    pass
            return available
        elif system_name == "Darwin":
            # Mac
            return glob.glob('/dev/cu*')
        else:
            # Assume Linux or something else
            return glob.glob('/dev/ttyUSB*')

    def cb_update_serial_ports(self):
        ports = self.list_serial_ports()
       # port_count = len(ports)

        serialports = []
        for port in ports:
            serialports.append(port)

        items = None
        if serialports != []:
            items = serialports
            self.pb_connect_to_serial_ports.setEnabled(True) 
        else:
            items = [ "<no serial ports available>" ]
            self.pb_connect_to_serial_ports.setEnabled(False) 
  
        for row in range(0, 16):
            self.cbx_set_all_ports.clear()
            self.channel_table.cellWidget(row, 2).clear()
            self.cbx_set_all_ports.addItems( items )
            self.channel_table.cellWidget(row, 2).addItems( items )

            
        self.channel_table.resizeColumnsToContents()
 


    def cb_connect_to_serial_ports(self):
        for row in range(0, 16):
            active = self.channel_table.cellWidget(row, 0).isChecked()
            floppy_channel = int(self.channel_table.cellWidget(row, 1).currentText())
            port_str = self.channel_table.cellWidget(row, 2).currentText()
            self.fout.configure_midi_channel(row, active, floppy_channel, port_str)

        self.fout.connect_to_serial_ports()                

        # TODO: Gray out stuff


    def save_config(self):
        self.config.add_section('Channel1')
        self.config.set('Channel1', 'enabled', str(self.channel_table.cellWidget(0, 0).Value))
        self.config.set('Channel1', 'serialport', str(self.channel_table.cellWidget(0, 1).Value))
        self.config.add_section('Channel2')
        self.config.set('Channel2', 'enabled', str(self.channel_table.cellWidget(1, 0).Value))
        self.config.set('Channel2', 'serialport', str(self.channel_table.cellWidget(1, 1).Value))

        with open('~/.flyfirc', 'wb') as configfile:
            self.config.write(configfile)

    def load_config(self):
        ports = serial.tools.list_ports.comports()
        serialports = []
        for port in ports:
            if port[2] != 'n/a':
                serialports.append(port[0])
        for row in range(0, 16):
            # load channel active
            if self.config.getboolean('Channel'+ str(row + 1), 'enabled'):
                self.channel_table.cellWidget(row, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.channel_table.cellWidget(row, 0).setCheckState(QtCore.Qt.Unchecked)
            # load serial ports
            if self.config.get('Channel' + str(row + 1), 'serialport') in serialports:
                    index = self.channel_table.cellWidget(row, 1).findData(self.config.get('Channel' + str(row + 1), 'serialport'))
                    if not index == -1:
                        self.channel_table.cellWidget(row, 1).setCurrentIndex(index)


    # ui events

    def connect_pressed(self, button_id):
        sender_button = self.sender().button(button_id)       
    
           
        if sender_button.text() == "Connect":
            self.fout.connect_serial_port(button_id)
            sender_button.setText("Disconnect")
        else:
            self.fout.disconnect_serial_port(button_id)
            sender_button.setText("Connect")


    def cb_set_all_serial_ports(self):
        for row in range(0, 16): 
            self.channel_table.cellWidget(row, 2).setCurrentIndex(self.cbx_set_all_ports.currentIndex())



    def channel_mapping_changed(self, combobox_id):
        pass




     
