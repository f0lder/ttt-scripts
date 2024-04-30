"""This module contains the player class and the minimax algorithm for the AI player."""


board = [0 for _ in range(9)]  # 0 represents an empty space

# Function to check if the board is full
def is_board_full(board : list[int]):
    return 0 not in board

# Function to check if a player has won
def check_winner(player : int,board : list[int]):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            return True
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            return True
    # Check diagonals
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    return False

# Minimax function
def minimax(player : int,board :list[int]) -> tuple[int | None,float | None]:
    if check_winner(1,board):  # 1 represents 'X'
        return None, -1
    elif check_winner(2,board):  # 2 represents 'O'
        return None, 1
    elif is_board_full(board):
        return None, 0

    best_move = None
    if player == 2:  # Maximizing player
        best_score = -float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = player
                _, score = minimax(1,board)
                board[i] = 0
                if score is not None and (best_score is None or score > best_score):
                    best_score = score
                    best_move = i
    else:  # Minimizing player
        best_score = float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = player
                _, score = minimax(2,board)
                board[i] = 0
                if score is not None and score < best_score:
                    best_score = score
                    best_move = i

    return best_move, best_score

# Function to draw the board
def draw_board():
    print("---------")
    for i in range(0, 9, 3):
        print(board[i], board[i+1], board[i+2])
    print("---------")


def main():
    current_player = 1  # Player 1 starts

    while True:
        draw_board()
        if current_player == 1:
            move = int(input("Enter your move (0-8): "))
            if board[move] != 0:
                print("Invalid move. Try again.")
                continue
            board[move] = current_player
        else:
            move, _ = minimax(current_player, board)
            board[move] = current_player

        if check_winner(current_player, board):
            draw_board()
            print(f"Player {current_player} wins!")
            break
        elif is_board_full(board):
            draw_board()
            print("It's a draw!")
            break
        else:
            current_player = 3 - current_player  # Switch player


if __name__ == "__main__":
    main()