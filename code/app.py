from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': "Item not found!"}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': "An item with this name is already exist."}, 400
        data = request.get_json()
        item = {"name": name, "price": data.get('price')}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return items, 200


api.add_resource(Item, "/items/<string:name>/")
api.add_resource(ItemList, "/items/")

app.run(debug=True)