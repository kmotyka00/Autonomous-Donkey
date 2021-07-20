import motors
import sensors
from time import time
from timeit import default_timer

leftMotor = motors.MotorWithEncoder(DIR_pin=22, PWM_pin=17, ENC_pin=4)
rightMotor = motors.MotorWithEncoder(DIR_pin=23, PWM_pin=18, ENC_pin=26)

transducer = sensors.Transducer()

last_time = time()


try:
    while True:
        leftMotor.run(speed=20,direction='F')
        rightMotor.run(speed=20,direction='F')

        leftMotor.measure_distance()
        rightMotor.measure_distance()

        current_time = time()
        
        if current_time - last_time > 5:
            last_time = current_time

            print("\n\n1: ",end=" ")
            leftMotor.get_distance(do_print=True)

            print("2: ",end=" ")
            rightMotor.get_distance(do_print=True)



except KeyboardInterrupt:
    leftMotor.stop()
    rightMotor.stop()



