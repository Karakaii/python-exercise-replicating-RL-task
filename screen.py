########################################################################################################################
# In this file we setup the screen of the computer used for the experiment and we prepare value based on the size of the
# screen.
########################################################################################################################


##########################################################
#                        Imports                         #
##########################################################
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
##########################################################

##########################################################
#                  Preparing the Screen                  #
##########################################################
# Need to use the AA_EnableHighDpiScaling to allow both my psychopy and my pyqt windows to understand that my screen has
# a very high resolution (+start the application for pyqt):
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])
##########################################################

##########################################################
#       Preparing information for the pyqt window        #
##########################################################
# Getting screen information and saving it in a readable dictionary #
screen = QGuiApplication.primaryScreen()  # getting the computer screen
screenSize = screen.size()
pyqtScreen = {"width": screenSize.width(), "height": screenSize.height(),
              "midWidth": screenSize.width() / 2, "midHeight": screenSize.height() / 2,
              "guiGap": screenSize.height() * .025}
##########################################################


##########################################################
#     Preparing information for the psychopy window      #
##########################################################
# This function will create a dictionary with all the size information necessary for the psychopy window.
# It allows for my psychopy window to be flexible (in the experiment it will be full-screened -so the size of the
# window is the size of the screen because of the AA_EnableHighDpiScaling- but I was testing it with a smaller size).
def getScreenSize(window):
    size = window.size
    # size[0] is the width, and size[1] is the height of the window
    psychoPyScreen = {"resolution": size,
                      "width": size[0],
                      "height": size[1],
                      "midWidth": size[0] * .5,
                      "midHeight": size[1] * .5,
                      "quarterHeight": size[1] * .25,
                      "centre": [0, 0],
                      "centreTop": [0, (+size[1] * .125) + (size[1] * .01) / 2],  # adding a little gap for prettiness
                      "centreBottom": [0, (-size[1] * .125) - (size[1] * .01) / 2],
                      "left": [-size[0] * .25, 0],
                      "topLeft": [-size[0] * .25, (+size[1] * .125) + (size[1] * .01) / 2],
                      "bottomLeft": [-size[0] * .25, (-size[1] * .125) - (size[1] * .01) / 2],
                      "right": [+size[0] * .25, 0],
                      "topRight": [+size[0] * .25, (+size[1] * .125) + (size[1] * .01) / 2],
                      "bottomRight": [+size[0] * .25, (-size[1] * .125) - (size[1] * .01) / 2],
                      "containerGap": size[1] * .01}
    return psychoPyScreen

########################################################################################################################

