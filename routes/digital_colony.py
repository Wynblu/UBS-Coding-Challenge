from flask import Flask, request, jsonify

from routes import app
def calculate_weight(colony):
    """Calculate the weight of the colony."""
    return sum(int(digit) for digit in colony)

def calculate_signature(pair):
    """Calculate the signature of a digit pair."""
    a, b = int(pair[0]), int(pair[1])
    if a == b:
        return 0
    return abs(a - b) if a > b else 10 - abs(a - b)

def next_generation(colony):
    """Generate the next generation of the colony."""
    new_colony = []
    weight = calculate_weight(colony)

    for i in range(len(colony) - 1):
        pair = colony[i:i+2]
        signature = calculate_signature(pair)
        new_digit = (weight + signature) % 10
        new_colony.append(colony[i])  # retain the current digit
        new_colony.append(str(new_digit))  # add the new digit

    new_colony.append(colony[-1])  # append the last digit
    return ''.join(new_colony)

def simulate_generations(colony, generations):
    """Simulate the colony growth for a number of generations."""
    for _ in range(generations):
        colony = next_generation(colony)
    return calculate_weight(colony)

@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.json
    results = []

    for case in data:
        generations = case['generations']
        colony = case['colony']
        weight_after_generations = simulate_generations(colony, generations)
        results.append(str(weight_after_generations))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
