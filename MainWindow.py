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


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.resize(480, 320)
        self.setWindowTitle('FlyFi - Floppy-Fidelity')
        self.setWindowIcon(QtGui.QIcon('images/flyfi-logo.png'))
        self.center()

        centralwidget = QtGui.QWidget()
        grid = QtGui.QGridLayout()

        lcd_freq = QtGui.QLCDNumber()
        lcd_channel = QtGui.QLCDNumber()
        pb_play = QtGui.QPushButton('Play')
        pb_play.clicked.connect(self.pb_play_pressed)
        pb_play.resize(pb_play.sizeHint())

        grid.addWidget(QtGui.QLabel('Frequency:'), 0, 0)
        grid.addWidget(lcd_freq, 0, 1)
        grid.addWidget(QtGui.QLabel('Channel:'), 1, 0)
        grid.addWidget(lcd_channel, 1, 1)
        grid.addWidget(pb_play, 2, 0, 1, 2)

        centralwidget.setLayout(grid)
        self.setCentralWidget(centralwidget)

        self.statusBar().showMessage('Ready')

        act_exit = QtGui.QAction(QtGui.QIcon('images/exit.png'), '&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(act_exit)

        self.toolbar = self.addToolBar('&Exit')
        self.toolbar.addAction(act_exit)

        self.show()

    def center(self):
        frame_geo = self.frameGeometry()
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(desktop_center)
        self.move(frame_geo.topLeft())

    def pb_play_pressed(self):
        pass