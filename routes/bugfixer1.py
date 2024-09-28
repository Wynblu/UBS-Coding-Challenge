from flask import Flask, request, jsonify
from collections import defaultdict, deque

from routes import app

# Function to calculate the minimum time to resolve all bugs
def calculate_min_time(n, times, prerequisites):
    # Build the graph and indegree count
    graph = defaultdict(list)
    indegree = [0] * n

    # Prepare graph and indegree based on prerequisites
    for prereq in prerequisites:
        a, b = prereq
        graph[a - 1].append(b - 1)
        indegree[b - 1] += 1

    # Queue for projects that can be worked on immediately (i.e., no prerequisites)
    queue = deque()

    # Start time for each project
    start_time = [0] * n

    # Initialize queue with projects that have no prerequisites
    for i in range(n):
        if indegree[i] == 0:
            queue.append(i)

    # Topological sort and calculate the minimum time to complete all projects
    while queue:
        project = queue.popleft()

        for dependent_project in graph[project]:
            # Update the start time for dependent projects
            start_time[dependent_project] = max(
                start_time[dependent_project], start_time[project] + times[project])

            # Reduce indegree and add to the queue if all prerequisites are met
            indegree[dependent_project] -= 1
            if indegree[dependent_project] == 0:
                queue.append(dependent_project)

    # The total time to complete the projects is the maximum start_time + the project time
    return max(start_time[i] + times[i] for i in range(n))

# Endpoint to handle the bug fixing task
@app.route('/bugfixer/p1', methods=['POST'])
def bugfixer():
    data = request.get_json()
    result = []

    # Process each bug fixing task
    for task in data:
        times = task["time"]
        prerequisites = task["prerequisites"]
        n = len(times)

        # Calculate the minimum time for each task
        min_time = calculate_min_time(n, times, prerequisites)
        result.append(min_time)

    # Return the result as JSON
    return jsonify(result)

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
