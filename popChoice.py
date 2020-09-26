########################################################################################################################
# This function will randomly chose a value from a list and take out that value from the list it was chosen from
########################################################################################################################

########################################
#                Imports               #
########################################
from random import choice
########################################


########################################
#               popChoice              #
########################################
def popChoice(listSelectedFrom):
    chosenValue = choice(listSelectedFrom)
    listSelectedFrom.pop(listSelectedFrom.index(chosenValue))
    return chosenValue

########################################################################################################################
