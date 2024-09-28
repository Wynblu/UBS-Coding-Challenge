import random
from flask import Flask, request, jsonify
from routes import app

# Initialize the Flask app
app = Flask(__name__)

# Load a list of valid 5-letter words (you can use a public word list or your own)
with open("word_list.txt") as f:
    WORD_LIST = [word.strip() for word in f.readlines() if len(word.strip()) == 5]

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

def suggest_next_guess(guess_history, evaluation_history):
    # First guess is always a good word like "slate" if no history
    if not guess_history:
        return "slate"
    
    # Filter words based on previous feedback
    possible_words = filter_words(WORD_LIST, guess_history, evaluation_history)
    
    # Randomly select from the remaining valid words
    return random.choice(possible_words) if possible_words else None

# Define the /wordle-game POST endpoint
@app.route('/wordle-game', methods=['POST'])
def wordle_game():
    data = request.json
    
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])
    
    # Suggest the next guess
    next_guess = suggest_next_guess(guess_history, evaluation_history)
    
    # Respond with the next guess
    return jsonify({"guess": next_guess})

# Running the server
if __name__ == '__main__':
    app.run(debug=True)
