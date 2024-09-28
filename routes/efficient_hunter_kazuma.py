# import logging
# import json

# from flask import request

# from routes import app


# @app.route("/efficient-hunter-kazuma", methods=["POST"])
# def efficient_hunter_kazuma():
#     data = request.get_json()
#     logging.info(f"Data received for evaluation: {data}")
#     result = []
#     for entry in data:
#         monsters = entry["monsters"]
#         efficiency = calculate_efficiency(monsters)
#         result.append({"efficiency": efficiency})

#     # Return the result as a JSON response
#     logging.info("My result :{}".format(result))
#     return json.dumps(result)


# def calculate_efficiency(monsters):

#     pass


def calculate_efficiency(monsters):
    # initialise efficiency
    efficiency = 0
    # set num of battles
    n = len(monsters)
    # set max num of attacks possible
    max_atk = round(n / 3)
    
    monsters_copy = monsters.copy()
    monsters_copy.sort()
    lowest = monsters_copy[:max_atk]
    highest = monsters_copy[-max_atk:]
    print(lowest)
    print(highest)

    if n == 1:
        return efficiency

    i = 0
    while i < n:
        print(i)
        count = monsters[i]
        if count in lowest:
            efficiency -= count
            lowest.remove(count)
            i += 1
        elif count == max(highest):
            efficiency += count
            highest.remove(count)
            i += 2
        else:
            i += 1

    print(lowest)
    print(highest)

    return efficiency

monsters = [1,100,340,210,1,4,530]
print(calculate_efficiency(monsters))