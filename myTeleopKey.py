#!/usr/bin/env python

from cmath import pi
import termios, sys, os
from matplotlib.pyplot import get
import rospy
from turtlesim.srv import TeleportAbsolute, TeleportRelative
from geometry_msgs.msg import Twist 

TERMIOS = termios

def getkey():
    """
    This function asks the system for the key that is currently being pressed and returns
    the equivalent character in UTF-8 format.
    """
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c.decode("utf-8")

def teleport_abs(x, y, ang):
    """
    This funciton calls the rosservice to teleport the turtle to a given
    absolute pose in the canvas. It's used to send the turtle to the origin.
    """
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))

def teleport_rel(x, ang):
    """
    This function calls the rosservice to teleport the turtle a certain distance
    and angle relative to the current position. It's used to change the turtle's direction.
    """
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportR = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp1 = teleportR(x, ang)
        print('Teleported to x: {}, ang: {}'.format(str(x),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))

def pubPose():
    """
    The Main function of the code.  It calls the other functions to publish a pose
    or teleport the turtle according to the key that is pressed.
    """
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('posePub', anonymous=False)
    vel = Twist()
    vel.linear.x = 0
    vel.linear.y = 0
    vel.angular.z = 0
    rate = rospy.Rate(20)
    pressedKey = "o" 
    while pressedKey!="x": #Pressing X works as the exit to our program.
        pressedKey=getkey()
        if pressedKey == "a": #Pressing A turns the turtle counter clockwise
            vel.linear.x = 0
            vel.linear.y = 0
            vel.angular.z = pi/6
            pub.publish(vel)
        if pressedKey == "w": #Pressing W moves the turtle forward
            vel.linear.x = 1
            vel.linear.y = 0
            vel.angular.z = 0
            pub.publish(vel)
        if pressedKey == "s": #Pressing S moves the turtle backwards
            vel.linear.x = -1
            vel.linear.y = 0
            vel.angular.z = 0
            pub.publish(vel)
        if pressedKey == "d": #Pressing D turns the turtle clockwise
            vel.linear.x = 0
            vel.linear.y = 0
            vel.angular.z = -pi/6
            pub.publish(vel)
        if pressedKey == " ": #Pressing SPACE rotates the turtle 180 degrees
            teleport_rel(0,pi)
        if pressedKey == "r": #Pressimg R resets the turtle to the center of the canvas,
            teleport_abs(5.5,5.5,0) 
        rospy.loginfo(vel)   #We constantly print to the terminal the pose of the turtle
        rate.sleep()

if __name__ == '__main__':
    try:
        pubPose()
    except rospy.ROSInterruptException:
        pass