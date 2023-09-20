from flask import render_template, redirect, request, url_for, flash, abort , jsonify ,session
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from flask_ngrok import run_with_ngrok
from myproject import app, db
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from myproject.click import Favorite
from myproject.data_info import Article
from user_knn_model.user_userKNN  import knn_model
from flask import Flask
import pymysql
import os
from pathlib import Path
from knn_model import knn , serch , option

dataframe = None

#-------首頁(GET:首頁 ,POST:將下拉式選單以POST傳送至首頁)---------
@app.route('/',methods=['GET','POST'])
def index():
    #  image_root 需要根據圖片檔位置修改
    image_root = '../static/images/'
    ids  = serch.carousel()
    prod = []
    color = []
    type = []
    image_paths = []
    for id in ids:
        subfolder = "0" + str(id)[:2]
        # 輪播商品圖片完整路径
        image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
        image_paths.append(image_path)
         # 輪播商品資訊
        article = Article.query.filter_by(item_id=id).first()
        prod.append(article.prod_name)
        color.append(article.colour_group_name)
        type.append(article.product_type_name)
        
    base_data = zip(ids,image_paths,prod,color,type)

    if request.method == "GET":
        return render_template('First_page.html',base_data=base_data)
    
    elif request.method == "POST":
            global dataframe
            if len(request.form) == 2:
                # global dataframe
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
            
            elif len(request.form) == 1:
                # global dataframe
                color_df = dataframe
                color_input = request.form['color_input']
                ids , names , colors ,types  = option.small_screen_get_article(color_input,color_df)

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

# 小螢幕用
@app.route('/get_color',methods=['POST'])
def get_color():
    global dataframe
    type_df = dataframe
    type_input = str(request.json.get('typeMenu', '0'))
    color_list , color_df = option.get_color(type_input,type_df)
    dataframe = color_df
    return jsonify({'options':color_list})


#-------首頁(GET:首頁 ,POST:將下拉式選單以POST傳送至首頁)end---------


#-----登出後轉跳------
@app.route('/home')
def base():
    return render_template('home.html')
#-----登出後轉跳end------


#-----圖表--------
@app.route('/report')
def report():
    return render_template('report.html')
#-----圖表end--------


#-----推薦系統------

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
        # 創建列表，儲存每個ID對應的圖片路徑
        image_paths = []
        prod = []
        color = []
        type = []
        for id in similar_ids:
            subfolder = "0" + str(id)[:2]
                # 商品圖片完整路径
            image_path = image_root + f"{subfolder}"  + f"/0{id}.jpg"
            image_paths.append(image_path)
            article = Article.query.filter_by(item_id=id).first()
            prod.append(article.prod_name)
            color.append(article.colour_group_name)
            type.append(article.product_type_name)

        one_zip = zip(similar_ids[:1],image_paths[:1],prod[:1] ,color[:1],type[:1])
        five_zip= zip(similar_ids[1:],image_paths[1:],prod[1:] ,color[1:],type[1:])

        if current_user.is_authenticated:

            user_id = current_user.id
            favorites = Favorite.query.filter_by(user_id=user_id).all()

            # 从Favorites中提取item_id
            item_ids = [favorite.item_id for favorite in favorites]

            recommandations = knn_model(item_ids)

            image_paths = []
            prod_recommand = []  # 商品名称
            color_recommand = []
            type_recommand = []

            for id in recommandations:
                subfolder = "0" + str(id)[:2]
                # 商品图片完整路径
                image_path = f"../static/images/{subfolder}/0{id}.jpg"
                image_paths.append(image_path)

                article = Article.query.filter_by(item_id=id).first()
                prod_recommand.append(article.prod_name)
                color_recommand.append(article.colour_group_name)
                type_recommand.append(article.product_type_name)

            zip_recommand = zip(recommandations, image_paths, prod_recommand, color_recommand, type_recommand)


            return render_template('recommed.html',five_zip=five_zip,one_zip=one_zip,zip_recommand=zip_recommand) 
        else:
            # 用户未认证，可以执行未认证用户的操作

            # 在这里，您可以处理未认证用户的逻辑

            return render_template('recommed.html', five_zip=five_zip, one_zip=one_zip)
    
