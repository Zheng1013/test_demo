from myproject import db, login_manager, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Article(db.Model):
    __tablename__ = 'articles'
    
    item_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.Integer, nullable=False)
    prod_name = db.Column(db.String(255), nullable=False)
    product_type_no = db.Column(db.Integer, nullable=False)
    product_type_name = db.Column(db.String(255), nullable=False)
    product_group_name = db.Column(db.String(255), nullable=False)
    graphical_appearance_no = db.Column(db.Integer, nullable=False)
    graphical_appearance_name = db.Column(db.String(255), nullable=False)
    colour_group_code = db.Column(db.Integer, nullable=False)
    colour_group_name = db.Column(db.String(255), nullable=False)
    perceived_colour_value_id = db.Column(db.Integer, nullable=False)
    perceived_colour_value_name = db.Column(db.String(255), nullable=False)
    perceived_colour_master_id = db.Column(db.Integer, nullable=False)
    perceived_colour_master_name = db.Column(db.String(255), nullable=False)
    department_no = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.String(255), nullable=False)
    index_code = db.Column(db.String(255), nullable=False)
    index_name = db.Column(db.String(255), nullable=False)
    index_group_no = db.Column(db.Integer, nullable=False)
    index_group_name = db.Column(db.String(255), nullable=False)
    section_no = db.Column(db.Integer, nullable=False)
    section_name = db.Column(db.String(255), nullable=False)
    garment_group_no = db.Column(db.Integer, nullable=False)
    garment_group_name = db.Column(db.String(255), nullable=False)
    detail_desc = db.Column(db.Text, nullable=False)

    def __init__(self, product_code, prod_name, product_type_no, product_type_name, product_group_name,
                 graphical_appearance_no, graphical_appearance_name, colour_group_code, colour_group_name,
                 perceived_colour_value_id, perceived_colour_value_name, perceived_colour_master_id,
                 perceived_colour_master_name, department_no, department_name, index_code, index_name,
                 index_group_no, index_group_name, section_no, section_name, garment_group_no, garment_group_name,
                 detail_desc):
        self.product_code = product_code
        self.prod_name = prod_name
        self.product_type_no = product_type_no
        self.product_type_name = product_type_name
        self.product_group_name = product_group_name
        self.graphical_appearance_no = graphical_appearance_no
        self.graphical_appearance_name = graphical_appearance_name
        self.colour_group_code = colour_group_code
        self.colour_group_name = colour_group_name
        self.perceived_colour_value_id = perceived_colour_value_id
        self.perceived_colour_value_name = perceived_colour_value_name
        self.perceived_colour_master_id = perceived_colour_master_id
        self.perceived_colour_master_name = perceived_colour_master_name
        self.department_no = department_no
        self.department_name = department_name
        self.index_code = index_code
        self.index_name = index_name
        self.index_group_no = index_group_no
        self.index_group_name = index_group_name
        self.section_no = section_no
        self.section_name = section_name
        self.garment_group_no = garment_group_no
        self.garment_group_name = garment_group_name
        self.detail_desc = detail_desc