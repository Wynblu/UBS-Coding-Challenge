from flask import Flask, request, jsonify

from routes import app

# translate the input string to a board
def string_to_board(board_str):
    return [list(board_str[i:i+4]) for i in range(0, 20, 4)]

# translate the board back to string after shuffle
def board_to_string(board):
    return ''.join(''.join(row) for row in board)

# Find all coordinates occupied by a given letter block
def find_block_positions(board, block):
    positions = []
    for r in range(5):
        for c in range(4):
            if board[r][c] == block:
                positions.append((r, c))
    return positions

# check if space is open ('@') for the block to move
def can_move(block_positions, direction, board):
    if direction == 'N':
        return all(r - 1 >= 0 and board[r - 1][c] == '@' for r, c in block_positions if r == min(row[0] for row in block_positions))
    if direction == 'S':
        return all(r + 1 < 5 and board[r + 1][c] == '@' for r, c in block_positions if r == max(row[0] for row in block_positions))
    if direction == 'W':
        return all(c - 1 >= 0 and board[r][c - 1] == '@' for r, c in block_positions if c == min(col[1] for col in block_positions))
    if direction == 'E':
        return all(c + 1 < 4 and board[r][c + 1] == '@' for r, c in block_positions if c == max(col[1] for col in block_positions))
    return False

# Move the block on the board in the specified direction
def move_block(board, block, direction):
    block_positions = find_block_positions(board, block)
    # Don't move when it is invalid
    if not can_move(block_positions, direction, board):
        return board  

    # replace old position with "@" 
    for r, c in block_positions:
        board[r][c] = '@'

    # Calculate new positions based on the direction
    if direction == 'N':
        new_positions = [(r - 1, c) for r, c in block_positions]
    elif direction == 'S':
        new_positions = [(r + 1, c) for r, c in block_positions]
    elif direction == 'W':
        new_positions = [(r, c - 1) for r, c in block_positions]
    elif direction == 'E':
        new_positions = [(r, c + 1) for r, c in block_positions]

    # Place the letter block in new positions
    for r, c in new_positions:
        board[r][c] = block

    return board

# Apply moves in batches 
def apply_moves(board_str, moves_str):
    board = string_to_board(board_str)

    # Group moves by block
    i = 0
    while i < len(moves_str):
        block = moves_str[i]
        direction = moves_str[i + 1]
        board = move_block(board, block, direction)
        i += 2  # Move to the next block move pair

    return board_to_string(board)

# API endpoint to handle multiple board and move combinations
@app.route('/klotski', methods=['POST'])
def klotski():
    data = request.get_json()
    result = []
    
    for task in data:
        board_str = task["board"]
        moves_str = task["moves"]
        result_board = apply_moves(board_str, moves_str)
        result.append(result_board)
    
    return jsonify(result)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
