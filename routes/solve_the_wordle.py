from flask import Flask, request, jsonify
from routes import app

# Load a wordlist of 5 letter words
def load_word_list():
    with open('word_list.txt') as f:
        return [word.strip() for word in f.readlines()]
    
# Get the word list initialised and have the first word guessed be slate
word_list = load_word_list()
initial_guess = "slate"

# filter words based on feedback given
def filter_words(guess_history, eval_history):
    possible_words = word_list[:]
    for guess, eval in zip(guess_history, eval_history):
        if eval != "OOOOO":
            possible_words.remove(guess)
    for word, guess, eval in zip(possible_words, guess_history, eval_history):
        for w_letter, g_letter, symbol in zip(word, guess, eval):
            if symbol == '?':
                continue
            elif not match_eval(w_letter, g_letter, symbol):
                possible_words.remove(word)

    return possible_words
    
    return possible_words

def match_eval(w_letter, g_letter, symbol):
    if symbol == '-' and w_letter == g_letter:
        return False
    elif symbol == 'X' and w_letter == g_letter:
        return False
    elif symbol == 'O' and w_letter != g_letter:
        return False
    return True




# get the next guess
def get_next_guess(guess_history, eval_history):
    if not guess_history:
        return initial_guess
    possible_words = filter_words(guess_history, eval_history)
    return possible_words[0] if possible_words else "error"

@app.route('/wordle-game', methods=['POST'])
def wordle_game():
    data = request.get_json()
    guess_history = data.get('guessHistory', [])
    eval_history = data.get('evaluationHistory', [])
    next_guess = get_next_guess(guess_history, eval_history)
    return jsonify({"guess": next_guess})