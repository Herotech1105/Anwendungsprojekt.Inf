// @function: validating the payload for the sensor_data table
validateSensorPayload = (data) => {
    const {temperature, humidity, timestamp} = data;

    // check if temperature and humidity are numbers
    if (isNaN(temperature) || isNaN(humidity)) {
        console.error("Temperature and humidity must be numbers");
        return null;
    }

    // check if timestamp is valid
    const date = new Date(timestamp);
    if (!(date instanceof Date && !isNaN(date.getTime()))) {
        console.error("Invalid timestamp");
        return null;
    }

    // check if temperature and humidity are in valid ranges
    if (temperature < 0 || temperature > 60 || humidity < 10 || humidity > 70) {
        console.error("Temperature or humidity out of valid range");
        return null;
    }

    // check if timestamp is up-to-date
    const currentDate = new Date();
    const minuteDifference = Math.floor((currentDate - date) / 60000);
    if (minuteDifference < -5 || minuteDifference > 60) {
        console.error("Timestamp is not up-to-date");
        return null;
    }


    // Source - https://stackoverflow.com/a/11150727
    const formated_timestamp = date.toISOString().slice(0, 19).replace('T', ' ')

    // return valid data
    return {
        temperature,
        humidity,
        timestamp: formated_timestamp
    };
}

module.exports = {validateSensorPayload};