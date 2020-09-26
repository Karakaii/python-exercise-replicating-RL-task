########################################################################################################################
# This is the main python file. It is from here that you edit parts of the experiment or that you launch the experiment
########################################################################################################################

#################################################
#                    Imports                    #
#################################################
from psychopy import visual
from screen import *  # provides all the screen setting up
from stimuli import Stimuli
from experiment import Experiment
from gui import experimentGUI
from quiz import Quiz
from recordingResults import ResultsRecorder
#################################################

#################################################
#         Consent and Demographics GUI          #
#################################################
# This will create a GUI that will provide the experimenter with a menu to select an experiment set up or create a
# new experiment will provide participants with a consent form, a demographics form, and instructions.
# Using pyqt here because it makes for neater GUIs than psychopy that are easy to check for errors.

# Creating GUI:
myGUI = experimentGUI(uiFile="resources/experimentGUI.ui",
                      screenSizes=pyqtScreen,
                      app=app)
# Launching it:
myGUI.launchGUI()
# Getting the demographic data and the experiment ID (for the results):
demographics = myGUI.participantDemographics
experimentID = myGUI.experimentID
# Getting the experiment set up (for the experiment)
experimentSetUp = myGUI.experimentSetUp
# Getting a settings that determines if participants must get the quiz 100% accurate before going on to the trial
# (it has to be so for a real experiment, but for the marker we would want to bypass the quiz even if we are not 100%
# accurate):
quiz100 = myGUI.quiz100

#################################################

#################################################
#            Creating PsychoPy Window           #
#################################################
windowPsychoPy = visual.Window(
    units="pix",
    fullscr=True,
    color=[.8, .8, .8],
    screen=0,
    size=[1500, 1500])
# Do not really need a screen size because it is overridden by the fullscreen setting, but it can be useful if you want
# to put "fullscr=False".
windowPsychoPy.setMouseVisible(False)

# Get window/screen size information:
windowPsychoPy.screen = getScreenSize(windowPsychoPy)
#################################################

#################################################
#             Creating our Stimuli              #
#################################################
# Create a stimuli object:
myStimuli = Stimuli(window=windowPsychoPy)
# Launch the function that will create all the stimuli:
myStimuli.createStimuli()

# Obtain the room/object combinations from it (for the results):
roomsOfTheObjects = myStimuli.combiRoomsOfTheObjects
objectsOfTheRooms = myStimuli.combiObjectsOfTheRooms
#################################################

#################################################
#            Creating our Experiment            #
#################################################
# Creating our experiment object #
myExperiment = Experiment(window=windowPsychoPy,
                          stimuliClass=myStimuli,
                          experimentalSetUp=experimentSetUp)  # This is where you set the experiment set-up

# We also create our beginning quiz object #
# We launch this, and then it will launch our experiment, and when it is all done it will close the window:
myQuiz = Quiz(window=windowPsychoPy,
              stimuliClass=myStimuli,
              quiz100=quiz100,
              experiment=myExperiment)
myQuiz.launchWholeQuiz()
windowPsychoPy.close()
#################################################

#################################################
#               Generating Results              #
#################################################

# Get all the information from our experiment that we need for the results: #
quizAttempts = myQuiz.numberOfAttempts  # how many times the participant had to do the quiz to get 100% accuracy
randomWalk = myExperiment.randomWalk  # random gaussian walk of the room probabilities
experimentResults = myExperiment.results  # participant's results

# Create a result recorder object and launch it so it creates all the CSVs and PNGs necessary for keeping the results: #
myResultsRecorder = ResultsRecorder(experimentID=experimentID,
                                    demographics=demographics,
                                    quizAttempts=quizAttempts,
                                    randomWalk=randomWalk,
                                    experimentResults=experimentResults,
                                    roomsOfTheObjects=roomsOfTheObjects,
                                    objectsOfTheRooms=objectsOfTheRooms)
myResultsRecorder.recordResults()
# Results will be generated in the results directory, under a directory with the ID of the experiment, under a
# directory named with the participant's ID

########################################################################################################################
