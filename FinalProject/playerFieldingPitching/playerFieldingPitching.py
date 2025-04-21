from flask import Flask
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerFieldingPitching/<player_name>')
def getplayerFieldingPitching(player_name):
    # This will need to be changed to use the db correctly but is here as a placeholder
    playerFieldingPitching = {
    'gamesPlayed': 120,
    'gamesStarted': 110,
    'inningsAtPosition': 900.1,
    'putOuts': 245,
    'assists': 78,
    'errors': 5,
    'doublePlays': 32,
    'fieldingPercentage': '.985',
    'wins': 0,
    'losses': 0,
    'earnedRunAverage': '0.0',
    'saves': 0,
    'strikeOutsPitching': 0,
    'walksAllowed': 0,
    'hitsAllowed': 0
}
    #playerBio = redisDB.hget(player_name)
    #if playerBio is None:
    #    return 'Player not found', 404
    return str(playerFieldingPitching), 200

@app.route('/storeplayerFieldingPitching', methods=['POST'])
def storeplayerFieldingPitching():
    # This will need to be changed to use the db correctly but is here as a placeholder
    #redisDB.set()
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)