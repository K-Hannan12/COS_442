from flask import Flask, render_template, request, send_file
import requests
import ast
import redis
import io

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/viewPlayer/<player_name>')
def getplayer_report(player_name):
    # Get the players bio from the playerBio service
    player_nameToPassToDB = player_name.lower().strip()
    player_nameToPassToDB = player_name.replace(" ", "%20")
    responseBio = requests.get(f"http://player-bio:5005/getplayerBio/{player_nameToPassToDB}")
    if responseBio.status_code != 200:
        return f'Error: {responseBio.status_code} {player_name} not found'
    
    #Turn string into a dictionary
    playerBioStr = responseBio.text.split('=')
    playerBioStr = "{" + playerBioStr[1] + "}"
    playerBio = ast.literal_eval(playerBioStr)
    
    # Get the players batting stats from the batting service
    responseBatting = requests.get(f"http://player-batting:5005/getplayerBatting/{player_nameToPassToDB}")
    if responseBatting.status_code != 200:
        return f'Error: {responseBatting.status_code} {player_name} not found'
    
    # Turn batting stats str into a dictionary
    playerBattingStr = responseBatting.text.split('=')
    playerBattingStr = "{" + playerBattingStr[1] + "}"
    battingStats = ast.literal_eval(playerBattingStr)

    # Get the players fielding and pitching stats from the fielding-pitching service
    responseFielding_pitching = requests.get(f"http://player-fielding-pitching:5005/getplayerFieldingPitching/{player_nameToPassToDB}")
    if responseFielding_pitching.status_code != 200:
        return f'Error: {responseFielding_pitching.status_code} {player_name} not found'
    
    # Turn fielding and pitching stats into a dictionary
    playerFieldingPitchingStr = responseFielding_pitching.text.split('=')
    playerFieldingPitchingStr = "{" + playerFieldingPitchingStr[1] + "}"
    fielding_pitchingStats = ast.literal_eval(playerFieldingPitchingStr)

    return render_template('getPlayerHTML.html', playerBio=playerBio, battingStats=battingStats, fielding_pitchingStats=fielding_pitchingStats,player_name=player_name)

@app.route('/', methods=['GET'])
def addNewPlayer():
    return render_template('addNewPlayerBioHTML.html')

@app.route('/AddNewPlayerBatting', methods=['POST'])
def addNewPlayerBatting():
    playerName = request.form['name']
     
    #store Headshot in redis
    storeHeadshot(playerName)
    requests.post("http://player-bio:5005/storeplayerBio", data=request.form.to_dict())
    return render_template('addNewPlayerBattingHTML.html', playerName=playerName)

@app.route('/AddNewPlayerFieldingPitching', methods=['POST'])
def addNewPlayerFieldingPitching():
    playerName = request.form['playerName']
    requests.post("http://player-batting:5005/storeplayerBatting", data=request.form.to_dict())
    return render_template('addNewPlayerFieldingPitchingHTML.html', playerName=playerName)

@app.route('/AddNewPlayerComplete', methods=['POST'])
def addNewPlayerComplete():
    playerName = request.form['playerName']
    requests.post("http://player-fielding-pitching:5005/storeplayerFieldingPitching", data=request.form.to_dict())
    return render_template('addNewPlayerCompleteHTML.html', playerName=playerName)

@app.route('/getHeadshot/<player_name>')
def getHeadshot(player_name):
    player_name = player_name.lower().strip()
    player_name = player_name.replace(" ", "_")

    image_data = r.hget(f'headshot:{player_name.lower()}', 'data')
    mimetype = r.hget(f'headshot:{player_name.lower()}', 'mimetype')
   
    if not image_data or not mimetype:
        return send_file('static/defaultHeadshot.png', mimetype='image/png')
    
    # Send image file to HTML template
    return send_file(
        # Create a in memory file object to send the image bytes.
        io.BytesIO(image_data),
        mimetype=mimetype.decode('utf-8')
    )


def storeHeadshot(player_name):
   
    player_name = player_name.lower().strip()
    player_name = player_name.replace(" ", "_")
    image_data = request.files['headshot'].read()
    mimetype = request.files['headshot'].mimetype

    r.hset(f'headshot:{player_name}', mapping={
        'data': image_data,
        'mimetype': mimetype
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)