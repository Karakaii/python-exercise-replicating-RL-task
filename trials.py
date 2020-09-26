########################################################################################################################
# These two classes allow you to create all the different types of trials
########################################################################################################################

##################################################
#                    Imports                     #
##################################################
from psychopy import core, event, sound, visual
from random import shuffle
import numpy as np
##################################################


##################################################
#                  TrialTriplet                  #
##################################################
# This creates the three trials that form a triplet for the uncertain trials
class TrialTriplet:

    def __init__(self, window, stimuliClass,
                 uncertaintyComparison, ghostType, postType, standardType,
                 rewardProbabilities, isPractice=False):
        self.window = window
        self.stimuliClass = stimuliClass

        self.uncertaintyComparison = uncertaintyComparison  # the two pairs being compared in the uncertainty trial
        self.ghostType = ghostType  # the choice of the ghost (index 0 or 1 of the pair of objects chosen)
        self.postType = postType  # the type of trial occurring after the uncertainty trial ()
        self.standardType = standardType  # the two objects of the standard trial
        self.rewardProbabilities = rewardProbabilities  # The current reward probabilities of the different rooms
        self.isPractice = isPractice  # Whether this is a practice trial or not

        # The three trial types of a triplet
        self.trialTypes = ["standard", "uncertain", "post"]
        # The sound of the beep at the beginning of each trial
        self.startSound = sound.Sound(value=500, secs=0.100, volume=1.0)

        # Prepare the trial results (see Experiment for the heading):
        self.trialResults = ""
        self.myType = "triplet"

    # This function will run the trials of the triplet
    def runTrials(self):
        isBroken = False

        # It will go through each trial type
        for currentTrialType in self.trialTypes:
            # Adding trial type to results:
            self.trialResults += currentTrialType + ","

            # If post type, add the post trial's type, if not add NA:
            if currentTrialType == "post":
                self.trialResults += self.postType + ","
            else:
                self.trialResults += "NA,"

            # Get the objects (and generate the objects) for the trial:
            trialObjects = self.getTrialObjects(currentTrialType)
            # Adding the objects to results:
            leftString = ""
            rightString = ""
            for key in trialObjects:
                # by simply checking if there's left or right it allows to add the objects of standard trials that
                # just have a left and a right object, but also the objects of uncertain trials because there are two
                # left and two right objects. In uncertainty trial there will be two objects without a space between
                # them, but that informs the experimenter as which combination of objects were presented.
                if "left" in key.lower():  # use .lower() because it is top or bottom Left for uncertain trials
                    leftString += trialObjects[key]
                else:  # right object
                    rightString += trialObjects[key]
            self.trialResults += leftString + "," + rightString + ","

            # Create the clock for the trial:
            trialClock = core.Clock()

            # Inter-trial-interval (in total 1 second):
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

            # The participant has 2 seconds to answer (unless it is a practice, then time is unlimited)
            while (trialClock.getTime() < 2.000 or self.isPractice) and not hasResponded:

                # draw all of the objects
                self.drawObjects(objects=trialObjects,  # dictionary with all the objects
                                 position=list(trialObjects.keys()))  # keys of that dictionary (as a list)
                self.stimuliClass.drawContainers()  # draw the containers
                self.window.flip()

                # wait for a response as the left or right arrow key, if a response is given, break the while loop.
                response = event.getKeys(keyList=["left", "right"], timeStamped=trialClock)
                if response:
                    hasResponded = True

            # If participant responded...
            if response:  # NOTE: if there is no response on uncertainty trial, cannot generate posttrial
                responseTime = response[0][1]
                responseSide = response[0][0]  # left or right
                self.trialResults += responseSide + ","
                self.trialResults += str(responseTime) + ","

                # Preparations if it is an uncertain trial:
                if currentTrialType == "uncertain":

                    ############################
                    # Selecting with the ghost #
                    ############################
                    # Take the pair that was actually chosen (right or left)...
                    chosenPair = self.pairsForGhostSelection[responseSide]
                    # ...and select the one according to the ghost index (0 or 1)
                    ghostSelectedObject = chosenPair[self.ghostType]
                    # ...and keep track of which one was selected by the ghost
                    self.uncertaintyTrialInfo["ghostSelectedObject"] = ghostSelectedObject
                    self.trialResults += ghostSelectedObject + ","
                    # For each object in the chosen pair find the one NOT the select by the ghost one and set it as the
                    # rejected by the ghost
                    for object in chosenPair:
                        if object != ghostSelectedObject:
                            ghostRejectedObject = object
                    self.uncertaintyTrialInfo["ghostRejectedObject"] = ghostRejectedObject
                    self.trialResults += ghostRejectedObject + ","

                    #####################
                    # Getting the rooms #
                    #####################
                    # The room common to both objects on that side:
                    commonSideRoom = self.uncertaintyTrialInfo["commonRoomLeftOrRight"][responseSide]

                    # For each room's object pair...
                    for room in self.stimuliClass.combiObjectsOfTheRooms:
                        # ...if the ghost-selected object is part of that pair but the ghost-reject object is not...
                        if ghostSelectedObject in self.stimuliClass.combiObjectsOfTheRooms[room] and \
                                ghostRejectedObject not in self.stimuliClass.combiObjectsOfTheRooms[room]:
                            # ...set this as the room unique to the ghost-selected object.
                            roomUniqueToRewarded = room
                    # Create the rooms to be shown,
                    # the first one (the common one) will be shown first,
                    # and the second one (the one unique to the ghost-selected object) will be shown second.
                    roomsToBeShown = [commonSideRoom, roomUniqueToRewarded]

                    ###############################
                    # Getting the objectPositions #
                    ###############################
                    # Create a dictionary with the positions as keys and the objects that are top or bottom of the side
                    # chosen as entries.
                    if responseSide == "left":
                        responseObjects = {"centreTop": trialObjects["topLeft"],
                                           "centreBottom": trialObjects["bottomLeft"]}
                    else:  # right
                        responseObjects = {"centreTop": trialObjects["topRight"],
                                           "centreBottom": trialObjects["bottomRight"]}
                    # self.uncertaintyTrialInfo["chosenStim"] = responseObjects

                    responseObjectsPositions = list(responseObjects.keys())

                # Preparations if it is a post or standard trial:
                else:
                    # note that there was no ghost selection:
                    self.trialResults += "NA,NA,"

                    responseObjects = trialObjects[responseSide]  # just one left or right object
                    responseObjectsPositions = "centre"  # positioned in the centre
                    # select the rooms of the selected object and shuffle them to randomise which one is presented first
                    roomsToBeShown = self.stimuliClass.combiRoomsOfTheObjects[responseObjects]
                    shuffle(roomsToBeShown)

                # wait half a second
                core.wait(0.500)

                # present the objects on their own for a second #
                trialClock.reset()
                while trialClock.getTime() < 1.000:
                    # draw the objects
                    self.drawObjects(objects=responseObjects,
                                     position=responseObjectsPositions)
                    self.window.flip()

                # present the objects on top of the FIRST ROOM #
                # record which room:
                self.trialResults += roomsToBeShown[0] + ","
                # determine if there is treasure in this room:
                isTreasure = self.getTreasure(room=roomsToBeShown[0],
                                              currentTrialType=currentTrialType)
                # Noting it down
                if isTreasure:
                    self.trialResults += "1,"
                else:
                    self.trialResults += "0,"
                trialClock.reset()
                while trialClock.getTime() < 1.000:
                    # If there is treasure, draw the treasureImage
                    if isTreasure:
                        self.stimuliClass.treasureImage.draw()

                    # draw the room
                    self.stimuliClass.roomImages[roomsToBeShown[0]].draw()
                    # draw the objects
                    self.drawObjects(objects=responseObjects,
                                     position=responseObjectsPositions)
                    self.window.flip()

                # present the objects on their own for 650 ms #
                trialClock.reset()
                while trialClock.getTime() < 0.650:
                    # draw the objects
                    self.drawObjects(objects=responseObjects,
                                     position=responseObjectsPositions)
                    self.window.flip()

                # present the objects on top of the SECOND ROOM #
                # record which room:
                self.trialResults += roomsToBeShown[1] + ","
                # determine if there is treasure in this room:
                isTreasure = self.getTreasure(room=roomsToBeShown[1],
                                              currentTrialType=currentTrialType)
                # Noting it down
                if isTreasure:
                    self.trialResults += "1\n"  # the last value in the line
                else:
                    self.trialResults += "0\n"  # the last value in the line
                trialClock.reset()
                while trialClock.getTime() < 1.000:
                    # If there is treasure, draw the treasureImage
                    if isTreasure:
                        self.stimuliClass.treasureImage.draw()
                    # draw the room
                    self.stimuliClass.roomImages[roomsToBeShown[1]].draw()
                    # draw the objects
                    self.drawObjects(objects=responseObjects,
                                     position=responseObjectsPositions)
                    self.window.flip()

                # present the objects on their own for the outro duration #
                trialClock.reset()
                while trialClock.getTime() < self.outroTiming:
                    self.drawObjects(objects=responseObjects,
                                     position=responseObjectsPositions)
                    self.window.flip()

            # If participants DID NOT respond...
            else:
                # Present a warning message for 4 seconds
                trialClock.reset()
                while trialClock.getTime() < 4.000:
                    warningText = visual.TextStim(
                        win=self.window,
                        text="Please make sure you answer in the 2 seconds imparted.",
                        color=[-1, -1, -1],
                        height=self.window.screen["height"] / 32,
                        wrapWidth=self.window.screen["width"])
                    warningText.draw()
                    self.window.flip()

                # record all the aspects that could not be collected:
                self.trialResults += "NA,NA,NA,NA,NA,NA,NA,NA,NA,NA\n"

                # If this was an uncertainty trail that was skipped, the post trial cannot be created; hence,
                # it is best to break the loop here.
                if currentTrialType == "uncertain":
                    isBroken = True

                    # Need to record the skipped post trial that comes afterwards:
                    self.trialResults += "post," + self.postType + ",NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA\n"

            # If it is True, break the for loop
            if isBroken:
                break

    # This function will generate all the object to present in the trail (and do other preparations)
    def getTrialObjects(self, currentTrialType):

        ##################
        # Standard Trial #
        ##################
        if currentTrialType == "standard":
            self.outroTiming = 0.150  # time at the end of each trial when participant see the selected object(s)

            # Take the two objects of the standard trial and randomly set one to be on the left and one to be on the
            # right. The use of the keys will help go through the objects and position them.
            objectPair = list(self.standardType)
            shuffle(objectPair)
            trialObjects = {"left": objectPair[0],
                            "right": objectPair[1]}

        ###################
        # Uncertain Trial #
        ###################
        elif currentTrialType == "uncertain":
            self.outroTiming = 0.850  # time at the end of each trial when participant see the selected object(s)

            # Take the two pairs of objects from the uncertainty trial and randomly set one to be on the left and one
            # to be on the right. The use of the keys will help go through the objects and position them.
            uncertainComparison = self.uncertaintyComparison
            shuffle(uncertainComparison)
            leftPair = uncertainComparison[0]
            rightPair = uncertainComparison[1]
            #####

            # We are going to shuffle the left pair in order to randomly decide which objects goes on the top and
            # which objects goes on the bottom:

            # However, we want to keep the order of the pairs before the shuffle because we want the ghost selection
            # to be counterbalanced
            self.pairsForGhostSelection = {"left": leftPair,
                                           "right": rightPair}

            # shuffle the pair and set which on at top and which one at bottom:
            shuffle(leftPair)
            topLeft = leftPair[0]
            bottomLeft = leftPair[1]
            #####

            # Now we need to set the top and bottom right objects according to the room they have in common with the
            # top and bottom left objects:

            # Go through every room key of the combination of objects for each room...
            for room in self.stimuliClass.combiObjectsOfTheRooms:

                # ...if the top left object IS in the combination of objects for this room AND the bottom left object
                # IS in this combination (i.e., it IS the combination of the left top and bottom objects)...
                if topLeft in self.stimuliClass.combiObjectsOfTheRooms[room] and \
                        bottomLeft in self.stimuliClass.combiObjectsOfTheRooms[room]:
                    # ...set this room as the COMMON ROOM for the LEFT objects.
                    leftSideCommonRoom = room

                # ...if the top left object is NOT in the combination of objects for this room AND the bottom left
                # object is NOT in this combination (i.e., it is NOT the combination of the left top and bottom objects;
                # hence, it is the combination of the right top and bottom objects )...
                if topLeft not in self.stimuliClass.combiObjectsOfTheRooms[room] and \
                        bottomLeft not in self.stimuliClass.combiObjectsOfTheRooms[room]:
                    # ...set this room as the COMMON ROOM for the RIGHT objects.
                    rightSideCommonRoom = room

                # For every object in the right pair...
                for object in rightPair:

                    # ...if the top left object is in the combination of objects for this room AND the this current
                    # object of the right pair is part of the combination of objects for this room (i.e., this is the
                    # room in common for the top left and right objects)...
                    if topLeft in self.stimuliClass.combiObjectsOfTheRooms[room] and \
                            object in self.stimuliClass.combiObjectsOfTheRooms[room]:
                        # ...set this room as the top common room and...
                        topCommonRoom = room
                        # ...set this right pair object as the topRight object.
                        topRight = object

                    # ...if the bottom left object is in the combination of objects for this room AND the this current
                    # object of the right pair is part of the combination of objects for this room (i.e., this is the
                    # room in common for the bottom left and right objects)...
                    if bottomLeft in self.stimuliClass.combiObjectsOfTheRooms[room] and \
                            object in self.stimuliClass.combiObjectsOfTheRooms[room]:
                        # ...set this room as the bottom common room and...
                        bottomCommonRoom = room
                        # ...set this right pair object as the bottomRight object.
                        bottomRight = object

            trialObjects = {"topLeft": topLeft,
                            "bottomLeft": bottomLeft,
                            "topRight": topRight,
                            "bottomRight": bottomRight}

            self.uncertaintyTrialInfo = {"commonRoomLeftOrRight": {"left": leftSideCommonRoom,
                                                                   "right": rightSideCommonRoom},
                                         "commonRoomTopOrBottom": {"top": topCommonRoom,
                                                                   "bottom": bottomCommonRoom},
                                         "trialObjects": trialObjects}
        ##############
        # Post Trial #
        ##############
        else:  # post trial type
            self.outroTiming = 0.150  # time at the end of each trial when participant see the selected object(s)

            if self.postType == "repeat":  # ghost-selected vs. horizontal counterpart

                # For each possible position in the uncertainty trial...
                for position in self.uncertaintyTrialInfo["trialObjects"]:
                    # ...if the object at that position is the ghost-selected object...
                    if self.uncertaintyTrialInfo["trialObjects"][position] \
                            == self.uncertaintyTrialInfo["ghostSelectedObject"]:
                        # ...get the position of that object, and replace any left or right in it with an empty string
                        ghostSelectedPosition = position
                        ghostSelectedPosition = ghostSelectedPosition.replace("Left", "")
                        ghostSelectedPosition = ghostSelectedPosition.replace("Right", "")

                # For each possible position in the uncertainty trial...
                for position in self.uncertaintyTrialInfo["trialObjects"]:
                    # ...if the object at that position is different from ghost-selected object but has the same top or
                    # bottom position in it...
                    if self.uncertaintyTrialInfo["trialObjects"][position] != \
                            self.uncertaintyTrialInfo["ghostSelectedObject"] \
                            and ghostSelectedPosition in position:
                        # ...it is the vertical counter part of the ghost-selected object
                        horizontalCounterpart = self.uncertaintyTrialInfo["trialObjects"][position]

                # the object pair is made up of the ghost-selected and its horizontal counterpart
                objectPair = [self.uncertaintyTrialInfo["ghostSelectedObject"], horizontalCounterpart]

            elif self.postType == "switch":  # ghost-rejected vs. horizontal counterpart

                # For each possible position in the uncertainty trial...
                for position in self.uncertaintyTrialInfo["trialObjects"]:
                    # ...if the object at that position is the ghost-rejected object...
                    if self.uncertaintyTrialInfo["trialObjects"][position] \
                            == self.uncertaintyTrialInfo["ghostRejectedObject"]:
                        # ...get the position of that object, and replace any left or right in it with an empty string
                        ghostRejectedPosition = position
                        ghostRejectedPosition = ghostRejectedPosition.replace("Left", "")
                        ghostRejectedPosition = ghostRejectedPosition.replace("Right", "")

                # For each possible position in the uncertainty trial...
                for position in self.uncertaintyTrialInfo["trialObjects"]:
                    # ...if the object at that position is different from ghost-rejected object but has the same top or
                    # bottom position in it...
                    if self.uncertaintyTrialInfo["trialObjects"][position] != \
                            self.uncertaintyTrialInfo["ghostRejectedObject"] \
                            and ghostRejectedPosition in position:
                        # ...it is the vertical counter part of the ghost-rejected object
                        horizontalCounterpart = self.uncertaintyTrialInfo["trialObjects"][position]

                # the object pair is made up of the ghost-rejected and its horizontal counterpart
                objectPair = [self.uncertaintyTrialInfo["ghostRejectedObject"], horizontalCounterpart]

            else:  # CLASH: ghost-selected vs. ghost-rejected
                objectPair = [self.uncertaintyTrialInfo["ghostSelectedObject"],
                              self.uncertaintyTrialInfo["ghostRejectedObject"]]

            shuffle(objectPair)  # randomly sets which one is left and which one is right
            trialObjects = {"left": objectPair[0],
                            "right": objectPair[1]}

        return trialObjects

    # This function draws the objects
    def drawObjects(self, objects, position):

        # If the objects are given in a dictionary, and the positions as a list:
        if isinstance(objects, dict) and isinstance(position, list):
            iteration = -1
            for key in objects:
                # use the iteration to select the appropriate position for the object
                # (because I use the keys of the objects' dictionary, objects and positions will be in the same order)
                iteration += 1
                currentPosition = position[iteration]
                # get the object to draw using the key
                object = objects[key]

                # select the image of the object, set its position, and set the positionRect to the same position
                objectImage = self.stimuliClass.objectImages[object]
                objectImage.pos = self.window.screen[currentPosition]
                self.stimuliClass.positionRect.pos = objectImage.pos
                # draw the object and the positionRect
                self.stimuliClass.positionRect.draw()
                objectImage.draw()

        # If the object and the position are just one string each:
        else:
            # select the image of the object, set its position, and set the positionRect to the same position
            objectImage = self.stimuliClass.objectImages[objects]
            objectImage.pos = self.window.screen[position]
            self.stimuliClass.positionRect.pos = objectImage.pos
            # draw the object and the positionRect
            self.stimuliClass.positionRect.draw()
            objectImage.draw()

    # This function determines if there was a treasure or not by using the room and the currentTrialType
    def getTreasure(self, room, currentTrialType):
        # Use np.random.choice, that will randomly select True or False according to the probabilities set in argument p
        # - The probability for True is the reward probability for the room
        # - The probability for False is the 1 minus reward probability
        isTreasure = np.random.choice([True, False],
                                      p=[self.rewardProbabilities[currentTrialType][room],
                                         1 - self.rewardProbabilities[currentTrialType][room]
                                         ]
                                      )
        # add the probability of the room to the results:
        self.trialResults += str(self.rewardProbabilities[currentTrialType][room]) + ","

        return isTreasure

##################################################


##################################################
#                 StandardTrial                  #
##################################################
# This is the same as a triplet except it only has one trialType, the standard type:
class StandardTrial(TrialTriplet):
    def __init__(self, window, stimuliClass, standardType, rewardProbabilities, isPractice=False):
        self.window = window
        self.stimuliClass = stimuliClass

        self.standardType = standardType  # the two objects of the standard trial
        self.rewardProbabilities = rewardProbabilities  # The current reward probabilities of the different rooms
        self.isPractice = isPractice  # Whether this is a practice trial or not

        # The only trial type: standard
        self.trialTypes = ["standard"]
        # The sound of the beep at the beginning of each trial
        self.startSound = sound.Sound(value=500, secs=0.100, volume=1.0)

        # Prepare the trial results (see Experiment for the heading):
        self.trialResults = ""
        self.myType = "standard"

########################################################################################################################
