# Repository for implementing object detection in ROS 
## Introduction
This repository is for implementing object detection on a simple turtlebot in ROS.

## Step1

Install ROS on you computer, ROS noetic would be most preferable. To install ROS refer to this link [http://wiki.ros.org/noetic/Installation/Ubuntu](http://wiki.ros.org/noetic/Installation/Ubuntu), make sure that you install all the mentioned dependencies on the site as well. also it wouid be preferable to install the full version of ROS.

## Step2

Next step is to source the setup.bash file located in the ros installation file, to do this open your terminal and type the following command ,
$sudo gedit .bashrc
go to the end of this text file and paste the text line given below, 
source /opt/ros/noetic/setup.bash.

## Step 3 
Now we need to create a catkin workspace for ROS, to do that type in the following comands on your terminal,
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/
$ catkin_make
```
once you have done that, type in the following command,
```
$ sudo gedit .bashrc 
```
as explained in Step2 you need to paste another text line in the text file, that text line is given below,   
source devel/setup.bash

## Step 4 
Now you need to clone another repository, the link to the repo is [https://github.com/aniskoubaa/ros_essentials_cpp](https://github.com/aniskoubaa/ros_essentials_cpp), to clone this, type in the following commands on your terminal.
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/aniskoubaa/ros_essentials_cpp.git
```
## Step 5 
Type in the following command on the terminal, 
```
$ catkin_make
```
## Step 6 
type in the following commands
```
$ cd /home/rajat/catkin_ws/src/ros_essentials_cpp/src/topic03_perception/
$ git clone 
```
## Step 7 
Now type in the following commands
```
$ cd /home/rajat/catkin_ws/src/ros_essentials_cpp/src/topic03_perception/image_detection
$ cp CMakeLists.txt /home/rajat/catkin_ws/src/ros_essentials_cpp/CMakeLists.txt
$ cp objectdetection.msg /home/rajat/catkin_ws/src/ros_essentials_cpp/objectdetection.msg
```
## Step 8 
Open terminal, and type in the following command
```
$ catkin_make
$ roscore
```
## Step 9
Open another 3 terminals parallely, and type in the following commands individually on each of the terminal respectively,
 
 on terminal 1:
 ```
$ cd /home/rajat/catkin_ws/src/ros_essentials_cpp/src/topic03_perception/image_detection
$ rosrun ros_essentials_cpp test.py
```
 on terminal 2:
 ```
$ rosrun turtlesim turtlesim_node
```
 on terminal 3:
 ```
 $ cd /home/rajat/catkin_ws/src/ros_essentials_cpp/src/topic03_perception/image_detection
 $ rosrun ros_essentials_cpp turtlesim_cleaner.py 
 ```
 ## Conclusion
 By now you should be able to detect the egg in the camera feed and also be able to observe changes in turtlebot.
 
