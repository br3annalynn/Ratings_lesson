from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from math import sqrt

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

    def similarity(self, other):
        user_ratings = {}
        paired_ratings = []
        for s_rating in self.ratings:
            user_ratings[s_rating.movie_id] = s_rating

        for o_rating in other.ratings:
            u_r = user_ratings.get(o_rating.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, o_rating.rating))

        if paired_ratings:
            return pearson(paired_ratings)
        else:
            return 0.0


    def predict_rating(self, movie):
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) for r in other_ratings] 
        similarities.sort(reverse=True) 
        similarities = [sim for sim in similarities if sim[0] > 0]
        if not similarities:
            return None
        numerator = sum([r.rating * similarity for similarity, r in similarities])
        denominator = sum([ similarity[0] for similarity in similarities])
        return numerator/denominator



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

def get_rating(user_id, movie_id, movie_ratings):

    user_rating = None
    prediction = None
    movie = get_movie_by_id(movie_id)
    
    for rating in movie_ratings:
        if rating.user_id == user_id:
            user_rating = rating.rating #user rating is a number 1-5

    if not user_rating:
        user = get_user_by_id(user_id)
        prediction = user.predict_rating(movie)
        if prediction:
            prediction = round(prediction, 2)

    return (user_rating, prediction)



def add_rating(movie_id, user_id, rating):
    existing_rating = session.query(Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if not existing_rating: 
        current_rating = Rating(movie_id=movie_id, user_id=user_id, rating=rating)
        session.add(current_rating)
    else:
        existing_rating.rating = rating
    session.commit()

def get_user_by_id(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def average_ratings(ratings_list):
    ratings_sum = 0
    for rating in ratings_list:
        ratings_sum += rating.rating
    average_ratings = ratings_sum / len(ratings_list)
    return average_ratings



def pearson(pairs):
    # Takes in a list of pairwise ratings and produces a pearson similarity
    series_1 = [float(pair[0]) for pair in pairs]
    series_2 = [float(pair[1]) for pair in pairs]
 
    sum1 = sum(series_1)
    sum2 = sum(series_2)
 
    squares1 = sum([ n*n for n in series_1 ])
    squares2 = sum([ n*n for n in series_2 ])
 
    product_sum = sum([ n * m for n,m in pairs ])
 
    size = len(pairs)
 
    numerator = product_sum - ((sum1 * sum2)/size)
    denominator = sqrt((squares1 - (sum1*sum1) / size) * (squares2 - (sum2*sum2)/size))
 
    if denominator == 0:
        return 0
    
    return numerator/denominator

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
