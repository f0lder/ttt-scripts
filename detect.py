"""
-----------------------------------------------------------------------
Project: Playing Tic-Tac-Toe with a robot using Computer Vision and RoboDK
Filename: detect.py
Object: This file contains the functions to detect the Tic-Tac-Toe grid and the shapes inside it
Created Date: Ursan Bogdan-Gabriel 22/04/2024
Last Modified: Ursan Bogdan-Gabriel 5/09/2024
-----------------------------------------------------------------------
"""

# Import the necessary libraries
import cv2
import numpy as np
import player as player

# Define color ranges for red and green
LOWER_RED = np.array([0, 70, 50])
UPPER_RED = np.array([10, 255, 255])

LOWER_GREEN = np.array([50, 70, 50])
UPPER_GREEN = np.array([70, 255, 255])

def show_ranges():
    """
    Function name: show_ranges
    Objective: Display the color ranges for red and green
    Input: None
    Output: None
    """

    # Create an image filled with the lower bound of the red color range
    lower_red_img = np.full((100, 150, 3), LOWER_RED, dtype=np.uint8)
    lower_red_img = cv2.cvtColor(lower_red_img, cv2.COLOR_HSV2BGR)

    # Create an image filled with the upper bound of the red color range
    upper_red_img = np.full((100, 150, 3), UPPER_RED, dtype=np.uint8)
    upper_red_img = cv2.cvtColor(upper_red_img, cv2.COLOR_HSV2BGR)

    # Create an image filled with the lower bound of the green color range
    lower_green_img = np.full((100, 150, 3), LOWER_GREEN, dtype=np.uint8)
    lower_green_img = cv2.cvtColor(lower_green_img, cv2.COLOR_HSV2BGR)

    # Create an image filled with the upper bound of the green color range
    upper_green_img = np.full((100, 150, 3), UPPER_GREEN, dtype=np.uint8)
    upper_green_img = cv2.cvtColor(upper_green_img, cv2.COLOR_HSV2BGR)

    # Concatenate the images horizontally
    all_colors_img = np.concatenate((lower_red_img, upper_red_img, lower_green_img, upper_green_img), axis=1)
    # Display the image
    cv2.imshow('Color Ranges', all_colors_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def convert_matrix(m: list[list[int]]) -> list[int]:
    """
    Function name: convert_matrix
    Objective: Convert a matrix to a list
    Input: m: list[list[int]]
    Output: list[int]
    """
    m = [list(i) for i in zip(*m)]
    l = [item for sublist in m for item in sublist]
    return l


def process_image(img: np.ndarray) -> tuple[cv2.Mat | np.ndarray, list[list[int]]]:
    """
    Function name: process_image
    Objective: Process the image to detect the Tic-Tac-Toe grid and the shapes inside it
    Input: m: np.ndarray (image)
    Output: tuple[cv2.Mat | np.ndarray, list[list[int]]]
    """
    h, w = img.shape[:2]
    img = cv2.resize(img, (w//2, h//2))

    tictactoe = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to binary so that only black areas are left
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assume the grid is the largest contour
        grid_contour = max(contours, key=cv2.contourArea)
        x_main, y_main, w_main, h_main = cv2.boundingRect(grid_contour)

        # Assume the grid is a 9x9 grid
        grid_size = 3

        # Calculate the size of each square
        square_size = w_main// grid_size

        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate the position of the square
                x1 = x_main + i * square_size
                y1 = y_main + j * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size

                # only convert the square to hsv
                square = img[y1:y2, x1:x2]

                hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)

                # Threshold the HSV image to get only red and green colors
                mask_red = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
                mask_green = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

                # Find contours in the red and green masks
                contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # Process the red contours
                for cnt in contours_red:
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(img, (x + x1, y + y1), (x + x1 +w, y + y1+h), (0, 0, 255), 2)  # Draw a red rectangle
                        tictactoe[i][j] = 1

                # Process the green contours
                for cnt in contours_green:
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(img, (x + x1, y + y1), (x + x1+ w, y + y1+h), (0, 255, 0), 2)  # Draw a green rectangle
                        tictactoe[i][j] = 2

        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate the position of the square
                x1 = x_main + i * square_size
                y1 = y_main + j * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                # Draw the square
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Label the square
                label_position = (x1 + 5, y1 + 25)  # Adjust as needed
                cv2.putText(img, f'{i},{j}', label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    else:
        print("No contours found")
        raise ValueError("No contours found")

    return img, tictactoe


# Main function
if __name__ == '__main__':
    img = cv2.imread('C:/Users/Bogdan/Desktop/licenta/unity/Paint3D/ScreenShot.png')
    img, m = process_image(img)

    print("Matrix: ",m)

    l = convert_matrix(m)
    print("List: ",l)

    move, score = player.minimax(2, l)

    # Show the image
    show_ranges()
    cv2.imshow('Detected Shapes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
