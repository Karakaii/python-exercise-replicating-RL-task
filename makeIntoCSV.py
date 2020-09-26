########################################################################################################################
# This function will streamline the process of making CSV by using only one line of code:
########################################################################################################################


#########################################
#              makeIntoCSV              #
#########################################
def makeIntoCSV(csvName, stringToWrite, openingStyle="w"):
    fileName = csvName
    csvFile = open(fileName, openingStyle)  # default will be to write
    csvFile.write(stringToWrite)
    csvFile.close()

########################################################################################################################
