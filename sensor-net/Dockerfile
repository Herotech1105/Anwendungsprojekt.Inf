FROM python:3.12-alpine
WORKDIR /code
ENV MQTT_HOST=127.0.0.1
ENV MQTT_USER="testuser"
ENV MQTT_PASSWORD="test"
ENV MQTT_TOPIC="sensor/data"
ENV MQTT_CA_FILE="ca.crt"
ENV MQTT_CLIENT_ID="controller"
COPY requirements.txt .
COPY ../CA/ca.crt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "controller.py" , "--debug"]