from flask import Flask , request
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

@app.route('/getplayerBio/<player_name>')
def getplayerBio(player_name):
    player_name = player_name.lower().replace(" ", "_")

    #get the players information from the redis database
    playerBio = redisDB.hgetall(f'{player_name}:bio') 
    if not playerBio:
        return 'Player not found', 404
    
    print(playerBio)
    
    return str(playerBio), 200

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
    'throws': request.form['throws'],
    'headshot': request.form['headshot']
    }
    #store the players bio information in the redis database
    redisDB.hset(f'{player_name}:bio', mapping=player_bio)
    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)