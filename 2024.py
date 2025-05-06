import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def init_board():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)
    board[i][j] = 2 if random.random() < 0.9 else 4

def print_board(board):
    clear_screen()
    print("\n2048 Game — Use W/A/S/D to move. Press Q to quit.\n")
    for row in board:
        print("+------+------+------+------+")

        for cell in row:
            print(f"|{str(cell).center(6) if cell else '      '}", end="")
        print("|")
    print("+------+------+------+------+")

def compress(row):
    """Shift non-zero values to the left."""
    new_row = [i for i in row if i != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def merge(row):
    """Merge the same values."""
    for i in range(3):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    return row

def move_left(board):
    moved = False
    new_board = []
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        new_board.append(final)
        if row != final:
            moved = True
    return new_board, moved

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved_board, moved = move_left(reversed_board)
    return [row[::-1] for row in moved_board], moved

def move_up(board):
    transposed = list(zip(*board))
    moved_board, moved = move_left([list(row) for row in transposed])
    return [list(row) for row in zip(*moved_board)], moved

def move_down(board):
    transposed = list(zip(*board))
    moved_board, moved = move_right([list(row) for row in transposed])
    return [list(row) for row in zip(*moved_board)], moved

def is_game_over(board):
    for move in [move_left, move_right, move_up, move_down]:
        _, moved = move(board)
        if moved:
            return False
    return True

def play_2048():
    board = init_board()
    while True:
        print_board(board)
        move = input("Move (W/A/S/D): ").upper()
        if move == 'Q':
            print("Thanks for playing!")
            break
        moves = {'W': move_up, 'A': move_left, 'S': move_down, 'D': move_right}
        if move in moves:
            board, moved = moves[move](board)
            if moved:
                add_new_tile(board)
                if is_game_over(board):
                    print_board(board)
                    print("💀 Game Over!")
                    break
        else:
            print("Invalid input. Use W/A/S/D to move.")

if __name__ == "__main__":
    play_2048()
