#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum
import gpiozero

track = list()
rotate = list()

class ProgramState(Enum):
    START = 1
    RUNNING = 2


# TODO: make this into a real app
def user_interface(program_state=ProgramState.RUNNING):
    if program_state == ProgramState.START:
        introduction = "This program will allow you to control the Donkey. \n" \
                       "You can command robot to move forward by typing the distance, you want the robot to travel. \n" \
                       "If You wish to change the direction type: \n" \
                       "R - to turn right \n" \
                       "L - to turn left \n" \
                       "T - to turn back \n" \
                       "F - to finish giving the commands \n\n"

        print(introduction)


    user_input = list()
    while True:
        command = input(">")
        if command == 'F':
            break

        # translacja na wartość kąta obrotu i odległość
        # robiona głównie dla ułatwienia późniejszego preprocessingu
        if command == 'R':
            command = '-90'
        elif command == 'L':
            command = '90'
        elif command == 'T':
            command = '180'
        else:
            command = int(command)

        user_input.append(command)

    return user_input


def preprocessing(user_input):
    global track
    global rotate

    for i in range(len(user_input)):
        if type(user_input[i]) is int:
            if type(user_input[i]) == type(user_input[i-1]) and i != 0:
                track[-1] += user_input[i]
            else:
                track.append(user_input[i])
        else:
            if type(user_input[i]) == type(user_input[i - 1]) and i != 0:
                rotate[-1] += int(user_input[i])
            else:
                rotate.append(int(user_input[i]))


def setup():
    global track
    global rotate

    user_intput = user_interface(ProgramState.START)
    preprocessing(user_intput)

    # FIXME: usunąć te 2 linijki - są tylko do podglądu wyników preprocessingu
    print("Track: ", track)
    print("Rotate: ", rotate)

    return


def loop():
    global track
    global rotate
    return



setup()

# while True:
#     loop()