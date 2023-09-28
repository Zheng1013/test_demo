# test_demo
#完整功能使用

#選擇workplace資料夾（parquet檔）想放置的位置，之後更改test_Final_Project\app\user_knn_model\user_userKNN.py裡的路徑

#選擇workplace資料夾（parquet檔）想放置的位置，之後更改test_Final_Project\app\knn_model\option.py裡的路徑

#將kaggle下載的h&m服裝的images檔，放置到test_Final_Project\app\myproject\static下


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
    detail_desc text NOT NULL,
    PRIMARY KEY (item_id)
);

＃新建articles的table後,導入articles.csv

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\articles.csv' 
INTO TABLE articles 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
