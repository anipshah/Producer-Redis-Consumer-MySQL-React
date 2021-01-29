from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from services.PostConsumer import PostConsumer
import Constants
from error_handler import MessageException

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'

# init consumer service
post_consumer = PostConsumer()


@app.errorhandler(MessageException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/send', methods=['POST'])
@cross_origin('*')
def add_post():
    """
    Route to store message request

    :return: response with message number
    """
    message_number: int = post_consumer.consume(request.json)

    return {Constants.MESSAGE_NUMBER: message_number}


@app.route('/stats', methods=['GET'])
@cross_origin('*')
def get_stats():
    """
    Route to get statistics using seconds parameter

    :return: Dict[str,Any]: response with max message number and average time
    """

    seconds: int = request.args.get(Constants.SECONDS_PARAM)
    stats = post_consumer.get_stats(seconds)
    return stats


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
