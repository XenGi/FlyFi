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
import serial.tools.list_ports


class SettingsWindow(QtGui.QMainWindow):

    def __init__(self):
        super(SettingsWindow, self).__init__()

        self.init_ui()
        self.update_serial_ports()

    def init_ui(self):
        self.resize(480, 320)
        self.setWindowTitle('FlyFi - Settings')
        self.setWindowIcon(QtGui.QIcon('images/settings.png'))
        self.center()

        centralwidget = QtGui.QTabWidget()

        tab_channel = QtGui.QWidget()
        channel_vbox = QtGui.QVBoxLayout()
        self.channel_table = QtGui.QTableWidget(16, 2)
        self.channel_table.cellClicked.connect(self.cell_clicked)
        self.channel_table.setHorizontalHeaderLabels(['Active',
                                              'Serial port'])
        for row in range(0, 16):
            self.channel_table.setCellWidget(row, 0, QtGui.QCheckBox())
            #TODO: load from config
            self.channel_table.cellWidget(row, 0).setCheckState(QtCore.Qt.Checked)
            self.channel_table.setCellWidget(row, 1, QtGui.QComboBox())
        pb_update_serial = QtGui.QPushButton('Reload serial ports')
        pb_update_serial.clicked.connect(self.update_serial_ports)

        channel_vbox.addWidget(self.channel_table)
        channel_vbox.addWidget(pb_update_serial)
        tab_channel.setLayout(channel_vbox)

        centralwidget.addTab(tab_channel, "Channels")

        self.setCentralWidget(centralwidget)

    def center(self):
        frame_geo = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(desktop_center)
        self.move(frame_geo.topLeft())

    def cell_clicked(self, row, col):
        if col == 0:
            self.channel_table.cellWidget(row, 0).toggle()

    def update_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        serialports = []
        for port in ports:
            if port[2] != 'n/a':
                serialports.append(port[0])
        for row in range(0, 16):
            self.channel_table.cellWidget(row, 1).clear()
            self.channel_table.cellWidget(row, 1).addItems(serialports)
            #TODO: if config.channel.serial in serialports: select config.channel.serial
        self.channel_table.resizeColumnsToContents()