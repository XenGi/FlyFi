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
from FloppyOut import FloppyOut


class MainWindow(QtGui.QMainWindow):
    """
    The mainwindow containing options to fine tune things
    and start everything up.
    """
    def __init__(self):
        """
        generate other windows, floppy output control and create the gui
        """
        super(MainWindow, self).__init__()

        self.fout = FloppyOut()
        self.settingswindow = SettingsWindow()
        
        self.init_ui()


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

        centralwidget = QtGui.QWidget()
        grid = QtGui.QGridLayout()

        self.lab_freq = QtGui.QLabel()
        self.lab_freq.setMinimumWidth(50)
        self.lab_freq.setAlignment(QtCore.Qt.AlignRight |
                                   QtCore.Qt.AlignVCenter)
        sld_freq = QtGui.QSlider()
        sld_freq.setOrientation(QtCore.Qt.Horizontal)
        sld_freq.setTracking(True)
        sld_freq.setRange(0, 80000)
        sld_freq.valueChanged.connect(self.setFloatNum)
        sld_freq.setPageStep(1)
        sld_freq.setSingleStep(1) 

        self.setFloatNum(sld_freq.value())
        self.spb_channel = QtGui.QSpinBox()
        self.spb_channel.setRange(1, 16)
        pb_play = QtGui.QPushButton('Play')
        pb_play.clicked.connect(self.pb_play_pressed)
        pb_play.resize(pb_play.sizeHint())
        pb_stop = QtGui.QPushButton('Stop')
        pb_stop.clicked.connect(self.pb_stop_pressed)
        pb_stop.resize(pb_stop.sizeHint())


        grid.addWidget(QtGui.QLabel('Frequency:'), 0, 0)
        grid.addWidget(sld_freq, 0, 1)
        grid.addWidget(self.lab_freq, 0, 2)
        grid.addWidget(QtGui.QLabel('Hz'), 0, 3)
        grid.addWidget(QtGui.QLabel('Channel:'), 1, 0)
        grid.addWidget(self.spb_channel, 1, 1, 1, 3)
        grid.addWidget(pb_play, 2, 0, 1, 2)
        grid.addWidget(pb_stop, 1, 0, 2, 2)

        centralwidget.setLayout(grid)
        self.setCentralWidget(centralwidget)

        self.statusBar().showMessage('Ready')

        act_exit = QtGui.QAction(QtGui.QIcon('images/exit.png'), '&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        act_settings = QtGui.QAction(QtGui.QIcon('images/settings.png'),
                                     '&Settings', self)
        act_settings.setShortcut('Ctrl+S')
        act_settings.setStatusTip('Configure FlyFi')
        act_settings.triggered.connect(self.settingswindow.show)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(act_settings)
        file_menu.addAction(act_exit)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(act_settings)
        toolbar.addAction(act_exit)


        #TOOO: quick and dirty hack! Später wieder entfernen!        
        #self.fout.map_serial_port_to_channel(1, "/dev/ttyUSB0")
        #self.fout.map_serial_port_to_channel(2, "/dev/ttyUSB0")
        #self.fout.connect_serial_ports()


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
