from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt, association_proxy


class Wine(db.Model, SerializerMixin):
    __tablename__ = 'wines'

    serialize_rules = ('-reviews.wine',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    flavor_profile = db.Column(db.String)
    location = db.Column(db.String)
    price = db.Column(db.Float)
    viewed_at = db.Column(db.DateTime, default=None)  
    image = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='wine', cascade='all, delete-orphan')
    users = association_proxy('reviews', 'user', creator=lambda user_obj: Review(user=user_obj))
    
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-wine.reviews', '-user.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    star_review = db.Column(db.Integer)
    comment = db.Column(db.String)

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    wine = db.relationship('Wine', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    wines = association_proxy('reviews', 'wine', creator=lambda wine_obj: Review(wine=wine_obj))

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be null")
        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    