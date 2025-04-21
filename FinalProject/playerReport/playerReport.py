from flask import Flask, render_template_string, request
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
        <tbody>
            <tr>
                <td>{{ battingStats.atBats }}</td>
                <td>{{ battingStats.runs }}</td>
                <td>{{ battingStats.hits }}</td>
                <td>{{ battingStats.homeRuns }}</td>
                <td>{{ battingStats.runsBattedIn }}</td>
                <td>{{ battingStats.walks }}</td>
                <td>{{ battingStats.strikeOuts }}</td>
                <td>{{ battingStats.stolenBases }}</td>
                <td>{{ battingStats.battingAverage }}</td>
                <td>{{ battingStats.onBasePercentage }}</td>
                <td>{{ battingStats.sluggingPercentage }}</td>
            </tr>
        </tbody>
     </table>

    <h3>Fielding and Pitching Stats </h3>
    <table>
        <thead>
            <tr>
                <th>Games Played</th>
                <th>Games Started</th>
                <th>Innings At Position</th>
                <th>Put Outs</th>
                <th>Assists</th>
                <th>Errors</th>
                <th>Double Plays</th>
                <th>Fielding Percentage</th>
                <th>Wins</th>
                <th>Losses</th>
                <th>Earned Run Average</th>
                <th>Saves</th>
                <th>Strike Outs</th>
                <th>Walks Allowed</th>
                <th>Hits Allowed</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ fielding_pitchingStats.gamesPlayed }}</td>
                <td>{{ fielding_pitchingStats.gamesStarted }}</td>
                <td>{{ fielding_pitchingStats.inningsAtPosition }}</td>
                <td>{{ fielding_pitchingStats.putOuts }}</td>
                <td>{{ fielding_pitchingStats.assists }}</td>
                <td>{{ fielding_pitchingStats.errors }}</td>
                <td>{{ fielding_pitchingStats.doublePlays }}</td>
                <td>{{ fielding_pitchingStats.fieldingPercentage }}</td>
                <td>{{ fielding_pitchingStats.wins }}</td>
                <td>{{ fielding_pitchingStats.losses }}</td>
                <td>{{ fielding_pitchingStats.earnedRunAverage }}</td>
                <td>{{ fielding_pitchingStats.saves }}</td>
                <td>{{ fielding_pitchingStats.strikeOutsPitching }}</td>
                <td>{{ fielding_pitchingStats.walksAllowed }}</td>
                <td>{{ fielding_pitchingStats.hitsAllowed }}</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

addNewPlayerBioHTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Add New Player Bio</title>
    <style>
    </style>
</head>
<body>
    <h1>Add New Player</h1>
    <h2>Player Bio</h2>
    <form method="post" action="/AddNewPlayerBatting">
        <label for="name">Name:</label><br>
        <input type="text" name="name" id="name"required><br>
        <label for="age">Age:</label><br>
        <input type="text" name="age" id="age"required><br>
        <label for="height">Height:</label><br>
        <input type="text" name="height" id="height"required><br>
        <label for="weight">Weight:</label><br>
        <input type="text" name="weight" id="weight"required><br>
        <label for="position">Position:</label><br>
        <select name="position" id="position">
            <option value="Starting Pitcher">Starting Pitcher</option>
            <option value="Relief Pitcher">Relief Pitcher</option>
            <option value="Catcher">Catcher</option>
            <option value="First Base">First Base</option>
            <option value="Second Base">Second Base</option>
            <option value="Third Base">Third Base</option>
            <option value="Short Stop">Short Stop</option>
            <option value="Left Field">Left Field</option>
            <option value="Center Field">Center Field</option>
            <option value="Right Field">Right Field</option>
            <option value="Designated Hitter">Designated Hitter</option>
        </select><br>
        <label for="team">Team:</label><br>
        <select name="team" id="team">
            <option value="Arizona Diamondbacks">Arizona Diamondbacks</option>
            <option value="Atlanta Braves">Atlanta Braves</option>
            <option value="Baltimore Orioles">Baltimore Orioles</option>
            <option value="Boston Red Sox">Boston Red Sox</option>
            <option value="Chicago Cubs">Chicago Cubs</option>
            <option value="Chicago White Sox">Chicago White Sox</option>
            <option value="Cincinnati Reds">Cincinnati Reds</option>
            <option value="Cleveland Guardians">Cleveland Guardians</option>
            <option value="Colorado Rockies">Colorado Rockies</option>
            <option value="Detroit Tigers">Detroit Tigers</option>
            <option value="Houston Astros">Houston Astros</option>
            <option value="Kansas City Royals">Kansas City Royals</option>
            <option value="Los Angeles Angels">Los Angeles Angels</option>
            <option value="Los Angeles Dodgers">Los Angeles Dodgers</option>
            <option value="Miami Marlins">Miami Marlins</option>
            <option value="Milwaukee Brewers">Milwaukee Brewers</option>
            <option value="Minnesota Twins">Minnesota Twins</option>
            <option value="New York Mets">New York Mets</option>
            <option value="New York Yankees">New York Yankees</option>
            <option value="Oakland Athletics">Oakland Athletics</option>
            <option value="Philadelphia Phillies">Philadelphia Phillies</option>
            <option value="Pittsburgh Pirates">Pittsburgh Pirates</option>
            <option value="San Diego Padres">San Diego Padres</option>
            <option value="San Francisco Giants">San Francisco Giants</option>
            <option value="Seattle Mariners">Seattle Mariners</option>
            <option value="St. Louis Cardinals">St. Louis Cardinals</option>
            <option value="Tampa Bay Rays">Tampa Bay Rays</option>
            <option value="Texas Rangers">Texas Rangers</option>
            <option value="Toronto Blue Jays">Toronto Blue Jays</option>
            <option value="Washington Nationals">Washington Nationals</option>
        </select><br>
        <label for="number">Number:</label><br>
        <input type="text" name="number" id="number"required><br>
        <label for="bats">Bats:</label><br>
        <select name="bats" id="bats">
            <option value="Left">Left</option>
            <option value="Right">Right</option>
            <option value="Switch">Switch</option>
        </select><br>
        <label for="throws">Throws:</label><br>
         <select name="throws" id="throws">
            <option value="Left">Left</option>
            <option value="Right">Right</option>
            <option value="Switch">Switch</option>
        </select><br>
        <label for="headshot">Headshot URL:</label><br>
        <input type="text" name="headshot" id="headshot"required><br>
        <input type="submit" value="Next">
    </form><br>
    </body>
