# !/bin python
# -*- coding: utf-8 -*- 

import RPi.GPIO as io
from time import sleep

io.setmode(io.BCM)

#TODO: obsluzyc wyjatki
class MotorWithEncoder:
    def __init__(self, DIR_pin, PWM_pin, ENC_pin=None, circ=339.12, statesPerRotation=64):
        io.setup(DIR_pin, io.OUT)
        io.setup(PWM_pin, io.OUT)
        
        #Motor
        self.DIR_pin = DIR_pin
        self.PWM_pin = PWM_pin
        self.PWM_MAX = 100

        self.PWM = io.PWM(PWM_pin, self.PWM_MAX)

        #Encoder
        if ENC_pin is not None:
            self.ENC_pin = ENC_pin
            io.setup(ENC_pin, io.IN, pull_up_down=io.PUD_UP)
            self.stateLast = io.input(ENC_pin)
            self.rotationCount = 0
            self.stateCount = 0
            self.stateCountTotal = 0
            self.distance = 0

        if ENC_pin is None:
            raise Warning('Warning! You have to specify encoder channel.')

        # TODO: zmierzy dokladnie z opona
        self.circ = circ #mm
        self.statesPerRotation = statesPerRotation
        self.distancePerStep = circ / statesPerRotation

    def run(self, speed=0, direction='F'):
        if direction == 'F':
            io.output(self.DIR_pin, io.LOW)
        elif direction == 'B':
            io.output(self.DIR_pin, io.HIGH)
        else:
            raise ValueError('Wrong direction. Should be "F" or "B"')

        if speed < 0 or speed > 100:
            raise ValueError('Speed is not between <0, 100>.')
        
        self.PWM.start(speed)
        self.measure_distance()

    def measure_distance(self):
        self.stateCurrent = io.input(self.ENC_pin)
        if self.stateCurrent != self.stateLast:
            self.stateLast = self.stateCurrent
            self.stateCount += 1
            self.stateCountTotal += 1

        if self.stateCount == self.statesPerRotation:
            self.rotationCount += 1
            self.stateCount = 0

        self.distance = self.distancePerStep * self.stateCountTotal

    def reset_measurement(self):
        self.stateLast = io.input(self.ENC_pin)
        self.rotationCount = 0
        self.stateCount = 0
        self.stateCountTotal = 0
        self.distance = 0

    def get_distance(self, do_print=True):
        if do_print:
            print(f'Distance = {self.distance} mm.')

        return self.distance

    def stop(self):
        self.PWM.start(0) 

    def shutdown(self): #FIXME: Might be static?
        io.cleanup()

    