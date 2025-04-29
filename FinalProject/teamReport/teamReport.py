from flask import Flask, render_template, request, send_file
import requests
import ast
import redis
import io

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

# This route will render the viewTeamInfo template when the root URL is accessed that will return team information.
# It will use a get request to get the teams information from the teamInfo container.
@app.route('/<team_name>')
def getTeamReport(team_name):
    # get team information from the teamInfo container
    team_nameToPassToDB = team_name.lower().strip()
    team_nameToPassToDB = team_name.replace(" ", "%20")
    teamInfoResponse = requests.get(f"http://team-info:5005/getTeamInfo/{team_nameToPassToDB}")
    if teamInfoResponse.status_code != 200:
        return f'Error: {teamInfoResponse} {team_name} not found'
    
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
    storeTeamLogo(teamName)
    requests.post(f"http://team-info:5005/storeTeamInfo",data=request.form.to_dict())
    return render_template('addNewTeamComplete.html', teamName=teamName)

@app.route('/getTeamLogo/<team_name>')
def getTeamLogo(team_name):
    team_name = team_name.lower().strip()
    team_name = team_name.replace(" ", "_")

    image_data = r.hget(f'teamLogo:{team_name.lower()}', 'data')
    mimetype = r.hget(f'teamLogo:{team_name.lower()}', 'mimetype')
   
    if not image_data or not mimetype:
        return send_file('static/defaultHeadshot.png', mimetype='image/png')
    
    # Send image file to HTML template
    return send_file(
        # Create a in memory file object to send the image bytes.
        io.BytesIO(image_data),
        mimetype=mimetype.decode('utf-8')
    )

def storeTeamLogo(team_name):
   
    team_name = team_name.lower().strip()
    team_name = team_name.replace(" ", "_")
    image_data = request.files['team_logo'].read()
    mimetype = request.files['team_logo'].mimetype

    r.hset(f'teamLogo:{team_name}', mapping={
        'data': image_data,
        'mimetype': mimetype
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)