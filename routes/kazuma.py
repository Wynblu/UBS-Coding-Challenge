from flask import Flask, request, jsonify

from routes import app
def calculate_efficiency(monsters):
    n = len(monsters)
    # dp[i] will hold the maximum efficiency starting from time i
    dp = [0] * (n + 1)

    # Iterate backwards through time
    for i in range(n - 1, -1, -1):
        max_efficiency = 0
        
        # Evaluate possible attacks from current time i
        total_gold = 0
        total_cost = 0

        # Explore all potential future attacks starting from i
        for j in range(i, n):
            # If this is the first attack opportunity
            if j == i:
                total_gold += monsters[j]  # Earn gold from military
                total_cost += monsters[j]   # Pay for adventurers' protection

            # If we are not in the first attack, we consider previous attacks and costs
            else:
                total_gold += monsters[j]
                # Add adventurers' cost for the previous turn
                if j - 1 >= i:
                    total_cost += monsters[j - 1]  # Protecting him for this turn

            # Calculate current efficiency including future possibilities
            if j + 1 < n:  # After attacking at j, he can start again at j + 2
                current_efficiency = total_gold - total_cost + dp[j + 1]
            else:
                current_efficiency = total_gold - total_cost
            
            max_efficiency = max(max_efficiency, current_efficiency)

        # Save the best efficiency starting from this time frame
        dp[i] = max_efficiency

    return dp[0]

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def efficient_hunter_kazuma():
    data = request.get_json()
    efficiencies = []

    for case in data:
        monsters = case.get("monsters", [])
        efficiency = calculate_efficiency(monsters)
        efficiencies.append({"efficiency": efficiency})

    return jsonify(efficiencies)

if __name__ == "__main__":
    app.run(debug=True)
