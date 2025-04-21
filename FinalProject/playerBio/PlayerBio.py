from flask import Flask
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBio/<player_name>')
def getplayerBio(player_name):
    # This will need to be changed to use the db correctly but is here as a placeholder
    playerBio = {
    'name': "Kaleb Hannan",
    'age': "28",
    'height': "6 feet 2 inches",
    'weight': "210 lbs",
    'position': "Left Field",
    'team': "Red Sox",
    'number': "12",
    'bats': "Left",
    'throws': "Left",
    'headshot': 'https://via.placeholder.com/120x150.png?text=Kaleb'
}
    #playerBio = redisDB.hget(player_name)
    #if playerBio is None:
    #    return 'Player not found', 404
    return str(playerBio), 200

@app.route('/storeplayerBio', methods=['POST'])
def storeplayerBio():
    # This will need to be changed to use the db correctly but is here as a placeholder
    #redisDB.set(player_name, player_bio)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)