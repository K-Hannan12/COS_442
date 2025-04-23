from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/viewPlayer/<player_name>')
def getplayer_report(player_name):
    # Get the players bio from the playerBio service
    player_name = player_name.replace(" ", "%20")
    responseBio = requests.get("http://player-bio:5005/getplayerBio/{player_name}")
    if responseBio.status_code != 200:
        return f'Error: {responseBio.status_code}'
    
    # This gets the player bio from the playerBio service and splits it into a dictionary
    dataSplit = responseBio.text.split('{')
    dataSplit = dataSplit[1].split(',')
    name = dataSplit[0].split(':', 1)[1].replace("'", "")
    age = dataSplit[1].split(':', 1)[1].replace("'", "")
    height = dataSplit[2].split(':', 1)[1].replace("'", "")
    weight = dataSplit[3].split(':', 1)[1].replace("'", "")
    position = dataSplit[4].split(':', 1)[1].replace("'", "")
    team = dataSplit[5].split(':', 1)[1].replace("'", "")
    number = dataSplit[6].split(':', 1)[1].replace("'", "")
    bats = dataSplit[7].split(':', 1)[1].replace("'", "")
    throws = dataSplit[8].split(':', 1)[1].replace("'", "")
    headshot = dataSplit[9].split(':', 1)[1].replace("'", "").replace("}", "")
    
    playerBio = {
        'name': name,
        'age': age,
        'height': height,
        'weight': weight,
        'position': position,
        'team': team,
        'number': number,
        'Bats': bats,
        'Throws': throws,
        'headshot': headshot
    }

    # Get the players batting stats from the batting service
    responseBatting = requests.get("http://player-batting:5005/getplayerBatting/{player_name}")
    if responseBatting.status_code != 200:
        return f'Error: {responseBatting.status_code}'
    
    # Format batting stats and storing them in a dictionary
    dataSplit = responseBatting.text.split('{')
    dataSplit = dataSplit[1].split(',')
    atBats = dataSplit[0].split(':')[1]
    runs = dataSplit[1].split(':')[1]
    hits = dataSplit[2].split(':')[1]
    homeRuns = dataSplit[3].split(':')[1]
    runsBattedIn = dataSplit[4].split(':')[1]
    walks = dataSplit[5].split(':')[1]
    strikeOuts = dataSplit[6].split(':')[1]
    stolenBases = dataSplit[7].split(':')[1]
    battingAverage = dataSplit[8].split(':')[1].replace("'", "")
    onBasePercentage = dataSplit[9].split(':')[1].replace("'", "")
    sluggingPercentage = dataSplit[10].split(':')[1].replace("'", "").replace("}", "")
    
    battingStats = {
        'atBats': atBats,
        'runs': runs,
        'hits': hits,
        'homeRuns': homeRuns,
        'runsBattedIn': runsBattedIn,
        'walks': walks,
        'strikeOuts': strikeOuts,
        'stolenBases': stolenBases,
        'battingAverage': battingAverage,
        'onBasePercentage': onBasePercentage,
        'sluggingPercentage': sluggingPercentage
    }

    # Get the players fielding and pitching stats from the fielding-pitching service
    responseFielding_pitching = requests.get("http://player-fielding-pitching:5005/getplayerFieldingPitching/{player_name}")
    if responseFielding_pitching.status_code != 200:
        return f'Error: {responseFielding_pitching.status_code}'
    
    # Format fielding and pitching stats and storing them in a dictionary
    dataSplit = responseFielding_pitching.text.split('{')
    dataFeilding_pitchingSplit = dataSplit[1].split(',')  
    gamesPlayed = dataFeilding_pitchingSplit[0].split(':')[1]
    gamesStarted = dataFeilding_pitchingSplit[1].split(':')[1]
    inningsAtPosition = dataFeilding_pitchingSplit[2].split(':')[1]
    putOuts = dataFeilding_pitchingSplit[3].split(':')[1]
    assists = dataFeilding_pitchingSplit[4].split(':')[1]
    errors = dataFeilding_pitchingSplit[5].split(':')[1]
    doublePlays = dataFeilding_pitchingSplit[6].split(':')[1]
    fieldingPercentage = dataFeilding_pitchingSplit[7].split(':')[1].replace("'", "")
    wins = dataFeilding_pitchingSplit[8].split(':')[1]
    losses = dataFeilding_pitchingSplit[9].split(':')[1]
    earnedRunAverage = dataFeilding_pitchingSplit[10].split(':')[1].replace("'", "")
    saves = dataFeilding_pitchingSplit[11].split(':')[1]
    strikeOutsPitching = dataFeilding_pitchingSplit[12].split(':')[1]
    walksAllowed = dataFeilding_pitchingSplit[13].split(':')[1]
    hitsAllowed = dataFeilding_pitchingSplit[14].split(':')[1].replace("'", "").replace("}", "")

    fielding_pitchingStats = {
        'gamesPlayed': gamesPlayed,
        'gamesStarted': gamesStarted,
        'inningsAtPosition': inningsAtPosition,
        'putOuts': putOuts,
        'assists': assists,
        'errors': errors,
        'doublePlays': doublePlays,
        'fieldingPercentage': fieldingPercentage,
        'wins': wins,
        'losses': losses,
        'earnedRunAverage': earnedRunAverage,
        'saves': saves,
        'strikeOutsPitching': strikeOutsPitching,
        'walksAllowed': walksAllowed,
        'hitsAllowed': hitsAllowed
    }
    return render_template('getPlayerHTML.html', playerBio=playerBio, battingStats=battingStats, fielding_pitchingStats=fielding_pitchingStats)

@app.route('/', methods=['GET'])
def addNewPlayer():
    return render_template('addNewPlayerBioHTML.html')

@app.route('/AddNewPlayerBatting', methods=['POST'])
def addNewPlayerBatting():
    playerName = request.form['name']
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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)