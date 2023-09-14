from flask import render_template, redirect, request, url_for, flash, abort , jsonify ,session
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from flask_ngrok import run_with_ngrok
from myproject import app, db
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from myproject.click import Favorite
from user_knn_model.user_userKNN  import knn_model
from flask import Flask
import pymysql
import os
from pathlib import Path
from knn_model import knn , serch , option

dataframe = None

@app.route('/',methods=['GET','POST'])
def index():
    #  image_root 需要根據圖片檔位置修改
    image_root = '../static/images/'
    ids , prod , graphical = serch.carousel()
    image_paths = []
    for id in ids:
        subfolder = "0" + str(id)[:2]
        # 輪播商品圖片完整路径
        image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
        image_paths.append(image_path)
        base_data = zip(ids,image_paths,prod,graphical)
    if request.method == "GET":
        return render_template('First_page.html',base_data=base_data)
    
    elif request.method == "POST":
        global dataframe
        group_df = dataframe
        type_input = request.form['typeSelect']
        color_input = request.form['color_input']
        ids , names , colors ,types  = option.get_article(type_input,color_input,group_df)

        image_root = '../static/images/'
        image_paths = []
        for id in ids:
            subfolder = "0" + str(id)[:2]
            # top10 商品圖片完整路径
            image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
            image_paths.append(image_path)
        zip_top10 =  zip(ids,names,colors,types,image_paths)
        return render_template('First_page.html',zip_top10=zip_top10 ,base_data=base_data)

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

#--------加到購物車----------

@app.route('/add_to_favorite', methods=['POST'])
def add_to_favorite():
    if current_user.is_authenticated:
        item_id = request.form.get('item_id')  # 从POST请求中获取item_id
        user_id = current_user.id  # 获取当前已登录用户的ID
        favorite = Favorite(user_id=user_id, item_id=item_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(message="商品已添加到購物車！"),200
    else:
        return jsonify(message="添加商品到購物車时出现錯誤。"), 401  # 返回未授权状态码

#--------我的最愛頁面
@app.route('/myfavorite')
@login_required  # 確保只有登錄的用戶可以訪問這個頁面
def myfavorite():
    # 在這裡，你需要根據當前已登錄用戶的ID查詢其最愛的商品
    user_id = current_user.id
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    # 從Favorites中提取item_id
    item_ids = [favorite.item_id for favorite in favorites]
    
    # 使用上述已訓練的KNN模型為這些item_id生成推薦
    recommandations = knn_model(item_ids)
    
    # 返回myfavorite.html模板，將最愛列表和推薦商品傳遞給模板
    return render_template('myfavorite.html', favorites=favorites, recommandations=recommandations)

cart = {
    'cartItems': [],
    'totalItems': 0
    }

@app.route('/add_to_cart',methods=['POST'])
def add_to_cart():
    if current_user.is_authenticated:
        data = request.get_json()
        already_exit = False
        if cart['cartItems'] == []:
            cart['cartItems'].append(data)
            cart['totalItems'] = len(cart['cartItems'])
        else:
            for item in cart['cartItems']:
                if item['id'] == data['id']:
                    already_exit = True
                    break
            if not already_exit:
                cart['cartItems'].append(data)
                cart['totalItems'] = len(cart['cartItems'])         
        return jsonify(cart)
    else:
        return jsonify(message="添加商品到購物車时出现錯誤。"), 401
    
@app.route('/remove', methods=['POST'])
def remove_item():
    data = request.json
    item_id = data.get('itemId')

    # 在购物车数据中查找并删除具有匹配 itemId 的商品
    updated_cart_items = [item for item in cart['cartItems'] if item['id'] != item_id]

    # 更新购物车数据，这可能涉及到在数据库中更新购物车或会话中的内容
    cart['cartItems'] = updated_cart_items

    # 计算购物车中商品的总数量
    total_items = sum(item.get('quantity', 1) for item in updated_cart_items)

    # 最后，返回更新后的购物车内容和总数量
    return jsonify({'cartItems': updated_cart_items, 'totalItems': total_items})



if __name__ == '__main__':
    app.run(debug=True)
    
    # 使用ngrok註解app.run(debug=True),使用以下
    # app.run()
    # run_with_ngrok(app)
