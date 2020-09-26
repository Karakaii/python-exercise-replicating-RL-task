########################################################################################################################
# This is where we create the core of the experiment: Creates and runs all the trials.
########################################################################################################################

########################################
#                Imports               #
########################################
# Other modules
import numpy as np
from random import choice, shuffle
from itertools import combinations
from math import ceil
# My modules
from trials import TrialTriplet, StandardTrial
from waitText import waitText
from popChoice import popChoice
from gaussianIncrement import *
########################################


########################################
#             Experiment               #
########################################
class Experiment:

    def __init__(self, window, stimuliClass, experimentalSetUp):
        self.window = window
        self.stimuliClass = stimuliClass
        self.experimentalSetUp = experimentalSetUp  # the phases, blocks and amounts of trials

        # having the three types of trials possible:
        self.trialTypes = ["standard", "uncertain", "post"]

        # Creating all the possible pairs of objects:
        self.standardStimuliPairs = list(combinations(self.stimuliClass.objectNames, 2))
        # Getting the number of possible pairs (There will be 6, but I kept flexibility):
        self.nbStandardPairs = len(self.standardStimuliPairs)

        # Get all the pairs of objects for each room (there should be 4 pairs, because there are 4 rooms):
        eligibleStimuliPairs = []
        # For each room (here the key for each of it's two objects)...
        for room in self.stimuliClass.combiObjectsOfTheRooms:
            # append the pair of objects related to that room
            eligibleStimuliPairs.append(self.stimuliClass.combiObjectsOfTheRooms[room])

        # Get the possible comparisons for uncertainty trials
        # (that should be 2, because we only want to compare pairs of objects that do not have the same common room,
        # and you cannot compare pairs that have the same object)
        self.eligibleUncertaintyComparisons = []
        comparison = []  # make the current comparison empty
        # for every 2 object pair (hence, 2 iterations)...
        for i in range(int(len(eligibleStimuliPairs) / 2)):
            # ...select one pair randomly to be the first pair of the comparison
            pair1 = choice(eligibleStimuliPairs)

            # If this first pair was already in the comparison list choose another one;
            # namely, if this is the second iteration, and the pair randomly chosen was in the previous comparison
            # (i.e., it was either the previous pair 1 or 2).
            while pair1 in comparison:
                pair1 = choice(eligibleStimuliPairs)

            # Randomly select pair 2, but if there is any object of pair two in pair1, choose again.
            pair2 = choice(eligibleStimuliPairs)
            while (pair2[0] in pair1) or (pair2[1] in pair1):
                pair2 = choice(eligibleStimuliPairs)

            # This forms the comparison, append it to the eligible comparisons for uncertainty trials.
            # If this is the first comparison it will be used to avoid selecting the same comparison as the second one.
            comparison = [pair1, pair2]
            self.eligibleUncertaintyComparisons.append(comparison)
        self.nbUncertaintyComparisons = len(self.eligibleUncertaintyComparisons)  # There will be 2, kept flexibility

        # The post trial types and their number (there will be 3 but I keep this flexibility).
        self.postTypes = ["repeat", "switch", "clash"]
        self.nbPostTypes = len(self.postTypes)

        # The possible ghostChoices, the object indexed 0 or indexed 1 of the pair chosen by the participant.
        # This allows it to be counterbalanced.
        self.ghostChoices = [0, 1]

        # Getting the starting probabilities of the different rooms:
        # Create a list of probabilities ranging from .25 to .75 with increments of .5
        startingProbabilities = np.arange(0.25, 0.75, 0.05).tolist()
        # for each of these probabilities neatly round them to two decimals (otherwise the numbers are not nicely round)
        for i in range(len(startingProbabilities)):
            startingProbabilities[i] = round(startingProbabilities[i], 2)
        # for each room, randomly select a possible starting probability and take it out so that the other rooms will
        # have to have a different starting probability
        # Also prepare the dictionary that will record the random walk of the rooms' probabilities:
        self.rewardProbabilities = {}
        self.randomWalk = {}
        for room in self.stimuliClass.roomNames:
            self.rewardProbabilities[room] = popChoice(startingProbabilities)
            # start a list for this random walk with the first value being the starting probability:
            self.randomWalk[room] = [self.rewardProbabilities[room]]

        # Recording the responses:
        self.results = "phaseType,isPractice,blockNb,trialNb,trialType,postType,leftObjects,rightObjects," \
                       "responseSide,responseTime,ghostSelected,ghostRejected,room1,rewardProbability1," \
                       "isTreasure1,room2,rewardProbability2,isTreasure2\n"
        self.currentTrialNb = 0

    # This function will use all the bits previously created to create the trials:
    # It will be called in each different phase of the experiment, the phase indicating what kind of trial to make
    # and how many of them.
    # NOTE: the function ceil rounds up no matter the decimals (cannot have half trials)
    def createTrials(self, phase, isPractice):
        trials = []

        nbTrials = self.experimentalSetUp[phase]["trials"]

        if "standard" in phase:
            repetitions = ceil(nbTrials / self.nbStandardPairs)  # every 6 possible pairs, there is a repetition
            # have each possible stimuli pair for a standard trial as many times as there are repetitions
            standardTrialElements = self.standardStimuliPairs * repetitions
            # for a good counterbalancing it is best to have standard trials in multiples of 6

            # for each trial create a standard trial
            for i in range(nbTrials):
                # for each trial, increment the reward probabilities of the rooms
                self.incrementProbabilities()
                # this will be the reward probabilities of the rooms for this standard trial
                rewardProbabilities = {"standard": self.rewardProbabilities}

                standardTrial = StandardTrial(window=self.window,
                                              stimuliClass=self.stimuliClass,
                                              standardType=standardTrialElements[i],
                                              isPractice=isPractice,  # tells if practice trial or not
                                              rewardProbabilities=rewardProbabilities)
                trials.append(standardTrial)

        else:  # if triplet
            repetitions = ceil(nbTrials / (self.nbPostTypes * self.nbUncertaintyComparisons))
            # every 6 trials means we went through 2 triplets, which means one repetition because there are 2 possible
            # comparisons with 3 post trials each.

            ghostElements = self.ghostChoices * repetitions * self.nbPostTypes
            # for each repetition there will be 2*3 = 6 elements, three 0s and three 1s. So that each type of post trial
            # has a version with 0 being the ghost-selected object and a version with 1 being the ghost-selected object.

            postTypeElements = self.postTypes * repetitions * self.nbUncertaintyComparisons
            # for each repetition there will be 3*2 = 6 elements, two of each post type.

            standardTrialElements = self.standardStimuliPairs * ceil(repetitions / 2)
            # for every 2 repetition there will be 6 elements, one per post trial.
            # For a triple to have one of each instance it is best if the repetition is multiples of 2;
            # hence, the number of trials should be a multiple of 12.

            # Despite trials in multiple of 12 being the best, this still allows to create triplets
            # if the trials are multiples of 3 #
            trials = []
            # for every three trials
            for i in range(ceil(nbTrials / self.nbPostTypes)):

                # Create a dictionary that will hold the reward probabilities for each trial type, after having
                # incremented them every time (i.e., the standard trial comes first, so the probabilities will be
                # incremented once, then the uncertainty trial comes with the probabilities being incremented a
                # second time, etc.)
                rewardProbabilities = {}
                for trialType in self.trialTypes:
                    self.incrementProbabilities()
                    rewardProbabilities[trialType] = self.rewardProbabilities

                triplet = TrialTriplet(window=self.window,
                                       stimuliClass=self.stimuliClass,
                                       uncertaintyComparison=self.eligibleUncertaintyComparisons[i % 2],
                                       ghostType=ghostElements[i],
                                       postType=postTypeElements[i],
                                       standardType=standardTrialElements[i],
                                       isPractice=isPractice,  # tells if practice triplet or not
                                       rewardProbabilities=rewardProbabilities)
                trials.append(triplet)
                # i % 2 returns 0 if even and 1 if odd. This means that if the iteration is even, the first eligible
                # comparison (index 0) will be selected, if the iteration is odd, the second eligible comparison will
                # be selected.

        # shuffle the trials
        # (shuffle the different standard trials OR)
        # (the triplets will keep the standard/uncertainty/post order, but which triplet will be when will be shuffled)
        shuffle(trials)
        return trials

    # This function increments the probabilities for th rooms by applying my gaussianIncrement function on each room:
    def incrementProbabilities(self):
        for room in self.rewardProbabilities:
            self.rewardProbabilities[room] = gaussianIncrement(roomRewardProbability=self.rewardProbabilities[room],
                                                               mu=0,
                                                               sigma=0.025)
            # keep record of the random walk:
            self.randomWalk[room].append(self.rewardProbabilities[room])

    # This is the function that launches the experiment (it will be launched from the quizz)
    def launchExperiment(self):

        # The phases of an experiment can be experimental/practice and triplet/standard
        for phase in self.experimentalSetUp:

            # Make message where participants have to press the spacebar to continue (using waitText function).
            # Content of the message depends on whether it is a standard or triplet phase.
            if "standard" in phase:
                phaseType = "standard"
                phaseText = "This is a standard phase. On each trial you will be presented with two objects." \
                            "\n" \
                            "\n- Press the LEFT ARROW KEY to select the LEFT object." \
                            "\n- Press the RIGHT ARROW KEY to select the RIGHT object." \
                            "\n" \
                            "\nYou will then be presented with the two rooms that this object opens." \
                            "\n" \
                            "\nEach room has a probability to yield a treasure. If the room yielded a treasure during" \
                            " your current visit, there will be gold coins on the screen."

            else:  # it is triplet
                phaseType = "triplet"
                phaseText = "This is a triplet phase." \
                            "\nOn some trials you will be presented with two objects and on some trials you will be " \
                            "presented with two pairs of objects." \
                            "\n" \
                            "\n- Press the LEFT ARROW KEY to select the LEFT objects." \
                            "\n- Press the RIGHT ARROW KEY to select the RIGHT objects." \
                            "\n" \
                            "\nIf there is only one object you will be presented with the two rooms that this object" \
                            " opens." \
                            "\n" \
                            "\nIf you selected a pair of objects, a ghost that haunts the castle will randomly select" \
                            " one of the two objects and you will be presented with the rooms of that object." \
                            "\n" \
                            "\nEach room has a probability to yield a treasure. If the room yielded a treasure during" \
                            " your current visit, there will be gold coins on the screen."
            phaseText += "\n\nPress the SPACEBAR to continue."
            waitText(self.window, phaseText)

            # Make message where participants have to press the spacebar to continue (using waitText function).
            # Content of the message depends on whether it is a practice or experimental phase.
            if "Practice" in phase:
                isPractice = True  # will tell the trial creation if it IS a practice
                resultsIsPractice = "1"
                practiceOrExperimental = "PRACTICE"
                timingCondition = "\n\nYou have as much time as you want to give your answers."
            else:
                isPractice = False  # will tell the trial creation if it is NOT a practice
                resultsIsPractice = "0"
                practiceOrExperimental = "EXPERIMENTAL"
                timingCondition = "\n\nCAREFUL! You have 2 seconds from the beep to give your answers."
            waitText(self.window, f"{practiceOrExperimental} TRIALS. Press the SPACEBAR when you are ready to start."
                                  f"{timingCondition}")

            # For each block in the phase, create the trials and wait message to announce which block it is:
            for block in range(self.experimentalSetUp[phase]["blocks"]):
                trials = self.createTrials(phase, isPractice)
                waitText(self.window, f"BLOCK {block + 1} OF {self.experimentalSetUp[phase]['blocks']}. "
                                      f"Press the SPACEBAR when you are ready to start.")

                # For each trial, run that trial/triplet:
                for trial in trials:
                    trial.runTrials()

                    # And record the results:
                    if trial.myType == "standard":
                        self.currentTrialNb += 1
                        self.results += phaseType + "," + resultsIsPractice + "," + str(block+1) + "," + str(
                            self.currentTrialNb) + "," + trial.trialResults
                    else:  # it is a triplet
                        tripletResults = trial.trialResults
                        tripletResults = tripletResults.split("\n")
                        # this will create four values, but the fourth one is empty so it doesn't interest us:
                        for i in range(len(tripletResults) - 1):
                            self.currentTrialNb += 1
                            self.results += phaseType + "," + resultsIsPractice + "," + str(block+1) + "," + str(
                                self.currentTrialNb) + "," + tripletResults[i]

                            # if this is not the last line, add a line break:
                            if i != (len(tripletResults) - 1):
                                self.results += "\n"

        # debriefing message before the end:
        waitText(self.window, "Thank you for taking part in our study."
                              "\n"
                              "\nThis study was investigating aspects of model-based and model-free reinforcement"
                              " learning."
                              "\n"
                              "\nIf you want to learn more you can read Moran et al. (2019) - Retrospective model-based"
                              " inference guides model-free credit assignment."
                              "\n"
                              "\nPress the SPACEBAR to end the experiment.")

########################################################################################################################
