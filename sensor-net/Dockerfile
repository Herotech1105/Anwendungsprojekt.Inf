FROM python:3.12-alpine
WORKDIR /code
ENV MQTT_HOST=192.268.4.18
ENV MQTT_PORT=8883
ENV MQTT_USER=testuser
ENV MQTT_PASSWORD=test
ENV MQTT_TOPIC=sensor/data
ENV MQTT_CA_FILE=ca.crt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ca.crt .
COPY . .
EXPOSE 5000
CMD ["python3", "controller.py" , "--debug"]