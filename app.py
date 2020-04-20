from flask import Flask, request
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# Get environment variables
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

# Def of APIs
def get_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    return db

@app.route('/health')
def health():
    return 'I am healthy!'

@app.route('/show_posts/<author>')
def show_posts(author):
    posts = get_db().posts
    r = posts.find_one({'author': author})
    if r:
        return r
    else:
        return 'Err: Author not found!'

@app.route('/insert_post')
def insert_post():
    if request.method == 'POST':
        posts = get_db().posts
        post = {
            'author': request.form['author'],
            'text': request.form['text'],
            'date': datetime.datetime.utcnow()
        }
        post_id = posts.insert_one(post).inserted_id
        return 'Post Inserted: {}'.format(post_id)


# Exec
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
