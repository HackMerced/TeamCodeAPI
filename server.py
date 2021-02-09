import os
from flask import Flask, render_template
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback


app = Flask(__name__)

@app.route("/")
def index():
    return "test"