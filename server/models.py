from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("All authors must have a name.")
        elif db.session.query(Author).filter_by(name=name).first():
            raise ValueError("Duplicate names are not allowed.")
        else:
            return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number must be equal to 10 digits")
        else:
            return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Post must have a title")
        elif not any(word in title for word in clickbait_words):
            raise ValueError(f"Post must contain one or more from {clickbait_words}")
        return title

    @validates('content', 'summary')
    def validate_length(self, key, text):
        if key == 'content':
            if len(text) < 250:
                raise ValueError("Content length must be at least 250 characters")
            else:
                return text
        elif key == 'summary':
            if len(text) >= 250:
                raise ValueError(
                    "Summary length cannot be greater than or equal to 250 characters"
                )
            else:
                return text

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    