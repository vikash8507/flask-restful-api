from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "hadgznxasjghaygbnasn12986365gi=2t21y@$5mnzvxhgf"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="Price required"
    )

    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': "Item not found!"}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': "An item with this name is already exist."}, 400
        data = Item.parser.parse_args()
        item = {"name": name, "price": data.get('price')}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {"message": "Item deleted successfully"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item is None:
            item = {'name': name, "price": data['price']}
            items.append(item)
        else:
            item.update(data)
        return item, 200

class ItemList(Resource):
    def get(self):
        return items, 200


api.add_resource(Item, "/items/<string:name>/")
api.add_resource(ItemList, "/items/")

app.run(debug=True)