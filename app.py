from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def homepage():
    """"Render homepage"""
    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    """"Return all cupcakes"""
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """create a new cupcake and return data about it"""
    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        rating = data['rating'],
        size = data['size'],
        image = data['image'] or None
    )
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on a specific cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(Cupcake_id):
    """Update data about specific cupcake and return updated data"""

    data = request.json
    cupcake = Cupcake.query.get_or_404(Cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return success message"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
