from datetime import datetime
from flask import Flask
from flask import request, Response
from os import environ
import logging
from pathlib import Path
from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepoStub
from slack_bolt import App as BoltApp
from slack_bolt.adapter.flask import SlackRequestHandler
import json

from logging.config import dictConfig

def init_config():
    path_to_logging_config = Path(".") / "config" / "logging_config.json"
    assert path_to_logging_config.exists(), f"The JSON file doesn't exist! expected at {path_to_logging_config.absolute()}"
    logging_config={}
    with open(path_to_logging_config, 'r') as config_file:
        logging_config = json.load(config_file)
    dictConfig(logging_config)

init_config()

logger = logging.getLogger(__name__)

app = BoltApp(signing_secret=environ.get("SIGNING_SECRET"),
              token=environ.get("SLACK_BOT_TOKEN"))

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)
repo = ParkingSpotRepoStub()
designator = ParkingSpotDesignator(repo)

@app.message('omw')
def omw(ack, say, context, client):
    ack()
    user_id, team_id = context['user_id'], context['team_id']
    info = client.users_info(user=user_id)
    logger.info(f'Received omw request from {info} at {team_id}')
    assigned_spot = designator.try_reserve_spot(user_id)
    response_message = "There are no spots available" \
                       if assigned_spot is None \
                       else f"Success, {info['user']['real_name']}! You may park at spot {assigned_spot}" 
    say(response_message)

@app.message('release')
def release(ack, say, context, client):
    ack()
    user_id, team_id = context['user_id'], context['team_id']
    info = client.users_info(user=user_id)
    logger.info(f'Received release request from {info} at {team_id}')
    user_reserved_spots = designator.release_by_user_id(user_id)
    if len(user_reserved_spots) == 0:
        response_message = "User had no assigned parking"
    elif len(user_reserved_spots) == 1:
        response_message = f"Parking spot {user_reserved_spots[0]} has been released successfully"
    else:
        response_message = f"You have several reserved spots: {user_reserved_spots}. Releasing such reservations is not possible in the current version of the app."
    say(response_message)

@app.message('spots')
def spots(ack, say):
    ack()
    number_of_spots = designator.spots()
    say(f"There are {number_of_spots} spots available")


@app.command('/suggestion')
def feedback(ack, say, context, client, command):
    ack()
    logger.debug(context)
    user_id = context['user_id']
    user_name = client.users_info(user=user_id)['user']['real_name']
    feedback = command['text']
    logger.info(f'Feedback from {user_name}: {feedback}')
    say(f'Thanks for your input, {user_name}!')


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
    if data is not None and data['type'] == 'url_verification':
        return data['challenge']
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=int(environ.get("PORT", 5000)))
