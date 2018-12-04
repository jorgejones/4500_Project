#!/usr/bin/env python3

'''
Development Team:
Andrew Audrain, Eric Goodwin, Jorge Jones, Nick Wooldridge, RJ Liceralde

Concept:
This game tests children's understanding and comprehension of the standard, addative color wheel.
There are two modes to this game.  Each mode uses the file provided by Anki called color_finder.py.  This file has been
modified to meet the needs of this program and therefore to execute this game, must use the version of the file
included in this bundle.  Modifications to be documented in color_finder.py

The mode is chosen at random when program is executed.

-FUTURE DEVELOPMENT: Add a GUI to let user select game mode and to run progrm again without needed to run via command
line-

Mode 1 - tests children's knowledge of complementary (opposite) colors as defined addative color wheel.
Mode 2 - tests children's knowledge of combining primary colors to form a secondary color.

Both game modes use the color_finder.py file and both use the cards provided.

In mode 1, Cozmo speaks one color and asks the user what color is opposite.  Cozmo then drives off the charger in search
of that color.

In mode 2, Cozmo speaks two colors and asks the user what color is made by the two colors.  Cozmo then drives off the
charger in search of that color.

Cozmo will continue to search for that color until his sensor detects.  BE AWARE - Cozmo can detect color for objects
other than then cards provided.

-FUTURE DEVELOPMENT: Develop a method for Cozmo to only consider the colors on the card.  Possible to use the
custom markers provided by Anki to accomplish this. -]


During gameplay, child may tap the provided cube to get a hint

Equipment required:
Cozmo robot, Cozmo Cubes, color cards (any source of color can be used in lieu of the cards), iOS/Andriod phone running
the Anki application, a PC/Mac to run the software.

Software required:
Python running interrupter 3.7, updated Anki application

Files required:
main.py - execute this file
color_finder.py

Important information regarding cubes:
Each cube does provide functionality to color_finder.py.

DO NOT PROVIDE THESE CUBES TO THE CHILD:
Cube that lights up in a solid color shows the current color Cozmo is looking for.  When tapped, it changes
the color Cozmo is looking for.
Cube that has the blinking lights will change the view mode on the PC to Cozmo's grid mode.  This allows the person
controller the game execution to see what colors are in Cozmo's view.

PROVIDE THIS CUBE TO THE CHILD:
Cube with no lights, when tapped, Cozmo will stop looking for a color, give a hint and then start looking for the color
again.

KNOWN ISSUES:
COZMO currently has difficulty detecting Purple.  Uncertain if it is due to the HSV values set in color_finder.py,
game being played in variable lighting conditions, or issue with the printing of the test cards.

COZMO looks around for the colors be rotating his head and this can cause him to look at the table.  Depending
on the color of the table, Cozmo can detect the color that is being searched for in the table. Example - if searching
for Orange or Red, a brown table may satisfy the search

Lighting plays an important roll in Cozmo's ability to accurately detect colors.  Playing the game in a well lit
area increases reliability of Cozmo's color detection.
'''


import numpy
import cozmo
import time
import asyncio
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import color_finder
import functools
import sys
import random


'''
color_list order is in order of color wheel going clockwise
Important - do not change the order of this list.  Mode 1 requires this specific order to correctly calculate
which complemmentary color will be passed to the color object
'''
color_list = ["yellow", "green", "blue", "purple", "red", "orange"]

'''
each of these lists are needed to control Mode 2 of the program.
mode 2 uses the index to calculate what color is being looked for.  
use caution when changing, addeding, or removing colors from this list.  
'''
primary_color_list = ['yellow', 'blue', 'red']
secondary_color_list = ['green', 'orange', 'purple']

'''
game_selector = 0 - Cozmo provides two primary colors and user displays 1 secondary color in response
game_selector = 1 - Cozmo provides one primary or secondary color and user days complimentary color according to color
wheel
'''

'''
Selecting game mode is a simple random roll of either 0 or 1.  uncomment game_selector = 1 to force a game mode.
consulate above list to determine which game to force
'''

# game_selector = 1

# determine which game is going to run
game_selector = random.randint(0, 1)



