import subprocess
import time

def parse_board(output_lines):
    #Parse the tic-tac-toe board from the output lines.
    board = []
    for line in output_lines:
        if len(line.strip().split()) == 3 and all(char in 'x_o' for char in line.strip().replace(' ', '')):
            board.append(line.strip().split())
    return board

def n_moves(board):
    #Count the number of moves made on the board.
    ans = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != '_':
                ans += 1
    print(f"Board state in n_moves function:\n{board}")
    print(f"Number of moves: {ans}")
    return ans

def find_best_move(board):
    # Find the best move (row, col) for the bot.
    moves = n_moves(board)
    if moves == 0:
        return (0, 0)
    elif moves == 2:
        if board[1][1] == '_' and board[2][2] == '_':
            return (1, 1)
        else:
            return (2, 0)
    elif moves == 4:
        if board[1][1] == 'o' and board[2][2] == '_':
            return (2, 2)
        if board[1][1] == 'o' and board[2][2] == 'x':
            if board[0][2] == 'x':
                return (1, 2)
            elif board[1][2] == 'x':
                return (0, 2)
            elif board[2][0] == 'x':
                return (2, 1)
            else:
                return (2, 0)
        if board[2][0] == 'o' and board[1][0] == '_':
            return (1, 0)
        if board[2][0] == 'o' and board[1][0] == 'x':
            if board[1][1] == 'x':
                return (1, 2)
            else: 
                return (1, 1)
    elif moves == 6:
        if board[1][1] == 'o' and board[2][2] == 'x':
            if board[0][2] == 'x' and board[1][2] == 'o':
                if board[1][0] == 'x':
                    return (2, 0)
                else:
                    return (1, 0)
            elif board[1][2] == 'x' and board[0][2] == 'o':
                if board[0][1] == 'x':
                    return (2, 0)
                else:
                    return (0, 1)
            elif board[2][0] == 'x' and board[2][1] == 'o':
                if board[0][1] == 'x':
                    return (0, 2)
                else:
                    return (0, 1)
            else:
                if board[0][2] == 'x':
                    return (1, 2)
                else:
                    return (0, 2)
        elif board[2][0] == 'o' and board[1][0] == 'x':
            if board[1][1] == 'x' and board[1][2] == 'o':
                if board[0][1] == 'x':
                    return (2, 1)
                else:
                    return (0, 1)
            else: 
                if board[0][2] == 'x':
                    return (1, 2)
                else:
                    return (0, 2)
    elif moves == 8:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == '_':
                    return (i, j)
    return None

def run_game(executable_path):
    process = subprocess.Popen([executable_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = []

    while True:
        output = process.stdout.readline()
        output_lines.append(output)
        print(output.strip())  # Print each line of output for debugging
        
        if "Enter the block" in output:
            board = parse_board(output_lines)
            for row in board:  # Print the current board state for debugging
                print(" ".join(row))
            move = find_best_move(board)
            if move:
                move_str = f"{move[0]},{move[1]}"
                print(f"Bot move: {move_str}")  # Print the selected move for debugging
                process.stdin.write(move_str + "\n")
                process.stdin.flush()
            else:
                print("No valid moves left.")
                break
            output_lines = []  # Clear output_lines after making a move
        elif "You lost" in output or "You won" in output or "Draw" in output:
            print(output)
        elif "flag" in output:
            print(output)
            break

# Run the game
executable_path = "./ttt"  # Update this path to the correct location of your executable
run_game(executable_path)
