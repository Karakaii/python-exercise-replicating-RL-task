########################################################################################################################
# This is class to create all the objects for the experiment
########################################################################################################################

########################################
#                Imports               #
########################################
from psychopy import visual
from random import choice, shuffle
from popChoice import popChoice
########################################


########################################
#                Stimuli               #
########################################
class Stimuli:
    def __init__(self, window):
        self.window = window  # The psychopy window we are using

        self.pathToImages = "resources/"  # where we put the images

        # the different objects (needs the be the same names as the images)
        self.objectNames = ["key", "light", "phone", "stove"]
        self.objectImages = {}  # preparing to create the images
        self.objectSize = self.window.screen["quarterHeight"]  # square of the quarter of the size
        self.positionRectColour = [.5, .5, .5]  # a light grey

        # the different rooms (needs the be the same names as the images)
        self.roomNames = ["pink", "blue", "green", "brown"]
        self.roomImages = {}  # preparing to create the images
        self.roomSize = self.window.screen["height"] * .90  # Squares taking up most of the screen

        self.allImages = {}  # preparing to create the images

        # Preparing to record all the different combinations
        self.combiRoomsOfTheObjects = {}  # each object will be a key for a list with its two rooms
        self.combiObjectsOfTheRooms = {}  # each room will be a key for a list with its two objects

        # Creating a position rectangle for the objects (so that they are all in the same colour square when presented)
        self.positionRect = visual.Rect(
            win=self.window,
            units="pix",
            width=self.objectSize,
            height=self.objectSize,
            fillColor=self.positionRectColour,
            lineColor=self.positionRectColour)

        # Creating an empty rectangle with a border that surrounds the objects in the trials
        self.selectionContainer = visual.Rect(
            win=self.window,
            units="pix",
            width=self.objectSize + self.window.screen["containerGap"],
            # a height spacious enough for the trails with two objects and nice visual gaps
            height=self.objectSize * 2 + 2 * self.window.screen["containerGap"],
            lineColor=[-1, -1, -1],  # black
            lineWidth=5)

        # Creating the image for the treasure (the whole of the screen size)
        self.treasureImage = visual.ImageStim(
                win=self.window,
                image=self.pathToImages + "treasure.jpg",
                units="pix",
                size=self.window.size)

    # This is the function that users use. It will create the objects and their combinations
    def createStimuli(self):
        self.createObjects()
        self.createRooms()
        self.createCombinations()

    # Creating all objects and storing them in appropriate dictionaries
    # The use of their names as keys makes them easy to retrieve
    def createObjects(self):
        for name in self.objectNames:
            image = visual.ImageStim(
                win=self.window,
                image=self.pathToImages + name + ".png",
                units="pix",
                size=self.objectSize)

            self.objectImages[name] = image
            self.allImages[name] = image

    # Creating all rooms and storing them in appropriate dictionaries
    # The use of their names as keys makes them easy to retrieve
    def createRooms(self):
        for name in self.roomNames:
            image = visual.ImageStim(
                win=self.window,
                image=self.pathToImages + name + ".jpg",
                units="pix",
                size=self.roomSize)

            self.roomImages[name] = image
            self.allImages[name] = image

    # Randomly creates the combinations for each object and its associated rooms
    def createCombinations(self):
        roomNamesSelect = self.roomNames.copy()  # copy to avoid messing up
        roomNamesSelect = roomNamesSelect * 2  # need twice the rooms because each room has two objects

        objectsNamesSelect = self.objectNames.copy()  # copy to avoid messing up
        shuffle(objectsNamesSelect)

        # For each room create a key for which there is an empty list
        for room in self.roomNames:
            self.combiObjectsOfTheRooms[room] = []

        # For each object...
        for object in objectsNamesSelect:
            # ...randomly select a first room (and take that room out of the list) and...
            room1 = popChoice(roomNamesSelect)
            # ...randomly select a second room that cannot be the same as the first room.
            room2 = choice(roomNamesSelect)
            while room2 == room1:
                room2 = choice(roomNamesSelect)
            # take out the second room from the list
            roomNamesSelect.pop(roomNamesSelect.index(room2))

            # create the key of that object and put its two rooms in its list
            self.combiRoomsOfTheObjects[object] = [room1, room2]
            # append the object to each appropriate key of the object
            self.combiObjectsOfTheRooms[room1].append(object)
            self.combiObjectsOfTheRooms[room2].append(object)

    # This function can be used to draw a container on both sides of the screen
    def drawContainers(self):
        self.selectionContainer.pos = self.window.screen["left"]
        self.selectionContainer.draw()

        self.selectionContainer.pos = self.window.screen["right"]
        self.selectionContainer.draw()

########################################################################################################################
