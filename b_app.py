from flask import Flask, render_template, request, session, redirect, url_for, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
import os

class userName(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    btn_submit = SubmitField("Submit")
    print(username)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")

@app.route('/', methods=["GET", "POST"])
def index():
    form = userName()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('test'))
    return render_template("index.html", form=form)

@app.route('/test')
def test():
     return render_template("test.html")

@app.route('/save_reaction_time', methods=["POST"])
def save_reaction_time():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    username = data.get("username")
    reaction_time = data.get("reactionTime")

    if not username:
        return jsonify({"status": "error", "message": "Username required"}), 400

    if reaction_time is None:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    if reaction_time:
        try:
            reaction_time = float(reaction_time)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid reaction time"}), 400

    update_best_time(username, reaction_time)

    return jsonify({"status": "success", "message": "Reaction time saved!"})

def update_best_time(username, reaction_time):
    user_times = {}

    if os.path.exists("reaction_times.csv"):
        with open("reaction_times.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    user, time_str = row
                    try:
                        user_times[user] = float(time_str)
                    except ValueError:
                        continue

    if username in user_times:
        if reaction_time < user_times[username]:
            user_times[username] = reaction_time
    else:
        user_times[username] = reaction_time


    with open("reaction_times.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for user, time in user_times.items():
                writer.writerow([user, time])
                
     
    
if __name__ == "__main__":
    app.run(debug=True)
