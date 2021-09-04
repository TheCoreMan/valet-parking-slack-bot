FROM python:3.9
WORKDIR /app
COPY . /app/
RUN poetry install
EXPOSE 5000
ENV FLASK_APP=valet_parking_slack_bot.server
CMD ["flask", "run"]