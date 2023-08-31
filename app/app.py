from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required
from myproject import app, db
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from flask import Flask
import pymysql
import os
import knn_model.knn as model

#---連線DATABASE---




#---框架---



@app.route('/')
def index():
    return render_template('base.html')


@app.route('/home')
def base():
    return render_template('home.html')


@app.route('/report')
def report():
    return render_template('report.html')


@app.route('/recommed')
def recommed():
        return render_template('recommed.html')
    
@app.route('/test',methods=['POST'])
def test(): 
    if request.method == 'POST':
        item_id = request.form['itemId']
        item_id = int(item_id)
        similar_ids = model.knn_model(item_id)
        return render_template('test.html',data=similar_ids) 

#--------登錄系統-------

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("您已經成功的登入系統")
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            return redirect(next)
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已經登出系統")
    return redirect(url_for('base'))

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data, password=form.password.data)
        
        # add to db table
        db.session.add(user)
        db.session.commit()
        flash("感謝註冊本系統成為會員")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

#--------登錄系統end-------


# @app.route('/test',methods=['GET','POST'])
# def get_similar_ids():
#     item_id = request.json['item_id']
#     similar_ids = model.knn_model(item_id)
#     return render_template('test.html',data=similar_ids)  # Return the first 5 similar item IDs

if __name__ == '__main__':
    app.run(debug=True)
