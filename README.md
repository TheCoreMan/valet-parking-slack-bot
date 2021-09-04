# valet-parking-slack-bot
🔑 Right this way, sir. 🅿

## Running the app locally
Install dependencied via poetry. 
Configure flask app name as env variable and run flask app.
```
poetry install
ENV FLASK_APP="valet_parking_slack_bot.server.py"
flask run

```
## Dockerizing
### Building a Docker image

```
docker build -t nehmads/valet_parking_slack_bot:latest .
```
*Curretly versioned as "latest", will be properly semversioned in the future.*
## Deploying Docker locally

```
docker run -d --rm -p 5000:5000 nehmads/valet_parking_slack_bot:latest
```
## Deploying Docker on CGP
*To Be Continued*