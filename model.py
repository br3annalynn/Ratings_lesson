from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    released_at = Column(Date())
    imdb_url = Column(String(64), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

### End class declarations

def check_for_user(email):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user.id
    else:
        return False


def register_user(email, password, age, gender, zipcode):
    user = User(email=email, password=password, age=age, gender=gender, zipcode=zipcode)    
    session.add(user)
    session.commit()

def login(email, password):
    user = session.query(User).filter_by(email=email).one()
    if user.password == password:
        return user.id

def get_ratings_by_user_id(user_id):
    ratings_list = session.query(Rating).filter_by(user_id=user_id).all()
    return ratings_list

def get_ratings_by_movie_id(movie_id):
    movie_ratings_list=session.query(Rating).filter_by(movie_id=movie_id).all()
    return movie_ratings_list

def get_movie_by_id(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return movie

def get_all_movies():
    movies = session.query(Movie).all()
    return movies

def get_all_users():
    user_list = session.query(User).limit(100).all()
    return user_list

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
