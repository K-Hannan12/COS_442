from flask import Flask, render_template, request
import requests
import ast

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
    
    # This will convert the response string into a dictionary.
    teamInfoStr = teamInfoResponse.text.split('=')
    teamInfoStr = "{" + teamInfoStr[1] + "}"
    teamInfo = ast.literal_eval(teamInfoStr)
    return render_template('viewTeamInfo.html',teamInfo=teamInfo)

# This route will render the addTeamInfo template when the /addTeamInfo URL is accessed that will return a form to add team information
# and send that infomtaion to the teamInfo contanin to store the data.
@app.route('/addTeamInfo')
def addNewTeam():
    return  render_template('addNewTeam.html')

@app.route('/addNewTeamComplete', methods=['POST'])
def addNewTeamComplete():
    teamName = request.form['teamName']
    requests.post(f"http://team-info:5005/storeTeamInfo",data=request.form.to_dict())
    return render_template('addNewTeamComplete.html', teamName=teamName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)