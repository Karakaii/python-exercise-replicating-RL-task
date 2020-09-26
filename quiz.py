########################################################################################################################
# These two classes allow you to create the quiz and all the quiz questions
########################################################################################################################

########################################
#                Imports               #
########################################
from random import choice, shuffle
from psychopy import core, event, sound
from popChoice import popChoice
from waitText import waitText
########################################


########################################
#                 Quiz                 #
########################################
# This is the object the user will directly create and launch.
# This creates all the quiz questions (the next class in this module).
class Quiz:
    def __init__(self, window, stimuliClass, quiz100, experiment):
        self.window = window
        self.stimuliClass = stimuliClass

        # If this is set to True, the quiz will end even if the user did not get all the questions correct
        self.quiz100 = quiz100

        # The experiment needs to be launched from here
        self.experimentToBeLaunched = experiment

        self.quizQuestions = []
        self.correctness = -1
        self.numberOfAttempts = 0

        # create objects questions
        self.createQuestions(self.stimuliClass.objectNames)
        # create room questions
        self.createQuestions(self.stimuliClass.roomNames)

    def createQuestions(self, stimuliNames):
        names = stimuliNames.copy()  # copy the names of the stimuli to not mess the list up
        names = names * 2  # double the amount
        halfPoint = len(names) / 2
        for i in range(len(names)):
            name = names[i]

            # first time a question for that stimulus is asked:
            if i < halfPoint:
                firstOrSecond = 0
            # second time a question for that stimulus is asked:
            else:  # equal or above the halfPoint
                firstOrSecond = 1

            # create the question with the stimulus name and whether it is the first or second question:
            quizQuestion = QuizQuestion(window=self.window,
                                        stimuliClass=self.stimuliClass,
                                        testStimulus=name,
                                        firstOrSecond=firstOrSecond)
            # append questions to overall list of questions
            self.quizQuestions.append(quizQuestion)

    # This is the function the quiz will call to start the questions:
    def launchQuizQuestions(self):
        # beginning of the quiz, so set correctness at zero
        self.correctness = 0

        # shuffle the order of the questions
        shuffle(self.quizQuestions)

        # welcome and instructions message to the quizz (using waitText to wait for participants to press the spacebar)
        waitText(self.window, "WELCOME TO THE QUIZ"
                              "\nYou will be presented with a top objects (rooms or objects) and two possible related "
                              "objects."
                              "\nEach object is related to two rooms, and each room is related to two objects. No "
                              "object has the same two rooms, and no room has the same two objects."
                              "\n "
                              "\n- Press the LEFT ARROW KEY if you think the LEFT possible objects is related to the "
                              "top objects"
                              "\n- Press the RIGHT ARROW KEY if you think the RIGHT possible objects is related to the "
                              "top objects"
                              "\n"
                              "\n You have 3 seconds to answer each quiz question. If you do not respond in time, "
                              "your answer will be considered incorrect."
                              "\n"
                              "\nYou will receive feedback. You will be doing the quiz until you can correctly answer "
                              "each of the 16 questions."
                              "\n "
                              "\nPress the SPACEBAR when you are ready to start.")

        # for each question...
        for quizQuestion in self.quizQuestions:
            # ...launch the question
            quizQuestion.launch()
            # ...update the correctness (+1 if it was correct)
            self.correctness += quizQuestion.correct

            # create a feedback text, based on whether the answer was correct or not
            # (using waitText to wait for participants to press the spacebar)
            if quizQuestion.correct == 1:
                resultText = "CORRECT!"
            else:
                resultText = "INCORRECT..."
            waitText(self.window, f"{resultText}"
                                  f"\nYour score is currently {self.correctness}/{len(self.quizQuestions)}"
                                  f"\nPress the SPACEBAR to continue.")

        # after doing each question use the launchWholeQuizz function to check the whether the quiz should start again:
        self.launchWholeQuiz()

    # This is the function that the user launches
    def launchWholeQuiz(self):

        # if this is NOT the first time (i.e., correctness is different from -1)
        # and the participant got all the questions right
        # or quiz100 is True (allowing the marker/tester to continue after the quiz
        # despite not getting all the questions right)
        if self.correctness == len(self.quizQuestions) or (self.quiz100 and self.correctness != -1):

            # Reset the size and position of all the room images:
            for key in self.stimuliClass.roomImages:
                image = self.stimuliClass.roomImages[key]
                image.size = self.stimuliClass.roomSize
                image.pos = [0, 0]

            # Create a congratulation text,
            # wait for the participant to press the spacebar (using waitText) before launching the experiment:
            waitText(self.window, "Congratulations! You mastered the quiz. Now the trials will begin."
                                  "\nPress the SPACEBAR to continue.")
            self.experimentToBeLaunched.launchExperiment()

        # If this IS the first time, or if the participant did not get all the answers correct
        # (and it quiz100 is False), relaunch the quiz:
        else:
            self.launchQuizQuestions()
            # keep track of the number of attempts for this quiz:
            self.numberOfAttempts += 1

########################################


