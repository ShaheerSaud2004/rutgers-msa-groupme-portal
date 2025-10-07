import os
from flask import Flask, jsonify

# Set environment variable for Vercel
os.environ['VERCEL'] = '1'

# Create Flask app
app = Flask(__name__)

# Simple test route
@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Vercel!',
        'status': 'working',
        'vercel': os.environ.get('VERCEL', 'false')
    })

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint working!',
        'environment': {
            'vercel': os.environ.get('VERCEL'),
            'python_version': os.sys.version,
            'current_dir': os.getcwd()
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)