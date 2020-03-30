"""Flask app for Cupcakes"""
from flask import Flask, jsonify
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
    return {"flavor": cupcake.flavor,
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

    return jsonify(current_cupcake=serialized)

   # inquire if this jsonify argument has to match our created variable



