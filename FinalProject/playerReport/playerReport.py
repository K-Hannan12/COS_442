from flask import Flask
import requests

app = Flask(__name__)

@app.route('/<player_name>')
def getplayer_report():
    # Get the players bio from the playerBio service
    responseBio = requests.get("http://playerBio:5005/getplayerBio/{player_name}")
    if responseBio.status_code != 200:
        return f'Error: {responseBio.status_code}'
    # This gets the player bio from the playerBio service and splits it into a dictionary
    dataSplit = responseBio.text.split(',')
    name = dataSplit[0].split('=')[1]
    age = dataSplit[1].split('=')[1]
    height = dataSplit[2].split('=')[1]
    weight = dataSplit[3].split('=')[1]
    position = dataSplit[4].split('=')[1]
    team = dataSplit[5].split('=')[1]
    number = dataSplit[6].split('=')[1]
    headshot = dataSplit[7].split('=')[1]
    playerBio = {
        'name': name,
        'age': age,
        'height': height,
        'weight': weight,
        'position': position,
        'team': team,
        'number': number,
        'headshot': headshot
    }
    # Get the players batting stats from the batting service
    responseBatting = requests.get("http://batting:5005/getBattingStats/{player_name}")
    if responseBatting.status_code != 200:
        return f'Error: {responseBatting.status_code}'
    dataSplit = responseBatting.text.split(',')
    atBats = dataSplit[0].split('=')[1]
    runs = dataSplit[1].split('=')[1]
    hits = dataSplit[2].split('=')[1]
    homeRuns = dataSplit[3].split('=')[1]
    runsBattedIn = dataSplit[4].split('=')[1]
    walks = dataSplit[5].split('=')[1]
    strikeOuts = dataSplit[6].split('=')[1]
    stolenBases = dataSplit[7].split('=')[1]
    battingAverage = dataSplit[8].split('=')[1]
    onBasePercentage = dataSplit[9].split('=')[1]
    sluggingPercentage = dataSplit[10].split('=')[1]
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
    responseFielding_pitching = requests.get("http://fielding-pitching:5005/getFielding-pitchingStats/{player_name}")
    if responseFielding_pitching.status_code != 200:
        return f'Error: {responseFielding_pitching.status_code}'
    dataFeilding_pitchingSplit = responseFielding_pitching.text.split(',')  
    gamesPlayed = dataFeilding_pitchingSplit[0].split('=')[1]
    gamesStarted = dataFeilding_pitchingSplit[1].split('=')[1]
    inningsAtPosition = dataFeilding_pitchingSplit[2].split('=')[1]
    putOuts = dataFeilding_pitchingSplit[3].split('=')[1]
    assists = dataFeilding_pitchingSplit[4].split('=')[1]
    errors = dataFeilding_pitchingSplit[5].split('=')[1]
    doublePlays = dataFeilding_pitchingSplit[6].split('=')[1]
    fieldingPercentage = dataFeilding_pitchingSplit[7].split('=')[1]
    wins = dataFeilding_pitchingSplit[8].split('=')[1]
    losses = dataFeilding_pitchingSplit[9].split('=')[1]
    earnedRunAverage = dataFeilding_pitchingSplit[10].split('=')[1]
    saves = dataFeilding_pitchingSplit[11].split('=')[1]
    strikeOutsPitching = dataFeilding_pitchingSplit[12].split('=')[1]
    walksAllowed = dataFeilding_pitchingSplit[13].split('=')[1]
    hitsAllowed = dataFeilding_pitchingSplit[14].split('=')[1]
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
    return f'player report: {playerBio} {battingStats} {fielding_pitchingStats}'