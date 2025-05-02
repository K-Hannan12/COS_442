from flask import Flask, request
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBatting/<player_name>')
def getplayerBatting(player_name):
    player_name = player_name.lower().replace(" ", "_")

    playerBatting = redisDB.hgetall(f'{player_name}:batting')
    if not playerBatting:
        return f'Player {player_name} not found', 404
    playerBattingStr = str(playerBatting).strip('{').strip('}')
    playerBattingStr = f'{player_name}\'s Batting Stats = {playerBattingStr}'
    
    return playerBattingStr, 200

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
    redisDB.hset(f'{player_name}:batting', mapping=playerBatting)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)