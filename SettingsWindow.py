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
        self.update_serial_ports()

    def init_ui(self):
        self.resize(480, 320)
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

            self.channel_table.cellWidget(row, 2).addItems( [str(s) for s in range(1, 8 + 1)] )
            self.channel_table.cellWidget(row, 2).setCurrentIndex(self.fout.midi_channels[row].serial_port - 1)

            
        pb_update_serial = QtGui.QPushButton('Reload serial ports')
        pb_update_serial.clicked.connect(self.update_serial_ports)

                
        channel_vbox.addWidget(self.channel_table)
        tab_channel.setLayout(channel_vbox)


        # serial ports tab
	serial_ports_vbox = QtGui.QVBoxLayout()
        self.serial_ports_table = QtGui.QTableWidget(0, 2)
        self.serial_ports_table.setHorizontalHeaderLabels(['Serial Port', 'Connection'])
        serial_ports_vbox.addWidget(self.serial_ports_table)

        centralwidget.addTab(tab_channel, "Channels")
        centralwidget.addTab(tab_serial_ports, "Serial Ports")

              
        serial_ports_vbox.addWidget(pb_update_serial)
        self.serial_ports_table.cellClicked.connect(self.cell_clicked)                
        tab_serial_ports.setLayout(serial_ports_vbox)

        self.setCentralWidget(centralwidget)

    def center(self):
        frame_geo = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(desktop_center)
        self.move(frame_geo.topLeft())

    def cell_clicked(self, row, col):
        if col == 0:
            self.channel_table.cellWidget(row, 0).toggle()

    # old version
    #def _update_serial_ports_old(self):
    #    ports = serial.tools.list_ports.comports()
    #    serialports = []
    #    for port in ports:
    #        if port[2] != 'n/a':
    #            serialports.append(port[0])
    #    for row in range(0, 16):
    #        self.channel_table.cellWidget(row, 1).clear()
    #        self.channel_table.cellWidget(row, 1).addItems(serialports)
    #    self.channel_table.resizeColumnsToContents()


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

    def update_serial_ports(self):
        ports = self.list_serial_ports()
        port_count = len(ports)

        serialports = []
        for port in ports:
            #if port[2] != 'n/a':
                serialports.append(port)

        self.serial_ports_table.setRowCount(len(serialports)) 

        self.fout.reset()
        self.fout.set_serial_port_list(serialports)     

         
        self.bg_connect = QtGui.QButtonGroup()                 

        for i in range(0, len(serialports)):
            pb_connect = QtGui.QPushButton("Connect")
            self.bg_connect.addButton(pb_connect, i)
                
            self.serial_ports_table.setItem(i, 0, QtGui.QTableWidgetItem(serialports[i]))
            self.serial_ports_table.setCellWidget(i, 1, pb_connect)


        QtCore.QObject.connect(self.bg_connect, QtCore.SIGNAL("buttonClicked(int)"), self.connect_pressed )


                



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


    def channel_mapping_changed(self, combobox_id):
        pass




     
