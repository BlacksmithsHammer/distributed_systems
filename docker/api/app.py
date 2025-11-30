from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'database'),
    'port': os.getenv('DATABASE_PORT', '5432'),
    'user': os.getenv('DATABASE_USER', 'admin'),
    'password': os.getenv('DATABASE_PASSWORD', 'secret123'),
    'dbname': os.getenv('DATABASE_NAME', 'myapp')
}

def get_db():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.route('/')
def index():
    return jsonify({'message': 'Docker API работает!', 'endpoints': ['/health', '/users', '/products', '/stats']})

@app.route('/health')
def health():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected', 'version': version['version']})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY id;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'count': len(users), 'users': users})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, email) VALUES (%s, %s) RETURNING *;', (data['username'], data['email']))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Создан!', 'user': user}), 201

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products ORDER BY id;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    for p in products:
        p['price'] = float(p['price'])
    return jsonify({'count': len(products), 'products': products})

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s) RETURNING *;', (data['name'], data['price'], data.get('quantity', 0)))
    product = cur.fetchone()
    product['price'] = float(product['price'])
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Создан!', 'product': product}), 201

@app.route('/stats')
def stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as users FROM users;')
    users = cur.fetchone()['users']
    cur.execute('SELECT COUNT(*) as products, COALESCE(SUM(quantity), 0) as qty FROM products;')
    prod = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({'users': users, 'products': prod['products'], 'total_qty': prod['qty']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
