"""
-----------------------------------------------------------------------
Priect de diploma: APLICAȚIE BAZATĂ PE INTELIGENȚĂ ARTIFICIALĂ DE TIP TIC TAC TOE SIMULATĂ PE UN ROBOT VIRTUAL
Nume fișier: main.py
Descriere: Acest fișier conține codul principal al aplicației
Data creării: Ursan Bogdan-Gabriel 22/04/2024
Ultima modificare: Ursan Bogdan-Gabriel 20/06/2024
-----------------------------------------------------------------------
"""

print("Project: Playing Tic-Tac-Toe with a robot using Computer Vision and RoboDK")
print("Running main.py...")

import server

s = server.RobotSocket()
print("Initializing the server.")

s.connect()
print("Connecting to the Robot.")
