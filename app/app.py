from flask import render_template, redirect, request, url_for, flash, abort , jsonify
from flask_login import login_user, logout_user, login_required
from myproject import app, db
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from flask import Flask
import pymysql
import os
from pathlib import Path
from knn_model import knn , serch , option

dataframe = None

@app.route('/')
def index():
    #  image_root 需要根據圖片檔位置修改
    image_root = '../static/images/'
    ids , prod , graphical = serch.carousel()
    image_paths = []
    for id in ids:
        subfolder = "0" + str(id)[:2]
        # 商品圖片完整路径
        image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
        image_paths.append(image_path)
        base_data = zip(ids,image_paths,prod,graphical)
    return render_template('base.html',base_data=base_data)

@app.route('/get_index',methods=['POST'])
def get_index():
    global dataframe
    age_input = int(request.json.get('age_input', '0'))
    index_group_name_list , age_df = option.get_index(age_input)
    dataframe = age_df
    return jsonify({'options':index_group_name_list})

@app.route('/get_group',methods=['POST'])
def get_groupx():
    global dataframe
    age_df = dataframe
    index_input = str(request.json.get('indexMenu', '0'))
    product_group_name_list , index_df = option.get_group_list(index_input,age_df)
    dataframe = index_df
    return jsonify({'options':product_group_name_list})

@app.route('/get_type',methods=['POST'])
def get_type():
    global dataframe
    index_df = dataframe
    group_input = str(request.json.get('groupMenu', '0'))
    group_type_list , group_df = option.get_type_list(group_input,index_df)
    dataframe = group_df
    return jsonify({'options':group_type_list})

@app.route('/get_image',methods=['POST'])
def get_image():
    global dataframe
    group_df = dataframe
    type_input = request.form['typeSelect']
    color_input = request.form['color_input']
    ids , names , colors ,types , volumes = option.get_article(type_input,color_input,group_df)

    image_root = '../static/images/'
    image_paths = []
    for id in ids:
        subfolder = "0" + str(id)[:2]
        # 商品圖片完整路径
        image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
        image_paths.append(image_path)
    zip_top10 =  zip(ids,names,colors,types,volumes,image_paths)

    cids , cprod , cgraphical = serch.carousel()
    cimage_paths = []
    for cid in cids:
        subfolder = "0" + str(cid)[:2]
        # 商品圖片完整路径
        cimage_path = image_root + f"{subfolder}"  + f"/0{cid}.jpg"
        cimage_paths.append(cimage_path)
        base_data = zip(cids,cimage_paths,cprod,cgraphical)
    return render_template('base.html',zip_top10=zip_top10 ,base_data=base_data)

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
    image_root = '../static/images/'
    if request.method == 'POST':
        item_id = request.form['itemId']
        item_id = int(item_id)
        similar_ids = knn.knn_model(item_id)
        prod , grap= serch.serch_article(similar_ids)
        # 創建列表，儲存每個ID對應的圖片路徑
        image_paths = []
        for id in similar_ids:
            subfolder = "0" + str(id)[:2]
            # 商品圖片完整路径
            image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
            image_paths.append(image_path)
        one_zip = zip(similar_ids[:1],image_paths[:1],prod[:1] ,grap[:1])
        five_zip= zip(similar_ids[1:],image_paths[1:],prod[1:] ,grap[1:])
        return render_template('recommed.html',five_zip=five_zip,one_zip=one_zip)  


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



if __name__ == '__main__':
    app.run(debug=True)
