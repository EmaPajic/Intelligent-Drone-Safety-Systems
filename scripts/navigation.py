#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: EmaPajic
"""

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from point import Point
from math import atan2

class Navigator:
    def __init__(self):
        self.odom_msg = None
        rospy.init_node('navigation', anonymous=True)
        self.rate = rospy.Rate(25) # 25hz
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size = 1)
	self.odom_sub = rospy.Subscriber("odom", Odometry, self.callback)
        
    def callback(self, msg):
        self.odom_msg = msg
                        
    def move_linear_cmd(self, speed = 1):
	print('linear cmd ' + str(speed))
        move_cmd = Twist()
        move_cmd.linear.x = speed
	move_cmd.angular.z = 0
        self.cmd_vel.publish(move_cmd)
        self.rate.sleep()
	print('linear cmd end')
        
    def move_angular_cmd(self, angle = 0):
	print('angular cmd ' + str(angle))
	turn_cmd = Twist()
	turn_cmd.linear.x = 0
	turn_cmd.angular.z = angle
	self.cmd_vel.publish(turn_cmd)
	self.rate.sleep()
	print('angular cmd end')
        
    def move_point_to_point(self,destination):
	if self.odom_msg is not None:
		x_from = self.odom_msg.pose.pose.position.x
		y_from = self.odom_msg.pose.pose.position.y
		x_to = destination.x
		y_to = destination.y
		q = self.odom_msg.pose.pose.orientation
		quaternion = [q.x, q.y, q.z, q.w]
		roll,pitch,yaw = euler_from_quaternion(quaternion)
		new_angle = 0
		'''if y_to - y_from > 0:
			new_angle = np.arccos((x_to - x_from) / np.sqrt((x_to - x_from)**2 + (y_to - y_from)**2))
		else:
			new_angle = - np.arccos((x_to - x_from) / np.sqrt((x_to - x_from)**2 + (y_to - y_from)**2))'''
		while abs(new_angle - yaw) > 0.02:
			new_angle = atan2(y_to - y_from, x_to - x_from)
			self.move_angular_cmd(new_angle - yaw)
			x_from = self.odom_msg.pose.pose.position.x
			y_from = self.odom_msg.pose.pose.position.y
			q = self.odom_msg.pose.pose.orientation
			quaternion = [q.x, q.y, q.z, q.w]
			roll,pitch,yaw = euler_from_quaternion(quaternion)
		while (abs(x_from - x_to) > 0.2 or abs(y_from - y_to) > 0.2):
			self.move_linear_cmd(0.5)
			x_from = self.odom_msg.pose.pose.position.x
			y_from = self.odom_msg.pose.pose.position.y
		self.move_linear_cmd(0)
	
    def navigation(self):
        while not rospy.is_shutdown():
            self.move_point_to_point(Point(0,0))
	    self.move_point_to_point(Point(2,2))
        
if __name__ == '__main__':
    try:
        nav = Navigator()
        nav.navigation()
    except rospy.ROSInterruptException:
        pass