</html>
"""

addNewPlayerBattingHTML = """ 
<!DOCTYPE html>
<html>
<head>
    <title>Add New Player Batting</title>
    <style>
    </style>
</head>
<body>
    <h1>Batting Stats for {{playerName}}</h1>
    <form method="post" action="/AddNewPlayerFieldingPitching">
    <input type="hidden" name="playerName" id="playerName" value="{{ playerName }}">
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
        <tbody>
            <tr>
                <td><input type="number" name="atBats" id="atBats" required ></td>
                <td><input type="number" name="runs" id="runs"required ></td>
                <td><input type="number" name="hits" id="hits"required ></td>
                <td><input type="number" name="homeRuns" id="homeRuns"required ></td>
                <td><input type="number" name="runsBattedIn" id="runsBattedIn"required ></td>
                <td><input type="number" name="walks" id="walks"required ></td>
                <td><input type="number" name="strikeOuts" id="strikeOuts"required ></td>
                <td><input type="number" name="stolenBases" id="stolenBases"required ></td>
                <td><input type="text" name="battingAverage" id="battingAverage"required ></td>
                <td><input type="text" name="onBasePercentage" id="onBasePercentage"required ></td>
                <td><input type="text" name="sluggingPercentage" id="sluggingPercentage"required ></td>
            </tr>
        </tbody>
    </table>
    <input type="submit" value="Next">
    </form>
    </body>
</html>
"""

addNewPlayerFieldingPitchingHTML = """ 
<!DOCTYPE html>
<html>
<head>
    <title>Add New Player Fielding and Pitching</title>
    <style>
    </style>
</head>
<body>
    <h1>Fielding and Pitching Stats for {{playerName}}</h1>
    <form method="post" action="http://player-fielding:5005/storeplayerFieldingPitching">
    <input type="hidden" name="playerName" id="playerName" value="{{ playerName }}">
    <table>
        <thead>
            <tr>
                <th>Games Played</th>
                <th>Games Started</th>
                <th>Innings At Position</th>
                <th>Put Outs</th>
                <th>Assists</th>
                <th>Errors</th>
                <th>Double Plays</th>
                <th>Fielding Percentage</th>
                <th>Wins</th>
                <th>Losses</th>
                <th>Earned Run Average</th>
                <th>Saves</th>
                <th>Strike Outs</th>
                <th>Walks Allowed</th>
                <th>Hits Allowed</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><input type="number" name="gamesPlayed" id="gamesPlayed"required ></td>
                <td><input type="number" name="gamesStarted" id="gamesStarted"required ></td>
                <td><input type="number" name="inningsAtPosition" id="inningsAtPosition"required ></td>
                <td><input type="number" name="putOuts" id="putOuts"required ></td>
                <td><input type="number" name="assists" id="assists"required ></td>
                <td><input type="number" name="errors" id="errors"required ></td>
                <td><input type="number" name="doublePlays" id="doublePlays"required ></td>
                <td><input type="text" name="fieldingPercentage" id="fieldingPercentage"required ></td>
                <td><input type="number" name="wins" id="wins"required ></td>
                <td><input type="number" name="losses" id="losses"required ></td>
                <td><input type="text" name="earnedRunAverage" id="earnedRunAverage"required ></td>
                <td><input type="number" name="saves" id="saves"required ></td>
                <td><input type="number" name="strikeOutsPitching" id="strikeOutsPitching"required ></td>
                <td><input type="number" name="walksAllowed" id="walksAllowed"required ></td>
                <td><input type="number" name="hitsAllowed" id="hitsAllowed"required ></td>
            </tr>
        </tbody>
    </table>
    <input type="submit" value="Submit">
    </form>
    </body>
</html>
"""

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
    return render_template_string(getPlayerHTML, playerBio=playerBio, battingStats=battingStats, fielding_pitchingStats=fielding_pitchingStats)

@app.route('/', methods=['GET'])
def addNewPlayer():
    return render_template_string(addNewPlayerBioHTML)

@app.route('/AddNewPlayerBatting', methods=['POST'])
def addNewPlayerBatting():
    playerName = request.form['name']
    requests.post("http://player-bio:5005/storeplayerBio", data=request.form.to_dict())
    return render_template_string(addNewPlayerBattingHTML, playerName=playerName)

@app.route('/AddNewPlayerFieldingPitching', methods=['POST'])
def addNewPlayerFieldingPitching():
    playerName = request.form['playerName']
    requests.post("http://player-batting:5005/storeplayerBatting", data=request.form.to_dict())
    return render_template_string(addNewPlayerFieldingPitchingHTML, playerName=playerName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)