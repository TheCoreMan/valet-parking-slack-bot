# valet-parking-slack-bot

🔑 Right this way, sir. 🅿

## Development Setup

(If you just want to run the app, see the Docker section.)

You'll need:

- Python 3.9. You should probably use [pyenv](https://github.com/pyenv/pyenv) to set this up.
- [Poetry](https://python-poetry.org/docs/)

Then open a virtualenv using poetry:

```sh
poetry shell
```

And then install the dependencies via poetry.

```sh
poetry install
```

## Running the app locally


Configure flask app name as env variable and run flask app.

```sh
ENV FLASK_APP="valet_parking_slack_bot.server.py"
flask run
```

## Running Tests

To run the tests, simply use pytest!

```sh
pytest .
```

## Dockerizing

### Building a Docker image

To build the docker image, run:

```sh
docker build -t nehmads/valet_parking_slack_bot:latest .
```

*Curretly versioned as "latest", will be properly semversioned in the future.*

### Deploying Docker locally

To deploy the docker locally, run:

```sh
docker run -d --rm -p 5000:5000 nehmads/valet_parking_slack_bot:latest
```

### Deploying Docker on GCP

#### Setting up environment

- Download and install cloud SDK from [here](https://cloud.google.com/sdk/docs/install).
- Run

```sh
gcloud run deploy --port 5000
```

*The port is specified because Cloud Run defaults to apps listening on 8080, and since we have port 5000 defined in the server app and the dockerfile, the default Cloud Run value needs to be overridden.*

*As of now the app is unreachable due to permission issues. We'll fix that in the next edition of "Olga's adventures in getting back to work"*.

## Site

The site is built using Hugo and hosted using Firebase.

To run locally for writing, run `hugo server -D`.

To run locally for hosting emulation, run `firebase emulators:start`.

To build and deploy, run `hugo && firebase deploy`.
