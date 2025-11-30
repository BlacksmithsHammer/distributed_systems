from flask import Flask, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend-service:5000')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Frontend App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 20px; border-radius: 8px; max-width: 600px; }
        h1 { color: #333; }
        .response { background: #e8f5e9; padding: 15px; border-radius: 4px; margin: 10px 0; }
        .error { background: #ffebee; }
        a { color: #1976d2; margin-right: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Frontend Application</h1>
        <p>Links:</p>
        <a href="/">Home</a>
        <a href="/backend/data">Get Backend Data</a>
        <a href="/backend/info">Backend Info</a>
        <a href="/health">Health Check</a>
        <div class="response">
            <strong>Response:</strong><br>
            <pre>{{ response }}</pre>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, response='Welcome! Click links above to test backend connection.')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'frontend'})

@app.route('/backend/data')
def backend_data():
    try:
        resp = requests.get(f'{BACKEND_URL}/api/data', timeout=5)
        return render_template_string(HTML_TEMPLATE, response=resp.text)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, response=f'Error: {str(e)}')

@app.route('/backend/info')
def backend_info():
    try:
        resp = requests.get(f'{BACKEND_URL}/api/info', timeout=5)
        return render_template_string(HTML_TEMPLATE, response=resp.text)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, response=f'Error: {str(e)}')

@app.route('/api/backend/data')
def api_backend_data():
    try:
        resp = requests.get(f'{BACKEND_URL}/api/data', timeout=5)
        return jsonify({'source': 'frontend', 'backend_response': resp.json()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
