from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from . import utils
import json

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        api_key1 = request.form['api_key1']
        api_key2 = request.form['api_key2']
        user1_name = request.form['user1_name']
        user2_name = request.form['user2_name']
        
        if utils.validate_api_keys(api_key1, api_key2):
            resp = make_response(redirect(url_for('routes.dashboard')))
            resp.set_cookie('api_key1', api_key1)
            resp.set_cookie('api_key2', api_key2)
            resp.set_cookie('user1_name', user1_name)
            resp.set_cookie('user2_name', user2_name)
            return resp
        else:
            flash('Invalid API keys. Please try again.')
    return render_template('login.html')

@bp.route('/dashboard')
def dashboard():
    api_key1 = request.cookies.get('api_key1')
    api_key2 = request.cookies.get('api_key2')
    user1_name = request.cookies.get('user1_name')
    user2_name = request.cookies.get('user2_name')
    if not api_key1 or not api_key2:
        return redirect(url_for('routes.login'))
    data1, data2 = utils.get_dashboard_data(api_key1, api_key2)

    # return render_template("dashboard.html", data1=data1, data2=data2)
    # user1_name = request.form.get("user1_name")
    # user2_name = request.form.get("user2_name")
    print("User 1 Name Cookie:", user1_name)
    print("User 2 Name Cookie:", user2_name)

    return render_template(
        "dashboard.html",
        data1=data1,
        data2=data2,
        user1_name=user1_name,
        user2_name=user2_name
    )

@bp.route('/update_data', methods=['POST'])
def update_data():
    api_key1 = request.cookies.get('api_key1')
    api_key2 = request.cookies.get('api_key2')
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    data1, data2 = utils.get_dashboard_data(api_key1, api_key2, start_date, end_date)
    return jsonify(data1=data1, data2=data2)

