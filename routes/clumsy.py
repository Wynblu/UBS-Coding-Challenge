from flask import request, jsonify

from routes import app
def is_mistyped(correct_word, mistyped_word):
    """Check if mistyped_word can be formed by mistyping one character in correct_word."""
    if len(correct_word) != len(mistyped_word):
        return False

    diff_count = sum(1 for a, b in zip(correct_word, mistyped_word) if a != b)
    return diff_count == 1

def correct_mistypes(dictionary, mistypes):
    """Correct mistyped words based on the dictionary."""
    corrections = []
    
    for mistyped in mistypes:
        # Find the correct word that differs by exactly one character
        correct_word = next((word for word in dictionary if is_mistyped(word, mistyped)), None)
        corrections.append(correct_word if correct_word else mistyped)  # Append the correct word or original if none found

    return corrections

@app.route('/the-clumsy-programmer', methods=['POST'])
def clumsy_programmer():
    data = request.json
    results = []

    for case in data:
        dictionary = case.get("dictionary", [])
        mistypes = case.get("mistypes", [])
        corrections = correct_mistypes(dictionary, mistypes)
        results.append({"corrections": corrections})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
