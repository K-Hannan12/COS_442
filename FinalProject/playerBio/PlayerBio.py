from flask import Flask , request
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBio/<player_name>')
def getplayerBio(player_name):
    player_name_to_DB = player_name.lower().replace(" ", "_")

    #get the players bio information from the redis database
    playerBio = redisDB.hgetall(f'{player_name_to_DB}:bio') 
    if not playerBio:
        return f'''
        <h2>Player {player_name} not found. Please check the name and try again.</h2>
        <a>href="/"><button>Go back to the home page</button</a>
        ''', 404
    playerBioStr = str(playerBio).strip('{').strip('}')
    playerBioStr = f'{player_name}\'s Bio = {playerBioStr}'
    
    return playerBioStr, 200

@app.route('/storeplayerBio', methods=['POST'])
def storeplayerBio():
    player_name = request.form['name'].lower().replace(" ", "_")
    player_bio = {
    'age': request.form['age'],
    'height': request.form['height'],
    'weight': request.form['weight'],
    'position': request.form['position'],
    'team': request.form['team'],
    'number': request.form['number'],
    'bats': request.form['bats'],
    'throws': request.form['throws']
    }
    team_name = player_bio['team'].lower().replace(" ", "_")
   # add the player to the team in redis
    redisDB.sadd(f'{team_name}:players', f'{request.form['name']}: {player_bio['number']}: {player_bio['position']}')


    #store the players bio information in the redis database
    redisDB.hset(f'{player_name}:bio', mapping=player_bio)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)