import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread


#to capture video
video = cv2.VideoCapture(0)
# to give the system time
time.sleep(1)


first_frame = None
status_list = []
count = 1


def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")

image_with_object = None
#to show video
while True:
    status = 0
    check, frame = video.read()



    # to convert the frame to grayscale frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Gaussian blur method, this is to make the camera blur
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0)



    # pre process of the frame
    if first_frame is None:
        first_frame = gray_frame_gau

#difference ((absdiff means absolut different)
    delta_frame=  cv2.absdiff(first_frame, gray_frame_gau)
    

    thresh_frame= cv2.threshold(delta_frame, 65 ,255,cv2.THRESH_BINARY)[1]
    dil_frame= cv2.dilate(thresh_frame, None, iterations= 2)
    # to  display image or video 
    # that what imshow means, it displayes video
   # cv2.imshow("MY VIDEO",dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle= cv2.rectangle(frame, (x, y), (x+w,y+h), (0,255,0), 3)
        if rectangle.any():
            status= 1
            # to store images
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images= glob.glob("images/*.png")
            index = int(len(all_images)/ 2)
            image_with_object= all_images[index]
            
            
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0 and image_with_object is not None:
        email_thread = Thread(target= send_email, args=(image_with_object, ))
        email_thread.daemon =True

        clean_thread = Thread(target= clean_folder)
        clean_thread.daemon =True
        
        email_thread.start()

    print(status_list)

    cv2.imshow("video", frame)
    key = cv2.waitKey(1)
 
#("q") this is to quit the video, to stop video from displaying.
# to stop video just press q, to end it.
    if key == ord("q"):
        break


video.release()


clean_thread.start()

