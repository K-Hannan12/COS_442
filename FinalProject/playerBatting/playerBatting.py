from flask import Flask, request
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
    playerBatting = redisDB.hget(f'{player_name}:batting')
    if playerBatting is None:
        return 'Player not found', 404
    return str(playerBatting), 200

@app.route('/storeplayerBatting', methods=['POST'])
def storeplayerBatting():
    player_name = request.form['playerName'].lower().replace(" ", "_")
    playerBatting = {
    'atBats': request.form['atBats'],
    'runs': request.form['runs'],
    'hits': request.form['hits'],
    'homeRuns': request.form['homeRuns'],
    'runsBattedIn': request.form['runsBattedIn'],
    'walks': request.form['walks'],
    'strikeOuts': request.form['strikeOuts'],
    'stolenBases': request.form['stolenBases'],
    'battingAverage': request.form['battingAverage'],
    'onBasePercentage': request.form['onBasePercentage'],
    'sluggingPercentage': request.form['sluggingPercentage']
    }
    #redisDB.set(f'{player_name}:batting', playerBatting)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)