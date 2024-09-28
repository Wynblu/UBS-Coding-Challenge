from flask import Flask, request, jsonify
from collections import defaultdict

from routes import app

def generate_mistyped_variants(word):
    """Generate all possible mistyped variants of the given word by changing one character."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    variants = set()
    
    for i in range(len(word)):
        for letter in letters:
            if word[i] != letter:
                variant = word[:i] + letter + word[i+1:]
                variants.add(variant)
    
    return variants

def correct_mistypes(dictionary, mistypes):
    """Correct mistyped words based on the dictionary."""
    # Create a mapping from mistyped variants to the correct words
    mistyped_to_correct = defaultdict(list)

    for word in dictionary:
        for mistyped_variant in generate_mistyped_variants(word):
            mistyped_to_correct[mistyped_variant].append(word)

    corrections = []
    
    for mistyped in mistypes:
        # Find the correct word corresponding to the mistyped word
        correct_words = mistyped_to_correct.get(mistyped, [])
        corrections.append(correct_words[0] if correct_words else mistyped)  # Append the first correct word or original if none found

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
