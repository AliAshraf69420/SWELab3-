from flask import Flask 
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title='Items API', description='A simple API for managing items')

# Define the namespace
ns = api.namespace('items', description='Operations related to items')

# Define the model (schema) for the items
item_model = api.model('Item', {
    'id': fields.Integer(required=True, description='The item ID'),
    'name': fields.String(required=True, description='The name of the item'),
    'price': fields.Float(required=True, description='The price of the item')
})

# Sample data
items = [
    {'id': 1, 'name': 'Item 1', 'price': 10.99},
    {'id': 2, 'name': 'Item 2', 'price': 12.99},
    {'id': 3, 'name': 'Item 3', 'price': 9.99}
]

# Root route (Home)
@app.route('/')
def home():
    return "Welcome to the Flask API! Use /swagger-ui to view the API documentation."

# GET all items
@ns.route('/')
class ItemList(Resource):
    @ns.doc('get_items')
    @ns.marshal_list_with(item_model)
    def get(self):
        '''Fetch all items'''
        return items

    @ns.doc('create_item')
    @ns.expect(item_model)
    @ns.marshal_with(item_model, code=201)
    def post(self):
        '''Create a new item'''
        new_item = api.payload
        items.append(new_item)
        return new_item, 201
@ns.route('/<int:id>')
@ns.response(404, 'Item not found')
@ns.param('id', 'The item identifier')
class Item(Resource):
    @ns.doc('get_item')
    @ns.marshal_with(item_model)
    def get(self, id):
        '''Fetch a specific item by ID'''
        item = next((item for item in items if item['id'] == id), None)
        if item:
            return item
        ns.abort(404, "Item not found")

    @ns.doc('update_item')
    @ns.expect(item_model)
    @ns.marshal_with(item_model)
    def put(self, id):
        '''Update an item by ID'''
        item = next((item for item in items if item['id'] == id), None)
        if item:
            updated_data = api.payload
            item.update(updated_data)
            return item
        ns.abort(404, "Item not found")

    @ns.doc('delete_item')
    @ns.response(204, 'Item deleted')
    def delete(self, id):
        '''Delete an item by ID'''
        global items
        items = [item for item in items if item['id'] != id]
        return '', 204

# Add the namespace to the API
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug=True)
