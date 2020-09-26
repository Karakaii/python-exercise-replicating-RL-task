########################################################################################################################
# This is the gui using PyQt that will show the experiment set up form to the experimenter and the
# consent form/demographics form/instructions to participants.
# Using PyQt because the designer allows for a GUI that is a lot neater that using the GUI option from psychopy.
# This also allows me to better my OOP writing with PyQt
########################################################################################################################

#################################
#           Imports             #
#################################
from os import listdir
from PyQt5 import uic
from psychopy import core
from makeIntoCSV import makeIntoCSV
#################################


#################################
#              GUI              #
#################################
class experimentGUI:
    def __init__(self, uiFile, screenSizes, app):
        self.window = uic.loadUi(uiFile)  # create the window
        self.window.screen = screenSizes  # get the screenSizes
        self.app = app  # the app that will be launched

        # Create clock (using psychopy).
        # Time the participants in order to check if they are not just skipping through.
        self.demographicsClock = core.Clock()

    # The only function the user need to use, this launches the GUI.
    def launchGUI(self):
        self.setUp()
        self.window.showFullScreen()
        self.app.exec_()

    # This function using the screen values I have created to set a text widget at the top:
    def setTitleAtTop(self, widget):
        widget.setGeometry(0,
                           self.window.screen["guiGap"],
                           self.window.screen["width"],
                           # The titles are aligned centre, so this just ensures their text fits
                           50)  # The titles will fit in this height

    # This function hides children of container widgets:
    def hideWidgetChildren(self, widgetContainer, isToBeHidden):
        if isToBeHidden:
            for child in widgetContainer.children():
                child.hide()
        else:
            for child in widgetContainer.children():
                child.show()

    def setUp(self):
        # making the stacked widget the size of the screen and making sure it is on the first page.
        self.window.pages.setGeometry(0, 0, self.window.screen["width"], self.window.screen["height"])
        self.window.pages.setCurrentIndex(0)

        # putting 'continue' button at the bottom of the screen.
        self.window.continueButton.setGeometry(self.window.screen["midWidth"] - self.window.continueButton.width() / 2,
                                               self.window.screen["height"] - (self.window.continueButton.height() +
                                                                               self.window.screen["guiGap"]),
                                               self.window.continueButton.width(),
                                               self.window.continueButton.height())
        self.window.continueButton.clicked.connect(self.advance)  # connecting to main function.

        # putting error message above the 'continue' button.
        self.window.errorMessage.setGeometry(self.window.screen["midWidth"] - self.window.screen["width"] / 2,
                                             self.window.continueButton.y() - (self.window.errorMessage.height() +
                                                                               self.window.screen["guiGap"]),
                                             self.window.screen["width"],
                                             self.window.errorMessage.height())
        self.window.errorMessage.hide()

        # putting the page titles at the top of the screen.
        self.setTitleAtTop(self.window.consentFormTitle)
        self.setTitleAtTop(self.window.demographicsPageTitle)
        self.setTitleAtTop(self.window.instructionsTitle)
        self.setTitleAtTop(self.window.expPageTitle)

        # putting the help textBrowser for the experiment set up below the title on the first page
        self.window.experimentHelp.setGeometry(
            self.window.screen["midWidth"] - self.window.screen["midWidth"] / 2,
            self.window.expPageTitle.y() + self.window.expPageTitle.height() + self.window.screen["guiGap"],
            self.window.screen["midWidth"],
            self.window.screen["midHeight"] * .33)  # make its size proportional to screen size

        # putting the list of experiments combo box below the help text
        self.window.listOfExperimentsContainer.setGeometry(
            self.window.screen["midWidth"] - self.window.expFormContainer.width() / 2,
            self.window.experimentHelp.y() + self.window.experimentHelp.height() + self.window.screen["guiGap"],
            self.window.listOfExperimentsContainer.width(),
            self.window.listOfExperimentsContainer.height())
        # Connect to the function to reveal the experiment set up:
        self.window.listOfExperimentsBox.currentIndexChanged.connect(self.expSetUpReveal)

        # putting the main form for creating experiments below the list of experiments
        self.window.expFormContainer.setGeometry(
            self.window.screen["midWidth"] - self.window.expFormContainer.width() / 2,
            self.window.listOfExperimentsContainer.y() + self.window.listOfExperimentsContainer.height(),
            self.window.expFormContainer.width(),
            self.window.expFormContainer.height())
        # hiding it so that it can be revealed later on when selecting an experiment or the 'NEW EXPERIMENT' option
        # from the combo box:
        self.window.expFormContainer.hide()

        # Setting the warning signs for errors to the left of experiment creation options.
        # Image obtained at: https://www.pngguru.com/free-transparent-background-png-clipart-bkkxv
        self.window.expWarnings.setGeometry(
            self.window.listOfExperimentsContainer.x() - self.window.expWarnings.width(),
            self.window.listOfExperimentsContainer.y(),
            self.window.expWarnings.width(),
            self.window.expWarnings.height())
        # Hiding warning signs.
        self.hideWidgetChildren(self.window.expWarnings, True)

        # Collect all the files in the 'experimentFormats' folder and if they have "_settings.csv" in their name
        # their names will be added to the list of experiments that can be selected from the combo box.
        self.window.files = listdir("experimentFormats/")
        for file in self.window.files:
            if "_settings.csv" in file:
                fileName = file.split("_")  # This is why I instruct users to not put _ in their experiment names
                self.window.listOfExperimentsBox.addItem(fileName[0])  # the first part of the split is the name

        # Setting consent form text close to the centre (leaving space for check boxes).
        # QTextBoxes allow for participants to scroll to see all the information no matter the screen size.
        self.window.consentFormText.setGeometry(
            self.window.screen["midWidth"] - self.window.screen["midWidth"] / 2,
            self.window.screen["midHeight"] / 2 - self.window.screen["midHeight"] / 4,
            self.window.screen["midWidth"],
            self.window.screen["midHeight"])

        # putting the consent form check boxes below the consent form.
        self.window.checkBoxesContainer.setGeometry(
            self.window.screen["midWidth"] - self.window.checkBoxesContainer.width() / 2,
            self.window.consentFormText.y() + self.window.consentFormText.height(),
            self.window.checkBoxesContainer.width(),
            self.window.checkBoxesContainer.height())

        # putting the demographics form in the middle of the screen.
        self.window.demoLayoutContainer.setGeometry(
            self.window.screen["midWidth"] - self.window.demoLayoutContainer.width() / 2,
            self.window.screen["midHeight"] - self.window.demoLayoutContainer.height() / 2,
            self.window.demoLayoutContainer.width(),
            self.window.demoLayoutContainer.height())

        # Setting the warning signs for errors to the left of the demographics form.
        self.window.demoWarnings.setGeometry(self.window.demoLayoutContainer.x() - self.window.demoWarnings.width(),
                                             self.window.demoLayoutContainer.y(),
                                             self.window.demoWarnings.width(),
                                             self.window.demoWarnings.height())
        # Hiding warning signs.
        self.hideWidgetChildren(self.window.demoWarnings, True)

        # hiding the field of study options so that they can be revealed when checking the 'yes' radio button to the
        # question about being a student.
        self.window.fieldOfStudyLine.hide()
        self.window.fieldOfStudyLabel.hide()
        self.window.yesStudentRadio.toggled.connect(self.isStudentCheck)

        # Putting the instructions in the middle of the screen.
        self.window.instructionsText.setGeometry(
            self.window.screen["midWidth"] - self.window.screen["midWidth"] / 2,
            self.window.screen["midHeight"] - self.window.screen["midHeight"] / 2,
            self.window.screen["midWidth"],
            self.window.screen["midHeight"])

        # Putting the check below the instructions.
        # QTextBoxes allow for participants to scroll to see all the information no matter the screen size.
        self.window.instructionsCheck.setGeometry(
            self.window.screen["midWidth"] - self.window.instructionsCheck.width() / 2,
            self.window.instructionsText.y() + self.window.instructionsText.height() + 50,
            self.window.instructionsCheck.width(),
            self.window.instructionsCheck.height())

    # This function will react to changes in the combo box #
    def expSetUpReveal(self, index):
        # If the combo box is set back to the default option, it will hide the form and the help buttons.
        # Otherwise, it will show the help buttons and the main form.
        if index == 0:
            self.window.expFormContainer.hide()
        else:
            self.window.expFormContainer.show()

            # If the combo box is set to the NEW EXPERIMENT option it will call setBlankExpSettings() to make sure the
            # option of the experiment form are blank so that experimenters can fill them in.
            if index == 1:
                self.setBlankExpSettings()
                self.window.expFormContainer.setEnabled(True)

            # Otherwise, it means the name of a pre-created experiment is selected, thereby it will call
            # setPreviousExpSettings() in order to fill in the form.
            else:
                self.setPreviousExpSettings()
                self.window.expFormContainer.setEnabled(False)
        # Hide the error message and the warnings when the experiment selection changes:
        self.hideWidgetChildren(self.window.expWarnings, True)
        self.window.errorMessage.hide()

    # This function will be called when a previously created experiment is selected in the experiment list combo box.
    # It will fill in the form according to the settings file for this experiment.
    def setPreviousExpSettings(self):
        # prepare the path to the file, then open and read it.
        expFileName = "experimentFormats/" + self.window.listOfExperimentsBox.currentText() + "_settings.csv"
        expFile = open(expFileName, "r")
        currentExpSettings = expFile.read()
        expFile.close()

        # The file has a header line and a line with the values. This allows me to get an index for each value.
        # That way it is flexible if someone changes this code and wants to add settings differently.
        expInformation = currentExpSettings.split("\n")
        header = expInformation[0].split(",")
        values = expInformation[1].split(",")

        # Get all the information for the experiment set up:
        expSetUp = {"id": values[header.index("id")],
                    "quiz100": values[header.index("quiz100")],
                    "standardPracticeBlocks": int(values[header.index("standardPracticeBlocks")]),
                    "standardPracticeTrials": int(values[header.index("standardPracticeTrials")]),
                    "standardExperimentalBlocks": int(values[header.index("standardExperimentalBlocks")]),
                    "standardExperimentalTrials": int(values[header.index("standardExperimentalTrials")]),
                    "tripletPracticeBlocks": int(values[header.index("tripletPracticeBlocks")]),
                    "tripletPracticeTrials": int(values[header.index("tripletPracticeTrials")]),
                    "tripletExperimentalBlocks": int(values[header.index("tripletExperimentalBlocks")]),
                    "tripletExperimentalTrials": int(values[header.index("tripletExperimentalTrials")])}

        # Use this information to set every part of the form:
        # id
        self.window.expIDLine.setText(expSetUp["id"])

        # quiz 100% accuracy
        if expSetUp["quiz100"] == "yes":
            self.window.quizYes.setChecked(True)
        else:  # no
            self.window.quizNo.setChecked(True)

        # all the blocks and trials
        self.window.standardPracticeBlocksSpinBox.setValue(expSetUp["standardPracticeBlocks"])
        self.window.standardPracticeTrialsSpinBox.setValue(expSetUp["standardPracticeTrials"])
        self.window.standardExperimentalBlocksSpinBox.setValue(expSetUp["standardExperimentalBlocks"])
        self.window.standardExperimentalTrialsSpinBox.setValue(expSetUp["standardExperimentalTrials"])
        self.window.tripletPracticeBlocksSpinBox.setValue(expSetUp["tripletPracticeBlocks"])
        self.window.tripletPracticeTrialsSpinBox.setValue(expSetUp["tripletPracticeTrials"])
        self.window.tripletExperimentalBlocksSpinBox.setValue(expSetUp["tripletExperimentalBlocks"])
        self.window.tripletExperimentalTrialsSpinBox.setValue(expSetUp["tripletExperimentalTrials"])

    # This function will be called when NEW EXPERIMENT is selected in the experiment list combo box.
    # It will reset the form:
    def setBlankExpSettings(self):
        self.window.expIDLine.setText("")

        self.window.quizYes.setAutoExclusive(False)
        self.window.quizNo.setAutoExclusive(False)
        self.window.quizYes.setChecked(False)
        self.window.quizNo.setChecked(False)
        self.window.quizYes.setAutoExclusive(True)
        self.window.quizNo.setAutoExclusive(True)

        self.window.standardPracticeBlocksSpinBox.setValue(1)
        self.window.standardPracticeTrialsSpinBox.setValue(1)
        self.window.standardExperimentalBlocksSpinBox.setValue(1)
        self.window.standardExperimentalTrialsSpinBox.setValue(1)
        self.window.tripletPracticeBlocksSpinBox.setValue(1)
        self.window.tripletPracticeTrialsSpinBox.setValue(3)
        self.window.tripletExperimentalBlocksSpinBox.setValue(1)
        self.window.tripletExperimentalTrialsSpinBox.setValue(3)

    # If 'yes' radio button becomes checked, the field of study options will show, if no is checked, the field of study
    # options will be hidden.
    def isStudentCheck(self, isChecked):
        if isChecked:
            self.window.fieldOfStudyLine.show()
            self.window.fieldOfStudyLabel.show()
        else:
            self.window.fieldOfStudyLine.hide()
            self.window.fieldOfStudyLabel.hide()
            self.window.fieldOfStudyWarning.hide()

    # Checking if there is an error in a page, dependent on the type of page it is.
    def errorCheck(self, currentPage):
        isError = False

        if currentPage == 0:  # experiment set up

            # experiment needs a name
            if self.window.expIDLine.text() == "":
                isError = True
                self.window.experimentIDWarning.show()
            else:
                self.window.experimentIDWarning.hide()

            # need to set quiz accuracy
            if not self.window.quizYes.isChecked() and not self.window.quizNo.isChecked():
                isError = True
                self.window.experimentQuizWarning.show()
            else:
                self.window.experimentQuizWarning.hide()

            # Triplet trials need to be multiples of 3
            if int(self.window.tripletPracticeTrialsSpinBox.text()) % 3 != 0:
                isError = True
                self.window.tripletPracticeTrialsWarning.show()
            else:
                self.window.tripletPracticeTrialsWarning.hide()

            # Triplet trials need to be multiples of 3
            if int(self.window.tripletExperimentalTrialsSpinBox.text()) % 3 != 0:
                isError = True
                self.window.tripletExperimentalTrialsWarning.show()
            else:
                self.window.tripletExperimentalTrialsWarning.hide()

            # need to have made a selection
            if self.window.listOfExperimentsBox.currentText() == "Please select an experiment":
                isError = True
                self.window.experimentSelectWarning.show()

                # Hide the warnings for the elements that would be hidden if the experiment is not shown:
                self.window.experimentIDWarning.hide()
                self.window.experimentQuizWarning.hide()
                self.window.tripletPracticeTrialsWarning.hide()
                self.window.tripletExperimentalTrialsWarning.hide()
            else:
                self.window.experimentSelectWarning.hide()

        elif currentPage == 1:  # consentForm
            # error if one of the check boxes are not checked
            for checkBox in self.window.checkBoxesContainer.children():
                if not checkBox.isChecked():
                    isError = True

        elif currentPage == 2:  # demographics

            # Check that they are older than 18.
            if int(self.window.ageSpinBox.text()) < 18:
                isError = True
                self.window.ageWarning.show()
            else:
                self.window.ageWarning.hide()

            # A gender must be selected.
            if not self.window.maleRadio.isChecked() and not self.window.femaleRadio.isChecked() \
                    and not self.window.otherRadio.isChecked():
                isError = True
                self.window.genderWarning.show()
            else:
                self.window.genderWarning.hide()

            # An education level other than the default sentence must be selected.
            if self.window.educationList.currentText() == "Please select the furthest one completed":
                isError = True
                self.window.educationWarning.show()
            else:
                self.window.educationWarning.hide()

            # Either yes or no for the student status must be check.
            if not self.window.yesStudentRadio.isChecked() and not self.window.noStudentRadio.isChecked():
                isError = True
                self.window.studentWarning.show()
            else:
                self.window.studentWarning.hide()

            # If the yes to the student status is selected, something must be written there.
            if self.window.yesStudentRadio.isChecked() and self.window.fieldOfStudyLine.text() == "":
                isError = True
                self.window.fieldOfStudyWarning.show()
            else:
                self.window.fieldOfStudyWarning.hide()

        else:  # instructions page
            # error if the check box is not checked.
            if not self.window.instructionsCheck.isChecked():
                isError = True

        return isError

    # Every time the 'continue' button is pressed, the advance() function will behave according to the needs of the
    # current page in the stacked widget.
    def advance(self):
        currentPage = self.window.pages.currentIndex()
        isError = self.errorCheck(currentPage)

        if currentPage != 3:  # experiment setUp, consent form, or demographics form

            if not isError:
                self.window.errorMessage.hide()
                self.window.pages.setCurrentIndex(currentPage + 1)  # move to next page
            else:  # show error message as long as there is an error
                self.window.errorMessage.show()

        else:  # instructions page
            if not isError:
                # get the demographics information:
                self.generateDemographics()
                # get experiment information:
                self.generateExperimentSetUp()

                # end the application and close the window:
                self.window.close()
                self.app.exit()

            else:  # show error message as long as there is an error
                self.window.errorMessage.show()

    # This function will use the information from the demographics form in order to prepare a demographics variable
    # with all the information needed.
    def generateDemographics(self):
        # Age #
        age = str(self.window.ageSpinBox.text())

        # Gender #
        if self.window.femaleRadio.isChecked():
            gender = "female"
        elif self.window.maleRadio.isChecked():
            gender = "male"
        else:
            gender = "other"

        # Education level #
        education = str(self.window.educationList.currentIndex())

        # If they are a student and their field of study #
        if self.window.yesStudentRadio.isChecked():
            studentStatus = "yes"
            fieldOfStudy = self.window.fieldOfStudyLine.text()
        else:
            studentStatus = "no"
            fieldOfStudy = "NA"

        # Time to complete #
        timeToComplete = str(self.demographicsClock.getTime())

        self.participantDemographics = {"age": age, "gender": gender,
                                        "education": education, "student": studentStatus, "fieldOfStudy": fieldOfStudy,
                                        "timeToComplete": timeToComplete}

    # This function will prepare the experiment set up information and write a new experiment settings.csv if a new
    # experiment was created:
    def generateExperimentSetUp(self):
        # prepare the experiment set up information:
        self.experimentSetUp = {"standardPractice":
                                    {"blocks": int(self.window.standardPracticeBlocksSpinBox.text()),
                                     "trials": int(self.window.standardPracticeTrialsSpinBox.text())},
                                "standardExperimental":
                                    {"blocks": int(self.window.standardExperimentalBlocksSpinBox.text()),
                                     "trials": int(self.window.standardExperimentalTrialsSpinBox.text())},
                                "tripletPractice":
                                    {"blocks": int(self.window.tripletPracticeBlocksSpinBox.text()),
                                     "trials": int(self.window.tripletPracticeTrialsSpinBox.text())},
                                "tripletExperimental":
                                    {"blocks": int(self.window.tripletExperimentalBlocksSpinBox.text()),
                                     "trials": int(self.window.tripletExperimentalTrialsSpinBox.text())}}

        # quiz 100% accuracy:
        if self.window.quizYes.isChecked():
            self.quiz100 = True  # This variable is used for the setting of the quiz
            quizForFile = "yes"  # This variable is used for the settings.csv file
        else:  # not checked
            self.quiz100 = False
            quizForFile = "no"

        # If this is a new experiment (there is no settings file for it) create one:
        self.experimentID = self.window.expIDLine.text()
        if self.experimentID + "_settings.csv" not in self.window.files:
            # the header and value lines are created here:
            settingsText = f"id,quiz100,standardPracticeBlocks,standardPracticeTrials,standardExperimentalBlocks," \
                           f"standardExperimentalTrials,tripletPracticeBlocks,tripletPracticeTrials," \
                           f"tripletExperimentalBlocks,tripletExperimentalTrials\n" \
                           f"{self.experimentID}," \
                           f"{quizForFile}," \
                           f"{self.window.standardPracticeBlocksSpinBox.text()}," \
                           f"{self.window.standardPracticeTrialsSpinBox.text()}," \
                           f"{self.window.standardExperimentalBlocksSpinBox.text()}," \
                           f"{self.window.standardExperimentalTrialsSpinBox.text()}," \
                           f"{self.window.tripletPracticeBlocksSpinBox.text()}," \
                           f"{self.window.tripletPracticeTrialsSpinBox.text()}," \
                           f"{self.window.tripletExperimentalBlocksSpinBox.text()}," \
                           f"{self.window.tripletExperimentalBlocksSpinBox.text()}"
            makeIntoCSV(csvName="experimentFormats/" + self.experimentID + "_settings.csv",
                        stringToWrite=settingsText)

########################################################################################################################
