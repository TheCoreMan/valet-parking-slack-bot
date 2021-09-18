from datetime import datetime
from flask import Flask
from flask import request
from os import environ
from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepoStub

app = Flask(__name__)
repo = ParkingSpotRepoStub()
designator = ParkingSpotDesignator(repo)
user = 'test_user'

@app.route('/omw', methods=['POST'])
def omw():
    #TODO extract 'user' field from payload
    return designator.try_reserve_spot(user)

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
