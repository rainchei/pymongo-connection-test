from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
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

@app.route('/health', methods=['GET'])
def health():
    return 'I am healthy!'

@app.route('/show_posts/<author>', methods=['GET'])
def show_posts(author):
    posts = get_db().posts
    r = posts.find_one({'author': author})
    if r:
        return dumps(r)
    else:
        return 'Err: Author not found!'

@app.route('/insert_post', methods=['POST'])
def insert_post():
    if request.method == 'POST':
        posts = get_db().posts
        post = {
            'author': request.json['author'],
            'text': request.json['text'],
            'date': datetime.datetime.utcnow()
        }
        post_id = posts.insert_one(post).inserted_id
        return 'Post Inserted: {}'.format(post_id)


# Exec
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