########################################
#             QuizQuestion             #
########################################
class QuizQuestion:
    def __init__(self, window, stimuliClass, testStimulus, firstOrSecond):
        self.window = window
        self.stimuliClass = stimuliClass

        # The stimulus that will be at the top of the screen in the quiz question, participants answer a question about
        # this stimulus
        self.testStimulus = {"name": testStimulus,
                             "image": self.stimuliClass.allImages[testStimulus],
                             "position": "centreTop"}

        # If this is the first or second question for this stimulus
        # must be 0 (first) or 1 (second)
        self.firstOrSecond = firstOrSecond

        # The sound of the beep at the beginning of each trial
        self.startSound = sound.Sound(value=500, secs=.100, volume=1.0)

    # This function creates the target and distractor stimulus that the participant
    # must choose between for this quiz question:
    def createResponseStimuli(self):

        positions = ["bottomLeft", "bottomRight"]

        if self.testStimulus["name"] in self.stimuliClass.objectNames:  # it is an object
            # set the target as the first or second (dependent on firstOrSecond) related room to that object
            target = self.stimuliClass.combiRoomsOfTheObjects[self.testStimulus["name"]][self.firstOrSecond]
            # set the distractor as any room that is not part of those related to the testStimulus
            distractor = choice(self.stimuliClass.roomNames)
            while distractor in self.stimuliClass.combiRoomsOfTheObjects[self.testStimulus["name"]]:
                distractor = choice(self.stimuliClass.roomNames)

            # To know whether I need to draw a position rect behind the stimulus,
            # I need to know if it is an object or not. The target and distractor will be the opposite of that.
            self.testStimulus["isObject"] = True

        else:  # it is a room
            # set the target as the first or second (dependent on firstOrSecond) related object to that room
            target = self.stimuliClass.combiObjectsOfTheRooms[self.testStimulus["name"]][self.firstOrSecond]
            # set the distractor as any object that is not part of those related to the testStimulus
            distractor = choice(self.stimuliClass.objectNames)
            while distractor in self.stimuliClass.combiObjectsOfTheRooms[self.testStimulus["name"]]:
                distractor = choice(self.stimuliClass.objectNames)

            # To know whether I need to draw a position rect behind the stimulus,
            # I need to know if it is an object or not. The target and distractor will be the opposite of that.
            self.testStimulus["isObject"] = False

        # Make the distractor and the target by creating their names, selecting their images,
        # and randomly choosing one the positions (and taking it out so that the other cannot have the same position).
        self.distractor = {"name": distractor,
                           "image": self.stimuliClass.allImages[distractor],
                           "position": popChoice(positions)}
        self.target = {"name": target,
                       "image": self.stimuliClass.allImages[target],
                       "position": popChoice(positions)}

    # When called, this function will draw all three stimuli for the question
    # NOTE: this changes the size of the images from what they were intended, so this will have to be reset.
    def drawStimuli(self):
        if self.testStimulus["isObject"]:
            self.stimuliClass.positionRect.pos = self.testStimulus["image"].pos
            self.stimuliClass.positionRect.draw()
        else:  # the target and distractor are objects
            self.stimuliClass.positionRect.pos = self.distractor["image"].pos
            self.stimuliClass.positionRect.draw()

            self.stimuliClass.positionRect.pos = self.target["image"].pos
            self.stimuliClass.positionRect.draw()

        self.testStimulus["image"].pos = self.window.screen[self.testStimulus["position"]]
        self.testStimulus["image"].size = self.window.screen["quarterHeight"]
        self.testStimulus["image"].draw()

        self.distractor["image"].pos = self.window.screen[self.distractor["position"]]
        self.distractor["image"].size = self.window.screen["quarterHeight"]
        self.distractor["image"].draw()

        self.target["image"].pos = self.window.screen[self.target["position"]]
        self.target["image"].size = self.window.screen["quarterHeight"]
        self.target["image"].draw()

    # This function will launch the quiz question:
    def launch(self):
        # create the target and distractor:
        self.createResponseStimuli()

        # Create the clock for the question:
        trialClock = core.Clock()

        # Inter-QUESTION-interval (in total 1 second):
        trialClock.reset()
        while trialClock.getTime() < 0.700:
            self.window.flip()
        self.startSound.play()  # play the beginning sound
        core.wait(0.300)

        # Getting the participant's response for the trial:
        hasResponded = False
        response = []
        # need to clear the events, otherwise left/right presses prior to this moment can affect the code
        event.clearEvents()
        trialClock.reset()
        while trialClock.getTime() < 3.000 and not hasResponded:
            # draw all of the stimuli of the question
            self.drawStimuli()
            self.window.flip()

            # wait for a response as the left or right arrow key, if a response is given, break the while loop.
            response = event.getKeys(keyList=["left", "right"], timeStamped=trialClock)
            if response:
                hasResponded = True

        # Create the self.correct variable that will be used for checking that the participants are answering correctly:
        if hasResponded and (response[0][0][1:] in self.target["position"].lower()):  # gave the correct response
            # NOTE: I am making the position lowercase because otherwise the L or the R would be uppercase and will
            # not allow for a correct response
            self.correct = 1
        else:  # did not respond or gave the wrong response
            self.correct = 0

########################################################################################################################
