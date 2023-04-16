from flask import Flask, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Dummy data to simulate a database
houses = [
    {
        'id': 1,
        'name': 'Spacious apartment near campus',
        'description': '2-bedroom apartment with parking, laundry, and balcony',
        'location': '123 Main St.',
        'rent': 1500,
        'provider_id': 1
    },
    {
        'id': 2,
        'name': 'Cozy studio with great view',
        'description': 'Furnished studio with kitchenette and utilities included',
        'location': '456 Elm St.',
        'rent': 800,
        'provider_id': 1
    }
]

providers = [
    {
        'id': 1,
        'username': 'provider1',
        'password_hash': generate_password_hash('password1')
    }
]

# Authentication endpoints
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    provider = next((p for p in providers if p['username'] == username), None)
    if not provider or not check_password_hash(provider['password_hash'], password):
        abort(401)
    
    return jsonify({'success': True})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if next((p for p in providers if p['username'] == username), None):
        abort(400, 'Username already exists')
    
    provider = {
        'id': len(providers) + 1,
        'username': username,
        'password_hash': generate_password_hash(password)
    }
    providers.append(provider)
    
    return jsonify({'success': True})

# House endpoints
@app.route('/houses', methods=['GET'])
def get_houses():
    return jsonify(houses)

@app.route('/houses/<int:house_id>', methods=['GET'])
def get_house(house_id):
    house = next((h for h in houses if h['id'] == house_id), None)
    if not house:
        abort(404)
    
    return jsonify(house)

@app.route('/houses', methods=['POST'])
def add_house():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    rent = data.get('rent')
    provider_id = data.get('provider_id')

    if not next((p for p in providers if p['id'] == provider_id), None):
        abort(400, 'Provider ID does not exist')

    house = {
        'id': len(houses) + 1,
        'name': name,
        'description': description,
        'location': location,
        'rent': rent,
        'provider_id': provider_id
    }
    houses.append(house)
    
    return jsonify({'success': True})

@app.route('/houses/<int:house_id>', methods=['PUT'])
def update_house(house_id):
    house = next((h for h in houses if h['id'] == house_id), None)
    if not house:
        abort(404)

    data = request.json
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')
    rent
