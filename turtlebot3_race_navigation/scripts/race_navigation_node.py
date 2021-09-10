#!/usr/bin/env python
from logging import info
import rospy
import time
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import String
#The following checkpoint coordinates only apply to the Gazebo world "turtlebot3_autorace.launch"

start_time = time.time()

class FinalMessage:

    info_string = ""

class Checkpoint:

    checkpoints = []
    checkpoints.append((0,-1.5, "Finish Line"))
    checkpoints.append((1.90, 0.95,"Parking Lot"))
    checkpoints.append((-1,1.45,"Roundabout"))
    checkpoints.append((-1,0, "Maze"))
    lap, finish_check, parking_check, round_check, maze_check = 0,0,0,0,0
    next_location = []

def line_checker(x,y):

    if Checkpoint.lap == 0:
        
        Checkpoint.next_location.clear()
        Checkpoint.next_location.append(Checkpoint.checkpoints[1])
        Checkpoint.lap+=1

    elif x >= 0 and x <= 2 and y >= 0.95 and Checkpoint.parking_check == 0:
        Checkpoint.next_location.clear()
        Checkpoint.next_location.append(Checkpoint.checkpoints[2])
        Checkpoint.parking_check+=1
        Checkpoint.finish_check = 0
    
    elif x < 0 and y > 0 and y <= 1.45 and Checkpoint.round_check == 0 and Checkpoint.parking_check == 1:
        Checkpoint.next_location.clear()
        Checkpoint.next_location.append(Checkpoint.checkpoints[3])
        Checkpoint.round_check+=1
    
    elif x < 0 and y < 0 and Checkpoint.maze_check == 0 and Checkpoint.round_check == 1:
        Checkpoint.next_location.clear()
        Checkpoint.next_location.append(Checkpoint.checkpoints[0])
        Checkpoint.maze_check+=1
    
    elif x >= 0 and y <= -1 and Checkpoint.maze_check == 1 and Checkpoint.finish_check == 0:
        Checkpoint.next_location.clear()
        Checkpoint.next_location.append(Checkpoint.checkpoints[1])
        Checkpoint.lap+=1
        Checkpoint.finish_check += 1
        Checkpoint.parking_check, Checkpoint.round_check, Checkpoint.maze_check = 0


def checkpoint_checker(x,y):
    closest_name = None
    closest = None
    for check_locx, check_locy, check_name in Checkpoint.checkpoints:
        tmp = math.sqrt((x - check_locx)**2 * (y - check_locy)**2)
        if closest_name is None or tmp < closest:
            closest = tmp
            closest_name = check_name
    print("I'm close to the ", closest_name, ", Distance:", round(closest))#replace with pub
    prev_closest = closest_name
    line_checker(x,y)
    current_time = time.time() - start_time
    FinalMessage.info_string = "I'm close to the " + str(closest_name) + ", Distance:" + str(round(closest)) + "I should head towards " + str(Checkpoint.next_location) + " Lap:" + str(Checkpoint.lap) + "Elapsed time: " + str(round(current_time))
    print("I should head towards ", Checkpoint.next_location, " Lap:", Checkpoint.lap, "Elapsed time: ", round(current_time))


def callback(data):
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    checkpoint_checker(x,y)
    
def main():

    #Choose a unique ID 
    rospy.init_node('race_navigator', anonymous=True) #!!!WATCH OUT FOR NAME DIFFERENCE!!!
    rospy.Subscriber("/odom", Odometry, callback)
    pub = rospy.Publisher('closest', String, queue_size=10)
    pub.publish(FinalMessage.info_string)
    rate = rospy.Rate(10)#10hz
    while not rospy.is_shutdown():
        rospy.loginfo(FinalMessage.info_string)
        pub.publish(FinalMessage.info_string)
        rate.sleep()
    rospy.spin() #Loop

if __name__ == '__main__':
    main()