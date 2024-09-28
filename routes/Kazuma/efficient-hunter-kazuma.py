import logging
import json
from flask import request

from routes import app

# Function to calculate efficiency


def calculate_efficiency(monster_counts):
    efficiency = 0
    n = len(monster_counts)
    i = 0

    while i < n:
        if monster_counts[i] > 0:
            # Prepare transmutation circle at time tX
            circle_cost = monster_counts[i]
            total_monsters_defeated = 0

            # Find the best time to attack (Kazuma can wait)
            # Check for the next non-zero time slot to attack
            while i < n and monster_counts[i] > 0:
                total_monsters_defeated += monster_counts[i]
                i += 1

            # Earnings are the total monsters defeated minus the cost to prepare the circle
            efficiency += (total_monsters_defeated - circle_cost)
        else:
            i += 1

    return max(efficiency, 0)  # Efficiency can't be negative

# Route to expose the POST endpoint for verification


@app.route('/efficient-hunter-kaszuma', methods=['POST'])
def evaluate():
    # Parse the incoming request data
    data = request.get_json()
    logging.info(f"Data received for evaluation: {data}")

    # Process the data
    input_data = data.get("input", [])

    result = []

    # Loop over all sets of monster counts in the input
    for entry in input_data:
        monsters = entry.get("monsters", [])
        efficiency = calculate_efficiency(monsters)
        result.append({"efficiency": efficiency})

    # Log and return the result as a JSON response
    logging.info(f"Result sent: {result}")
    return json.dumps(result)


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
