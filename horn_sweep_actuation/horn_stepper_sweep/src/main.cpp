#include <Arduino.h>
#include <math.h>
#include <CNCShield.h>
#include <string.h>

#define NO_OF_STEPS               200
#define SLEEP_BETWEEN_STEPS_MS    10
#define SPEED_STEPS_PER_SECOND    50 

/*
 * Create a CNCShield object and get a pointer to motor 1 (Y axis).
 */
CNCShield cnc_shield;
StepperMotor *motor = cnc_shield.get_motor(1);
float cur_angle = 0;

void setup()
{
  /*
   * Calling CNCShield.begin() is mandatory before using any motor.
   */
  cnc_shield.begin();

  /*
   * Enable the shield (set enable pin to LOW).
   */
  cnc_shield.enable();


  motor->set_speed(SPEED_STEPS_PER_SECOND);


  Serial.begin(115200);
  Serial.println("R");
}

void loop()
{
  static String inputString = "";  // String to store received characters
  
  while (Serial.available() > 0) {
    char incomingChar = Serial.read();  // Read the incoming character

    if (incomingChar == '\n') {  // Check if newline character is received
      int ref_angle = inputString.toInt();  // Convert the string to an integer
      inputString = "";  // Clear the string for the next input
      
      if(ref_angle >= 0 && ref_angle<=360){
        if(ref_angle>cur_angle){
          int n_steps = (long)(ref_angle-cur_angle)*200/360;
          motor->step(n_steps,CLOCKWISE);
          cur_angle = cur_angle+n_steps*1.8;
          delay(n_steps/SPEED_STEPS_PER_SECOND*1000);

        }
        else if(ref_angle<cur_angle){
          int n_steps = (long)(cur_angle-ref_angle) * 200/360;
          motor->step(n_steps,COUNTER);
          cur_angle = cur_angle - n_steps*1.8;
          delay(n_steps/SPEED_STEPS_PER_SECOND*1000);

        }
        Serial.println("DONE");
      }
      else{
        Serial.println("OoB");
        break;
      }

    } else {
      inputString += incomingChar;  // Add the character to the string
    }
  }
  
}
