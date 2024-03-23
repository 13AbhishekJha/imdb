import os
import csv

from flask import Flask
from flask_login import UserMixin

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Define the User model for authentication
class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


class IMDBUtils:

    @classmethod
    def process_csv(cls, filename, movies_collection):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                show_id = row['show_id']
                type = row['type']
                title = row['title']
                director = row['director']
                cast = row['cast']
                country = row['country']
                date_added = row['date_added']
                release_year = int(row['release_year'])
                rating = row['rating']
                duration = row['duration']
                listed_in = row['listed_in']
                description = row['description']

                # Process the row data as needed (e.g., store it in the database)
                # Note: can also use insert_many here
                movies_collection.insert_one({'title': title, 'director': director, 'show_id': show_id,
                                              'type': type, 'cast': cast, 'country': country, 'date_added':
                                              date_added, 'release_year': release_year, 'rating': rating,
                                              'duration': duration, 'listed_in': listed_in, 'description': description})

        return True
