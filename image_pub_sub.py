#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image,CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import sys
import time
from ros_essentials_cpp.msg import objectdetection 
import math
from multiprocessing import Process
import threading

x1,x2,x3,x4 =1,1,1,1

bridge = CvBridge()
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

def image_callback(ros_image1):
  print ('got an image')
  global bridge
  global x1,x2,x3,x4
  #convert ros_image into an opencv-compatible image
  try:
    ros_image = bridge.imgmsg_to_cv2(ros_image1, "bgr8")
    cv2.imwrite('webcam.png', ros_image)
  except CvBridgeError as e:
      print(e)
  #from now on, you can work exactly like with opencv
  (rows,cols,channels) = ros_image.shape
  if cols > 200 and rows > 200 :
      #cv2.circle(ros_image, (100,100),90, 255)
      (h, w) = ros_image.shape[:2] #w:image-width and h:image-height
      #cv2.circle(ros_image, (w//2, h//2), 7, (255, 255, 255), -1) 
      tensorflowNet.setInput(cv2.dnn.blobFromImage(ros_image, size=(300, 300), swapRB=True, crop=False))
      networkOutput = tensorflowNet.forward()
      for detection in networkOutput[0,0]:

        score = float(detection[2])
        if score > 0.7: 
      
          x1 = detection[3] * cols
          x2 = detection[4] * rows
          x3 = detection[5] * cols
          x4 = detection[6] * rows
 
          #draw a red rectangle around detected objects
          cv2.rectangle(ros_image, (int(x1), int(x2)), (int(x3), int(x4)), (0, 255, 0), thickness=2)
      cv2.rectangle(ros_image, (0, 0), (50, 50), (0, 255, 0), thickness=2)
   

  font = cv2.FONT_HERSHEY_SIMPLEX
  #cv2.putText(ros_image,'Webcam Activated with ROS & OpenCV!',(10,350), font, 1,(255,255,255),2,cv2.LINE_AA)
  Flip=cv2.flip(ros_image, 1)
  cv2.imshow("Image window", Flip)
  cv2.waitKey(3)

  
def main2():
  rospy.init_node('image_converter', anonymous=True)
  #for turtlebot3 waffle
  image_topic="/camera/rgb/image_raw"
  #for usb cam

  #image_topic="/usb_cam/image_raw"
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
   image_sub = rospy.Subscriber(image_topic,Image,image_callback)
   rate.sleep()
  #try:
    #rospy.spin()
  #except KeyboardInterrupt:
    #print("Shutting down")
  #cv2.destroyAllWindows()
def main1():
  rospy.init_node('location_node', anonymous=True)
  image_pub = rospy.Publisher("locationx",objectdetection, queue_size=10)
  rate= rospy.Rate(1)
  while not rospy.is_shutdown():
      object_detection = objectdetection()
      object_detection.xlocation = 3                                   #int(math.sqrt(((x1-x3) ** 2) + ((x2-x4) ** 2)))
      image_pub.publish(object_detection)
      rospy.loginfo(object_detection)
      rate.sleep()
  

  
if __name__ == '__main__':
      main2()
 