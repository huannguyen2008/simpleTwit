from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Tweet(db.Model):
    id = Column(Integer, primary_key=True)
    tweet = Column(String(280), nullable=False)
    date = Column(DateTime, unique=True, nullable=False, default=datetime)

    def __repr__(self):
        return f"Tweet('{self.tweet}','{self.date}')"


def add_tweet(tweet, date):
    tweet = Tweet(tweet=tweet, date=date)
    db.session.add(tweet)
    db.session.commit()


@app.route("/")
def index():
    tweets = Tweet.query.all()

    def map_tweet(tweet):
        return {'id': tweet.id, 'tweet': tweet.tweet, 'date': tweet.date}

    tweets = map(map_tweet, tweets)
    tweets = list(tweets)
    return jsonify(tweets=tweets)


@app.route("/tweet", methods=['POST'])
def post_tweet():
    add_tweet(tweet=request.json['tweet'], date=datetime.datetime.now())
    return 'tweeted'


if __name__ == "__main__":
    app.run(debug=True)
