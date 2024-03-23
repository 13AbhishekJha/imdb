import os
import threading

from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_user, logout_user, login_required
from pymongo import MongoClient
from werkzeug.utils import secure_filename

from utils import User, IMDBUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

client = MongoClient('mongodb://localhost:27017')
db = client['imdb']
users_collection = db['users']
movies_collection = db['movies']

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    user_data = users_collection.find_one({'username': username})
    if user_data:
        return User(username)
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = users_collection.find_one(
            {'username': username, 'password': str(password)})
        if user_data:
            user = User(username)
            login_user(user)
            return jsonify({'message': 'Login successful'})
        return jsonify({'message': 'Invalid username or password'}), 401
    # Return the HTML template for GET requests
    return render_template('index.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# CSV Upload route
@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    if 'csv_file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if csv_file:
        filename = secure_filename(csv_file.filename)
        csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Start a new thread to process the uploaded CSV file
        threading.Thread(target=IMDBUtils.process_csv(
            filename=filename, movies_collection=movies_collection), args=(filename,)).start()

        return jsonify({'message': 'File uploaded successfully'})


# Get progress of uploaded CSV
@app.route('/progress')
@login_required
def get_progress():
    # Count the number of rows processed in the CSV file
    if 'csv_file' in request.files:
        csv_file = request.files['csv_file']
        if csv_file.filename != '':
            filename = secure_filename(csv_file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(path):
                with open(path, 'r') as file:
                    num_rows = sum(1 for line in file)
                return jsonify({'progress': 'Processing', 'total_rows': num_rows})
            else:
                return jsonify({'progress': 'File not found'}), 404
    return jsonify({'progress': 'No CSV file uploaded'})


# Movie List route
@app.route('/movies')
@login_required
def movie_list():
    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page
    movies = list(movies_collection.find(
        {}, {'_id': False}).skip(skip).limit(per_page))
    return jsonify(movies)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
