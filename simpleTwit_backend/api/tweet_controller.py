import datetime
from flask import Blueprint, request, jsonify
from flask_login import current_user

from model import Tweet, db, User

app = Blueprint('{}_api'.format(__name__), __name__, url_prefix='/api/tweet')


def add_tweet(name, tweet, date):
    tweet = Tweet(name=name, tweet=tweet, date=date)
    db.session.add(tweet)
    db.session.commit()


@app.route("/", methods=['POST'])
def post_tweet():
    add_tweet(name=request.json['name'], tweet=request.json['tweet'], date=datetime.datetime.now())
    return 'tweeted'


def delete_tweet(id_tweet):
    user = User.query.filter_by(username=current_user.username).first()
    tweet = Tweet.query.filter_by(id=id_tweet).first()
    if tweet.name == user.username:
        db.session.delete(tweet)
        db.session.commit()
        return 1
    else:
        return 0


@app.route("/delete", methods=['POST'])
def delete():
    del_tweet = delete_tweet(id_tweet=request.json['id'])
    if del_tweet == 1:
        return 'deleted'
    else:
        return 'false'


@app.route("/list_tweet")
def list_tweet():
    tweets = Tweet.query.all()

    def map_tweet(tweet):
        return tweet.to_dict()

    tweets = map(map_tweet, tweets)
    tweets = list(tweets)
    tweets.reverse()
    return jsonify(tweets=tweets)
