## What is this?

This is the result of a python coding assignment for an MSc course at UCL.
We had to 'replicate' the methodology of an experiment. I choose to replicate the methodology of: 

Moran, R., Keramati, M., Dayan, P., & Dolan, R. J. (2019). Retrospective model-based inference guides model-free credit assignment. *Nature Communications, 10*(1), 750. [https://doi.org/10.1038/s41467-019-08662-8](https://doi.org/10.1038/s41467-019-08662-8)

## How to use it

To use this replication of Moran et al.’s (2019) experiment please read the following instructions:
1.	The only file you need to launch is the MAIN.py file. For the experimenter it will present the experiment set up form. For the participant it will then present the consent form, then the demographics form, then the instructions, then the quiz, then the experiment, and finally it will generate the result files.
2.	In the experiment set up form you can select either a pre-existing experiment set up or create a new one by selecting 'NEW EXPERIMENT':
    1.	Give it an ID, preferably an easier to understand one. It MUST NOT have an underscore _ in its name.
    2.	Tick yes or no as to whether the participants need to be 100% accurate in the quiz in order to continue on to the trials. This is useful if you just want to check the functioning of the code (e.g., if you are a marker).
    3.	The triplet trial numbers MUST be multiples of 3, and it is best if they are multiples of 12.
    4.	The standard trial numbers can be any number but it is best if they are multiples of 6.
3.	You will see an explanation of the different column names from the results files in *explainingResults/explainingResultsColumnNames.xlsx*
4.	Libraries used:
    1.	PyQt
    2.	PsychoPy
    3.	pandas
    4.	numpy
    5.	random
    6.	os
    7.	matplotlib
    8.	math
    9.	itertools


*Note. Psychopy sometimes crashes for no apparent reason (I have read that psychopy has a gamma issue with windows?). If this happens please force it to end and retry it.*