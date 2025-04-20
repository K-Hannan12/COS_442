from flask import Flask, render_template_string
import requests

app = Flask(__name__)

getPlayerHTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Player Report</title>
    <style>
        .header {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .header img {
            height: 60px;
            border-radius: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 1rem;
            text-align: center;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="header">
            <img src="{{ playerBio.headshot }}" alt="Headshot of {{ playerBio.name }}">
            <h1>{{ playerBio.name }}</h1>
    </div>
    <h2>Player Bio</h2>
    <p><b>Age</b>: {{ playerBio.age }}</p>
    <p><b>Height</b>: {{ playerBio.height }}</p>
    <p><b>Weight</b>: {{ playerBio.weight }}</p>
    <p><b>Position</b>: {{ playerBio.position }}</p>
    <p><b>Bats</b>: {{ playerBio.Bats }}</p>
    <p><b>Throws</b>: {{ playerBio.Throws }}</p>
    <p><b>Team</b>: {{ playerBio.team }}</p>
    <p><b>Number</b>: {{ playerBio.number }}</p>
    </br>
    <h3>Batting Stats</h3>
    <table>
        <thead>
            <tr>
                <th>At Bats</th>
                <th>Runs</th>
                <th>Hits</th>
                <th>Home Runs</th>
                <th>Runs Batted In</th>
                <th>Walks</th>
                <th>Strike Outs</th>
                <th>Stolen Bases</th>
                <th>Batting Average</th>
                <th>On Base Percentage</th>
                <th>Slugging Percentage</th>
            </tr>
        </thead>

    </br>
    <h3>Fielding and Pitching Stats </h3>
</body>
</html>
"""

@app.route('/<player_name>')
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
    headshot = dataSplit[9].split(':', 1)[1].replace("'", "")
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
    #responseBatting = requests.get("http://batting:5005/getBattingStats/{player_name}")
    #if responseBatting.status_code != 200:
    #    return f'Error: {responseBatting.status_code}'
    #dataSplit = responseBatting.text.split(',')
    #atBats = dataSplit[0].split('=')[1]
    #runs = dataSplit[1].split('=')[1]
    #hits = dataSplit[2].split('=')[1]
    #homeRuns = dataSplit[3].split('=')[1]
    #runsBattedIn = dataSplit[4].split('=')[1]
    #walks = dataSplit[5].split('=')[1]
    #strikeOuts = dataSplit[6].split('=')[1]
    #stolenBases = dataSplit[7].split('=')[1]
    #battingAverage = dataSplit[8].split('=')[1]
    #onBasePercentage = dataSplit[9].split('=')[1]
    #sluggingPercentage = dataSplit[10].split('=')[1]
    #battingStats = {
    #    'atBats': atBats,
    #    'runs': runs,
    #    'hits': hits,
    #    'homeRuns': homeRuns,
    #    'runsBattedIn': runsBattedIn,
    #    'walks': walks,
    #    'strikeOuts': strikeOuts,
    #    'stolenBases': stolenBases,
    #    'battingAverage': battingAverage,
    #    'onBasePercentage': onBasePercentage,
    #    'sluggingPercentage': sluggingPercentage
    #}

    # Get the players fielding and pitching stats from the fielding-pitching service
    #responseFielding_pitching = requests.get("http://fielding-pitching:5005/getFielding-pitchingStats/{player_name}")
    #if responseFielding_pitching.status_code != 200:
    #    return f'Error: {responseFielding_pitching.status_code}'
    #dataFeilding_pitchingSplit = responseFielding_pitching.text.split(',')  
    #gamesPlayed = dataFeilding_pitchingSplit[0].split('=')[1]
    #gamesStarted = dataFeilding_pitchingSplit[1].split('=')[1]
    #inningsAtPosition = dataFeilding_pitchingSplit[2].split('=')[1]
    #putOuts = dataFeilding_pitchingSplit[3].split('=')[1]
    #assists = dataFeilding_pitchingSplit[4].split('=')[1]
    #errors = dataFeilding_pitchingSplit[5].split('=')[1]
    #doublePlays = dataFeilding_pitchingSplit[6].split('=')[1]
    #fieldingPercentage = dataFeilding_pitchingSplit[7].split('=')[1]
    #wins = dataFeilding_pitchingSplit[8].split('=')[1]
    #losses = dataFeilding_pitchingSplit[9].split('=')[1]
    #earnedRunAverage = dataFeilding_pitchingSplit[10].split('=')[1]
    #saves = dataFeilding_pitchingSplit[11].split('=')[1]
    #strikeOutsPitching = dataFeilding_pitchingSplit[12].split('=')[1]
    #walksAllowed = dataFeilding_pitchingSplit[13].split('=')[1]
    #hitsAllowed = dataFeilding_pitchingSplit[14].split('=')[1]
    #fielding_pitchingStats = {
    #    'gamesPlayed': gamesPlayed,
    #    'gamesStarted': gamesStarted,
    #    'inningsAtPosition': inningsAtPosition,
    #    'putOuts': putOuts,
    #    'assists': assists,
    #    'errors': errors,
    #    'doublePlays': doublePlays,
    #    'fieldingPercentage': fieldingPercentage,
    #    'wins': wins,
    #    'losses': losses,
    #    'earnedRunAverage': earnedRunAverage,
    #    'saves': saves,
    #    'strikeOutsPitching': strikeOutsPitching,
    #    'walksAllowed': walksAllowed,
    #    'hitsAllowed': hitsAllowed
    #}
    return render_template_string(getPlayerHTML, playerBio=playerBio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)