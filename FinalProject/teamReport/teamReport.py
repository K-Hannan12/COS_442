from flask import Flask, render_template
import requests

app = Flask(__name__)

# This route will render the viewTeamInfo template when the root URL is accessed that will return team information.
# It will use a get request to get the teams information from the teamInfo container.
@app.route('/<team_name>')
def getTeamReport(team_name):
    # get team information from the teamInfo container
    team_nameToPassToDB = team_name.lower().strip()
    team_nameToPassToDB = team_name.replace(" ", "%20")
    teamInfoResponse = requests.get(f"http://team-info:5005/getTeamInfo/{team_nameToPassToDB}")
    if teamInfoResponse.status_code != 200:
        return f'Error: {teamInfoResponse} is not found'
    dataSplit = teamInfoResponse.text.split('{')
    dataSplit = dataSplit[1].split(',')

    teamInfo = {
        "name": team_name,
        "abbreviation": dataSplit[0].split(':', 1)[1].replace("'", ""),
        "nickname": dataSplit[1].split(':', 1)[1].replace("'", ""),
        "location": dataSplit[2].split(':', 1)[1].replace("'", ""),
       "division": dataSplit[3].split(':', 1)[1].replace("'", ""),
        "league": dataSplit[4].split(':', 1)[1].replace("'", ""),
        "founding_year": dataSplit[5].split(':', 1)[1].replace("'", ""),
        "stadium": dataSplit[6].split(':', 1)[1].replace("'", ""),
        "all_time_wins": dataSplit[7].split(':', 1)[1].replace("'", ""),
        "all_time_losses": dataSplit[8].split(':', 1)[1].replace("'", ""),
        "division_titles": dataSplit[9].split(':', 1)[1].replace("'", ""),
        "world_series_titles": dataSplit[10].split(':', 1)[1].replace("'", ""), 
        "last_world_series_won": dataSplit[11].split(':', 1)[1].replace("'", "")
    }
    
    return render_template('viewTeamInfo.html',teamInfo=teamInfo)

# This route will render the addTeamInfo template when the /addTeamInfo URL is accessed that will return a form to add team information
# and send that infomtaion to the teamInfo contanin to store the data.
@app.route('/addTeamInfo')
def addNewTeam():
    return  render_template('addNewTeam.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)