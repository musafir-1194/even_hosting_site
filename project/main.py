from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User, Event, Host
from . import db
import sqlite3 as sql
from datetime import date

main = Blueprint('main', __name__)

@main.route('/')
def index():
    events=Event.query.all()
    return render_template('home.html',rows = events)

@main.route('/profile')
def profile():
    user=User.query.filter_by(username=current_user.username).first() 
    print("Hello done")
    p_host=Host.query.filter_by(u_id=user.id).all()
    event_list=[]
    if p_host:
        for i in p_host:
            event_list.append(Event.query.filter_by(id=i.e_id).first())

    return render_template('profile.html', username=current_user.username,host_list=event_list)

@main.route('/addevents')
def addevents():
    return render_template('addevents.html')

@main.route('/host', methods=['POST','GET'])
def host():
    i=request.args['id']
    event=Event.query.filter_by(id=i).first()
    return render_template('host.html',val=event)


