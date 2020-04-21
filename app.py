from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps
import datetime
import os
import time

app = Flask(__name__)

# Get environment variables
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
IDLE_TIME = os.getenv('IDLE_TIME')

# Connection pool
client = MongoClient(
            MONGO_URI,
            maxPoolSize=1,
            socketKeepAlive=False
            )
db = client[MONGO_DB_NAME]
posts = db.posts

# Def of APIs
@app.route('/health', methods=['GET'])
def health():
    return 'I am healthy!'

@app.route('/show_posts/<author>', methods=['GET'])
def show_posts(author):
    r = posts.find_one({'author': author})
    if r:
        time.sleep(int(IDLE_TIME))
        post = {
            'author': 'henlo',
            'text': 'world',
            'date': datetime.datetime.utcnow()
        }
        post_id = posts.insert_one(post).inserted_id
        return 'Post Inserted: {}\n{}'.format(post_id, dumps(r))
    else:
        return 'Err: Author not found!'

@app.route('/insert_post', methods=['POST'])
def insert_post():
    if request.method == 'POST':
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