'''
Ecah game mode must be declare as async due to color_finder.py use of async functions.
args - cozmo.robot.Robot to pass robot to the function
'''
async def gameOne_cozmo_program(robot: cozmo.robot.Robot):

    # determine a random number between 0 and 5 to determine which color Cozmo will speak
    index = random.randint(0, 5)
    # this calculation determines the color that is passed to the color_finder object.
    # order that the colors appear in the color_list array is the order on the addative color wheel
    # if that list is changed, the following formula will no longer generate the correct complementary color

    correct_color_to_find = (index + 3) % len(color_list)

    # these lines used for testing.  allows developers to monitor what colors are being selected
    # print(correct_color_to_find)
    # print(color_list[correct_color_to_find])


    # prompt for the user that begins the game
    await robot.say_text("What color is opposite of " + color_list[index]).wait_for_completed()

    '''
    color_finder_game object is dependent on the imported color_finder.py file.  
    this file is part of the Anki SDK but is modified for this game. 
    changes made color_finder.py will affect the execution of main.py
    modifications made have been documented in color_finder.py
    ARGS - color_list[correct_color_to_find] is a string that is used to initialize the object with the 
    color that Cozmo will search for
    '''
    color_finder_game = color_finder.ColorFinder(robot, color_list[correct_color_to_find])

    # execute the color_finder object
    await color_finder_game.run()



async def gameTwo_cozmo_program(robot: cozmo.robot.Robot):


    # colors_not_different purpose to ensure that Cozmo doesn't select te same primary color for both inputs
    colors_not_different = True
    color_to_pass = ""

    # select a random primary color
    primary_color_1_selected_index = random.randint(0, 2)
    primary_color_2_selected_index = 0

    # select a second random primary color.  the while loop ensures the same color is not selected twice
    while colors_not_different:
        primary_color_2_selected_index = random.randint(0, 2)
        if primary_color_1_selected_index is not primary_color_2_selected_index:
            colors_not_different = False

    # Next two lines for tesing during development
    # print(primary_color_list[primary_color_1_selected_index])
    # print(primary_color_list[primary_color_2_selected_index])


    # selects the color that cozmo will look for

    # this formula determines what color is selected that cozmo is looking for as for the chart below
    # if correct_color_to_find = 1 : Green
    # if correct_color_to_find = 2 : Orange
    # if correct_color_to_find = 3 : Purple

    # calculation to determine which elment in the color_list Cozmo will select.  the adjusment of -1 due to
    # 0 indexing
    correct_color_to_find_index = (primary_color_1_selected_index + primary_color_2_selected_index) - 1


    # cozmo will speak the two colors that he is looking forward
    await robot.say_text("What color is made by " + primary_color_list[primary_color_1_selected_index] +
                         " and" + primary_color_list[primary_color_2_selected_index]).wait_for_completed()

    # print statment for testing
    print("index: " + str(correct_color_to_find_index))

    # declare the object color)_finder_game
    # ARGS - robot, and array color_list and index correct_color_to_find
    print("i am looking for" + secondary_color_list[correct_color_to_find_index])

    '''
    color_finder_game object is dependent on the imported color_finder.py file.  
    this file is part of the Anki SDK but is modified for this game. 
    changes made color_finder.py will affect the execution of main.py
    modifications made have been documented in color_finder.py
    ARGS - color_list[correct_color_to_find] is a string that is used to initialize the object with the 
    color that Cozmo will search for
    '''

    color_finder_game = color_finder.ColorFinder(robot, secondary_color_list[correct_color_to_find_index])


    # run the color_finder_object
    await color_finder_game.run()

    # following code is for development and testing

    if correct_color_to_find_index == 1:
        color_to_pass = "Purple"
    elif correct_color_to_find_index == 2:
        color_to_pass = "Orange"
    else:
        color_to_pass = "Green"


    #bprint(color_to_pass)
    # print(correct_color_to_find)

    # await robot.say_text(color_to_pass + "is correct!  Great job!").wait_for_completed()





# When both colors are detected, Cozmo congratulates the players, speaks their names and preforms a dance



# this code is the execution of either of the two game modes depending game_selector
if game_selector == 1:
    cozmo.run_program(gameTwo_cozmo_program, use_viewer=True)
else:
    cozmo.run_program(gameOne_cozmo_program, use_viewer=True)
