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
## Deploying Docker on GCP
### Setting up environment
- Download and install cloud SDK from https://cloud.google.com/sdk/docs/install
- Run 
    ```
    gcloud run deploy --port 5000
    ```
*The port is specified because Cloud Run defaults to apps listening on 8080, and since we have port 5000 defined in the server app and the dockerfile, the default Cloud Run value needs to be overridden.*

*As of now the app is unreachable due to permission issues. We'll fix that in the next edition of "Olga's adventures in getting back to work"*