#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import time
from ros_essentials_cpp.msg import objectdetection 
import math
from multiprocessing import Process
import threading

x1,x2,x3,x4 =1.00,1.00,1.00,1.00
y1=True

bridge = CvBridge()
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

def image_callback():
  global y1
  video_capture = cv2.VideoCapture(0)
  global bridge
  global x1,x2,x3,x4
  y = 1
  #convert ros_image into an opencv-compatible image
  for i in range(0,1):
  #cv_image = bridge.imgmsg_to_cv2(cv_image2, "bgr8")
    ret, cv_image1 = video_capture.read() 
    cv2.imwrite('webcam.png', cv_image1)

  (rows,cols,channels) = cv_image1.shape
  if cols > 200 and rows > 200 :
      #cv2.circle(cv_image, (100,100),90, 255)
      (h, w) = cv_image1.shape[:2] #w:image-width and h:image-height
      #cv2.circle(cv_image1, (w//2, h//2), 7, (255, 255, 255), -1) 
      tensorflowNet.setInput(cv2.dnn.blobFromImage(cv_image1, size=(300, 300), swapRB=True, crop=False))
      networkOutput = tensorflowNet.forward()
      for detection in networkOutput[0,0]:

        score = float(detection[2])
        if score > 0.7: 
      
          x1 = detection[3] * cols
          x2 = detection[4] * rows
          x3 = detection[5] * cols
          x4 = detection[6] * rows
          y1,y2,y3,y4 = detection[3] * cols,detection[4] * rows,detection[5] * cols,detection[6] * rows
          cv2.rectangle(cv_image1, (int(y1), int(y2)), (int(y3), int(y4)), (0, 255, 0), thickness=2)   
      #cv2.rectangle(cv_image1, (0, 0), (25, 25), (0, 255, 0), thickness=2)
   
      
  font = cv2.FONT_HERSHEY_SIMPLEX
  #cv2.putText(cv_image,'Webcam Activated with ROS & OpenCV!',(10,350), font, 1,(255,255,255),2,cv2.LINE_AA)
  Flip=cv2.flip(cv_image1, 1)
  cv2.imshow("Image window", Flip)
  cv2.waitKey(3)

  
  
def main2():
  rospy.init_node('image_converter', anonymous=True)
  #for turtlebot3 waffle
  #image_topic="/camera/rgb/image_raw/compressed"
  #for usb cam

  image_topic="/usb_cam/image_raw"
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
   image_sub = rospy.Subscriber("/usb_cam/image_raw",Image, image_callback)
   rate.sleep()
  #try:
    #rospy.spin()
  #except KeyboardInterrupt:
    #print("Shutting down")
  #cv2.destroyAllWindows()
def main1():
  global y1
  global x1,x3
  y1 = False
  y3 = [0,0]
  rospy.init_node('location_node', anonymous=True)
  image_pub = rospy.Publisher("locationx",objectdetection, queue_size=10)
  rate= rospy.Rate(1000)
  image_callback()
  while not rospy.is_shutdown():
      object_detection = objectdetection()
      object_detection.xlocation = int((x1+x3)/2)
      for i in range(0,2):
        image_callback()
        y3[i] = x1
      
      if (y3[0]==y3[1]):
        object_detection.xlocation = 6
        print("no egg found") 
      else:
       rospy.loginfo(object_detection)  
       image_pub.publish(object_detection)
       rate.sleep()
  

  
if __name__ == '__main__':
 main1()
 