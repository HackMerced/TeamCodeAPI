import os
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback


app = Flask(__name__)

@app.route("/")
def index():
    return "test"

@app.route("/addTeam", methods = ["POST"])
def addTeam():
    addTeam_params = request.get_json()
    team_name = str(addTeam_params["team_name"])
    if(db.execute("SELECT COUNT(team_name) FROM teams WHERE upper(team_name) =:team_name", {"team_name":team_name.upper()}) != 0):
        db.execute("INSERT INTO teams (team_name) VALUES(:team_name",{"team_name":team_name})
        return jsonify({"error":"success"}),200


