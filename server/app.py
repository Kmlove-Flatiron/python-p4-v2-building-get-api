# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, asc

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route("/games")
def games():

    games_to_dict = [game.to_dict(rules=("-reviews",)) for game in Game.query.all()]
    
    return make_response(games_to_dict, 200, {"Content-Type": "application/json"})

    # games_to_dict = []
    # for game in Game.query.all():
    #     dict = {
    #         "id": game.id,
    #         "title": game.title,
    #         "genre": game.genre,
    #         "platform": game.platform,
    #         "price": game.price,
    #         "created_at": game.created_at,
    #         "updated_at": game.updated_at 
    #     }
    #     games_to_dict.append(dict)

    # return make_response(jsonify(games_to_dict), 200)

@app.route("/games/<int:id>")
def get_one_game(id):
    game = Game.query.filter_by(id=id).first()

    game_to_dict = game.to_dict()

    return make_response(game_to_dict, 200)

@app.route("/games/users/<int:id>")
def game_users_by_id(id):
    # # Without Association Proxy (so have to go through reviews)
    game = db.session.get(Game, id)
    # users = [review.user for review in game.reviews]
    # users_to_dict = [user.to_dict(rules=("-reviews",)) for user in users]
    # return make_response(users_to_dict, 200)

    # With Association
    users =[user.to_dict(rules=("-reviews",)) for user in game.users] 
    return make_response(users, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

