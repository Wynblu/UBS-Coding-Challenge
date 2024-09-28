from flask import jsonify
import logging
import json
from flask import request

from routes import app

# Function to extract the block positions from the board string


def get_block_positions(board):
    positions = {}
    for r in range(4):
        for c in range(5):
            block = board[r * 5 + c]
            if block != '@':
                if block not in positions:
                    positions[block] = []
                positions[block].append((r, c))
    return positions

# Function to create a new board from the block positions


def create_board(positions):
    board = ['@'] * 20
    for block, coords in positions.items():
        for (r, c) in coords:
            board[r * 5 + c] = block
    return ''.join(board)

# Function to apply moves on the board


def apply_moves(board, moves):
    positions = get_block_positions(board)
    for i in range(0, len(moves), 2):
        block = moves[i]
        direction = moves[i + 1]

        # Get the current positions of the block
        coords = positions[block]
        if direction == 'N':
            # Move up
            new_coords = [(r - 1, c) for (r, c) in coords]
        elif direction == 'S':
            # Move down
            new_coords = [(r + 1, c) for (r, c) in coords]
        elif direction == 'E':
            # Move right
            new_coords = [(r, c + 1) for (r, c) in coords]
        elif direction == 'W':
            # Move left
            new_coords = [(r, c - 1) for (r, c) in coords]

        # Update the positions
        positions[block] = new_coords

    # Create the final board after all moves
    return create_board(positions)

# POST endpoint for Klotski game


@app.route('/klotski', methods=['POST'])
def klotski():
    data = request.get_json()
    results = []

    for entry in data:
        board = entry['board']
        moves = entry['moves']
        result_board = apply_moves(board, moves)
        results.append(result_board)

    return jsonify(results)


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
