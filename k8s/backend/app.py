from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'backend'})

@app.route('/api/data')
def get_data():
    return jsonify({
        'message': 'Hello from Backend!',
        'hostname': socket.gethostname(),
        'pod_ip': os.getenv('POD_IP', 'unknown')
    })

@app.route('/api/info')
def info():
    return jsonify({
        'service': 'backend',
        'version': '1.0.0',
        'replicas': 'multiple',
        'hostname': socket.gethostname()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
