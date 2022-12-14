import cv2
import pandas as pd
from datetime import datetime

# Assigning our initial state in the form of variable initialState 
# as None for initial frames  
first_frame = None

# List of all the tracks when there is any detected of motion in the frames  
motionTrackList= [ None, None ]  

# A new list ‘time’ for storing the time when movement detected  
motionTime = []  

# Initialising DataFrame variable ‘dataFrame’ using pandas libraries panda 
# with Initial and Final column  
dataFrame = pd.DataFrame(columns = ["Initial", "Final"])

# First, we will start capturing video using the cv2 module and store that 
# in the video variable.
video = cv2.VideoCapture(0)

# use an infinite while loop to capture each frame from the video
while True:
    
    # use the read() method to read each frame and store them into 
    # respective variables. 
    check, frame = video.read()

    # Defining 'motion' variable equal to zero as initial frame 
    motion_change = 0
    
    # From colour images creating a gray frame      
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # To find the changes creating a GaussianBlur from the gray scale image    
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    # For the first iteration checking the condition
    # we will assign gray to initalState if is none      
    if first_frame is None:
        first_frame = gray
        continue
    
    # Calculation of difference between initial and gray frame we created 
    delta_frame = cv2.absdiff(first_frame, gray)
    
    # the change between initial background and current gray frame are 
    # highlighted
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    
    # For the moving object in the frame finding the coutours 
    (cnts, _) = cv2.findContours(thresh_frame.copy(), 
                                 cv2.RETR_EXTERNAL, 
                                 cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion_change = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # To create a rectangle of green color around the moving object 
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,255,0), 3)

    # from the frame adding the motion status   
    motionTrackList.append(motion_change)  
    motionTrackList = motionTrackList[-2:]  

    # Adding the Start time of the motion 
    if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:  
        motionTime.append(datetime.now())  

    # Adding the End time of the motion 
    if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:  
        motionTime.append(datetime.now())  

    # In the gray scale displaying the captured image                  
    cv2.imshow("Gray", gray)
    
    # To display the difference between inital frame and the current frame 
    cv2.imshow("Delta", delta_frame)
    
    # To display on the frame screen the black and white images from the video
    cv2.imshow("Thread", thresh_frame)
    
    # Through the colour frame displaying the contour of the object
    cv2.imshow("Color", frame)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        if motion_change == 1:  
            motionTime.append(datetime.now())  
        break
    
# At last we are adding the time of motion or var_motion inside the data frame  
for a in range(0, len(motionTime), 2):  
   dataFrame = dataFrame.append(
       {"Initial" : motionTime[a], "Final" : motionTime[a + 1]}, 
       ignore_index = True)  

   
# To record all the movements, creating a CSV file  
dataFrame.to_csv("EachMovement.csv")  

# Releasing the video   
video.release()

# Now, Closing or destroying all the open windows with the help of openCV  
cv2.destroyAllWindows()