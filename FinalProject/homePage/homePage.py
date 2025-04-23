from flask import Flask, render_template

app = Flask(__name__)

# This route will render the home.html template when the root URL is accessed
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)