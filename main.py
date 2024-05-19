"""
-----------------------------------------------------------------------
Project: Playing Tic-Tac-Toe with a robot using Computer Vision and RoboDK
Filename: main.py
Object: This file is the main file that runs the server and connects to the robot
Created Date: Ursan Bogdan-Gabriel 22/04/2024
Last Modified: Ursan Bogdan-Gabriel 5/09/2024
-----------------------------------------------------------------------
"""

import server

s = server.RobotSocket()

s.connect()
