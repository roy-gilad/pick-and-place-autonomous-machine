/*
 main program

 1. need to check that 1600 step its one revolve
 
 */



#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>

// pully and stepper define to calculate distance --> step
float XYpullyPich=5.08; // X and Y pullys
int XYpullyTeeth=15;    // X and Y pullys
int StepRev=1600;       //1600 step for full revolv
int Zdown=7000;         // step to pick egg
int Zplace=8000;        // step to place egg
int vacSwich=11;         // vacuum tank, near controller  num 1
int atmSwich=12;         // atm pressure, on Z axies 

//Define eggs coordination table in mm
int X_Egg[] = {150,150}; // in mm
int Y_Egg[] = {150,150};
int AngEgg[] = {30,60};

// carton coordination table in mm
int X_Carton[] = {150,150,150,150,150,0,0,0,0,0,0,0};
int Y_Carton[] = {0,50,100,156,208,260,0,0,0,0,0,0};



// egg direction in degree
int teta_Direction[] = {0,30,60,0,90};



int i=0;

// ---------stepper------- 
AccelStepper stepperX(1, 7, 6);   // 1 = Easy Driver interface, 7 step, 6 Dir  
AccelStepper stepperY(1, 2, 3);   // 1 = Easy Driver interface, 2 step, 3 Dir
AccelStepper stepperZ(1, 5, 4);   
MultiStepper XYsteppers;// Define X,Y as a group of motor that run simultaneousl. 

//-----------servo------------
Servo AngleServo;  // rotate for egg direction  
Servo PPservo;    // rotet for pick and place position

void setup() {
Serial.begin(9600); // define serial monitor

// Configure each stepper max speed
stepperX.setMaxSpeed(1000);// not eable 2000 speed with 1/8 step
stepperY.setMaxSpeed(2000);
stepperZ.setMaxSpeed(4500);
stepperZ.setAcceleration(10000); //define accelerationonly for z motor


//  give to XY steppers to manage the X,Y motors
XYsteppers.addStepper(stepperX);
XYsteppers.addStepper(stepperY);


// attaches the servo on pin -- 
AngleServo.attach(9);  
PPservo.attach(10);


//   start defines
PPservo.write(0);// pick & place servo ready in pick position


//pniumatic swich
pinMode(vacSwich, OUTPUT); 
pinMode(atmSwich, OUTPUT);
//all swich are close
digitalWrite(vacSwich, HIGH); 
digitalWrite(atmSwich, HIGH);

}
int a=sizeof(X_Egg);
void loop() {
while (i<12){ //complete  carton-12 eggs
if (Serial.available() > 0  )
  {
    int x_cord, y_cord,ang_egg;
    if (Serial.read() == 'X')
    {
      x_cord = Serial.parseInt();  // read center x-coordinate
      if (Serial.read() == 'Y')
        y_cord = Serial.parseInt(); // read center y-coordinate
      if (Serial.read() == 'A') 
        ang_egg= Serial.parseInt();// read angle of the picking egg
    }
   Serial.print("x coordinate is:  ");
   Serial.println(x_cord);
   Serial.print("  y coordinate is:  ");
   Serial.println(y_cord);
   Serial.print("  angle of the egg is:  ");
   Serial.println(ang_egg);  

  
   MoveTo(x_cord,y_cord);
   
   PickEgg(ang_egg);


   MoveTo(X_Carton[i],Y_Carton[i]);
 //  MoveTo(0,0);
   PlaceEgg();
   
    i=i+1;
    while(Serial.available() > 0) {// clear serial monitor
       char t = Serial.read();}
   
  }
  
  }
Serial.print("  carton is full  ");
exit(0);

  }





/* this function run over the XY coordinate, the function get the location and run the motors */
void MoveTo(long x,int y){
  
    float Xsteps=((x*1600UL)/(XYpullyPich*XYpullyTeeth)); // convert X distance to step 
    int Ysteps=((y*1600UL)/(XYpullyPich*XYpullyTeeth)); // convert Y distance to step 
  

  
    Serial.println("Moving stepper into position: ");
    Serial.print(Xsteps);




  
    long positions[2]; // Array of desired stepper positions
    positions[0] = Xsteps;
    positions[1] = Ysteps;

    Serial.print("Moving stepper into position: ");
    Serial.print(Xsteps);
    Serial.print(" , ");
    Serial.println(Ysteps);
    
    XYsteppers.moveTo(positions);
    XYsteppers.runSpeedToPosition(); // Blocks until all are in position
  }
  
/* this function pick the egg:   1. rotate egg direction 2. move down in Z direction 3.turn on the vacuum 4. move up in Z direction */
void PickEgg(int ang){

  
  // 1. rotate to the egg direction
  Serial.print("rotat angl servo");
  Serial.println(ang);
  AngleServo.write(ang);
  //delay(1000);

  // 2.  move down in Z direction
  Serial.println("Z go down");
  stepperZ.runToNewPosition(Zdown); 
 
  
  //3.turn on the vacuum
  digitalWrite(vacSwich, LOW);
  
  //4. move up in Z direction 
  Serial.println("Z go up");
   stepperZ.runToNewPosition(0); // return to z=0
   
   Serial.println("");
   Serial.println("");
   Serial.println("----finish pick");
     //1. rotate to place angle
  Serial.println("rotat PP servo 90");
  PPservo.write(90);
}

/* this function place the egg:     2. move down in Z direction 3.turn off the vacuum 4. move up in Z direction 5. rotate to pick angle*/
void PlaceEgg(){


  //2. move down in Z direction
  Serial.println("Z go down");
  stepperZ.runToNewPosition(Zplace); // *****need to cheack how many distans to place
  delay(500);

  //3.turn off the vacuum
  digitalWrite(vacSwich, HIGH);  
  digitalWrite(atmSwich, LOW);
  delay(100);
  digitalWrite(atmSwich, HIGH);

  //4. move up in Z direction
  Serial.println("Z go up");
  stepperZ.runToNewPosition(0); 

 //5. rotate to pick angle
 Serial.println("rotat PP servo 0");
 PPservo.write(0);

 Serial.println("");
   Serial.println("");
   Serial.println("----finish place");
delay(200);
 
  
  }



  
