"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


def serialize_cupcake(cupcake):
    return {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
            }


@app.route('/api/cupcakes')
def list_all():
    """get listing of all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_data(cupcake_id):

    """get info about current cupcake"""
    current_cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(current_cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    flavor = request.json["flavor"]
    image = request.json["image"] or None
    rating = request.json["rating"]
    size = request.json["size"]
    new_cupcake = Cupcake(flavor=flavor, image=image, rating=rating, size=size)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    flavor = request.json["flavor"]
    image = request.json["image"] or None
    rating = request.json["rating"]
    size = request.json["size"]
    current_cupcake = Cupcake.query.get_or_404(cupcake_id)
    current_cupcake.flavor = flavor
    if image is not None:
        current_cupcake.image = image
    current_cupcake.rating = rating
    current_cupcake.size = size
    db.session.commit()
    serialized = serialize_cupcake(current_cupcake)
    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    current_cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(current_cupcake)
    db.session.commit()
    return jsonify({"message": "Deleted"})

    



