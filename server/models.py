
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        if Author.query.filter(Author.name == name).first():
            raise ValueError("Author name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and (len(phone_number) != 10 or not phone_number.isdigit()):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title