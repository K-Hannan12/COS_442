from flask import Flask, render_template
import requests

app = Flask(__name__)

# This route will render the viewTeamInfo template when the root URL is accessed that will return team information.
# It will use a get request to get the teams information from the teamInfo container.
@app.route('/<team_name>')
def getTeamReport():
    return render_template('viewTeamInfo.html')

# This route will render the addTeamInfo template when the /addTeamInfo URL is accessed that will return a form to add team information
# and send that infomtaion to the teamInfo contanin to store the data.
@app.route('/addTeamInfo')
def addNewTeam():
    return  render_template('addNewTeam.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)