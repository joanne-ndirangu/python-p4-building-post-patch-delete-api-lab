#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['POST'])
def add_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')

    if not name or not price:
        return make_response(jsonify({"error": "Name and Price are required"}), 400)

    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()

    return make_response(jsonify(new_baked_good.to_dict()), 201)

@app.route('/bakeries/<int:id>' , methods =['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if request.method == 'GET':

        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        return response
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            jsonify(bakery_dict),
            200
        )

        return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]

    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    response = make_response(
        jsonify(most_expensive_serialized),
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['GET', 'POST'])
def baked_goods_post(id):
    if request.method == "GET":
        bakery = BakedGood.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        return response
    elif request.method == 'POST':
        new_bakery = BakedGood(
            name=request.form.get('name'),
            price=request.form.get('price'),
            bakery_id=request.form.get('bakery_id'),
        )
        db.session.add(new_bakery)
        db.session.commit()

        bakery_dict = new_bakery.to_dict()

        response = make_response(
            jsonify(bakery_dict), 201
        )
        return response
@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_delete(id):
    if request.method == "GET":
        bakery = BakedGood.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        return response
    elif request.method == 'DELETE':
        bakery = BakedGood.query.filter_by(id=id).first()
        db.session.delete(bakery)
        db.session.commit()

        response_body = {
            "Delete _ successful" : True,
            "message" : "Bakery deleted."
        }
        response = make_response(
            jsonify(response_body),200
        )
        return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
