# test_demo
#如果有從kaggle載下H&M的圖片檔images,可以將圖片檔放在myproject/template/static裡面
#首頁的下拉式選單要使用,需要將firstinput的parquet放在knn_model資料夾


#手動建立MYSQL table

CREATE TABLE users ( 
id INT AUTO_INCREMENT PRIMARY KEY,
age INT,
email VARCHAR(255) UNIQUE,
username VARCHAR(255) UNIQUE,
password_hash VARCHAR(255) )



CREATE TABLE clickdata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);