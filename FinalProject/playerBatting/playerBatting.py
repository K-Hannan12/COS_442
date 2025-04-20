from flask import Flask
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBatting/<player_name>')
def getplayerBatting(player_name):
    # This will need to be changed to use the db correctly but is here as a placeholder
    playerBatting = {
    'atBats': 350,
    'runs': 48,
    'hits': 102,
    'homeRuns': 18,
    'runsBattedIn': 56,
    'walks': 22,
    'strikeOuts': 61,
    'stolenBases': 7,
    'battingAverage': '.291',
    'onBasePercentage': '.342',
    'sluggingPercentage': '.487'
}
    #playerBio = redisDB.hget(player_name)
    #if playerBio is None:
    #    return 'Player not found', 404
    return str(playerBatting), 200

@app.route('/storeplayerBatting/<player_name>/<player_batting>')
def storeplayerBio(player_name, player_batting):
    # This will need to be changed to use the db correctly but is here as a placeholder
    redisDB.set(player_name, player_batting)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)