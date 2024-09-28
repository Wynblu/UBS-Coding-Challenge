from routes import app
import logging
import socket
from routes.Kazuma import kazuma

logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def default_route():
    return 'Python Template'


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)


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
