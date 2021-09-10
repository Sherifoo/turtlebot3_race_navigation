# turtlebot3_race_navigation
Basic information and infrastructure necessary for doing a race with Turtlebot3 simulation.

YOU NEED:
- ROS Noetic
- Turtlebot3 with turtlebot3_gazebo and turtlebot3_autorace.world

HOW TO RUN:
- Launch gazebo simulation (roslaunch turtlebot3_gazebo turtlebot3_autorace.launch)
- Launch the turtlebot teleop key (rosrun turtlebot3_teleop turtlebot3_teleop_key)
- Run the python code
- The node publishes the topic 'closest' (rostopic echo closest)

TODO:
- Countdown to start
- Set amount of laps
- Lane detection to limit movement to race tracks
- Different coordinates according to Gazebo world
