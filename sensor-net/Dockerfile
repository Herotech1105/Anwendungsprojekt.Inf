FROM python:3.12-slim
WORKDIR /code
ENV MQTT_HOST=192.168.4.18
ENV MQTT_PORT=8883
ENV MQTT_USER=testuser
ENV MQTT_PASSWORD=test
ENV MQTT_TOPIC=sensor/data
ENV MQTT_CA_FILE=ca.crt
ENV BACKEND_URL=https://www.lab.local/api/internal/sensordata
ENV API_KEY=api_key
ENV MQTT_TLS_INSECURE=false
ENV CA_CERT_PATH=/ca.crt
ENV KC_TOKEN_URL=https://www.lab.local/auth/realms/iot/protocol/openid-connect/token
ENV KC_CLIENT_ID=controller-client
ENV KC_CLIENT_SECRET=change-me-please
ENV KC_REQUIRED_ROLE=controller-ingest
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "controller.py"]