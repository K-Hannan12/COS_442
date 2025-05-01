from flask import Flask, request
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerFieldingPitching/<player_name>')
def getplayerFieldingPitching(player_name):
    player_name = player_name.lower().replace(" ", "_")
    
    playerFieldingPitching = redisDB.hgetall(f'{player_name}:feildingPitching')
    if not playerFieldingPitching:
        return f'''
        <h2>Player {player_name} not found. Please check the name and try again.</h2>
        <a>href="/"><button>Go back to the home page</button</a>
        ''', 404
    playerFieldingPitchingStr = str(playerFieldingPitching).strip('{').strip('}')
    playerFieldingPitchingStr = f'{player_name}\'s Fielding and Pitching Stats = {playerFieldingPitchingStr}'
    return playerFieldingPitchingStr, 200

@app.route('/storeplayerFieldingPitching', methods=['POST'])
def storeplayerFieldingPitching():
    player_name = request.form['playerName'].lower().replace(" ", "_")
    playerFieldingPitching = {
        'gamesPlayed': request.form['gamesPlayed'],
        'gamesStarted': request.form['gamesStarted'],
        'inningsAtPosition': request.form['inningsAtPosition'],
        'putOuts': request.form['putOuts'],
        'assists': request.form['assists'],
        'errors': request.form['errors'],
        'doublePlays': request.form['doublePlays'],
        'fieldingPercentage': request.form['fieldingPercentage'],
        'wins': request.form['wins'],
        'losses': request.form['losses'],
        'earnedRunAverage': request.form['earnedRunAverage'],
        'saves': request.form['saves'],
        'strikeOutsPitching': request.form['strikeOutsPitching'],
        'walksAllowed': request.form['walksAllowed'],
        'hitsAllowed': request.form['hitsAllowed']
    }
    
    redisDB.hset(f'{player_name}:feildingPitching', mapping=playerFieldingPitching)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)