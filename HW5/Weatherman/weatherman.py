from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def weatherman():
    responseTemp = requests.get("http://temp:5005/")
    responseWind = requests.get("http://wind:5005/")
    responseHumidity = requests.get("http://humidity:5005/")
    return f'wind: {responseWind.text}\ntemp: {responseTemp.text}\nhumidity: {responseHumidity.text}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)