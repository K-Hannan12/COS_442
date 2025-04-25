from flask import Flask , request
import redis

app = Flask(__name__)
redisDB = redis.Redis(host='redis', port=6379 , decode_responses=True)

# This route will get a teams information from the redis database.
@app.route('/getTeamInfo/<team_name>')
def getplayerBatting(team_name):
    team_name = team_name.lower().replace(" ", "_")
    
    #Get the teams info from the redis database
    teamInfo = redisDB.hgetall(f'{team_name}:info')
    if not teamInfo:
        return 'Team not found', 404
    
    return teamInfo

#This route will store a teams information in the redis database.
@app.route('/storeTeamInfo',methods=['POST'])
def addTeamInfo():
    team_name = request.form['name'].lower().replace(" ", "_")
    teamInfo = {
        'abbreviation': request.form['abbreviation'],
        'nickname': request.form['nickname'],
        'location': request.form['location'],
        'division': request.form['division'],
        'league': request.form['league'],
        'founding_year': request.form['founding_year'],
        'stadium': request.form['stadium'],
        'all_time_wins': request.form['all_time_wins'],
        'all_time_losses': request.form['all_time_losses'],
        'division_titles': request.form['division_titles'],
        'world_series_titles': request.form['world_series_titles'],
        'last_world_series_won': request.form['last_world_series_won']
    }
    #This will store the team info in the redis database.
    redisDB.hset(f'{team_name}:info', mapping=teamInfo)

    return 'Player bio stored', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)