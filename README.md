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


CREATE TABLE articles (
    item_id  INT NOT NULL,
    product_code INT NOT NULL,
    prod_name  VARCHAR(255) NOT NULL,
    product_type_no INT NOT NULL,
    product_type_name VARCHAR(255) NOT NULL,
    product_group_name VARCHAR(255) NOT NULL,
    graphical_appearance_no  INT NOT NULL,
    graphical_appearance_name  VARCHAR(255) NOT NULL,
    colour_group_code INT NOT NULL,
    colour_group_name VARCHAR(255) NOT NULL,
    perceived_colour_value_id  INT NOT NULL,
    perceived_colour_value_name VARCHAR(255) NOT NULL,
    perceived_colour_master_id INT NOT NULL,
    perceived_colour_master_name VARCHAR(255) NOT NULL,
    department_no INT NOT NULL,
    department_name VARCHAR(255) NOT NULL,
    index_code VARCHAR(255) NOT NULL,
    index_name VARCHAR(255) NOT NULL,
    index_group_no INT NOT NULL,
    index_group_name VARCHAR(255) NOT NULL,
    section_no  INT NOT NULL,
    section_name VARCHAR(255) NOT NULL,
    garment_group_no INT NOT NULL,
    garment_group_name VARCHAR(255) NOT NULL,
    detail_desc VARCHAR(255) NOT NULL,
    PRIMARY KEY (item_id)
);