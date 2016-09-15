#!/usr/bin/env python
import roslib; roslib.load_manifest('p3dx_mover')
import rospy
from socket import *
import re
import time

from geometry_msgs.msg import Twist

zTwist = 0.0000
xTwist = 0.0000
forward = 0.0
left = 0.0
Max_Forward = 0.5
Max_Side = 0.3

# This segment contains some preliminary items needed so that the socket can listen to anyone who would access its port
host = "" # So that IP doesn't matter
port = 2362 # Remember, this is the port that you MUST connect to on ARC
buf = 1024 # Buffer size
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

print "Waiting to receive messages..." # This is a printout that tells us that our server is ready 

while True: # Our server will continue receiving messages forever until you press the SELECT key on ARC
	#pub = rospy.Publisher('/RosAria/cmd_vel', Twist)
        pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('p3dx_mover')
	twist = Twist()
	(data, addr) = UDPSock.recvfrom(buf) # Socket is listening for messages
	buttonPressed=str(data)
	
        if buttonPressed == "button select 1":  # By pressing the SELECT button, you're shutting down connection between the ARC and GAZEBO
        	print "Closing Socket..."
        	break
        elif (buttonPressed == "button @ 1") and (forward<=Max_Forward):
                forward +=0.1
        elif (buttonPressed == "button % 1") and (left<=Max_Side):
                left+=0.1
        elif (buttonPressed == "button & 1") and (forward>= (0.0 - Max_Forward)):
                forward -=0.1
        elif (buttonPressed == "button # 1") and (left>= (0.0 - Max_Side)):
                left-=0.1
        else:
                zTwist = 0.0
                joyxy = re.findall(r"[-+]?\d*\.\d+|\d+", str(data))
                rightOrLeft = str(data).split(' ')
                if rightOrLeft[1] == "right":	#changes x twist / forward backward
                        print("RIGHT JOYSTICK")
                        print(joyxy[1])
                        temp1 = float(joyxy[1])
                        if temp1 > 0.2 or temp1 < -0.2:
                                xTwist = temp1 -0.2
                        else:
                                xTwist = 0
                if rightOrLeft[1] == "left":	#changes z twist / left right
                        print("LEFT JOYSTICK")
                        zTwist = float(joyxy[0])
                left = zTwist * Max_Side #L/R max .3/-.3
                forward = xTwist * Max_Forward #forward max -1.1 -> 1.1
                
   	print("Forward: " + str(forward) + "    Left/Right: " + str(left))
	twist.linear.x = forward
	twist.angular.z = -1 * left
	pub.publish(twist)
	#rospy.sleep(0.01)

pub = rospy.Publisher('/RosAria/cmd_vel', Twist)  #uncomment for physical p3dx
#pub = rospy.Publisher('cmd_vel', Twist) #for gazebo
rospy.init_node('p3dx_mover')
twist = Twist()
pub.publish(twist)
UDPSock.close()
exit()


        
	
	
