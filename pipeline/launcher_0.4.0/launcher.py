#!/usr/bin/python3

"""
ZetCode PyQt5 tutorial

In this example, we determine the event sender
object.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
import subprocess

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

from launcherlib import manageOS
from launcherlib import manageProjectDir
from launcherlib.manageOS import OSTYPE
from launcherlib import getHoudinis
from launcherlib import setHoudiniEnv
from launcherlib import replaceHistory

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
houdini_icon = dir_path + '/icons/icon_app_houdini.png'


launcher_path = os.path.dirname(__file__) 
print(launcher_path)
class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        appPath,vers = getHoudinis.getHoudinis()
        height = 0 
        for count,ver in enumerate(vers): ### creating all houdini verions button
            #print(count)
            name = 'Houdini'+ver
            btn = QPushButton(name, self)
            btn.setIcon(QIcon(houdini_icon))
            btn.resize(150, 40)
            btn.move(50,5+40*count)
            height += 40*(count+1)
            btn.clicked.connect(self.buttonClicked)


        self.statusBar()
        #print(height)
        self.setGeometry(800, 300, 250, height)
        self.setFixedSize(250,height)
        self.setWindowTitle('Launcher ' +launcher_path[-5:] )
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def setEnvVariables(self):
        #Env = os.environ.copy()
        Env = manageOS.setGlobalEnv() 
        return Env

    def buttonClicked(self):
        sender = self.sender()
        if sender.text().startswith('Houdini'):
            #print('houdini Button Clicked')
            appPath,vers = getHoudinis.getHoudinis()
            ver = sender.text()[-8:]
            print(ver)

            aEnv = setHoudiniEnv.setHoudiniEnv(self.setEnvVariables(),appPath,ver)
            #replaceHistory.DefReplaceHistory(aEnv)
            subprocess.Popen('hindie', env=aEnv, shell=True)
                
        self.statusBar().showMessage(sender.text() + ' was pressed')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()