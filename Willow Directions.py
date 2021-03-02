# Python Script for Willow Directions

# Import Flask to start and stop the Willow
from flask import Flask, render_template

#!/usr/bin/python
import RPi.GPIO as GPIO
import time

try:
      GPIO.setmode(GPIO.BCM)

      # Declare the GPIO pins for the cars
      # front motor, back motor, and steering motor
      FRONT_MOTOR_ONE = 14
      FRONT_MOTOR_TWO = 15

      BACK_MOTOR_ONE = 25
      BACK_MOTOR_TWO = 8

      STEERING_ONE = 23
      STEERING_TWO = 24

      # Declare the pins for the 3 sensors
      PIN_TRIGGER_FRONT = 4
      PIN_ECHO_FRONT = 17

      # PIN_TRIGGER_LEFT =
      # PIN_ECHO_LEFT =
      #
      # PIN_TRIGGER_RIGHT =
      # PIN_ECHO_RIGHT =

      GPIO.setup(PIN_TRIGGER_FRONT, GPIO.OUT)
      GPIO.setup(PIN_ECHO_FRONT, GPIO.IN)

      GPIO.setup(PIN_TRIGGER_LEFT, GPIO.OUT)
      GPIO.setup(PIN_ECHO_LEFT, GPIO.IN)

      GPIO.setup(PIN_TRIGGER_RIGHT, GPIO.OUT)
      GPIO.setup(PIN_ECHO_RIGHT, GPIO.IN)

      # Let the sensors settle
      GPIO.output(PIN_TRIGGER_FRONT, GPIO.LOW)
      # GPIO.output(PIN_TRIGGER_LEFT, GPIO.LOW)
      # GPIO.output(PIN_TRIGGER_RIGHT, GPIO.LOW)
        
    
      # Declare the boolean "killSwitch" to stop the Willow
      killSwitch = False
      # Declare distance for sensor distance to make changes
      max_distance = 45


      # Create an instance of flask
      app = Flask(__name__)

    
      # Start the car moving forward
      @app.route("/move_forward", methods=["POST"])
      def move_forward():
          forward(killSwitch, max_distance)
          print("Willow is moving to destination")
          return "ok"


      @app.route("/destination_reached", methods=["POST"])
      def destination_reached():
          destination_reached.has_been_called = True
          destination()
          print("Willow has reached its destination")
          return "ok"

      @app.route("/", methods=["GET"])
      def home():
            return render_template("willowButton.html", title="Willow Switch", name="And Yet it Compiles")



      def forward(killswitch, max_distance):
          # To move the car forward, turn
          # FRONT_MOTOR_ONE and BACK_MOTOR_ONE on high
          GPIO.output(FRONT_MOTOR_ONE, GPIO.HIGH)
          GPIO.output(BACK_MOTOR_ONE, GPIO.HIGH)
          # And make the other two pins
          # (FRONT_MOTOR_TWO and BACK_MOTOR_TWO) on low
          GPIO.output(FRONT_MOTOR_TWO, GPIO.LOW)
          GPIO.output(BACK_MOTOR_TWO, GPIO.LOW)

          while killSwitch == False:
              # Set the both steering motors to low so the car starts off moving straight
              GPIO.output(STEERING_ONE, GPIO.LOW)
              GPIO.output(STEERING_TWO, GPIO.LOW)

              # Call the moveback function to check if the sensor is
              # to close to an obstacle
              moveBack(max_distance)

              # Set max_distance back to 45
              max_distance = 45

              # Call the turn right function to check if the object is
              # to close to an obstacle on the left
              moveRight(max_distance)

              # Call the turn left function to check if the object is
              # too close to an obstacle on the right
              moveLeft(max_distance)

              #  Check if the destination_reached button has been pressed
              if destination_reached.has_been_called == True:
                  killSwitch = True


      def moveBack(max_distance):

          GPIO.output(PIN_TRIGGER_FRONT, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN_TRIGGER_FRONT, GPIO.LOW)

          while GPIO.input(PIN_ECHO_FRONT) == 0:
              pulse_start_time = time.time()
          while GPIO.input(PIN_ECHO_FRONT) == 1:
              pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          front_distance = round(pulse_duration * 17150, 2)

          # If the distance picked up by the front sensor is less than the maximum
          # distance, stop the car and put it in reverse
          if front_distance < max_distance:
              # Have to stop the car before putting it in reverse
              GPIO.output(FRONT_MOTOR_ONE, GPIO.LOW)
              GPIO.output(BACK_MOTOR_ONE, GPIO.LOW)
              GPIO.output(FRONT_MOTOR_TWO, GPIO.LOW)
              GPIO.output(BACK_MOTOR_TWO, GPIO.LOW)


              time.sleep(1)

              # Turning Pin 15 and pin 8 on
              GPIO.output(FRONT_MOTOR_TWO, GPIO.HIGH)
              GPIO.output(BACK_MOTOR_TWO, GPIO.HIGH)
              # Turning Pin 25 on and Pin 14 off makes the back motor reverse
              # And make the other two pins
              # (FRONT_MOTOR_TWO and BACK_MOTOR_TWO) on low
              GPIO.output(FRONT_MOTOR_ONE, GPIO.LOW)
              GPIO.output(BACK_MOTOR_ONE, GPIO.LOW)

              time.sleep(2)


              # Start the car moving forward again
              GPIO.output(FRONT_MOTOR_ONE, GPIO.HIGH)
              GPIO.output(BACK_MOTOR_ONE, GPIO.HIGH)
              GPIO.output(FRONT_MOTOR_TWO, GPIO.LOW)
              GPIO.output(BACK_MOTOR_TWO, GPIO.LOW)

              # Check which way the car needs to turn
              max_distance = 60
              moveRight(max_distance)
              moveLeft(max_distance)


      def moveRight(max_distance):
          GPIO.output(PIN_TRIGGER_LEFT, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN_TRIGGER_LEFT, GPIO.LOW)

          while GPIO.input(PIN_ECHO_LEFT) == 0:
              pulse_start_time = time.time()
          while GPIO.input(PIN_ECHO_LEFT) == 1:
              pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          left_distance = round(pulse_duration * 17150, 2)

          # If the distance picked up by the left sensor is less than the maximum
          # distance, turn the car slightly to the right
          if left_distance < max_distance:
              # Turn on "STEERING_MOTOR_ONE"
              GPIO.output(STEERING_ONE, GPIO.HIGH)
              # Keep it on for one second then turn it off
              time.sleep(1)
              GPIO.output(STEERING_ONE, GPIO.LOW)


      def moveLeft(max_distance):
          GPIO.output(PIN_TRIGGER_RIGHT, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN_TRIGGER_RIGHT, GPIO.LOW)

          while GPIO.input(PIN_ECHO_RIGHT) == 0:
              pulse_start_time = time.time()

          while GPIO.input(PIN_ECHO_RIGHT) == 0:
              pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          right_distance = round(pulse_duration * 17150, 2)

          # If the distance picked up by the right sensor is less than the maximum
          # distance, turn the car slightly to the left
          if right_distance < max_distance:
              # Turn on "STEERING_MOTOR_TWO"
              GPIO.output(STEERING_TWO, GPIO.HIGH)
              # Keep it on for 1 second then turn it off
              time.sleep(1)
              GPIO.output(STEERING_TWO, GPIO.LOW)


      def destination():
          time.sleep(1)
          # Turn off all the motors to stop the car
          GPIO.output(FRONT_MOTOR_ONE, GPIO.LOW)
          GPIO.output(FRONT_MOTOR_TWO, GPIO.LOW)
          GPIO.output(BACK_MOTOR_ONE, GPIO.LOW)
          GPIO.output(BACK_MOTOR_TWO, GPIO.LOW)




finally:
      GPIO.cleanup()

