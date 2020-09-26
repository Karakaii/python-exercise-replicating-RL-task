########################################################################################################################
# This function will randomly sample a value from a gaussian distribution of mu and sigma and increment the room
# reward probability with this value as long as the value is not above 1 or below 0.
########################################################################################################################

########################################
#                Imports               #
########################################
from random import gauss
########################################


########################################
#           gaussianIncrement          #
########################################
def gaussianIncrement(roomRewardProbability, mu, sigma):
    increment = gauss(mu=mu, sigma=sigma)
    while (roomRewardProbability + increment) < 0 or (roomRewardProbability + increment) > 1:
        increment = gauss(mu=mu, sigma=sigma)
    roomRewardProbability += increment
    return roomRewardProbability

########################################################################################################################
