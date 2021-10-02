from datetime import datetime
from flask import Flask
from flask import request, Response
from os import environ
import logging
from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepoStub
from slack_bolt import App as BoltApp
from slack_bolt.adapter.flask import SlackRequestHandler

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

app = BoltApp(signing_secret=environ.get("SIGNING_SECRET"),
              token=environ.get("SLACK_BOT_TOKEN"))

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)
repo = ParkingSpotRepoStub()
designator = ParkingSpotDesignator(repo)
user = 'test_user'

@app.message('omw')
def omw(ack, say, context, client):
    ack()
    user_id, team_id = context['user_id'], context['team_id']
    info = client.users_info(user=user_id)
    logger.info(f'Received omw request from {info} at {team_id}')
    say(designator.try_reserve_spot(info['user']['real_name']))

@app.message('release')
def release(ack, say, context):
    #TODO extract 'user' field from payload
    ack()
    user_id, team_id = context['user_id'], context['team_id']
    say(designator.release_by_username(user_id))

@app.message('spots')
def spots(ack, say):
    ack()
    say(designator.spots())

@flask_app.route('/test/healthcheck', methods=['GET'])
def healthcheck():
    response = {
            "message": "I'm alive!", 
            "ts": str(datetime.now())
    }
    return response


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    if data['type'] == 'url_verification':
        return data['challenge']
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=int(environ.get("PORT", 5000)))
