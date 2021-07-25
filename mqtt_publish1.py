import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from enum import Enum

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
        command = input(">")
        

        # translacja na wartość kąta obrotu i odległość
        # robiona głównie dla ułatwienia późniejszego preprocessingu
        if command == 'F':
            command = 'STOP'  

        # user_input.append(command)
        client.publish("COMMANDS", command)
        print("Just published " + str(command) + " to Topic COMMANDS")
        time.sleep(1)

        if command == 'F':
            break


user_interface()
# message = user_interface()
# client.publish("TEMPERATURE", message)
# print("Just published " + str(message) + " to Topic TEMPERATURE")
# time.sleep(1)