from flask import Flask, render_template
import requests

app = Flask(__name__)

# This route will get a teams information from the redis database.
@app.route('/getTeamInfo/<team_name>')
def getplayerBatting(team_name):
    return 

#This route will store a teams information in the redis database.
@app.route('/addTeamInfo')
def addTeamInfo():
    return  render_template('addTeamInfo.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)