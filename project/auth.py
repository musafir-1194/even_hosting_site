from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy.types import TypeDecorator, TIMESTAMP
import iso8601
from .models import User, Event, Host
from . import db
import sqlite3 as sql

import logging

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login_post', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup_post', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
 
    return redirect(url_for('main.index'))

@auth.route('/events', methods=['GET'])
def events():
    return render_template('addevents.html')

@auth.route('/submit_events', methods=['POST'])
def submit_events():
    title = request.form.get('title')
    s_date=iso8601.parse_date(request.form.get('start_date'))
    e_date=iso8601.parse_date(request.form.get('end_date'))
    # email = request.form.get('email')
    # name = request.form.get('name')
    event=Event.query.filter_by(title=title).first()
    
    if event:
        flash('Event already exists')
        return redirect(url_for('auth.event'))

    event=Event(title=title, s_date=s_date, e_date=e_date)
    db.session.add(event)
    db.session.commit()

    return redirect(url_for('auth.events'))

@auth.route('/event_host',methods=['GET', 'POST'])
def event_host():
    ev_title=request.form.get('event')
    event=Event.query.filter_by(title=ev_title).first()
    event_id=event.id
    email=request.form.get('email')
    user=User.query.filter_by(email=email).first()
    if user:
        user_id=user.id
        t_host=Host.query.filter_by(u_id=user_id, e_id=event_id).all()
        
        if t_host :
            flash('Event is already assigned to User')
            return redirect(url_for('main.index'))
        
        host=Host(u_id=user_id, e_id=event_id)
        db.session.add(host)
        db.session.commit()
        flash('Event assigned to User')
        
        return redirect(url_for('main.host'))
    flash('User not registered. Please register first')
    return redirect(url_for('auth.signup'))