from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# This route will render the home.html template when the root URL is accessed
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/searchForPlayer', methods=['POST'])
def searchForPlayer():
    player_name = request.form['player_name']
    player_name_for_redirect = player_name.lower().strip()
    player_name_for_redirect = player_name.replace(" ", "%20")
    return redirect(f"/viewPlayer/{player_name_for_redirect}")
    
@app.route('/searchForTeam', methods=['POST'])
def searchForTeam():
    team_name = request.form['team_name']
    team_name_for_redirect = team_name.lower().strip()
    team_name_for_redirect = team_name.replace(" ", "%20")
    return redirect(f"/viewTeam/{team_name_for_redirect}")    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)