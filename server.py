import socket
import detect
import player
import cv2
import json
import robodk.robolink as robolink
import robodk
import math

RDK = robolink.Robolink()

PATH_TO_UNITY_IMG = "C:/Users/Bogdan/Desktop/licenta/unity/Paint3D/ScreenShot.png"


class RobotSocket:
    def __init__(
        self,
        host="127.0.0.1",
        port=65432,
        robot="Doosan Robotics A0509",
        mid="MID",
        start="Start",
    ):
        self.host = host
        self.port = port
        self.robot = RDK.Item(robot)

        if not self.robot.Valid():
            print("Robot does not exist.")
            return

        self.robot.setPoseFrame(RDK.Item("Board"))

        self.mid = RDK.Item(mid)

        if not self.mid.Valid():
            print("Mid does not exist.")
            return

        self.start = RDK.Item(start)

        if not self.start.Valid():
            print("Start does not exist.")
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()
        self.start_server()

    def prepare_data(self, status: str, message: str, piece: int, choice: int):
        data_to_send = {
            "status": status,
            "joints": self.extractJoints(self.robot.Joints()),
            "message": message,
            "piece": piece,
            "choice": choice,
        }

        data_string = json.dumps(data_to_send)

        return data_string

    def extractJoints(self, joints):
        return [
            round(joints[0, 0], 2),
            round(joints[1, 0], 2),
            round(joints[2, 0], 2),
            round(joints[3, 0], 2),
            round(joints[4, 0], 2),
            round(joints[5, 0], 2),
        ]

    def make_move(self, cell: int, symbol: int):
        t = RDK.Item(str(cell))
        if t.Valid() and symbol in [1, 2]:
            self.robot.MoveJ(self.start)
            self.robot.MoveJ(t)
            if symbol == 1:
                self.moveRobotInXShape(50)
                return
            if symbol == 2:
                self.moveRobotInCircle(20, 20)
                return
        else:
            print("Target does not exist or symbol is invalid.")

    def moveRobotInXShape(self, size: float):
        # Get the current pose of the robot
        current_pose = self.robot.Pose()

        # Define the points of the X shape relative to the current position
        points = [
            current_pose * robodk.transl(0, -size, -size),  # Bottom left
            current_pose,  # Center
            current_pose * robodk.transl(0, size, size),  # Top right
            current_pose,  # Center
            current_pose * robodk.transl(0, -size, size),  # Top left
            current_pose,  # Center
            current_pose * robodk.transl(0, size, -size),  # Bottom right
            current_pose,  # Center
        ]

    def moveRobotInCircle(self, radius, num_points=100):
        # Get the current position of the robot
        current_pose = self.robot.Pose()

        # Calculate the points along the circle
        points = []
        for i in range(num_points):
            # Calculate the angle in radians
            angle = 2 * math.pi * i / num_points

            # Calculate the x and y coordinates
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Calculate the point's pose relative to the current pose
            point = current_pose * robodk.transl(x, y, 0)

            points.append(point)

    def returnCoords(self, target: robolink.Item) -> tuple[float, float, float]:
        """Return the x,y,z coordinates of a target item."""
        target_pose = target.Pose()
        x, y, z = target_pose.Pos()
        return x, y, z

    def createTarget(self, name, x: float, y: float, z: float):
        new_target = RDK.AddTarget(name)

        o = [0.0, 90.0, 0.0]

        target = robodk.KUKA_2_Pose([x, y, z] + o)

        new_target.setPose(target)

        return new_target

    def creategrid(self, distance: int):
        print("Creating grid...")

        x, y, z = self.returnCoords(self.mid)

        targets = [
            self.createTarget("0", x, y + distance, z + distance),
            self.createTarget("1", x, y, z + distance),
            self.createTarget("2", x, y - distance, z + distance),
            self.createTarget("3", x, y + distance, z),
            self.createTarget("4", x, y, z),
            self.createTarget("5", x, y - distance, z),
            self.createTarget("6", x, y + distance, z - distance),
            self.createTarget("7", x, y, z - distance),
            self.createTarget("8", x, y - distance, z - distance),
        ]

    def start_server(self):
        self.creategrid(50)
        with self.conn:
            d = self.prepare_data("done", "Connection established.", 1, -1)
            print(d)
            self.conn.sendall((d + "\n").encode())

            while True:
                try:
                    data = self.conn.recv(1024)

                    if data:

                        dataPos = data.decode("utf-8").split(";")

                        print(dataPos)

                        command = dataPos[0]
                        arg1 = dataPos[1]
                        arg2 = dataPos[2]
                        message = ""
                        piece = 1
                        c = -1

                        if command == "readGrid":
                            # on simulation just load the image
                            # on read case take a picture of the grid
                            img = cv2.imread(PATH_TO_UNITY_IMG)

                            detected, grid = detect.process_image(img)

                            m = detect.convert_matrix(grid)

                            print(m)
                            # cv2.imshow('Detected Shapes', detected)

                            num_X = m.count(1)
                            num_O = m.count(2)

                            if num_X == num_O:
                                piece = 1
                            else:
                                piece = 2

                            c, score = player.minimax(piece, m)
                            message = "Grid read: " + str(m) + " Choice: " + str(c)

                            # check for winner
                            if score == -1:
                                print("Player X wins")
                                message = (
                                    "Grid read: "
                                    + str(m)
                                    + " Choice: "
                                    + str(c)
                                    + "\nX wins"
                                )

                            if score == 1:
                                print("Player O wins")
                                message = (
                                    "Grid read: "
                                    + str(m)
                                    + " Choice: "
                                    + str(c)
                                    + "\nO wins"
                                )

                            if c is not None:
                                self.make_move(c, piece)

                        if command == "Prog1":
                            RDK.Item(command).RunProgram()
                            message = command + " executed."

                        if command == "test":
                            RDK.Item(command).RunProgram()
                            message = command + " executed."

                        if command == "move":
                            t = RDK.Item(arg1)
                            if t.Valid():
                                self.robot.MoveJ(t)
                                message = "Robot moved to " + arg1
                            else:
                                message = "Target does not exist"
                                print("Target does not exist")

                        if c is None:
                            c = -1

                        d = self.prepare_data("done", message, piece, c)
                        print(d)

                        self.conn.sendall((d + "\n").encode())
                except socket.error as e:
                    print(f"Socket error: {e}")

    def close(self):
        self.conn.close()
        self.sock.close()
