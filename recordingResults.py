########################################################################################################################
# This is a class that will create all the files of interest for recording the participant's results
########################################################################################################################

#########################################
#                Imports                #
#########################################
from os import mkdir, listdir
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from makeIntoCSV import makeIntoCSV
#########################################


#########################################
#            ResultsRecorder            #
#########################################
class ResultsRecorder:
    def __init__(self, experimentID, demographics, quizAttempts, randomWalk, experimentResults,
                 roomsOfTheObjects, objectsOfTheRooms):
        # Put in all the parts that will make up the results:
        self.experimentID = experimentID
        self.demographics = demographics
        self.quizAttempts = str(quizAttempts)
        self.randomWalk = randomWalk
        self.experimentResults = experimentResults
        self.roomsOfTheObjects = roomsOfTheObjects
        self.objectsOfTheRooms = objectsOfTheRooms
        # Prepare paths and names:
        self.pathToResults = "results/"
        self.totalFileName = "allResults.csv"

    # This is the function the user launches to create all the results files:
    def recordResults(self):
        self.getExperimentDirectory()
        self.makeParticipantDirectory()
        self.makeDemographics()
        self.makeCombinations()
        self.makeExperimentResults()
        self.makeQuizAttempts()
        self.makeRandomWalk()
        self.updateAllResultsFile()

    # This functions sets the path to the directory of the experiment and creates a new directory if this is the first
    # participant of this experiment (i.e., there was no directory for this experiment).
    def getExperimentDirectory(self):
        self.allFilesInResults = listdir(self.pathToResults)
        self.pathToResults += self.experimentID + "/"  # adding to the path streamlines the process for the next methods
        # If no directory, create a new one...
        if self.experimentID not in self.allFilesInResults:
            mkdir(self.pathToResults)

    # Creates the directory for this participant:
    def makeParticipantDirectory(self):
        self.allFilesInResults = listdir(self.pathToResults)
        if self.allFilesInResults:  # if there are folders in there

            # Find the maximum participant ID
            maximumParticipantID = -1
            for folderName in self.allFilesInResults:
                if folderName != self.totalFileName:  # check it isn't the allResults CSV
                    if int(folderName) > maximumParticipantID:
                        maximumParticipantID = int(folderName)

            # Set new participant's ID
            self.participantID = str(maximumParticipantID + 1)

        else:  # if there are no folder in there
            self.participantID = "1"

        # Make the participant's directory
        self.pathToParticipantDirectory = self.pathToResults + self.participantID + "/"
        mkdir(self.pathToParticipantDirectory)

    # Create the variable and the CSV with demographics:
    def makeDemographics(self):
        # Make a line with all the demographics information:
        self.demographicsLine = "age,gender,education,student,fieldOfStudy,timeToCompleteDemographics\n"
        numberOfDemographicItems = len(self.demographics)
        itemsProcessed = 0
        for key in self.demographics:
            self.demographicsLine += self.demographics[key]

            itemsProcessed += 1
            if itemsProcessed != numberOfDemographicItems:  # if this is not the last item, add a comma
                self.demographicsLine += ","

        # Making into a CSV #
        makeIntoCSV(csvName=self.pathToParticipantDirectory + self.participantID + "_demographics.csv",
                    stringToWrite=self.demographicsLine)

    # Create a CSV with all the room/object combinations:
    def makeCombinations(self):
        # Make a line for the different objects and their rooms:
        self.roomsOfTheObjectsLine = "object,room1,room2\n"
        numberOfObjects = len(self.roomsOfTheObjects)
        objectsProcessed = 0
        for object in self.roomsOfTheObjects:
            self.roomsOfTheObjectsLine += object + "," \
                                          + self.roomsOfTheObjects[object][0] + "," \
                                          + self.roomsOfTheObjects[object][1]

            objectsProcessed += 1
            if objectsProcessed != numberOfObjects:  # if this is not the last item, add a linebreak
                self.roomsOfTheObjectsLine += "\n"

        # Make a line for the different rooms and their objects:
        self.objectsOfTheRoomsLine = "room,object1,object2\n"
        numberOfRooms = len(self.objectsOfTheRooms)
        roomsProcessed = 0
        for room in self.objectsOfTheRooms:
            self.objectsOfTheRoomsLine += room + "," \
                                          + self.objectsOfTheRooms[room][0] + "," \
                                          + self.objectsOfTheRooms[room][1]

            roomsProcessed += 1
            if roomsProcessed != numberOfRooms:  # if this is not the last item, add a linebreak
                self.objectsOfTheRoomsLine += "\n"

        self.totalCombinations = self.roomsOfTheObjectsLine + "\n\n\n" + self.objectsOfTheRoomsLine

        # Making into a CSV #
        makeIntoCSV(csvName=self.pathToParticipantDirectory + self.participantID + "_combinations.csv",
                    stringToWrite=self.totalCombinations)

    # Create a CSV for the participant's experiment results, and a CSV for their results with the combination of their
    # demographics, quiz attempts, and experiment results:
    def makeExperimentResults(self):

        # Making just the experiment results into a CSV #
        makeIntoCSV(csvName=self.pathToParticipantDirectory + self.participantID + "_experimentResults.csv",
                    stringToWrite=self.experimentResults)

        # Making the experiment results combined to the demographics into a CSV #

        # Creating a new first line:
        self.demographicsAndResults = "id,age,gender,education,student,fieldOfStudy,timeToCompleteDemographics," \
                                      "quizAttempts,phaseType,isPractice,blockNb,trialNb,trialType,postType,leftObjects," \
                                      "rightObjects,responseSide,responseTime,ghostSelected,ghostRejected,room1," \
                                      "rewardProbability1,isTreasure1,room2,rewardProbability2,isTreasure2\n"

        # Taking all but the first line of the experiment results
        experimentResults = self.experimentResults.split("\n")
        experimentResults = experimentResults[1:]

        # Taking all but the first line of the demographics
        demographics = self.demographicsLine.split("\n")
        demographics = demographics[1:]

        # Putting all the parts together
        for i in range(len(experimentResults) - 1):  # for some reason the last line is empty so we must get rid of that
            self.demographicsAndResults += self.participantID + "," \
                                           + demographics[0] + "," \
                                           + self.quizAttempts + "," \
                                           + experimentResults[i]
            if i != (len(experimentResults) - 2):  # if this is not the last line (before empty line) add a line break
                self.demographicsAndResults += "\n"

        # Making the CSV
        makeIntoCSV(csvName=self.pathToParticipantDirectory + self.participantID + "_demographicsAndResults.csv",
                    stringToWrite=self.demographicsAndResults)

    # Create a CSV for the participant's quiz attempts:
    def makeQuizAttempts(self):
        makeIntoCSV(csvName=self.pathToParticipantDirectory + self.participantID + "_quizAttempts.csv",
                    stringToWrite=self.quizAttempts)

    # Create a CSV and a figure of the gaussian random walk of the room's reward probabilities:
    def makeRandomWalk(self):
        # NOTE: I am trying to learn some new tools (pandas dataframes and plots) that make this process less cumbersome

        # Making a dataframe of the random walk
        randomWalkDataframe = pd.DataFrame(self.randomWalk, columns=list(self.randomWalk.keys()))
        # the number of times each room was incremented/number of trials (the number of rows)
        numberOfIncrements = randomWalkDataframe.shape[0]
        # create a list of the number of increments (starts with 0, because 0 is the starting reward probability)
        # (or before the trial start)
        numberOfIncrements = np.arange(0, numberOfIncrements).tolist()
        # add these as the first column of the dataframe
        randomWalkDataframe.insert(0, "trials", numberOfIncrements, True)

        # Making a CSV for the random walk #
        fileName = self.pathToParticipantDirectory + self.participantID + "_randomWalk.csv"
        randomWalkDataframe.to_csv(fileName, index=False)  # without the names of the rows

        # Making a line plot of the randomWalks #
        randomWalkPlot = randomWalkDataframe.plot(x="trials",
                                                  y=list(self.randomWalk.keys()),
                                                  kind="line",
                                                  grid=True,
                                                  color=list(self.randomWalk.keys()))  # same colours as the rooms
        randomWalkPlot.set(xlabel="Trials", ylabel="Reward Probabilities")  # change the axes labels
        plt.savefig(self.pathToParticipantDirectory + self.participantID + "_randomWalk.png")

    # This function updates an overall file with all the results:
    def updateAllResultsFile(self):
        # if the total file already exits...
        if self.totalFileName in self.allFilesInResults:
            # ...we want to take the demographics and results of the participant without the column names:
            demographicsAndResults = self.demographicsAndResults.split("\n")
            demographicsAndResults = demographicsAndResults[1:]
            demographicsAndResults = "\n".join(demographicsAndResults)
            demographicsAndResults = "\n" + demographicsAndResults
        # Otherwise we do want the column names:
        else:
            demographicsAndResults = self.demographicsAndResults

        # Append this participant's data to the total results data file: #
        # If there is no previous data file, opening with "a" will create a new one
        makeIntoCSV(csvName=self.pathToResults + self.totalFileName,
                    stringToWrite=demographicsAndResults,
                    openingStyle="a")

########################################################################################################################
