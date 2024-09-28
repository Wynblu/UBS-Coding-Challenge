import logging
import json

from flask import request

from routes import app


@app.route("/the-clumsy-programmer", methods=["POST"])
def clumsy():
    data = request.get_json()
    logging.info(f"Data received for evaluation: {data}")
    print(data)
    dictionary = data[0]["dictionary"]
    mistypes = data[0]["mistypes"]
    result = fix_errors(dictionary, mistypes)
    # Return the result as a JSON response
    logging.info("My result :{}".format(result))
    return json.dumps(result)


import difflib

def fix_errors(dictionary, mistypes):
    corrected_words = []
    for word in mistypes:
        matches = difflib.get_close_matches(word, dictionary, n=1)
        if matches:
            corrected_words.append(matches[0])
        else:
            corrected_words.append(word) 
    return corrected_words

dictionary = ["purple", "rocket", "silver", "gadget", "window", "dragon"]
mistypes = ["purqle", "gadgat", "socket", "salver"]
corrected_words = fix_errors(dictionary, mistypes)

print(corrected_words)