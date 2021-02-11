'''
HACKMERCED 2021
BUSHER BRIDI and YASH SHARMA
'''

import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback

# Get env vars:
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# cors = CORS(server)
# app.config['CORS_HEADERS'] = 'Content-Type'
app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
@app.route("/")
def index():
    return "test"

# Add team endpoint
@app.route("/addTeam", methods = ["POST"])
def addTeam():
    addTeam_params = request.get_json()
    team_name = str(addTeam_params["team_name"])
    print(team_name)
    if(db.execute("SELECT COUNT(team_name) FROM teams WHERE upper(team_name) =:team_name", {"team_name":team_name.upper()}).fetchone()[0] == 0):
        print(db.execute("SELECT COUNT(team_name) FROM teams").fetchone()[0])
        db.execute("INSERT INTO teams (team_name) VALUES(:team_name)",{"team_name":team_name})
        db.commit()
        return jsonify({"error":"success"}),200
    else:
        return jsonify({"error":"team already exists"}),200

