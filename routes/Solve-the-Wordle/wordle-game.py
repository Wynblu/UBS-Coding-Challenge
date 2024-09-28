import random
import json
import logging
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load a list of valid 5-letter words
with open("word_list.txt") as f:
    WORD_LIST = [word.strip()
                 for word in f.readlines() if len(word.strip()) == 5]

# Function to filter words based on feedback


def filter_words(word_list, guess_history, evaluation_history):
    filtered_words = word_list.copy()

    for guess, feedback in zip(guess_history, evaluation_history):
        temp_filtered_words = []
        for word in filtered_words:
            match = True
            for i, symbol in enumerate(feedback):
                if symbol == "O" and word[i] != guess[i]:
                    match = False
                elif symbol == "X" and (word[i] == guess[i] or guess[i] not in word):
                    match = False
                elif symbol == "-" and guess[i] in word:
                    match = False
                # Masked symbols (?) are ignored for now
            if match:
                temp_filtered_words.append(word)
        filtered_words = temp_filtered_words

    return filtered_words

# Function to suggest the next best guess


def suggest_next_guess(guess_history, evaluation_history):
    # First guess is always a good word like "slate" if no history
    if not guess_history:
        return "slate"

    # Filter words based on previous feedback
    possible_words = filter_words(WORD_LIST, guess_history, evaluation_history)

    # Randomly select from the remaining valid words
    return random.choice(possible_words) if possible_words else None

# Define the /square route for evaluation


@app.route('/wordle-game', methods=['POST'])
def evaluate():
    # Get the data from the request
    data = request.get_json()

    logging.info("data sent for evaluation {}".format(data))

    # Extract guessHistory and evaluationHistory
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])

    # Log guess history and evaluation history for debugging
    logging.info("Guess history: {}".format(guess_history))
    logging.info("Evaluation history: {}".format(evaluation_history))

    # Suggest the next guess
    next_guess = suggest_next_guess(guess_history, evaluation_history)

    # Log the result
    logging.info("My result (next guess): {}".format(next_guess))

    # Return the next guess as a JSON response
    return json.dumps({"guess": next_guess})


# Running the server
if __name__ == '__main__':
    app.run(debug=True)
