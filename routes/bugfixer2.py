from flask import Flask, request, jsonify
import heapq

from routes import app

# Function to calculate the maximum number of bugs Bobby can fix
def max_bugsfixed(bugseq):
    # Sort bugs by their deadline limit
    bugseq.sort(key=lambda x: x[1])  # Sort by deadline
    
    total_time = 0  # Track the total time spent
    heap = []  # Min-heap to track the bugs Bobby has chosen to fix
    
    for bug in bugseq:
        difficulty, limit = bug
        
        if total_time + difficulty <= limit:
            # If we can complete this bug within its deadline, add it to the heap
            heapq.heappush(heap, -difficulty)  # Use negative values to simulate a max-heap
            total_time += difficulty
        elif heap and -heap[0] > difficulty:
            # If we cannot fit this bug, but we have a more time-consuming bug, replace it
            total_time += difficulty + heapq.heappop(heap)  # Remove the longest-duration bug
            heapq.heappush(heap, -difficulty)
    
    # The number of bugs Bobby can fix is the size of the heap
    return len(heap)

# API endpoint
@app.route('/bugfixer/p2', methods=['POST'])
def bugfixer_part2():
    data = request.get_json()
    result = []
    
    # Process each bug sequence task
    for task in data:
        bugseq = task["bugseq"]
        # Calculate the maximum number of bugs fixed
        max_fixed = max_bugsfixed(bugseq)
        result.append(max_fixed)
    
    # Return the result as JSON
    return jsonify(result)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
