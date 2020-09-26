########################################################################################################################
# This function will make the string you enter into a text, draw it, flip the window and wait for participants to
# press the spacebar.
########################################################################################################################

########################################
#                Imports               #
########################################
from psychopy import visual, event
########################################


########################################
#               waitText               #
########################################
def waitText(window, text):
    lineSize = window.screen["height"] / 32

    textToDraw = visual.TextStim(win=window,
                                 text=text,
                                 color=[-1, -1, -1],
                                 height=lineSize,
                                 wrapWidth=window.screen["width"])
    textToDraw.draw()

    window.flip()
    event.waitKeys(keyList="space")

########################################################################################################################
