#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
from ros_essentials_cpp.msg import objectdetection
global xlocation1
y1 = True
def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta

    #print "pose callback"
    #print ('x = {}'.format(pose_message.x)) #new in python 3
    #print ('y = %f' %pose_message.y) #used in python 2
    #print ('yaw = {}'.format(pose_message.theta)) #new in python 3
def xlocation_callback(xlocation_message):
     cmd_vel_topic='/turtle1/cmd_vel'
     velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
     xlocation1 = xlocation_message.xlocation
     rotate(velocity_publisher, 15, xlocation1)
     #rospy.loginfo(xlocation1)
     
    

def move(velocity_publisher, speed, distance, is_forward):
        #declare a Twist message to send velocity commands
        velocity_message = Twist()
        #get current location 
        global x, y
        x0=x
        y0=y

        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:
        	velocity_message.linear.x =-abs(speed)

        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
        
        while True :
                rospy.loginfo("Turtlesim moves forwards")
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print  (distance_moved)
                print(x)
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)
    
def rotate (velocity_publisher, angular_speed_degree, x6):
    
    velocity_message = Twist()

    angular_speed=math.radians(abs(angular_speed_degree))

    if (x6>320):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed) 

    #angle_moved = 0.0
    loop_rate = rospy.Rate(5) # we publish the velocity at 10 Hz (10 times a second)    
    #cmd_vel_topic='/turtle1/cmd_vel'
    #velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    #t0 = rospy.Time.now().to_sec()

    #while True :
    rospy.loginfo("Turtlesim rotates")
    rospy.loginfo(x6) 
    velocity_publisher.publish(velocity_message)

        #t1 = rospy.Time.now().to_sec()
        #current_angle_degree = (t1-t0)*angular_speed_degree
    loop_rate.sleep()


                       
        #if  (current_angle_degree>relative_angle_degree):
            #rospy.loginfo("reached")
            #break

    #finally, stop the robot when the distance is moved
    #velocity_message.angular.z =0
    #velocity_publisher.publish(velocity_message)
def rotate1 (velocity_publisher, angular_speed_degree,relative_angle_degree,clockwise):
    
    velocity_message = Twist()

    angular_speed=math.radians(abs(angular_speed_degree))

    if clockwise:
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()


                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)    


def go_to_goal(velocity_publisher, x_goal, y_goal):
    global x
    global y, yaw

    velocity_message = Twist()

    while (True):
        K_linear = 0.5 
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))

        linear_speed = distance * K_linear

        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        velocity_publisher.publish(velocity_message)
        print ('x=', x, ', y=',y, ', distance to goal: ', distance)

        if (distance <0.01):
            break

def setDesiredOrientation(publisher, speed_in_degree, desired_angle_degree):
    relative_angle_radians = math.radians(desired_angle_degree) - yaw
    clockwise=0
    if relative_angle_radians < 0:
        clockwise = 1
    else:
        clockwise = 0
    print ("relative_angle_radians: ",math.degrees(relative_angle_radians))
    print ("desired_angle_degree: ",desired_angle_degree)
    rotate(publisher, speed_in_degree,math.degrees(abs(relative_angle_radians)), clockwise)

def gridClean(publisher):
 
    desired_pose = Pose()
    desired_pose.x = 1
    desired_pose.y = 1
    desired_pose.theta = 0
 
    go_to_goal(publisher, 1,1)
 
    setDesiredOrientation(publisher, 30, math.radians(desired_pose.theta))
 
    for i in range(5):
        move(publisher, 2.0, 1.0, True)
        rotate(publisher, 20, 90, False)
        move(publisher, 2.0, 9.0, True)
        rotate(publisher, 20, 90, True)
        move(publisher, 2.0, 1.0, True)
        rotate(publisher, 20, 90, True)
        move(publisher, 2.0, 9.0, True)
        rotate(publisher, 20, 90, False)
    pass

 
 
def spiralClean(velocity_publisher, wk, rk,x5):
    global xlocation1
    vel_msg = Twist()
    loop_rate = rospy.Rate(1)

    if(x5>320):
        rk=rk+1
        vel_msg.linear.x =rk
        vel_msg.linear.y =0
        vel_msg.linear.z =0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z =wk
        velocity_publisher.publish(vel_msg)
    if(x5<320):
        rk=rk+1
        vel_msg.linear.x =rk
        vel_msg.linear.y =0
        vel_msg.linear.z =0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z =-wk
        velocity_publisher.publish(vel_msg)    

 
    #vel_msg.linear.x = 0
    #vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    rospy.loginfo(x5)
    



if __name__ == '__main__':
    if y1 == True :
        rospy.init_node('turtlesim_motion_pose', anonymous=True)
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        rotate1(velocity_publisher, 30, 90, True)
        y1=False
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        #declare velocity publisher
        #cmd_vel_topic='/turtle1/cmd_vel'
        #velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #position_topic = "/turtle1/pose"
        #pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        xlocation_sub = rospy.Subscriber("locationx", objectdetection, xlocation_callback)
        #x_goal = rospy.get_param("x_goal")
        #y_goal = rospy.get_param("y_goal")
        #move(velocity_publisher, 1.0, 9.0, True)
        #rotate(velocity_publisher, 30, -90, True)
        #go_to_goal(velocity_publisher, , y_goal)
        #setDesiredOrientation(velocity_publisher, 30, 90)
        #spiralClean(velocity_publisher, 4, 0)
        rospy.spin()
        #gridClean(velocity_publisher)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
