from flask import Flask
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBio/<player_name>')
def getplayerBio(player_name):
    # This will need to be changed to use the db correctly but is here as a placeholder
    playerBio = redisDB.get(player_name)
    if playerBio is None:
        return 'Player not found', 404
    return str(playerBio), 200