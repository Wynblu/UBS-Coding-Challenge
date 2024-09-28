import logging
import json

from flask import request, jsonify

from routes import app

@app.route("/the-clumsy-programmer", methods=["POST"])
def clumsy():
    data = request.get_json()
    dictionary = data[0]["dictionary"]
    mistypes = data[0]["mistypes"]
    result = fix_errors(dictionary, mistypes)
    correrctions = [{"correrctions": result}]
    return jsonify(correrctions)


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