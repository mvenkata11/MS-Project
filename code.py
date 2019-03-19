import tkinter as tk
import easygopigo3
import picamera
import io
import time
import smtplib 
import cv2
import numpy
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase  
from email import encoders

robot = easygopigo3.EasyGoPiGo3()

sleep = time.sleep(1)

servo_range = [2,3,4,5,6,7,8]
min_dist =500

def key_input(event): #controlling robot using keys
    key_press = event.keysym.lower()
    print(key_press)
    
    if key_press == 'w': #autonomy
        i=100
        while True:        #infinite loop
            try:
                servo = robot.init_servo()
                servo.rotate_servo(70)
                my_distance_sensor = robot.init_distance_sensor()
                dist=my_distance_sensor.read_mm()
                print("Distance Sensor Reading (mm): " + str(dist))     # display distance sensor reading
                if dist>min_dist:         #If measured distance is greater than min distance move forward  
                    robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, i)
                else:
                    robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, 0)#stop robot
                    servo.rotate_servo(28) #rotate using servo to 28 degrees left 
                    sleep
                    left_dir = my_distance_sensor.read_mm() # measure left distance
                    print("Left Distance Reading (mm): " + str(left_dir))
                    servo.rotate_servo(112) # rotate using servo to 112 degrees
                    sleep
                    right_dir = my_distance_sensor.read_mm() # measure right distance
                    print("Right Distance Reading (mm): " + str(right_dir))
                    if left_dir < min_dist and right_dir < min_dist: # if left and right distance less than min distance move backward and rotate right
                        robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, -i)
                        robot.right()
                        sleep
                    elif left_dir > right_dir and left_dir > min_dist: # if left distance greater than right and min distance rotate left
                        print('choose left')
                        robot.left()
                        sleep
                    elif left_dir < right_dir and right_dir > min_dist: # if right distance greater than left and min distance rotate right
                        print('choose right')
                        robot.right()
                    sleep
            except KeyboardInterrupt: # press any key to stop the robot
                robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, 0)
                
                
                    
                    
    elif key_press == 's': # to move backward
         i=100
         robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, -i)
         
    elif key_press == 'a': # to move left
         robot.left()
    elif key_press == 'e': # to email the image
         email_user = 'XXXXX@gmail.com' 
         email_password = 'XXXX' 
         email_send = 'XXXX@gmail.com' 
         subject = 'sending mail from gopigo' 
         msg = MIMEMultipart() 
         msg['From'] = email_user 
         msg['To'] = email_send 
         msg['Subject'] = subject 
         body = 'Hi there, sending this email from Python!' 
         msg.attach(MIMEText(body,'plain')) 
         filename='result.jpg' 
         attachment  =open(filename,'rb') 
         part = MIMEBase('application','octet-stream') 
         part.set_payload((attachment).read()) 
         encoders.encode_base64(part) 
         part.add_header('Content-Disposition',"attachment; filename= "+filename) 
         msg.attach(part) 
         text = msg.as_string() 
         server = smtplib.SMTP('smtp.gmail.com',587) 
         server.starttls() 
         server.login(email_user,email_password) 
         server.sendmail(email_user,email_send,text) 
         server.quit()
         
        
    elif key_press == 'i': # face detection
         #Create a memory stream so photos doesn't need to be saved in a file
         stream = io.BytesIO()
         #Get the picture (low resolution, so it should be quite fast)
         #Here you can also specify other parameters (e.g.:rotate the image)
         with picamera.PiCamera() as camera:
             camera.resolution = (320, 240)
             camera.capture(stream, format='jpeg')
         #Convert the picture into a numpy array
         buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

         #Now creates an OpenCV image
         image = cv2.imdecode(buff, 1)

         #Load a cascade file for detecting faces
         face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/test.xml')

         #Convert to grayscale
         gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

         #Look for faces in the image using the loaded cascade file
         faces = face_cascade.detectMultiScale(gray, 1.1, 5)

         print ("Found "+str(len(faces))+" face(s)")

         #Draw a rectangle around every found face
         for (x,y,w,h) in faces:
             cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

         #Save the result image
         cv2.imwrite('result.jpg',image)
     




   
    elif key_press =='d': # to move right
         robot.right()
    elif key_press == 'space': # to stop
         robot.set_motor_power(robot.MOTOR_LEFT + robot.MOTOR_RIGHT, 0)
    elif key_press == 'c': # to capture image
         camera = picamera.PiCamera()
         camera.capture('image.jpg')
    elif key_press == 'v': # to measure the voltage of battery
         v=robot.volt()
         print(v)
    elif key_press == 'r': # to record a video for 5 seconds
         camera = picamera.PiCamera()
         camera.start_recording('video.h264')
         time.sleep(5)
         camera.stop_recording()
   
    elif key_press == 'u': # to mesaure the distance
         my_distance_sensor = robot.init_distance_sensor()
         print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
         
    elif key_press.isdigit(): # to control the robot using numbers
        servo = robot.init_servo()
        servo.rotate_servo(int(key_press)*14)
        time.sleep(1)
            
command = tk.Tk()
command.bind_all('<Key>', key_input)
command.mainloop()
