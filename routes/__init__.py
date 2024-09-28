from flask import Flask

app = Flask(__name__)
import routes.square
import routes.solve_the_wordle
import efficient_hunter_kazuma