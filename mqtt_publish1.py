import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from enum import Enum
import os

mqttBroker = "192.168.1.113"
client = mqtt.Client("User")
client.connect(mqttBroker)

class ProgramState(Enum):
    START = 1
    RUNNING = 2



def user_interface(program_state=ProgramState.START):
    if program_state == ProgramState.START:
        introduction = "This program will allow you to control the Donkey. \n" \
                       "You can command robot to move forward by typing the distance, you want the robot to travel. \n" \
                       "If You wish to change the direction type: \n" \
                       "R - to turn right \n" \
                       "L - to turn left \n" \
                       "T - to turn back \n" \
                       "F - to finish giving the commands \n\n"

        print(introduction)

    command = 'START'
    client.publish("COMMANDS", command)
    print("Just published " + str(command) + " to Topic COMMANDS")
    time.sleep(1)

    while True:
        try:
            command = input(">")

            if command not in ['R', 'L', 'T', 'F', 'STOP']:
                # sprawdza czy input jest liczbą
                try:
                    int(command)
                except:
                    raise ValueError(f"Invalid command. You entered '{command}'. Command can be only an int() number or R, L, T, F")

        
            if command == 'F':
                command = 'STOP'  

            # user_input.append(command)
            client.publish("COMMANDS", command)
            print("Just published " + str(command) + " to Topic COMMANDS")
            time.sleep(1)

            if command == 'STOP':
                break

        except ValueError as input_exeption_msg:
            print(input_exeption_msg)


user_interface()
# 1345os.system('kill SIGINT2')
# message = user_interface()
# client.publish("TEMPERATURE", message)
# print("Just published " + str(message) + " to Topic TEMPERATURE")
# time.sleep(1)