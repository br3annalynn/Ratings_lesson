import model
import csv
import datetime


def load_users(session):
    # use u.user
    with open('seed_data/u.user') as csvfile:
        user_info = csv.reader(csvfile, delimiter='|')
        for row in user_info:
            user = model.User(id=row[0], age=row[1], gender=row[2], zipcode=row[4])
            session.add(user)
        session.commit()

def load_movies(session):
    # use u.item
    with open('seed_data/u.item') as csvfile:
        movie_info = csv.reader(csvfile, delimiter='|')
        for row in movie_info:
            release_date = datetime.datetime.strptime(row[2], "%d-%b-%Y")
            title=row[1].decode('latin-1')
            title=title.split(" (")
            title = title[0]
            movie = model.Movie(id=row[0], name=title, released_at=release_date, imdb_url=row[4])
            session.add(movie)
        session.commit()

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data') as csvfile:
        rating_info = csv.reader(csvfile, delimiter='\t')
        for row in rating_info:
            rating = model.Rating(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(rating)
        session.commit()



def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_ratings(s)

if __name__ == "__main__":
    s= model.connect()
    main(s)
