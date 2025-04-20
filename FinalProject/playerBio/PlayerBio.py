from flask import Flask
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBio/<player_name>')
def getplayerBio(player_name):
    # This will need to be changed to use the db correctly but is here as a placeholder
    playerBio = {
    'name': 'Kaleb Hannan',
    'age': '28',
    'height': "6'2\"",
    'weight': '210 lbs',
    'position': 'Left Field',
    'team': 'Red Sox',
    'number': '12',
    'headshot': 'https://via.placeholder.com/200x250.png?text=Headshot'
}
    #playerBio = redisDB.hget(player_name)
    #if playerBio is None:
    #    return 'Player not found', 404
    return str(playerBio), 200

@app.route('/storeplayerBio/<player_name>/<player_bio>')
def storeplayerBio(player_name, player_bio):
    # This will need to be changed to use the db correctly but is here as a placeholder
    redisDB.set(player_name, player_bio)
    return 'Player bio stored', 200