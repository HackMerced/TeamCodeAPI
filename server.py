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

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
@app.route("/")
def index():
    return "test"

# Add team endpoint
@app.route("/addTeam", methods = ["POST"])
def addTeam():
    addTeam_params = request.get_json()
    team_code = str(addTeam_params["team_code"])
    owner_id = str(addTeam_params["user_id"])
    print(team_code)
    if(db.execute("SELECT COUNT(team_code) FROM teams WHERE upper(team_code) =:team_code", {"team_code":team_code.upper()}).fetchone()[0] == 0):
        print(db.execute("SELECT COUNT(team_code) FROM teams").fetchone()[0])
        db.execute("INSERT INTO teams (team_code,owner) VALUES(:team_code,:owner)",{"team_code":team_code.upper(),"owner":owner_id})
        db.commit()
        return jsonify({"error":"success"}),200
    else:
        return jsonify({"error":"team already exists"}),200

# Join team endpoint
@app.route("/joinTeam", methods = ["POST"])
def joinTeam():
    joinTeam_params = request.get_json()
    team_code = str(joinTeam_params["team_code"])
    user_id = str(joinTeam_params["user_id"])
    # Check if team exists:
    if(db.execute("SELECT COUNT(team_code) FROM teams WHERE upper(team_code) =:team_code", {"team_code":team_code.upper()}).fetchone()[0] == 0):
        return jsonify({"error":"team doesnt exist"}),200
    else:
        # check if user is already in a team:
        if(db.execute("SELECT COUNT(team_code) FROM teams WHERE upper(owner)=:user_id",{"user_id":user_id}).fetchone()[0] != 0 or db.execute("SELECT COUNT(team_code) FROM teams WHERE :user_id = ANY (member_list)",{"user_id":user_id.upper()}).fetchone()[0] != 0):
            return jsonify({"error":"user already in team"}),200
        # join team:
        db.execute("UPDATE teams SET member_list = array_append(member_list, :user_id) WHERE upper(team_code)=:team_code",{"user_id":user_id, "team_code":team_code.upper()})
        db.commit()
        return jsonify({"error":"joined team"}),200

@app.route("/getTeamInfo/<string:team_code>")
def getTeamInfo(team_code):
    # check if team exists:
    owner = ""
    members = []
    if(db.execute("SELECT COUNT(team_code) FROM teams WHERE upper(team_code)=:team_code", {"team_code":team_code.upper()}).fetchone()[0] == 0):
        return jsonify({"error":"team doesnt exist"}),200
    else:
        owner = str(db.execute("SELECT owner FROM teams WHERE upper(team_code)=:team_code",{"team_code":team_code.upper()}).fetchone()[0])
        members = db.execute("SELECT member_list FROM teams WHERE upper(team_code)=:team_code",{"team_code":team_code.upper()}).fetchone()[0]
        return jsonify({"error":"success",
                        "owner":owner,
                        "members":members}),200