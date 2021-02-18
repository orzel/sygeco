#!/usr/bin/env python
# -*- coding: utf-8
# vim: set fileencoding=utf-8

# System
import sys
from time import sleep
from os import listdir
from subprocess import call

# pyside2
from PySide2.QtCore import Qt, Signal, QCoreApplication
from PySide2.QtGui import QPixmap, QColor
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QGridLayout, QGroupBox, QWidget, QVBoxLayout, QMessageBox


#
# Configuration:
#

# programmer known by avrdude, typically usbasp, arduino, ..
AVRDUDE_PROGRAMMER = "usbasp"

APP_IMAGE_WIDTH = 250
APP_IMAGE_HEIGHT = 100
GRID_COLUMNS = 5
AVRDUDE = 'avrdude -pattiny85 -c %s' % AVRDUDE_PROGRAMMER

games = [
    ["Tiny-Arkanoid.ino.hex", "Tiny-Arkanoid.png"],
    ["Tiny-Bert.ino.hex", "Tiny-Bert.jpg"],
    ["Tiny-Bike.ino.hex", "Tiny-Bike.png"],
    ["Tiny-Bomber.ino.hex", "Tiny-Bomber.jpeg"],
    ["Tiny-DDug.ino.hex", "Tiny-DDug.png"],
    ["Tiny-Gilbert.ino.hex", "Tiny-Gilbert.jpeg"],
    ["Tiny-Invaders.ino.hex", "Tiny-Invaders.jpg"],
    ["Tiny-Missile.ino.hex", "Tiny-Missile.png"],
    ["Tiny-Morpion.ino.hex", "Tiny-Morpion.png"],
    ["Tiny-Pacman.ino.hex", "Tiny-Pacman.jpeg"],
    ["Tiny-Pinball.ino.hex", "Tiny-Pinball.jpg"],
    ["Tiny-Plaque.ino.hex", "Tiny-Plaque.png"],
    ["Tiny-Trick.ino.hex", "Tiny-Trick.png"],
    ["Tiny-Tris.ino.hex", "Tiny-Tris.png"],
]

class ClickableLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, codefilename, imagefilename):
        super(ClickableLabel, self).__init__()
        self.codefilename = codefilename
        self.imagefilename = imagefilename
        self.setPixmap(QPixmap(imagefilename).scaled(APP_IMAGE_WIDTH, APP_IMAGE_HEIGHT, Qt.KeepAspectRatio))
        self.setObjectName(codefilename)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Sygeco 0.1 launcher")

        widget = QWidget(self)
        grid = QGridLayout(self)
        i = 0
        for codefilename, imagefilename in games:
            box = QGroupBox(imagefilename.split('.')[0], self)
            layout = QVBoxLayout()
            label = ClickableLabel(codefilename, imagefilename)
            label.clicked.connect(self.uploadCode)
            layout.addWidget(label)
            box.setLayout(layout)
            grid.addWidget(box, i//GRID_COLUMNS, i%GRID_COLUMNS)
            i+=1
        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def uploadCode(self, codefilename):
        # Create 'wait' dialog
        msg = QMessageBox(QMessageBox.Information, "C'est long", "Patiente pendant que le jeux est envoyé sur la console.", QMessageBox.NoButton)
        msg.setStandardButtons(QMessageBox.NoButton); # it's supposed to be the default according to doc, but they lie, an ok button is added

        # Display it
        msg.show()
        sleep(0.1) # Trick Qt, otherwise it wont display the dialog!$%!$!
        QCoreApplication.processEvents() # update content

        # upload game
        return_value = call(AVRDUDE + " -U flash:w:%s" % codefilename, shell=True)
        msg.close()

        msg = QMessageBox()
        if return_value !=0:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Oops..!")
            msg.setInformativeText("Cela n'a pas marché, est-ce que tout est bien branché ??\nSinon appelle papa !")
            msg.setWindowTitle("Attention !")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setText("Youpi !")
            msg.setInformativeText("Le jeux est bien installé.\nTu peux débrancher.")
            msg.setWindowTitle("Youpi !")

        msg.exec_()

    def checkTarget(self):
        """
        See if avrdude can see the target, validates both the programmer
        and the fact that the console is connected to it.
        """
        if call(AVRDUDE, shell=True)!=0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Oops..!")
            msg.setInformativeText('Je ne trouve pas le programmeur ou la console !\nVerifie que tout est bien branché.')
            msg.setWindowTitle("Attention !")
            msg.exec_()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.checkTarget()
sys.exit(app.exec_())