#-------推薦系統end------


#--------登錄系統-------

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if  user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('welcome_user')
            return redirect(next)
        else:
            flash("登入失敗：無效的電子郵件或密碼", 'error')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
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
        flash("感謝註冊本系統成為會員","success")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

#--------登錄系統end-------


#--------我的最愛頁面
# @app.route('/myfavorite')
# @login_required  # 確保只有登錄的用戶可以訪問這個頁面
# def myfavorite():
#     # 在這裡，你需要根據當前已登錄用戶的ID查詢其最愛的商品
#     user_id = current_user.id
#     favorites = Favorite.query.filter_by(user_id=user_id).all()
    
#     # 從Favorites中提取item_id
#     item_ids = [favorite.item_id for favorite in favorites]
    
#     fav_paths=[]
#     prod_fav = []  # 商品名稱
#     grap_fav = []  # 外觀描述

#     for id in item_ids:
#         subfolder = "0" + str(id)[:2]
#         # 商品圖片完整路径
#         fav_path = f"../static/images/{subfolder}/0{id}.jpg"
#         fav_paths.append(fav_path)
        
#         article = Article.query.filter_by(item_id=id).first()
#         prod_fav.append(article.prod_name)
#         grap_fav.append(article.graphical_appearance_name)
        
#     zip_favor = zip(favorites , fav_paths, prod_fav, grap_fav)



#     # 使用上述已訓練的KNN模型為這些item_id生成推薦
#     recommandations = knn_model(item_ids)
    
#     image_paths = []
#     prod_recommand = []  # 商品名稱
#     grap_recommand = []  # 外觀描述

#     for id in recommandations:
#         subfolder = "0" + str(id)[:2]
#         # 商品圖片完整路径
#         image_path = f"../static/images/{subfolder}/0{id}.jpg"
#         image_paths.append(image_path)

#         article = Article.query.filter_by(item_id=id).first()
#         prod_recommand.append(article.prod_name)
#         grap_recommand.append(article.graphical_appearance_name)

#     zip_recommand = zip(recommandations , image_paths, prod_recommand, grap_recommand)
    
        
#     # return render_template('recommed.html', zip_recommand = zip_recommand)
#     # 返回myfavorite.html模板，將最愛列表、推薦商品以及相關的商品資訊傳遞給模板
#     return render_template('myfavorite.html', zip_favor = zip_favor, zip_recommand = zip_recommand)


#--------加到購物車的點擊事件(itemID到資料庫)----------

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

#-------購物車-------
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
            cart['totalItems'] = sum(item.get('quantity') for item in cart['cartItems'])
        else:
            for item in cart['cartItems']:
                if item['id'] == data['id']:
                    item['quantity'] += 1
                    cart['totalItems'] = sum(item.get('quantity') for item in cart['cartItems'])
                    already_exit = True
                    break
            if not already_exit:
                cart['cartItems'].append(data)
                cart['totalItems'] = sum(item.get('quantity') for item in cart['cartItems'])         
        return jsonify(cart)
    else:
        return jsonify(message="添加商品到購物車时出现錯誤。"), 401
    
@app.route('/remove', methods=['POST'])
def remove_item():
    data = request.json
    item_id = data.get('itemId')

    # 在購物車列表中查找並排除匹配 itemId 的商品
    updated_cart_items = [item for item in cart['cartItems'] if item['id'] != item_id]

    # 更新購物車內容
    cart['cartItems'] = updated_cart_items

    # 計算購物車中商品的總數量
    cart['totalItems'] = sum(item.get('quantity') for item in updated_cart_items)

    # 返回購物車商品內容和商品總數量
    return jsonify(cart)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart['cartItems'] = []
    cart['totalItems'] = 0
    return jsonify(cart)
#--------購物車end--------


if __name__ == '__main__':
    app.run(debug=True)
    
    # 使用ngrok註解app.run(debug=True),使用以下
    # app.run()
    # run_with_ngrok(app)
