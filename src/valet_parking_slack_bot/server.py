from datetime import datetime
from flask import Flask
from flask import request
from os import environ
import logging
from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepoStub

from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

dictConfig(logging_config)

logger = logging.getLogger(__name__)

app = Flask(__name__)
repo = ParkingSpotRepoStub()
designator = ParkingSpotDesignator(repo)
user = 'test_user'

@app.route('/omw', methods=['POST'])
def omw():
    #TODO translate UIDs to display names
    data = request.form
    user_id, team_id = data['user_id'], data['team_id']
    logger.info(f'Received omw request from {user_id} at {team_id}')
    return designator.try_reserve_spot(data['user_name'])

@app.route('/release', methods=['POST'])
def release():
    #TODO extract 'user' field from payload
    return designator.release_by_username(user)

@app.route('/spots', methods=['POST'])
def spots():
    return designator.spots()

@app.route('/test/healthcheck', methods=['GET'])
def healthcheck():
    response = {
            "message": "I'm alive!", 
            "ts": str(datetime.now())
    }
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(environ.get("PORT", 5000)))
