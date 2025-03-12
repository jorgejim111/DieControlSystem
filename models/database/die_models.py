from .db import db

class Inch(db.Model):
    __tablename__ = 'inches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inch = db.Column(db.String, nullable=False, unique=True)
    die_descriptions = db.relationship('DieDescription', backref='inch_info', lazy=True)

class Part(db.Model):
    __tablename__ = 'parts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    part = db.Column(db.String, nullable=False, unique=True)
    die_descriptions = db.relationship('DieDescription', backref='part_info', lazy=True)

class Description(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False, unique=True)
    die_descriptions = db.relationship('DieDescription', backref='description_info', lazy=True)

class DieDescription(db.Model):
    __tablename__ = 'die_descriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_inch = db.Column(db.Integer, db.ForeignKey('inches.id'), nullable=False)
    id_part = db.Column(db.Integer, db.ForeignKey('parts.id'), nullable=False)
    id_description = db.Column(db.Integer, db.ForeignKey('descriptions.id'), nullable=False)
    products = db.relationship('Product', backref='die_description_info', lazy=True)
    serials = db.relationship('Serial', backref='die_description_info', lazy=True)
    __table_args__ = (db.UniqueConstraint('id_inch', 'id_part', 'id_description'),)

class StatusSerial(db.Model):
    __tablename__ = 'status_serial'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String, nullable=False, unique=True)
    serials = db.relationship('Serial', backref='status_info', lazy=True)

class Line(db.Model):
    __tablename__ = 'lines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line = db.Column(db.String, nullable=False, unique=True)
    serials = db.relationship('Serial', backref='line_info', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.String, nullable=False, unique=True)
    id_die_description = db.Column(db.Integer, db.ForeignKey('die_descriptions.id'))
    serials = db.relationship('Serial', backref='product_info', lazy=True)

class Serial(db.Model):
    __tablename__ = 'serials'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial = db.Column(db.String, nullable=False, unique=True)
    id_die_description = db.Column(db.Integer, db.ForeignKey('die_descriptions.id'), nullable=False)
    inner = db.Column(db.Float)
    outer = db.Column(db.Float)
    proudness = db.Column(db.Float)
    id_status_serial = db.Column(db.Integer, db.ForeignKey('status_serial.id'), nullable=False)
    id_line = db.Column(db.Integer, db.ForeignKey('lines.id'))
    id_product = db.Column(db.Integer, db.ForeignKey('products.id')) 